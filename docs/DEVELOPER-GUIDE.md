# 👩‍💻 Truth Lab 2.0 - Developer Guide

## 🎯 Overview for Contributors

Welcome to Truth Lab 2.0 development! This comprehensive guide covers everything you need to know to contribute effectively to our AI-powered misinformation detection platform. Whether you're implementing new features, fixing bugs, or improving performance, this guide will help you navigate our modern **FastAPI + React** architecture.

## 🏗️ Architecture Deep Dive

### 🔧 Backend Architecture (FastAPI + Python)

Truth Lab 2.0 uses a **clean architecture pattern** with clear separation of concerns:

```python
# Architecture Layers (from outside in)
🌐 API Layer (FastAPI Routes)
    ↓ HTTP Requests/Responses
🧠 Business Logic Layer (Analysis Engine)  
    ↓ Core Processing & Orchestration
🔧 Service Layer (External Integrations)
    ↓ AI APIs, Database, Cloud Services
📦 Data Layer (Models & Validation)
    ↓ Pydantic Models & Type Safety
```

#### 🎯 Key Architectural Principles

**🔄 Async-First Design**
```python
# All I/O operations use async/await
async def conduct_comprehensive_analysis(text: str) -> Dict[str, Any]:
    # Parallel execution of analysis modules
    tasks = [
        text_analyzer.analyze_content(text),
        source_tracker.trace_origin(text),
        tactics_analyzer.detect_manipulation(text)
    ]
    results = await asyncio.gather(*tasks)
    return aggregate_results(results)
```

**🏗️ Dependency Injection Pattern**
```python
# FastAPI's dependency system for clean testing
from fastapi import Depends

async def get_ai_service() -> AIService:
    return AIService(api_key=settings.google_api_key)

@router.post("/analyze")
async def analyze_text(
    request: AnalysisRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    return await ai_service.analyze(request.text)
```

**📋 Type Safety & Validation**
```python
# Pydantic models ensure runtime type safety
from pydantic import BaseModel, Field, validator

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)
    language: str = Field("en", regex="^[a-z]{2}$")
    level: AnalysisLevel = Field(AnalysisLevel.QUICK_SCAN)
    
    @validator('text')
    def validate_text_content(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v
```

### 🎨 Frontend Architecture (React 18 + Modern Hooks)

**🧩 Component-Based Architecture**
```javascript
// Modern React patterns with hooks and context
import React, { useState, useCallback, useMemo } from 'react';
import { motion } from 'framer-motion';

const AnalysisInterface = () => {
  // State management with hooks
  const [analysisState, setAnalysisState] = useState({
    text: '',
    isAnalyzing: false,
    results: null,
    error: null
  });
  
  // Memoized expensive computations
  const analysisConfig = useMemo(() => ({
    level: userPreferences.defaultLevel,
    language: detectLanguage(analysisState.text)
  }), [analysisState.text, userPreferences]);
  
  // Optimized event handlers
  const handleAnalysis = useCallback(async () => {
    setAnalysisState(prev => ({ ...prev, isAnalyzing: true, error: null }));
    
    try {
      const results = await analysisAPI.analyze({
        text: analysisState.text,
        ...analysisConfig
      });
      setAnalysisState(prev => ({ ...prev, results, isAnalyzing: false }));
    } catch (error) {
      setAnalysisState(prev => ({ ...prev, error: error.message, isAnalyzing: false }));
    }
  }, [analysisState.text, analysisConfig]);
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="analysis-interface"
    >
      {/* Component JSX */}
    </motion.div>
  );
};
```

---

## 🛠️ Development Environment Setup

### 🐍 Python Backend Development

#### Virtual Environment & Dependencies
```bash
# Create isolated Python environment
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install development dependencies
pip install -e ".[dev]"  # If setup.py exists
# OR
pip install -r requirements-dev.txt

# Development tools
pip install black isort flake8 mypy pytest pytest-asyncio pytest-cov
```

#### Code Quality Tools Configuration
```python
# pyproject.toml - Modern Python configuration
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  migrations
  | venv
  | build
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"
```

#### Pre-commit Hooks Setup
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
EOF

# Install hooks
pre-commit install
```

### ⚛️ React Frontend Development

#### Modern JavaScript Tooling
```bash
cd frontend

# Install development dependencies
npm install --save-dev \
  @types/react @types/react-dom \
  eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin \
  prettier eslint-config-prettier eslint-plugin-prettier \
  @testing-library/react @testing-library/jest-dom \
  @vitejs/plugin-react vite

# Husky for git hooks
npm install --save-dev husky lint-staged
npx husky install
```

#### ESLint & Prettier Configuration
```javascript
// .eslintrc.js
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: { jsx: true },
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['react', '@typescript-eslint'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    'react-hooks/exhaustive-deps': 'error',
  },
  settings: {
    react: { version: 'detect' },
  },
};

// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

---

## 🧠 Core Analysis Engine Development

### 🔬 Adding New Analysis Modules

