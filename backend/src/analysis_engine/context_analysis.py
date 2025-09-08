# backend/src/analysis_engine/context_analysis.py

import asyncio
import logging
import os
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    import google.generativeai as genai  # optional
except Exception:  # pragma: no cover
    genai = None  # gracefully degrade if not installed

logger = logging.getLogger(__name__)

INDIA_SENSITIVE_KEYWORDS = [
    # elections/politics
    "election", "vote", "poll", "eci", "booth", "evm", "manifesto", "rally",
    # religion/communal
    "temple", "mosque", "church", "hindu", "muslim", "christian", "sikh", "communal",
    # public safety/riots
    "riot", "violence", "curfew", "section 144", "law and order",
    # health
    "covid", "vaccine", "virus", "pandemic", "outbreak", "epidemic",
    # finance/scams
    "upi", "bank", "otp", "kyc", "fraud", "scam", "lottery",
    # disasters
    "flood", "earthquake", "cyclone", "heatwave", "landslide",
    # misinformation telltales
    "breaking", "urgent", "forward", "share", "viral", "alert",
]

RELATIVE_TIME_TERMS = [
    "today", "yesterday", "tonight", "this morning", "this evening",
    "last night", "breaking", "just now", "urgent", "immediately",
]

MONTHS = (
    "january","february","march","april","may","june",
    "july","august","september","october","november","december"
)

STOPWORDS = set((
    "the","a","an","and","or","but","if","then","else","on","in","at","to","for","of",
    "from","by","with","as","is","are","was","were","be","been","it","this","that",
    "these","those","i","we","you","he","she","they","them","his","her","their",
    "our","your","not","no","yes"
))

@dataclass
class ContextAnalyzerConfig:
    enabled: bool = True
    use_gemini: bool = True
    model: str = "gemini-1.5-flash"
    max_keywords: int = 12
    recency_days: int = 14