#### 1. Create Analysis Module Structure
```python
# backend/src/analysis_engine/new_analyzer.py
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import asyncio
import logging

logger = logging.getLogger(__name__)

class BaseAnalyzer(ABC):
    """Base class for all analysis modules"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', True)
    
    @abstractmethod
    async def analyze(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text and return results"""
        pass
    
    @abstractmethod
    def get_confidence_score(self, results: Dict[str, Any]) -> float:
        """Calculate confidence score for results"""
        pass

class NewAnalyzer(BaseAnalyzer):
    """Custom analyzer for specific detection logic"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.detection_patterns = config.get('patterns', [])
        self.threshold = config.get('threshold', 0.7)
    
    async def analyze(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Starting new analysis for text length: {len(text)}")
        
        try:
            # Parallel analysis tasks
            tasks = [
                self._detect_patterns(text),
                self._analyze_sentiment(text),
                self._check_linguistic_markers(text)
            ]
            
            pattern_results, sentiment_results, linguistic_results = await asyncio.gather(*tasks)
            
            # Combine results
            combined_results = {
                'patterns': pattern_results,
                'sentiment': sentiment_results,
                'linguistic': linguistic_results,
                'confidence': self.get_confidence_score({
                    'patterns': pattern_results,
                    'sentiment': sentiment_results,
                    'linguistic': linguistic_results
                })
            }
            
            logger.info(f"Analysis completed with confidence: {combined_results['confidence']}")
            return combined_results
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise
    
    async def _detect_patterns(self, text: str) -> Dict[str, Any]:
        """Detect specific patterns in text"""
        # Implementation here
        pass
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze emotional sentiment"""
        # Implementation here
        pass
    
    async def _check_linguistic_markers(self, text: str) -> Dict[str, Any]:
        """Check for linguistic manipulation markers"""
        # Implementation here
        pass
    
    def get_confidence_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        scores = []
        
        if results.get('patterns', {}).get('score'):
            scores.append(results['patterns']['score'])
        
        if results.get('sentiment', {}).get('confidence'):
            scores.append(results['sentiment']['confidence'])
        
        if results.get('linguistic', {}).get('reliability'):
            scores.append(results['linguistic']['reliability'])
        
        return sum(scores) / len(scores) if scores else 0.0
```

#### 2. Register in Analysis Orchestra
```python
# backend/src/analysis_engine/comprehensive_analysis.py
from .new_analyzer import NewAnalyzer

class AnalysisOrchestrator:
    def __init__(self):
        self.analyzers = {
            'text_analysis': TextAnalyzer(config.text_analysis),
            'source_tracking': SourceTracker(config.source_tracking),
            'tactics_breakdown': TacticsAnalyzer(config.tactics),
            'new_analyzer': NewAnalyzer(config.new_analyzer),  # Add new analyzer
        }
    
    async def conduct_comprehensive_analysis(
        self, 
        text: str, 
        options: AnalysisOptions
    ) -> AnalysisResult:
        
        context = self._build_context(text, options)
        
        # Run analyzers based on analysis level
        active_analyzers = self._get_active_analyzers(options.level)
        
        tasks = {
            name: analyzer.analyze(text, context)
            for name, analyzer in self.analyzers.items()
            if name in active_analyzers
        }
        
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        # Process results and handle exceptions
        processed_results = {}
        for (name, _), result in zip(tasks.items(), results):
            if isinstance(result, Exception):
                logger.error(f"Analyzer {name} failed: {str(result)}")
                processed_results[name] = {'error': str(result), 'confidence': 0.0}
            else:
                processed_results[name] = result
        
        return self._aggregate_results(processed_results, context)
```

### 🤖 AI Service Integration

#### Google Gemini Integration Pattern
```python
# backend/src/services/ai_service.py
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

class GoogleAIService:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.session = aiohttp.ClientSession()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def analyze_with_prompt(
        self, 
        text: str, 
        analysis_prompt: str,
        safety_settings: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Analyze text using custom prompts with retry logic"""
        
        try:
            # Prepare safety settings
            safety_config = safety_settings or {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
            
            # Construct full prompt
            full_prompt = f"""
            {analysis_prompt}
            
            Text to analyze:
            \"\"\"
            {text[:8000]}  # Limit text length
            \"\"\"
            
            Please provide your analysis in JSON format.
            """
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                safety_settings=safety_config
            )
            
            # Parse response
            if response.text:
                return self._parse_ai_response(response.text)
            else:
                raise ValueError("Empty response from AI service")
                
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            raise
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate AI response"""
        import json
        import re
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create structured response
                return {
                    'analysis': response_text,
                    'confidence': 0.5,
                    'structured': False
                }
        except json.JSONDecodeError:
            return {
                'raw_response': response_text,
                'error': 'Failed to parse JSON response',
                'confidence': 0.0
            }
    
    async def batch_analyze(
        self, 
        texts: List[str], 
        prompt_template: str,
        max_concurrent: int = 5
    ) -> List[Dict[str, Any]]:
        """Analyze multiple texts concurrently"""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def analyze_single(text: str) -> Dict[str, Any]:
            async with semaphore:
                return await self.analyze_with_prompt(text, prompt_template)
        
        tasks = [analyze_single(text) for text in texts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions in results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'error': str(result),
                    'text_index': i,
                    'confidence': 0.0
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
```

### 🕵️ Forensic Analysis Implementation

#### Source Tracking Module
```python
# backend/src/analysis_engine/source_tracking.py
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import aiohttp
from bs4 import BeautifulSoup
import tldextract

class SourceTracker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.search_engines = config.get('search_engines', ['google', 'bing'])
        self.max_search_results = config.get('max_results', 50)
    
    async def trace_origin(self, text: str) -> Dict[str, Any]:
        """Comprehensive source tracking and origin analysis"""
        
        # Generate content fingerprint
        content_hash = self._generate_content_fingerprint(text)
        
        # Parallel origin tracking tasks
        tasks = [
            self._search_for_duplicates(text),
            self._analyze_url_patterns(text),
            self._check_known_sources(content_hash),
            self._analyze_metadata_signatures(text)
        ]
        
        duplicate_results, url_patterns, known_sources, metadata = await asyncio.gather(*tasks)
        
        # Analyze temporal patterns
        temporal_analysis = await self._analyze_temporal_patterns(duplicate_results)
        
        # Generate origin report
        origin_report = {
            'content_fingerprint': content_hash,
            'duplicate_sources': duplicate_results,
            'url_patterns': url_patterns,
            'known_source_matches': known_sources,
            'metadata_analysis': metadata,
            'temporal_patterns': temporal_analysis,
            'origin_confidence': self._calculate_origin_confidence({
                'duplicates': duplicate_results,
                'patterns': url_patterns,
                'sources': known_sources,
                'temporal': temporal_analysis
            }),
            'tracking_timestamp': datetime.utcnow().isoformat()
        }
        
        return origin_report
    
    def _generate_content_fingerprint(self, text: str) -> str:
        """Generate unique fingerprint for content"""
        # Normalize text
        normalized = re.sub(r'\s+', ' ', text.lower().strip())
        
        # Remove common words and punctuation for fuzzy matching
        significant_words = re.findall(r'\b\w{4,}\b', normalized)
        
        # Create multiple hash signatures
        full_hash = hashlib.sha256(normalized.encode()).hexdigest()
        partial_hash = hashlib.md5(' '.join(significant_words[:20]).encode()).hexdigest()
        
        return {
            'full_hash': full_hash,
            'partial_hash': partial_hash,
            'word_count': len(text.split()),
            'significant_words': significant_words[:10]
        }
    
    async def _search_for_duplicates(self, text: str) -> List[Dict[str, Any]]:
        """Search for duplicate or similar content online"""
        search_phrases = self._extract_search_phrases(text)
        all_results = []
        
        for phrase in search_phrases[:3]:  # Limit search phrases
            for engine in self.search_engines:
                try:
                    results = await self._search_engine_query(phrase, engine)
                    all_results.extend(results)
                except Exception as e:
                    logger.warning(f"Search failed for {engine}: {str(e)}")
        
        # Deduplicate and analyze results
        unique_results = self._deduplicate_search_results(all_results)
        return await self._analyze_search_results(unique_results, text)
    
    async def _analyze_temporal_patterns(self, duplicate_results: List[Dict]) -> Dict[str, Any]:
        """Analyze temporal patterns in content spread"""
        timestamps = []
        
        for result in duplicate_results:
            if result.get('published_date'):
                timestamps.append(result['published_date'])
        
        if len(timestamps) < 2:
            return {'pattern': 'insufficient_data', 'confidence': 0.0}
        
        # Sort timestamps and analyze spread pattern
        sorted_timestamps = sorted(timestamps)
        
        # Calculate spread velocity
        time_span = sorted_timestamps[-1] - sorted_timestamps[0]
        spread_velocity = len(timestamps) / max(time_span.total_seconds() / 3600, 1)  # per hour
        
        # Identify suspicious patterns
        suspicious_indicators = {
            'rapid_spread': spread_velocity > 10,  # More than 10 sources per hour
            'coordinated_timing': self._detect_coordinated_publishing(sorted_timestamps),
            'bot_like_intervals': self._detect_bot_intervals(sorted_timestamps)
        }
        
        return {
            'first_seen': sorted_timestamps[0].isoformat() if sorted_timestamps else None,
            'last_seen': sorted_timestamps[-1].isoformat() if sorted_timestamps else None,
            'spread_velocity_per_hour': spread_velocity,
            'total_sources': len(timestamps),
            'suspicious_patterns': suspicious_indicators,
            'confidence': self._calculate_temporal_confidence(suspicious_indicators)
        }
```

---

## 🎨 Frontend Component Development

### 🧩 Modern React Component Patterns

#### Higher-Order Component for Analysis Features
```javascript
// frontend/src/components/withAnalysis.jsx
import React, { useState, useCallback, useContext } from 'react';
import { AnalysisContext } from '../contexts/AnalysisContext';
import { useAnalysisAPI } from '../hooks/useAnalysisAPI';

const withAnalysis = (WrappedComponent) => {
  return (props) => {
    const { analysisHistory, addToHistory } = useContext(AnalysisContext);
    const { analyzeText, isLoading, error } = useAnalysisAPI();
    
    const [analysisState, setAnalysisState] = useState({
      currentAnalysis: null,
      isAnalyzing: false,
      error: null
    });
    
    const handleAnalysis = useCallback(async (text, options = {}) => {
      setAnalysisState(prev => ({ ...prev, isAnalyzing: true, error: null }));
      
      try {
        const result = await analyzeText(text, options);
        
        setAnalysisState({
          currentAnalysis: result,
          isAnalyzing: false,
          error: null
        });
        
        // Add to history
        addToHistory({
          id: Date.now().toString(),
          timestamp: new Date().toISOString(),
          text: text.substring(0, 200) + '...',
          result: result,
          options: options
        });
        
        return result;
        
      } catch (err) {
        setAnalysisState({
          currentAnalysis: null,
          isAnalyzing: false,
          error: err.message
        });
        throw err;
      }
    }, [analyzeText, addToHistory]);
    
    const enhancedProps = {
      ...props,
      analysis: analysisState,
      onAnalyze: handleAnalysis,
      analysisHistory: analysisHistory,
      isAnalyzing: isLoading || analysisState.isAnalyzing
    };
    
    return <WrappedComponent {...enhancedProps} />;
  };
};

export default withAnalysis;
```

#### Custom Hooks for State Management
```javascript
// frontend/src/hooks/useAnalysisAPI.js
import { useState, useCallback, useRef } from 'react';
import { analysisAPI } from '../services/api';

export const useAnalysisAPI = () => {
  const [state, setState] = useState({
    isLoading: false,
    error: null,
    lastResult: null
  });
  
  const abortControllerRef = useRef(null);
  
  const analyzeText = useCallback(async (text, options = {}) => {
    // Cancel previous request if still running
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    abortControllerRef.current = new AbortController();
    
    setState(prev => ({
      ...prev,
      isLoading: true,
      error: null
    }));
    
    try {
      const result = await analysisAPI.analyze(
        { text, ...options },
        { signal: abortControllerRef.current.signal }
      );
      
      setState({
        isLoading: false,
        error: null,
        lastResult: result
      });
      
      return result;
      
    } catch (error) {
      if (error.name !== 'AbortError') {
        setState(prev => ({
          ...prev,
          isLoading: false,
          error: error.message
        }));
        throw error;
      }
    }
  }, []);
  
  const cancelAnalysis = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setState(prev => ({
        ...prev,
        isLoading: false
      }));
    }
  }, []);
  
  return {
    analyzeText,
    cancelAnalysis,
    isLoading: state.isLoading,
    error: state.error,
    lastResult: state.lastResult
  };
};
```