class ContextAnalyzer:
    """
    Context and background analysis for Truth Lab 2.0.

    Produces:
      - topics (keywords)
      - temporal_indicators (dates and relative terms)
      - sensitive_context_hits (India-centric risk domains)
      - events_correlation (heuristic risk)
      - gemini_context (optional LLM summary)
      - confidence (0-1)
    """

    def __init__(self, config: Dict[str, Any] | None = None):
        cfg = config or {}
        self.config = ContextAnalyzerConfig(
            enabled=cfg.get("enabled", True),
            use_gemini=cfg.get("use_gemini", True),
            model=cfg.get("model", "gemini-1.5-flash"),
            max_keywords=cfg.get("max_keywords", 12),
            recency_days=cfg.get("recency_days", 14),
        )

        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.gemini = None
        if self.config.use_gemini and self.google_api_key and genai:
            try:
                genai.configure(api_key=self.google_api_key)
                self.gemini = genai.GenerativeModel(self.config.model)
                logger.info("ContextAnalyzer: Gemini model initialized")
            except Exception as e:  # pragma: no cover
                logger.warning(f"ContextAnalyzer: Gemini init failed: {e}")
                self.gemini = None

    async def analyze(self, text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        if not self.config.enabled:
            return {"enabled": False, "confidence": 0.0}

        norm = self._normalize_text(text)
        keywords = self._extract_keywords(norm, self.config.max_keywords)
        dates, relative_terms = self._extract_temporal_signals(norm)
        sensitive_hits = self._detect_sensitive_hits(norm)

        # Heuristic correlation: higher risk if sensitive + recent/time-pressured language
        events_corr = self._correlate_events(dates, relative_terms, sensitive_hits)

        gemini_context = None
        if self.gemini:
            try:
                gemini_context = await self._gemini_context_summarize(text, keywords, dates, sensitive_hits)
            except Exception as e:  # pragma: no cover
                logger.warning(f"ContextAnalyzer: Gemini summarize failed: {e}")

        result = {
            "topics": keywords,
            "temporal_indicators": {
                "dates_found": [d.isoformat() for d in dates],
                "relative_time_terms": relative_terms,
                "recent_within_days": self.config.recency_days,
            },
            "sensitive_context_hits": sensitive_hits,
            "events_correlation": events_corr,
            "gemini_context": gemini_context,
            "confidence": self.get_confidence_score({
                "keywords": keywords,
                "dates": dates,
                "relative_terms": relative_terms,
                "sensitive_hits": sensitive_hits,
                "events_corr": events_corr,
                "gemini": gemini_context is not None
            })
        }
        return result

    def get_confidence_score(self, data: Dict[str, Any]) -> float:
        score = 0.3  # base
        if data.get("keywords"):
            score += 0.2
        if data.get("dates") or data.get("relative_terms"):
            score += 0.15
        if data.get("sensitive_hits"):
            score += 0.2
        if data.get("events_corr", {}).get("risk_level") in ("elevated", "high"):
            score += 0.1
        if data.get("gemini"):
            score += 0.05
        return min(1.0, round(score, 2))

    # ---------------- internal helpers ----------------

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip().lower()

    def _extract_keywords(self, text: str, k: int) -> List[str]:
        tokens = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text)
        tokens = [t for t in tokens if t not in STOPWORDS]
        freq = Counter(tokens)
        return [w for w, _ in freq.most_common(k)]

    def _extract_temporal_signals(self, text: str) -> tuple[List[datetime], List[str]]:
        dates: List[datetime] = []
        relative_found: List[str] = []

        # Relative time terms
        for term in RELATIVE_TIME_TERMS:
            if term in text:
                relative_found.append(term)

        # Numeric dates: 07/09/2025 or 07-09-2025
        for m in re.finditer(r"\b(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})\b", text):
            d, mth, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if y < 100:  # yy -> 20yy
                y += 2000
            try:
                dates.append(datetime(y, mth, d))
            except ValueError:
                pass

        # Month name forms: 7 September 2025, September 7, 2025
        month_map = {m: i + 1 for i, m in enumerate(MONTHS)}
        # 7 september 2025
        for m in re.finditer(r"\b(\d{1,2})\s+([a-z]+)\s+(\d{4})\b", text):
            day, mon, year = int(m.group(1)), m.group(2), int(m.group(3))
            if mon in month_map:
                try:
                    dates.append(datetime(year, month_map[mon], day))
                except ValueError:
                    pass
        # september 7, 2025
        for m in re.finditer(r"\b([a-z]+)\s+(\d{1,2}),\s*(\d{4})\b", text):
            mon, day, year = m.group(1), int(m.group(2)), int(m.group(3))
            if mon in month_map:
                try:
                    dates.append(datetime(year, month_map[mon], day))
                except ValueError:
                    pass

        return dates, relative_found

    def _detect_sensitive_hits(self, text: str) -> List[str]:
        hits = []
        for kw in INDIA_SENSITIVE_KEYWORDS:
            if kw in text:
                hits.append(kw)
        # de-duplicate while preserving order
        seen = set()
        unique = []
        for h in hits:
            if h not in seen:
                unique.append(h)
                seen.add(h)
        return unique

    def _correlate_events(
        self, dates: List[datetime], relative_terms: List[str], sensitive_hits: List[str]
    ) -> Dict[str, Any]:
        now = datetime.utcnow()
        recent_cutoff = now - timedelta(days=self.config.recency_days)
        recent_dates = [d for d in dates if d >= recent_cutoff]

        score = 0
        if sensitive_hits:
            score += 2
        if relative_terms:
            score += 1
        if recent_dates:
            score += 1

        if score >= 3:
            level = "high"
        elif score == 2:
            level = "elevated"
        elif score == 1:
            level = "low"
        else:
            level = "minimal"

        return {
            "risk_level": level,
            "signals": {
                "sensitive_hits_count": len(sensitive_hits),
                "relative_terms_count": len(relative_terms),
                "recent_dates_count": len(recent_dates),
            },
        }

    async def _gemini_context_summarize(
        self, text: str, keywords: List[str], dates: List[datetime], hits: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Optional LLM summary to enrich context; gracefully skipped if no API key/model.
        """
        if not self.gemini:
            return None

        prompt = f"""
        You are assisting a misinformation forensics system in India.
        Given the input content, provide a concise JSON with:
          - key_topics: top concepts (<=5)
          - likely_domain: one of ["political","communal","health","finance","public_safety","other"]
          - risk_triggers: brief bullet points explaining why timing/context might be sensitive
          - recommended_checks: 3 short next verification steps for analysts in India

        Keep it brief and strictly return JSON.
        Content:
        \"\"\"{text[:6000]}\"\"\"

        Extracted keywords: {keywords[:10]}
        Extracted dates (UTC): {[d.isoformat() for d in dates][:5]}
        Sensitive hits: {hits[:10]}
        """

        resp = await asyncio.to_thread(self.gemini.generate_content, prompt)
        raw = getattr(resp, "text", "") or ""
        # Try to extract JSON
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if not m:
            return {"raw": raw.strip()[:1000]}
        try:
            import json
            return json.loads(m.group(0))
        except Exception:
            return {"raw": raw.strip()[:1000]}

__all__ = ["ContextAnalyzer", "ContextAnalyzerConfig"]