#### Advanced Analysis Results Component
```javascript
// frontend/src/components/AnalysisResults/AnalysisResults.jsx
import React, { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  TrendingUp,
  Clock,
  Users,
  Globe
} from 'lucide-react';

const AnalysisResults = ({ results, isLoading, error }) => {
  const credibilityLevel = useMemo(() => {
    if (!results?.overall_credibility_score) return null;
    
    const score = results.overall_credibility_score;
    if (score >= 80) return { level: 'high', color: 'green', icon: CheckCircle };
    if (score >= 50) return { level: 'moderate', color: 'yellow', icon: AlertTriangle };
    return { level: 'low', color: 'red', icon: XCircle };
  }, [results]);
  
  const manipulationTactics = useMemo(() => {
    return results?.manipulation_analysis?.detected_tactics || [];
  }, [results]);
  
  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-center p-8"
      >
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="text-lg text-gray-600">Analyzing content...</span>
        </div>
      </motion.div>
    );
  }
  
  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-red-50 border border-red-200 rounded-lg p-6"
      >
        <div className="flex items-center space-x-3">
          <XCircle className="h-6 w-6 text-red-600" />
          <div>
            <h3 className="font-semibold text-red-800">Analysis Failed</h3>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        </div>
      </motion.div>
    );
  }
  
  if (!results) return null;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Credibility Score Header */}
      <div className={`bg-gradient-to-r from-${credibilityLevel?.color}-50 to-${credibilityLevel?.color}-100 rounded-lg p-6 border border-${credibilityLevel?.color}-200`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <credibilityLevel.icon className={`h-8 w-8 text-${credibilityLevel.color}-600`} />
            <div>
              <h2 className={`text-2xl font-bold text-${credibilityLevel.color}-800`}>
                {results.overall_credibility_score}/100
              </h2>
              <p className={`text-${credibilityLevel.color}-600 font-medium`}>
                {credibilityLevel.level.charAt(0).toUpperCase() + credibilityLevel.level.slice(1)} Credibility
              </p>
            </div>
          </div>
          
          <div className="text-right">
            <div className={`text-sm text-${credibilityLevel.color}-600`}>
              Analysis completed in {results.processing_time}s
            </div>
            <div className="text-xs text-gray-500">
              {new Date(results.timestamp).toLocaleString()}
            </div>
          </div>
        </div>
      </div>
      
      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={Shield}
          label="Factual Accuracy"
          value={results.factual_accuracy_score}
          color="blue"
        />
        <MetricCard
          icon={Globe}
          label="Source Quality"
          value={results.source_quality_score}
          color="green"
        />
        <MetricCard
          icon={TrendingUp}
          label="Logic Score"
          value={results.logical_consistency_score}
          color="purple"
        />
        <MetricCard
          icon={Users}
          label="Bias Level"
          value={100 - results.bias_score}
          color="orange"
        />
      </div>
      
      {/* Manipulation Tactics */}
      <AnimatePresence>
        {manipulationTactics.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-amber-50 border border-amber-200 rounded-lg p-6"
          >
            <h3 className="font-semibold text-amber-800 mb-4 flex items-center">
              <AlertTriangle className="h-5 w-5 mr-2" />
              Manipulation Tactics Detected ({manipulationTactics.length})
            </h3>
            
            <div className="space-y-3">
              {manipulationTactics.map((tactic, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-lg p-4 border border-amber-200"
                >
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-medium text-gray-900">{tactic.name}</h4>
                    <span className={`px-2 py-1 text-xs rounded-full ${{
                      'high': 'bg-red-100 text-red-800',
                      'medium': 'bg-yellow-100 text-yellow-800',
                      'low': 'bg-orange-100 text-orange-800'
                    }[tactic.severity]}`}>
                      {tactic.severity}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm mb-2">{tactic.description}</p>
                  {tactic.examples && (
                    <div className="text-xs text-gray-500">
                      <strong>Examples found:</strong> {tactic.examples.join(', ')}
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Source Tracking (Authority Users) */}
      {results.source_tracking && (
        <SourceTrackingResults data={results.source_tracking} />
      )}
      
      {/* Export Options */}
      <div className="flex justify-end space-x-3">
        <button
          onClick={() => exportToPDF(results)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Export PDF
        </button>
        <button
          onClick={() => shareAnalysis(results)}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        >
          Share Analysis
        </button>
      </div>
    </motion.div>
  );
};

const MetricCard = ({ icon: Icon, label, value, color }) => (
  <div className="bg-white rounded-lg p-4 border border-gray-200">
    <div className="flex items-center justify-between mb-2">
      <Icon className={`h-5 w-5 text-${color}-600`} />
      <span className={`text-2xl font-bold text-${color}-600`}>
        {value}
      </span>
    </div>
    <div className="text-sm text-gray-600">{label}</div>
    <div className="mt-2 bg-gray-200 rounded-full h-2">
      <div
        className={`bg-${color}-600 h-2 rounded-full transition-all duration-500`}
        style={{ width: `${value}%` }}
      />
    </div>
  </div>
);

export default AnalysisResults;
```

---

## 🧪 Testing Strategy & Implementation

### 🔧 Backend Testing

#### Unit Testing with PyTest
```python
# backend/tests/test_analysis_engine.py
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch
from src.analysis_engine.comprehensive_analysis import AnalysisOrchestrator
from src.models.analysis_models import AnalysisRequest, AnalysisLevel

class TestAnalysisOrchestrator:
    
    @pytest.fixture
    def orchestrator(self):
        return AnalysisOrchestrator()
    
    @pytest.fixture
    def sample_text(self):
        return "This is a sample text for testing analysis functionality."
    
    @pytest.fixture
    def analysis_request(self, sample_text):
        return AnalysisRequest(
            text=sample_text,
            language="en",
            level=AnalysisLevel.DEEP_ANALYSIS
        )
    
    @pytest.mark.asyncio
    async def test_basic_analysis_flow(self, orchestrator, analysis_request):
        """Test basic analysis workflow"""
        # Mock analyzer responses
        with patch.object(orchestrator, 'analyzers') as mock_analyzers:
            mock_analyzers.items.return_value = [
                ('text_analysis', AsyncMock(return_value={'score': 85})),
                ('source_tracking', AsyncMock(return_value={'origins': []})),
                ('tactics_breakdown', AsyncMock(return_value={'tactics': []}))
            ]
            
            result = await orchestrator.conduct_comprehensive_analysis(
                analysis_request.text,
                analysis_request
            )
            
            assert result is not None
            assert 'overall_credibility_score' in result
            assert 'processing_time' in result
            assert result['overall_credibility_score'] >= 0
    
    @pytest.mark.asyncio
    async def test_error_handling(self, orchestrator, analysis_request):
        """Test error handling in analysis"""
        with patch.object(orchestrator, 'analyzers') as mock_analyzers:
            # Simulate analyzer failure
            mock_analyzers.items.return_value = [
                ('text_analysis', AsyncMock(side_effect=Exception("API Error"))),
                ('source_tracking', AsyncMock(return_value={'origins': []}))
            ]
            
            result = await orchestrator.conduct_comprehensive_analysis(
                analysis_request.text,
                analysis_request
            )
            
            # Should still return result with error handled
            assert result is not None
            assert 'text_analysis' in result
            assert 'error' in result['text_analysis']
    
    @pytest.mark.asyncio
    async def test_performance_benchmarks(self, orchestrator, analysis_request):
        """Test that analysis completes within time limits"""
        import time
        
        start_time = time.time()
        result = await orchestrator.conduct_comprehensive_analysis(
            analysis_request.text,
            analysis_request
        )
        end_time = time.time()
        
        # Analysis should complete within 30 seconds for deep analysis
        assert (end_time - start_time) < 30
        assert result['processing_time'] < 30

# Integration tests
class TestAnalysisAPI:
    
    @pytest.mark.asyncio
    async def test_api_endpoint_integration(self, client):
        """Test full API endpoint with real analysis"""
        response = await client.post("/api/analyze", json={
            "text": "Sample text for integration testing",
            "language": "en",
            "level": "Quick Scan"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert 'overall_credibility_score' in data
        assert 'analysis_id' in data
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, client):
        """Test API rate limiting"""
        # Make multiple rapid requests
        tasks = [
            client.post("/api/analyze", json={
                "text": f"Test text {i}",
                "level": "Quick Scan"
            })
            for i in range(20)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # Some requests should be rate limited
        rate_limited = sum(1 for r in responses if r.status_code == 429)
        assert rate_limited > 0
```

#### Performance & Load Testing
```python
# backend/tests/test_performance.py
import asyncio
import pytest
import time
from concurrent.futures import ThreadPoolExecutor
import aiohttp

class TestPerformance:
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis_load(self):
        """Test system under concurrent load"""
        
        async def single_analysis():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:8000/api/analyze",
                    json={
                        "text": "Load testing text content for performance analysis",
                        "level": "Quick Scan"
                    }
                ) as response:
                    return await response.json()
        
        # Simulate 50 concurrent users
        start_time = time.time()
        tasks = [single_analysis() for _ in range(50)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        # Check results
        successful = sum(1 for r in results if not isinstance(r, Exception))
        avg_time = (end_time - start_time) / len(tasks)
        
        assert successful >= 40  # At least 80% success rate
        assert avg_time < 5.0    # Average response time under 5 seconds
    
    @pytest.mark.asyncio
    async def test_memory_usage(self):
        """Test memory usage during analysis"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run multiple analyses
        for i in range(10):
            # Simulate analysis here
            await asyncio.sleep(0.1)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 100MB for 10 analyses)
        assert memory_increase < 100
```

### ⚛️ Frontend Testing

#### Component Testing with Testing Library
```javascript
// frontend/src/components/__tests__/AnalysisResults.test.jsx
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import AnalysisResults from '../AnalysisResults/AnalysisResults';

describe('AnalysisResults Component', () => {
  const mockResults = {
    overall_credibility_score: 75,
    factual_accuracy_score: 80,
    source_quality_score: 70,
    logical_consistency_score: 75,
    bias_score: 25,
    manipulation_analysis: {
      detected_tactics: [
        {
          name: 'Emotional Appeal',
          severity: 'medium',
          description: 'Uses emotional language to influence opinion',
          examples: ['shocking news', 'urgent action needed']
        }
      ]
    },
    processing_time: 2.5,
    timestamp: '2024-01-15T10:30:00Z'
  };

  test('renders credibility score correctly', () => {
    render(<AnalysisResults results={mockResults} />);
    
    expect(screen.getByText('75/100')).toBeInTheDocument();
    expect(screen.getByText('Moderate Credibility')).toBeInTheDocument();
  });

  test('displays manipulation tactics when present', () => {
    render(<AnalysisResults results={mockResults} />);
    
    expect(screen.getByText('Manipulation Tactics Detected (1)')).toBeInTheDocument();
    expect(screen.getByText('Emotional Appeal')).toBeInTheDocument();
    expect(screen.getByText('medium')).toBeInTheDocument();
  });

  test('shows loading state', () => {
    render(<AnalysisResults isLoading={true} />);
    
    expect(screen.getByText('Analyzing content...')).toBeInTheDocument();
    expect(screen.getByRole('status')).toBeInTheDocument(); // Loading spinner
  });

  test('handles error state', () => {
    const errorMessage = 'Analysis failed due to network error';
    render(<AnalysisResults error={errorMessage} />);
    
    expect(screen.getByText('Analysis Failed')).toBeInTheDocument();
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  test('export functionality works', async () => {
    const mockExportToPDF = vi.fn();
    global.exportToPDF = mockExportToPDF;
    
    render(<AnalysisResults results={mockResults} />);
    
    const exportButton = screen.getByText('Export PDF');
    fireEvent.click(exportButton);
    
    await waitFor(() => {
      expect(mockExportToPDF).toHaveBeenCalledWith(mockResults);
    });
  });
});
```

#### End-to-End Testing with Playwright
```javascript
// frontend/e2e/analysis-flow.spec.js
import { test, expect } from '@playwright/test';

test.describe('Analysis Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('complete analysis workflow', async ({ page }) => {
    // Navigate to home page
    await expect(page.locator('h1')).toContainText('Truth Lab 2.0');

    // Enter text for analysis
    const testText = 'This is a sample text to test the analysis functionality of Truth Lab 2.0';
    await page.fill('[data-testid="analysis-input"]', testText);

    // Select analysis level
    await page.selectOption('[data-testid="analysis-level"]', 'Deep Analysis');

    // Start analysis
    await page.click('[data-testid="analyze-button"]');

    // Wait for loading state
    await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible();
    await expect(page.locator('text=Analyzing content...')).toBeVisible();

    // Wait for results (with timeout)
    await page.waitForSelector('[data-testid="analysis-results"]', { timeout: 30000 });

    // Verify results are displayed
    await expect(page.locator('[data-testid="credibility-score"]')).toBeVisible();
    await expect(page.locator('[data-testid="metric-cards"]')).toBeVisible();

    // Test export functionality
    await page.click('[data-testid="export-pdf-button"]');
    
    // Verify download started (or modal opened)
    // This depends on your implementation
  });

  test('handles analysis errors gracefully', async ({ page }) => {
    // Mock API to return error
    await page.route('**/api/analyze', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' })
      });
    });

    // Enter text and analyze
    await page.fill('[data-testid="analysis-input"]', 'Test text');
    await page.click('[data-testid="analyze-button"]');

    // Wait for error message
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('text=Analysis Failed')).toBeVisible();
  });

  test('responsive design works on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Verify mobile navigation
    await expect(page.locator('[data-testid="mobile-menu-button"]')).toBeVisible();
    
    // Open mobile menu
    await page.click('[data-testid="mobile-menu-button"]');
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();

    // Test analysis on mobile
    await page.fill('[data-testid="analysis-input"]', 'Mobile test');
    await page.click('[data-testid="analyze-button"]');

    // Verify mobile results display
    await page.waitForSelector('[data-testid="analysis-results"]', { timeout: 30000 });
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible();
  });
});
```

---

## 📊 Performance Optimization

### 🔧 Backend Performance

#### Database Query Optimization
```python
# backend/src/services/database_service.py
import asyncpg
from typing import List, Dict, Any, Optional
import asyncio

class DatabaseService:
    def __init__(self, connection_pool: asyncpg.Pool):
        self.pool = connection_pool
    
    async def bulk_insert_analyses(self, analyses: List[Dict[str, Any]]) -> List[str]:
        """Optimized bulk insertion of analysis results"""
        
        query = """
        INSERT INTO analyses (id, text_hash, results, timestamp, user_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Use executemany for bulk operations
                analysis_data = [
                    (
                        analysis['id'],
                        analysis['text_hash'],
                        json.dumps(analysis['results']),
                        analysis['timestamp'],
                        analysis['user_id']
                    )
                    for analysis in analyses
                ]
                
                results = await conn.executemany(query, analysis_data)
                return [result[0] for result in results]
    
    async def get_analyses_with_pagination(
        self, 
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Optimized pagination with filters"""
        
        where_conditions = ["user_id = $1"]
        params = [user_id]
        param_count = 1
        
        if filters:
            if filters.get('date_from'):
                param_count += 1
                where_conditions.append(f"timestamp >= ${param_count}")
                params.append(filters['date_from'])
            
            if filters.get('min_credibility'):
                param_count += 1
                where_conditions.append(f"(results->>'overall_credibility_score')::int >= ${param_count}")
                params.append(filters['min_credibility'])
        
        where_clause = " AND ".join(where_conditions)
        
        # Count query for total records
        count_query = f"""
        SELECT COUNT(*) FROM analyses 
        WHERE {where_clause}
        """
        
        # Data query with pagination
        data_query = f"""
        SELECT id, text_hash, results, timestamp
        FROM analyses 
        WHERE {where_clause}
        ORDER BY timestamp DESC 
        LIMIT ${param_count + 1} OFFSET ${param_count + 2}
        """
        
        params.extend([limit, offset])
        
        async with self.pool.acquire() as conn:
            # Execute both queries concurrently
            count_task = conn.fetchval(count_query, *params[:-2])
            data_task = conn.fetch(data_query, *params)
            
            total_count, records = await asyncio.gather(count_task, data_task)
            
            return {
                'records': [dict(record) for record in records],
                'total_count': total_count,
                'has_more': offset + limit < total_count,
                'next_offset': offset + limit if offset + limit < total_count else None
            }
```

#### Caching Strategy Implementation
```python
# backend/src/utils/caching.py
import redis.asyncio as redis
import json
import hashlib
from typing import Any, Optional, Dict
from datetime import timedelta
import pickle

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, decode_responses=False)
    
    def _generate_cache_key(self, prefix: str, **kwargs) -> str:
        """Generate consistent cache keys"""
        key_parts = [prefix]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()[:16]
    
    async def cached_analysis(
        self,
        text: str,
        options: Dict[str, Any],
        ttl: int = 3600  # 1 hour default
    ):
        """Decorator for caching analysis results"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Generate cache key from text and options
                text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
                cache_key = self._generate_cache_key(
                    "analysis",
                    text_hash=text_hash,
                    **options
                )
                
                # Try to get from cache
                cached_result = await self.redis.get(cache_key)
                if cached_result:
                    return pickle.loads(cached_result)
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Cache result
                await self.redis.setex(
                    cache_key,
                    ttl,
                    pickle.dumps(result)
                )
                
                return result
            
            return wrapper
        return decorator
    
    async def cache_manipulation_patterns(
        self, 
        patterns: List[Dict[str, Any]]
    ) -> None:
        """Cache manipulation pattern database"""
        cache_key = "manipulation_patterns:latest"
        pattern_data = {
            'patterns': patterns,
            'last_updated': datetime.utcnow().isoformat(),
            'version': '2.0.1'
        }
        
        await self.redis.setex(
            cache_key,
            timedelta(hours=24).total_seconds(),
            pickle.dumps(pattern_data)
        )
    
    async def get_cached_patterns(self) -> Optional[List[Dict[str, Any]]]:
        """Retrieve cached manipulation patterns"""
        cache_key = "manipulation_patterns:latest"
        cached_data = await self.redis.get(cache_key)
        
        if cached_data:
            pattern_data = pickle.loads(cached_data)
            return pattern_data['patterns']
        
        return None
    
    async def invalidate_user_cache(self, user_id: str) -> None:
        """Invalidate all cache entries for a user"""
        pattern = f"*user:{user_id}*"
        keys = await self.redis.keys(pattern)
        
        if keys:
            await self.redis.delete(*keys)
```

### ⚛️ Frontend Performance

#### Code Splitting & Lazy Loading
```javascript
// frontend/src/App.jsx
import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorBoundary from './components/ErrorBoundary';

// Lazy load pages for better performance
const Home = lazy(() => import('./pages/Home'));
const Archive = lazy(() => 
  import('./pages/Archive').then(module => ({
    default: module.Archive
  }))
);
const Learn = lazy(() => import('./pages/Learn'));
const Dashboard = lazy(() => 
  import('./pages/Dashboard').then(module => ({
    default: module.Dashboard
  }))
);

// Preload critical routes
const preloadRoutes = () => {
  const routes = [
    () => import('./pages/Home'),
    () => import('./pages/Archive')
  ];
  
  // Preload after initial render
  setTimeout(() => {
    routes.forEach(routeLoader => routeLoader());
  }, 100);
};

const App = () => {
  React.useEffect(() => {
    preloadRoutes();
  }, []);

  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/archive" element={<Archive />} />
              <Route path="/learn" element={<Learn />} />
              <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
          </Suspense>
        </div>
      </Router>
    </ErrorBoundary>
  );
};

export default App;
```

#### Optimized API Client
```javascript
// frontend/src/services/optimizedAPI.js
class OptimizedAPIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.requestCache = new Map();
    this.abortControllers = new Map();
  }
  
  // Debounced analysis requests
  analyzeWithDebounce = this.debounce(async (text, options) => {
    return this.analyze(text, options);
  }, 500);
  
  async analyze(text, options = {}) {
    const requestKey = this.generateRequestKey(text, options);
    
    // Cancel previous request if exists
    if (this.abortControllers.has(requestKey)) {
      this.abortControllers.get(requestKey).abort();
    }
    
    // Check cache first
    if (this.requestCache.has(requestKey)) {
      const cached = this.requestCache.get(requestKey);
      if (Date.now() - cached.timestamp < 300000) { // 5 minutes
        return cached.data;
      }
    }
    
    const controller = new AbortController();
    this.abortControllers.set(requestKey, controller);
    
    try {
      const response = await fetch(`${this.baseURL}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, ...options }),
        signal: controller.signal
      });
      
      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Cache successful response
      this.requestCache.set(requestKey, {
        data,
        timestamp: Date.now()
      });
      
      // Clean up
      this.abortControllers.delete(requestKey);
      
      return data;
      
    } catch (error) {
      this.abortControllers.delete(requestKey);
      
      if (error.name !== 'AbortError') {
        throw error;
      }
    }
  }
  
  generateRequestKey(text, options) {
    const normalizedText = text.substring(0, 100); // Use first 100 chars
    return btoa(normalizedText + JSON.stringify(options)).substring(0, 16);
  }
  
  debounce(func, delay) {
    let timeoutId;
    return (...args) => {
      clearTimeout(timeoutId);
      return new Promise((resolve, reject) => {
        timeoutId = setTimeout(async () => {
          try {
            const result = await func(...args);
            resolve(result);
          } catch (error) {
            reject(error);
          }
        }, delay);
      });
    };
  }
  
  // Cleanup method
  clearCache() {
    this.requestCache.clear();
    this.abortControllers.forEach(controller => controller.abort());
    this.abortControllers.clear();
  }
}

export const apiClient = new OptimizedAPIClient(
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
);
```

---

## 🔗 API Integration Guidelines

### 📊 REST API Design

#### Consistent Response Format
```python
# backend/src/models/api_models.py
from pydantic import BaseModel
from typing import Any, Optional, Dict, List
from datetime import datetime
from enum import Enum

class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
    timestamp: datetime
    request_id: str
    
class PaginatedResponse(APIResponse):
    """Paginated response format"""
    data: List[Any]
    pagination: Dict[str, Any]  # total, page, per_page, has_next, etc.

class AnalysisResponse(APIResponse):
    """Specialized response for analysis endpoints"""
    data: Dict[str, Any]  # Analysis results
    processing_time: float
    analysis_id: str
    cached: bool = False
```

#### API Versioning Strategy
```python
# backend/src/api/versioning.py
from fastapi import APIRouter, Header
from typing import Optional

def create_versioned_router(version: str = "v1") -> APIRouter:
    """Create router with version prefix"""
    return APIRouter(prefix=f"/api/{version}")

async def get_api_version(
    x_api_version: Optional[str] = Header(None),
    accept_version: Optional[str] = Header(None)
) -> str:
    """Determine API version from headers"""
    return x_api_version or accept_version or "v1"

# Usage in routes
v1_router = create_versioned_router("v1")
v2_router = create_versioned_router("v2")

@v1_router.post("/analyze")
async def analyze_v1(request: AnalysisRequestV1):
    # V1 implementation
    pass

@v2_router.post("/analyze") 
async def analyze_v2(request: AnalysisRequestV2):
    # V2 implementation with enhanced features
    pass
```

---

## 🎓 Contributing Guidelines

### 📋 Code Standards

#### Python Code Style
```python
# Follow these conventions for all Python code

# 1. Use type hints everywhere
def analyze_text(text: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze text with comprehensive type safety"""
    pass

# 2. Use docstrings for all functions and classes
class TextAnalyzer:
    """
    Comprehensive text analysis using AI models.
    
    This class handles text processing, AI integration,
    and result formatting for the Truth Lab platform.
    
    Attributes:
        model_name (str): Name of the AI model to use
        api_key (str): API key for external service
        cache_enabled (bool): Whether to cache results
    
    Example:
        >>> analyzer = TextAnalyzer("gemini-1.5-flash", api_key)
        >>> result = await analyzer.analyze("Sample text")
    """
    pass

# 3. Use async/await for all I/O operations
async def fetch_external_data(url: str) -> Dict[str, Any]:
    """Always use async for network/file operations"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# 4. Handle errors explicitly
async def safe_analysis(text: str) -> Dict[str, Any]:
    """Example of proper error handling"""
    try:
        result = await analyze_text(text)
        return result
    except APIException as e:
        logger.error(f"API failed: {e}")
        raise AnalysisError(f"Analysis failed: {e}") from e
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise
```

#### JavaScript/React Code Style
```javascript
// Follow these conventions for all frontend code

// 1. Use TypeScript-style prop documentation
/**
 * Analysis results display component
 * @param {Object} props - Component props
 * @param {Object} props.results - Analysis results data
 * @param {boolean} props.isLoading - Loading state
 * @param {string} props.error - Error message if any
 * @returns {JSX.Element} Rendered analysis results
 */
const AnalysisResults = ({ results, isLoading, error }) => {
  // Component implementation
};

// 2. Use proper hook patterns
const useAnalysisData = (analysisId) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    let mounted = true;
    
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await api.getAnalysis(analysisId);
        
        if (mounted) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (mounted) {
          setError(err.message);
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };
    
    if (analysisId) {
      fetchData();
    }
    
    return () => {
      mounted = false;
    };
  }, [analysisId]);
  
  return { data, loading, error };
};

// 3. Use proper error boundaries
class AnalysisErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Analysis component error:', error, errorInfo);
    // Send to error reporting service
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    
    return this.props.children;
  }
}
```

### 🔄 Git Workflow

#### Branch Naming Convention
```bash
# Feature branches
feature/add-source-tracking
feature/improve-ui-accessibility
feature/batch-analysis-api

# Bug fix branches  
fix/credibility-score-calculation
fix/mobile-responsive-layout
fix/api-timeout-handling

# Hotfix branches
hotfix/critical-security-patch
hotfix/production-db-connection

# Documentation branches
docs/update-developer-guide
docs/add-api-examples
```

#### Commit Message Format
```bash
# Format: <type>(<scope>): <description>

# Types: feat, fix, docs, style, refactor, test, chore

# Examples:
feat(analysis): add source tracking for authority users
fix(ui): resolve mobile navigation menu overflow
docs(api): update analysis endpoint documentation
test(backend): add comprehensive analysis engine tests
refactor(frontend): optimize component re-rendering
chore(deps): update security dependencies

# Breaking changes:
feat(api)!: change analysis response format

BREAKING CHANGE: Analysis response now includes metadata object.
Migrate existing code to use result.data instead of result.
```

### 🧪 Testing Requirements

#### Pull Request Checklist
```markdown
## PR Checklist

### Code Quality
- [ ] Code follows project style guidelines
- [ ] All functions have type hints (Python) or proper types (TypeScript)  
- [ ] Comprehensive docstrings/comments added
- [ ] No console.log or debug prints left in code
- [ ] Error handling implemented properly

### Testing
- [ ] Unit tests added for new functionality
- [ ] Integration tests updated if needed
- [ ] All existing tests pass
- [ ] Test coverage >= 80% for new code
- [ ] Manual testing completed on multiple browsers/devices

### Performance
- [ ] No obvious performance regressions
- [ ] Async/await used for I/O operations
- [ ] Database queries optimized
- [ ] Frontend bundle size impact acceptable

### Documentation  
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Code comments explain complex logic
- [ ] Migration guide provided for breaking changes

### Security
- [ ] No sensitive data exposed
- [ ] Input validation implemented
- [ ] Authentication/authorization working
- [ ] Dependencies security checked
```

---

**🎉 You're Ready to Contribute!**

This developer guide provides everything you need to:
- ✅ Understand the codebase architecture
- ✅ Set up your development environment  
- ✅ Follow coding standards and best practices
- ✅ Implement new features effectively
- ✅ Write comprehensive tests
- ✅ Optimize for performance
- ✅ Contribute to the project successfully

**🔗 Additional Resources:**
- [Testing Guide](TESTING-GUIDE.md) - Comprehensive testing documentation
- [Deployment Guide](DEPLOYMENT-GUIDE.md) - Production deployment procedures
- [User Guide](USER-GUIDE.md) - Understanding user requirements
- [Master README](../MASTER-README.md) - Project overview and goals

*Ready to build the future of misinformation detection! 🚀*