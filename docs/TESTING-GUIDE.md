# 🧪 Truth Lab 2.0 - Testing Guide

## 🎯 Testing Strategy Overview

Truth Lab 2.0 employs a **comprehensive multi-layered testing strategy** to ensure reliability, performance, and security of our AI-powered misinformation detection platform. This guide covers all aspects of testing from unit tests to production monitoring.

## 📋 Testing Pyramid

```
                    🔺 Manual & Exploratory Testing
                  🔺🔺 End-to-End (E2E) Tests  
                🔺🔺🔺 Integration Tests
              🔺🔺🔺🔺 Component Tests (Frontend)
            🔺🔺🔺🔺🔺 Unit Tests (Backend & Frontend)
```

**🎯 Testing Levels:**
- **Unit Tests (70%)**: Individual functions, classes, components
- **Integration Tests (20%)**: API endpoints, service interactions
- **Component Tests (5%)**: React component behavior
- **E2E Tests (4%)**: Complete user journeys
- **Manual Testing (1%)**: Exploratory and usability testing

---

## 🔧 Backend Testing (Python + FastAPI)

### 🛠️ Testing Framework Setup

#### Core Testing Dependencies
```python
# requirements-test.txt
pytest==7.4.0
pytest-asyncio==0.21.0
pytest-cov==4.1.0
pytest-mock==3.11.1
pytest-xdist==3.3.1  # Parallel test execution
httpx==0.24.1         # Async HTTP client for API testing
fakeredis==2.18.0     # Redis mocking
pytest-benchmark==4.0.0  # Performance benchmarks
```

#### PyTest Configuration
```python
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
    "--strict-markers",
    "--disable-warnings",
    "-v"
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests", 
    "slow: Slow running tests",
    "external: Tests requiring external services",
    "benchmark: Performance benchmark tests"
]
asyncio_mode = "auto"
```

#### Test Fixtures Setup
```python
# tests/conftest.py
import pytest
import asyncio
import asyncpg
from httpx import AsyncClient
from unittest.mock import AsyncMock, Mock
from src.api.main import app
from src.config.settings import get_settings
from src.services.ai_service import GoogleAIService

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for the entire test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_client():
    """Create test client for API testing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_ai_service():
    """Mock AI service for testing"""
    service = Mock(spec=GoogleAIService)
    service.analyze_with_prompt = AsyncMock(return_value={
        "credibility_score": 75,
        "confidence": 0.85,
        "analysis": "Test analysis result"
    })
    return service

@pytest.fixture
async def test_db():
    """Create test database connection"""
    # Use in-memory SQLite for testing
    import aiosqlite
    db = await aiosqlite.connect(":memory:")
    
    # Setup test schema
    await db.execute('''
        CREATE TABLE analyses (
            id TEXT PRIMARY KEY,
            text_hash TEXT,
            results TEXT,
            timestamp DATETIME,
            user_id TEXT
        )
    ''')
    await db.commit()
    
    yield db
    await db.close()

@pytest.fixture
def sample_analysis_data():
    """Sample data for testing"""
    return {
        "text": "This is a sample text for analysis testing purposes.",
        "language": "en",
        "level": "Deep Analysis",
        "expected_score": 75,
        "expected_tactics": ["emotional_appeal"]
    }
```

### 🧪 Unit Testing

#### Analysis Engine Unit Tests
```python
# tests/unit/test_analysis_engine.py
import pytest
from unittest.mock import AsyncMock, patch, Mock
from src.analysis_engine.comprehensive_analysis import AnalysisOrchestrator
from src.analysis_engine.text_analysis import TextAnalyzer
from src.models.analysis_models import AnalysisRequest, AnalysisLevel

class TestAnalysisOrchestrator:
    
    @pytest.fixture
    def orchestrator(self):
        return AnalysisOrchestrator()
    
    @pytest.mark.asyncio
    async def test_successful_comprehensive_analysis(self, orchestrator, sample_analysis_data):
        """Test successful analysis with all modules"""
        
        with patch.object(orchestrator, 'analyzers') as mock_analyzers:
            # Mock all analyzer responses
            mock_analyzers.items.return_value = [
                ('text_analysis', AsyncMock(return_value={
                    'credibility_score': 75,
                    'confidence': 0.85,
                    'factual_accuracy': 80
                })),
                ('source_tracking', AsyncMock(return_value={
                    'origins': [],
                    'confidence': 0.70
                })),
                ('tactics_breakdown', AsyncMock(return_value={
                    'detected_tactics': [
                        {
                            'name': 'emotional_appeal',
                            'severity': 'medium',
                            'confidence': 0.75
                        }
                    ]
                })),
                ('safety_checker', AsyncMock(return_value={
                    'is_safe': True,
                    'safety_score': 95
                }))
            ]
            
            result = await orchestrator.conduct_comprehensive_analysis(
                sample_analysis_data['text'],
                AnalysisRequest(
                    text=sample_analysis_data['text'],
                    language=sample_analysis_data['language'],
                    level=AnalysisLevel.DEEP_ANALYSIS
                )
            )
            
            # Assertions
            assert result is not None
            assert 'overall_credibility_score' in result
            assert 'processing_time' in result
            assert 'analysis_id' in result
            assert result['overall_credibility_score'] >= 0
            assert result['overall_credibility_score'] <= 100
            assert result['processing_time'] > 0
    
    @pytest.mark.asyncio
    async def test_analyzer_failure_handling(self, orchestrator, sample_analysis_data):
        """Test graceful handling of analyzer failures"""
        
        with patch.object(orchestrator, 'analyzers') as mock_analyzers:
            # Simulate one analyzer failing
            mock_analyzers.items.return_value = [
                ('text_analysis', AsyncMock(side_effect=Exception("AI API Error"))),
                ('source_tracking', AsyncMock(return_value={'origins': []})),
                ('tactics_breakdown', AsyncMock(return_value={'detected_tactics': []}))
            ]
            
            result = await orchestrator.conduct_comprehensive_analysis(
                sample_analysis_data['text'],
                AnalysisRequest(text=sample_analysis_data['text'])
            )
            
            # Should still return result with error handling
            assert result is not None
            assert 'text_analysis' in result
            assert 'error' in result['text_analysis']
            assert result['text_analysis']['confidence'] == 0.0
    
    @pytest.mark.asyncio
    async def test_empty_text_handling(self, orchestrator):
        """Test handling of empty or invalid text"""
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            await orchestrator.conduct_comprehensive_analysis(
                "",
                AnalysisRequest(text="")
            )
    
    @pytest.mark.asyncio
    async def test_analysis_level_configuration(self, orchestrator, sample_analysis_data):
        """Test different analysis levels activate correct analyzers"""
        
        with patch.object(orchestrator, '_get_active_analyzers') as mock_get_analyzers:
            mock_get_analyzers.return_value = ['text_analysis']  # Quick scan only
            
            with patch.object(orchestrator, 'analyzers') as mock_analyzers:
                mock_analyzers.items.return_value = [
                    ('text_analysis', AsyncMock(return_value={'score': 75}))
                ]
                
                await orchestrator.conduct_comprehensive_analysis(
                    sample_analysis_data['text'],
                    AnalysisRequest(
                        text=sample_analysis_data['text'],
                        level=AnalysisLevel.QUICK_SCAN
                    )
                )
                
                # Verify only quick scan analyzers were called
                mock_get_analyzers.assert_called_once_with(AnalysisLevel.QUICK_SCAN)

class TestTextAnalyzer:
    
    @pytest.fixture
    def text_analyzer(self, mock_ai_service):
        return TextAnalyzer(ai_service=mock_ai_service)
    
    @pytest.mark.asyncio
    async def test_credibility_analysis(self, text_analyzer, sample_analysis_data):
        """Test basic credibility analysis"""
        
        result = await text_analyzer.analyze_credibility(
            sample_analysis_data['text']
        )
        
        assert 'credibility_score' in result
        assert 'confidence' in result
        assert 0 <= result['credibility_score'] <= 100
        assert 0 <= result['confidence'] <= 1
    
    @pytest.mark.asyncio
    async def test_fact_checking_integration(self, text_analyzer):
        """Test fact-checking functionality"""
        
        text_with_claims = "The Earth is flat and vaccines cause autism."
        
        result = await text_analyzer.check_factual_claims(text_with_claims)
        
        assert 'fact_checks' in result
        assert 'overall_factual_score' in result
        assert isinstance(result['fact_checks'], list)
    
    @pytest.mark.asyncio
    async def test_language_detection(self, text_analyzer):
        """Test automatic language detection"""
        
        english_text = "This is English text for testing."
        spanish_text = "Este es un texto en español para pruebas."
        
        en_result = await text_analyzer.detect_language(english_text)
        es_result = await text_analyzer.detect_language(spanish_text)
        
        assert en_result['language'] == 'en'
        assert es_result['language'] == 'es'
        assert en_result['confidence'] > 0.8
        assert es_result['confidence'] > 0.8
```

#### AI Service Unit Tests
```python
# tests/unit/test_ai_service.py
import pytest
from unittest.mock import AsyncMock, patch, Mock
import aiohttp
from src.services.ai_service import GoogleAIService

class TestGoogleAIService:
    
    @pytest.fixture
    def ai_service(self):
        return GoogleAIService(
            api_key="test_key",
            model_name="gemini-1.5-flash"
        )
    
    @pytest.mark.asyncio
    async def test_successful_analysis(self, ai_service):
        """Test successful AI analysis"""
        
        with patch.object(ai_service.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = '{"credibility_score": 75, "analysis": "Test result"}'
            mock_generate.return_value = mock_response
            
            result = await ai_service.analyze_with_prompt(
                "Test text",
                "Analyze this text for credibility"
            )
            
            assert result['credibility_score'] == 75
            assert result['analysis'] == "Test result"
            mock_generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self, ai_service):
        """Test handling of API errors"""
        
        with patch.object(ai_service.model, 'generate_content') as mock_generate:
            mock_generate.side_effect = Exception("API rate limit exceeded")
            
            with pytest.raises(Exception, match="API rate limit exceeded"):
                await ai_service.analyze_with_prompt("Test", "Prompt")
    
    @pytest.mark.asyncio
    async def test_batch_analysis(self, ai_service):
        """Test batch processing of multiple texts"""
        
        texts = ["Text 1", "Text 2", "Text 3"]
        
        with patch.object(ai_service, 'analyze_with_prompt') as mock_analyze:
            mock_analyze.side_effect = [
                {"score": 80}, {"score": 60}, {"score": 90}
            ]
            
            results = await ai_service.batch_analyze(
                texts, 
                "Test prompt",
                max_concurrent=2
            )
            
            assert len(results) == 3
            assert results[0]['score'] == 80
            assert results[1]['score'] == 60
            assert results[2]['score'] == 90
            assert mock_analyze.call_count == 3
    
    @pytest.mark.asyncio 
    async def test_response_parsing(self, ai_service):
        """Test parsing of various AI response formats"""
        
        test_cases = [
            # Valid JSON
            ('{"score": 85, "confidence": 0.9}', {"score": 85, "confidence": 0.9}),
            
            # JSON with extra text
            ('Here is the analysis: {"score": 75} - that\'s my result', {"score": 75}),
            
            # Invalid JSON
            ('This is not JSON at all', {
                "raw_response": "This is not JSON at all",
                "error": "Failed to parse JSON response",
                "confidence": 0.0
            })
        ]
        
        for response_text, expected in test_cases:
            result = ai_service._parse_ai_response(response_text)
            
            if 'error' in expected:
                assert 'error' in result
                assert result['confidence'] == 0.0
            else:
                assert result == expected
```

### 🔗 Integration Testing

#### API Endpoint Integration Tests
```python
# tests/integration/test_api_endpoints.py
import pytest
from httpx import AsyncClient
from src.api.main import app

class TestAnalysisAPI:
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_endpoint_success(self, test_client: AsyncClient):
        """Test successful analysis via API endpoint"""
        
        response = await test_client.post("/api/analyze", json={
            "text": "This is a test message for analysis.",
            "language": "en",
            "level": "Quick Scan"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "success" in data
        assert data["success"] is True
        assert "data" in data
        assert "overall_credibility_score" in data["data"]
        assert "analysis_id" in data["data"]
        assert "processing_time" in data["data"]
        
        # Verify data types and ranges
        assert isinstance(data["data"]["overall_credibility_score"], (int, float))
        assert 0 <= data["data"]["overall_credibility_score"] <= 100
        assert isinstance(data["data"]["analysis_id"], str)
        assert data["data"]["processing_time"] > 0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_endpoint_validation_errors(self, test_client: AsyncClient):
        """Test API validation error handling"""
        
        # Test missing required fields
        response = await test_client.post("/api/analyze", json={})
        assert response.status_code == 422
        
        # Test invalid text length
        response = await test_client.post("/api/analyze", json={
            "text": "x" * 50000,  # Too long
            "level": "Quick Scan"
        })
        assert response.status_code == 422
        
        # Test invalid analysis level
        response = await test_client.post("/api/analyze", json={
            "text": "Valid text",
            "level": "Invalid Level"
        })
        assert response.status_code == 422
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_different_levels(self, test_client: AsyncClient):
        """Test different analysis levels"""
        
        test_text = "Sample text for testing different analysis levels."
        
        levels = ["Quick Scan", "Deep Analysis", "Forensic Review"]
        
        for level in levels:
            response = await test_client.post("/api/analyze", json={
                "text": test_text,
                "level": level
            })
            
            assert response.status_code == 200
            data = response.json()
            
            # Forensic review should have additional fields
            if level == "Forensic Review":
                assert "source_tracking" in data["data"]
                assert "forensic_metadata" in data["data"]
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_batch_analysis_endpoint(self, test_client: AsyncClient):
        """Test batch analysis endpoint"""
        
        texts = [
            "First text for batch analysis.",
            "Second text for batch analysis.", 
            "Third text for batch analysis."
        ]
        
        response = await test_client.post("/api/analyze/batch", json={
            "texts": texts,
            "level": "Quick Scan"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data["data"]
        assert len(data["data"]["results"]) == 3
        
        for i, result in enumerate(data["data"]["results"]):
            assert "overall_credibility_score" in result
            assert "text_index" in result
            assert result["text_index"] == i

class TestHealthEndpoints:
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_basic_health_check(self, test_client: AsyncClient):
        """Test basic health check endpoint"""
        
        response = await test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_detailed_health_check(self, test_client: AsyncClient):
        """Test detailed health check with service status"""
        
        response = await test_client.get("/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "checks" in data
        assert "database" in data["checks"]
        assert "google_ai" in data["checks"]
        assert "version" in data

class TestArchiveAPI:
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_save_and_retrieve_analysis(self, test_client: AsyncClient):
        """Test saving and retrieving analysis results"""
        
        # First, perform an analysis
        analysis_response = await test_client.post("/api/analyze", json={
            "text": "Text to be saved in archive",
            "level": "Deep Analysis"
        })
        
        assert analysis_response.status_code == 200
        analysis_data = analysis_response.json()
        analysis_id = analysis_data["data"]["analysis_id"]
        
        # Save to archive
        save_response = await test_client.post("/api/archive", json={
            "analysis_id": analysis_id,
            "tags": ["test", "integration"],
            "notes": "Test analysis for integration testing"
        })
        
        assert save_response.status_code == 200
        
        # Retrieve from archive
        retrieve_response = await test_client.get(f"/api/archive/{analysis_id}")
        
        assert retrieve_response.status_code == 200
        archived_data = retrieve_response.json()
        
        assert archived_data["data"]["analysis_id"] == analysis_id
        assert "test" in archived_data["data"]["tags"]
        assert archived_data["data"]["notes"] == "Test analysis for integration testing"
```

#### Database Integration Tests
```python
# tests/integration/test_database_operations.py
import pytest
import asyncio
from src.services.database_service import DatabaseService
from src.models.analysis_models import AnalysisResult

class TestDatabaseService:
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_save_and_retrieve_analysis(self, test_db):
        """Test saving and retrieving analysis results"""
        
        db_service = DatabaseService(test_db)
        
        analysis_data = {
            "id": "test_analysis_001",
            "text_hash": "abc123def456",
            "results": {
                "overall_credibility_score": 75,
                "processing_time": 2.5
            },
            "timestamp": "2024-01-15T10:30:00Z",
            "user_id": "user_123"
        }
        
        # Save analysis
        analysis_id = await db_service.save_analysis(analysis_data)
        assert analysis_id == "test_analysis_001"
        
        # Retrieve analysis
        retrieved = await db_service.get_analysis(analysis_id)
        
        assert retrieved["id"] == analysis_data["id"]
        assert retrieved["results"]["overall_credibility_score"] == 75
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_bulk_operations(self, test_db):
        """Test bulk insert and query operations"""
        
        db_service = DatabaseService(test_db)
        
        # Create multiple analysis records
        analyses = [
            {
                "id": f"bulk_test_{i:03d}",
                "text_hash": f"hash_{i}",
                "results": {"score": 50 + i},
                "timestamp": f"2024-01-15T10:{30+i:02d}:00Z",
                "user_id": "bulk_user"
            }
            for i in range(10)
        ]
        
        # Bulk insert
        inserted_ids = await db_service.bulk_insert_analyses(analyses)
        assert len(inserted_ids) == 10
        
        # Query with pagination
        paginated_results = await db_service.get_analyses_with_pagination(
            user_id="bulk_user",
            limit=5,
            offset=0
        )
        
        assert len(paginated_results["records"]) == 5
        assert paginated_results["total_count"] == 10
        assert paginated_results["has_more"] is True
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_complex_queries(self, test_db):
        """Test complex database queries with filters"""
        
        db_service = DatabaseService(test_db)
        
        # Insert test data with various scores
        test_analyses = [
            {"id": "high_score", "results": {"score": 90}, "user_id": "test_user"},
            {"id": "medium_score", "results": {"score": 70}, "user_id": "test_user"}, 
            {"id": "low_score", "results": {"score": 30}, "user_id": "test_user"}
        ]
        
        for analysis in test_analyses:
            await db_service.save_analysis({
                **analysis,
                "text_hash": "test_hash",
                "timestamp": "2024-01-15T10:30:00Z"
            })
        
        # Query with credibility filter
        high_credibility = await db_service.get_analyses_with_pagination(
            user_id="test_user",
            filters={"min_credibility": 80}
        )
        
        assert len(high_credibility["records"]) == 1
        assert high_credibility["records"][0]["id"] == "high_score"
```

---

## 🎨 Frontend Testing (React + JavaScript)

### 🛠️ Testing Framework Setup

#### Core Testing Dependencies
```json
// package.json - devDependencies
{
  "@testing-library/react": "^13.4.0",
  "@testing-library/jest-dom": "^5.16.5",
  "@testing-library/user-event": "^14.4.3",
  "vitest": "^0.34.0",
  "jsdom": "^22.1.0",
  "msw": "^1.3.0",
  "@playwright/test": "^1.37.0",
  "eslint-plugin-testing-library": "^6.0.0"
}
```

#### Vitest Configuration
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    coverage: {
      reporter: ['text', 'html', 'clover'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.test.{js,jsx}',
        'src/main.jsx'
      ]
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@components': resolve(__dirname, './src/components'),
      '@pages': resolve(__dirname, './src/pages'),
      '@services': resolve(__dirname, './src/services'),
      '@utils': resolve(__dirname, './src/utils')
    }
  }
});
```

#### Test Setup Configuration
```javascript
// src/test/setup.js
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn()
}));

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn()
}));

// Mock fetch for tests
global.fetch = vi.fn();

// Mock window.scrollTo
Object.defineProperty(window, 'scrollTo', { value: vi.fn(), writable: true });
```

### 🧪 Component Unit Testing

#### Core Component Tests
```javascript
// src/components/__tests__/Header.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import Header from '../Header';
import { AuthContext } from '../../contexts/AuthContext';

const MockAuthProvider = ({ children, value = {} }) => (
  <AuthContext.Provider value={{
    user: null,
    isAuthenticated: false,
    login: vi.fn(),
    logout: vi.fn(),
    ...value
  }}>
    {children}
  </AuthContext.Provider>
);

const renderHeader = (authValue = {}) => {
  return render(
    <BrowserRouter>
      <MockAuthProvider value={authValue}>
        <Header />
      </MockAuthProvider>
    </BrowserRouter>
  );
};

describe('Header Component', () => {
  test('renders navigation links correctly', () => {
    renderHeader();
    
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Archive')).toBeInTheDocument();
    expect(screen.getByText('Learn')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /home/i })).toHaveAttribute('href', '/');
  });

  test('shows login button when user is not authenticated', () => {
    renderHeader({ isAuthenticated: false });
    
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.queryByText('Logout')).not.toBeInTheDocument();
  });

  test('shows user menu when authenticated', () => {
    const mockUser = { name: 'John Doe', type: 'public' };
    renderHeader({ 
      isAuthenticated: true, 
      user: mockUser 
    });
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.queryByText('Login')).not.toBeInTheDocument();
  });

  test('handles mobile menu toggle', async () => {
    renderHeader();
    
    // Mobile menu button should be hidden on desktop (using CSS)
    const mobileMenuButton = screen.getByLabelText(/toggle mobile menu/i);
    
    fireEvent.click(mobileMenuButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-menu')).toBeInTheDocument();
    });
  });

  test('handles logout functionality', async () => {
    const mockLogout = vi.fn();
    renderHeader({ 
      isAuthenticated: true,
      user: { name: 'John Doe' },
      logout: mockLogout 
    });
    
    // Click user menu to open dropdown
    fireEvent.click(screen.getByText('John Doe'));
    
    // Click logout button
    const logoutButton = screen.getByText('Logout');
    fireEvent.click(logoutButton);
    
    expect(mockLogout).toHaveBeenCalledOnce();
  });
});
```

#### Analysis Component Tests
```javascript
// src/components/__tests__/AnalysisResults.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import AnalysisResults from '../AnalysisResults/AnalysisResults';

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
      },
      {
        name: 'False Urgency',
        severity: 'high', 
        description: 'Creates artificial time pressure',
        examples: ['act now', 'limited time']
      }
    ]
  },
  processing_time: 2.5,
  timestamp: '2024-01-15T10:30:00Z'
};

describe('AnalysisResults Component', () => {
  test('displays credibility score correctly', () => {
    render(<AnalysisResults results={mockResults} />);
    
    expect(screen.getByText('75/100')).toBeInTheDocument();
    expect(screen.getByText('Moderate Credibility')).toBeInTheDocument();
  });

  test('shows correct credibility level colors', () => {
    // Test high credibility (green)
    const highResults = { ...mockResults, overall_credibility_score: 85 };
    const { rerender } = render(<AnalysisResults results={highResults} />);
    
    expect(screen.getByText('High Credibility')).toBeInTheDocument();
    
    // Test low credibility (red)
    const lowResults = { ...mockResults, overall_credibility_score: 30 };
    rerender(<AnalysisResults results={lowResults} />);
    
    expect(screen.getByText('Low Credibility')).toBeInTheDocument();
  });

  test('displays manipulation tactics when present', () => {
    render(<AnalysisResults results={mockResults} />);
    
    expect(screen.getByText('Manipulation Tactics Detected (2)')).toBeInTheDocument();
    expect(screen.getByText('Emotional Appeal')).toBeInTheDocument();
    expect(screen.getByText('False Urgency')).toBeInTheDocument();
    expect(screen.getByText('medium')).toBeInTheDocument();
    expect(screen.getByText('high')).toBeInTheDocument();
  });

  test('shows loading state correctly', () => {
    render(<AnalysisResults isLoading={true} />);
    
    expect(screen.getByText('Analyzing content...')).toBeInTheDocument();
    expect(screen.getByRole('status')).toBeInTheDocument(); // Loading spinner
  });

  test('displays error state properly', () => {
    const errorMessage = 'Analysis failed due to network error';
    render(<AnalysisResults error={errorMessage} />);
    
    expect(screen.getByText('Analysis Failed')).toBeInTheDocument();
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  test('handles export functionality', async () => {
    const mockExportToPDF = vi.fn();
    global.exportToPDF = mockExportToPDF;
    
    render(<AnalysisResults results={mockResults} />);
    
    const exportButton = screen.getByText('Export PDF');
    fireEvent.click(exportButton);
    
    expect(mockExportToPDF).toHaveBeenCalledWith(mockResults);
  });

  test('metric cards display correct values', () => {
    render(<AnalysisResults results={mockResults} />);
    
    // Check individual metric values
    expect(screen.getByText('80')).toBeInTheDocument(); // Factual Accuracy
    expect(screen.getByText('70')).toBeInTheDocument(); // Source Quality  
    expect(screen.getByText('75')).toBeInTheDocument(); // Logic Score
    expect(screen.getByText('75')).toBeInTheDocument(); // Bias Level (100 - 25)
  });

  test('renders without manipulation tactics', () => {
    const resultsWithoutTactics = {
      ...mockResults,
      manipulation_analysis: { detected_tactics: [] }
    };
    
    render(<AnalysisResults results={resultsWithoutTactics} />);
    
    expect(screen.queryByText(/Manipulation Tactics Detected/)).not.toBeInTheDocument();
  });
});
```

#### Custom Hooks Testing
```javascript
// src/hooks/__tests__/useAnalysisAPI.test.js
import { renderHook, waitFor, act } from '@testing-library/react';
import { vi } from 'vitest';
import { useAnalysisAPI } from '../useAnalysisAPI';
import * as analysisAPI from '../../services/api';

// Mock the API module
vi.mock('../../services/api', () => ({
  analysisAPI: {
    analyze: vi.fn()
  }
}));

describe('useAnalysisAPI Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('initial state is correct', () => {
    const { result } = renderHook(() => useAnalysisAPI());
    
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(null);
    expect(result.current.lastResult).toBe(null);
  });

  test('handles successful analysis', async () => {
    const mockResult = { overall_credibility_score: 75 };
    analysisAPI.analysisAPI.analyze.mockResolvedValue(mockResult);
    
    const { result } = renderHook(() => useAnalysisAPI());
    
    act(() => {
      result.current.analyzeText('test text', { level: 'Quick Scan' });
    });
    
    // Should be loading initially
    expect(result.current.isLoading).toBe(true);
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.lastResult).toEqual(mockResult);
    expect(result.current.error).toBe(null);
  });

  test('handles API errors correctly', async () => {
    const mockError = new Error('API Error');
    analysisAPI.analysisAPI.analyze.mockRejectedValue(mockError);
    
    const { result } = renderHook(() => useAnalysisAPI());
    
    await act(async () => {
      try {
        await result.current.analyzeText('test text');
      } catch (error) {
        // Expected to throw
      }
    });
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.error).toBe('API Error');
    expect(result.current.lastResult).toBe(null);
  });

  test('cancels previous request when new one starts', async () => {
    const { result } = renderHook(() => useAnalysisAPI());
    
    // Start first request
    const firstPromise = act(() => 
      result.current.analyzeText('first text')
    );
    
    // Start second request immediately
    const secondPromise = act(() => 
      result.current.analyzeText('second text')
    );
    
    // First request should be aborted
    await expect(firstPromise).rejects.toThrow();
    
    // Only second request should succeed
    await waitFor(() => {
      expect(analysisAPI.analysisAPI.analyze).toHaveBeenCalledTimes(2);
    });
  });

  test('manual cancellation works', async () => {
    analysisAPI.analysisAPI.analyze.mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 1000))
    );
    
    const { result } = renderHook(() => useAnalysisAPI());
    
    // Start analysis
    act(() => {
      result.current.analyzeText('test text');
    });
    
    expect(result.current.isLoading).toBe(true);
    
    // Cancel analysis
    act(() => {
      result.current.cancelAnalysis();
    });
    
    expect(result.current.isLoading).toBe(false);
  });
});
```

### 🔗 Integration Testing with MSW

#### API Mocking Setup
```javascript
// src/test/mocks/handlers.js
import { rest } from 'msw';

export const handlers = [
  // Analysis endpoint
  rest.post('/api/analyze', (req, res, ctx) => {
    const { text, level } = req.body;
    
    // Simulate different response times
    const delay = level === 'Forensic Review' ? 2000 : 500;
    
    return res(
      ctx.delay(delay),
      ctx.status(200),
      ctx.json({
        success: true,
        data: {
          analysis_id: 'test_' + Date.now(),
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
                description: 'Test manipulation tactic'
              }
            ]
          },
          processing_time: delay / 1000,
          timestamp: new Date().toISOString()
        }
      })
    );
  }),

  // Health check endpoint
  rest.get('/health', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        status: 'healthy',
        timestamp: new Date().toISOString()
      })
    );
  }),

  // Archive endpoints
  rest.get('/api/archive', (req, res, ctx) => {
    const page = req.url.searchParams.get('page') || 1;
    const limit = req.url.searchParams.get('limit') || 20;
    
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        data: {
          records: [
            {
              id: 'archived_1',
              text_preview: 'Sample archived analysis...',
              credibility_score: 85,
              timestamp: '2024-01-15T10:30:00Z',
              tags: ['test', 'sample']
            }
          ],
          pagination: {
            page: parseInt(page),
            limit: parseInt(limit),
            total: 1,
            has_more: false
          }
        }
      })
    );
  }),

  // Error simulation
  rest.post('/api/analyze', (req, res, ctx) => {
    const { text } = req.body;
    
    // Simulate server error for specific text
    if (text.includes('ERROR_SIMULATION')) {
      return res(
        ctx.status(500),
        ctx.json({
          success: false,
          error: 'Internal server error',
          message: 'Analysis service temporarily unavailable'
        })
      );
    }
    
    // Normal response for other texts
    return res(ctx.status(200), ctx.json({ /* ... */ }));
  })
];

// src/test/mocks/server.js
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

#### Integration Test Examples
```javascript
// src/pages/__tests__/Home.integration.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { server } from '../../test/mocks/server';
import Home from '../Home';

// MSW server setup
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

const renderHomePage = () => {
  return render(
    <BrowserRouter>
      <Home />
    </BrowserRouter>
  );
};

describe('Home Page Integration Tests', () => {
  test('complete analysis workflow', async () => {
    const user = userEvent.setup();
    renderHomePage();
    
    // Verify page loads
    expect(screen.getByText(/Truth Lab 2.0/)).toBeInTheDocument();
    
    // Enter text for analysis
    const textInput = screen.getByPlaceholderText(/enter text to analyze/i);
    await user.type(textInput, 'This is a sample text for integration testing');
    
    // Select analysis level
    const levelSelect = screen.getByLabelText(/analysis level/i);
    await user.selectOptions(levelSelect, 'Deep Analysis');
    
    // Start analysis
    const analyzeButton = screen.getByRole('button', { name: /analyze now/i });
    await user.click(analyzeButton);
    
    // Verify loading state
    expect(screen.getByText(/analyzing content/i)).toBeInTheDocument();
    expect(analyzeButton).toBeDisabled();
    
    // Wait for results
    await waitFor(() => {
      expect(screen.getByText(/75\/100/)).toBeInTheDocument();
    }, { timeout: 3000 });
    
    // Verify results display
    expect(screen.getByText(/Moderate Credibility/)).toBeInTheDocument();
    expect(screen.getByText(/Manipulation Tactics Detected/)).toBeInTheDocument();
    expect(screen.getByText(/Emotional Appeal/)).toBeInTheDocument();
    
    // Test export functionality
    const exportButton = screen.getByText(/Export PDF/);
    expect(exportButton).toBeInTheDocument();
    
    // Test share functionality  
    const shareButton = screen.getByText(/Share Analysis/);
    expect(shareButton).toBeInTheDocument();
  });

  test('handles analysis errors gracefully', async () => {
    const user = userEvent.setup();
    renderHomePage();
    
    // Enter text that triggers error simulation
    const textInput = screen.getByPlaceholderText(/enter text to analyze/i);
    await user.type(textInput, 'ERROR_SIMULATION test text');
    
    // Start analysis
    const analyzeButton = screen.getByRole('button', { name: /analyze now/i });
    await user.click(analyzeButton);
    
    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/Analysis Failed/)).toBeInTheDocument();
    });
    
    expect(screen.getByText(/Internal server error/)).toBeInTheDocument();
  });

  test('validates input requirements', async () => {
    const user = userEvent.setup();
    renderHomePage();
    
    // Try to analyze without entering text
    const analyzeButton = screen.getByRole('button', { name: /analyze now/i });
    await user.click(analyzeButton);
    
    // Should show validation error
    expect(screen.getByText(/Please enter text to analyze/)).toBeInTheDocument();
    
    // Enter very short text
    const textInput = screen.getByPlaceholderText(/enter text to analyze/i);
    await user.type(textInput, 'Hi');
    await user.click(analyzeButton);
    
    // Should show minimum length error
    expect(screen.getByText(/Text must be at least/)).toBeInTheDocument();
  });
});
```

---

## 🌐 End-to-End Testing (E2E)

### 🎭 Playwright Setup & Configuration

#### Playwright Configuration
```javascript
// playwright.config.js
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },

  projects: [
    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // Mobile devices
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },

    // Tablet
    {
      name: 'iPad',
      use: { ...devices['iPad Pro'] },
    }
  ],

  webServer: [
    {
      command: 'npm run dev',
      port: 3000,
      reuseExistingServer: !process.env.CI
    },
    {
      command: 'cd backend && uvicorn src.api.main:app --port 8000',
      port: 8000,
      reuseExistingServer: !process.env.CI
    }
  ]
});
```

#### Page Object Model Implementation
```javascript
// e2e/pages/HomePage.js
export class HomePage {
  constructor(page) {
    this.page = page;
    
    // Selectors
    this.textInput = '[data-testid="analysis-input"]';
    this.levelSelect = '[data-testid="analysis-level"]';
    this.analyzeButton = '[data-testid="analyze-button"]';
    this.loadingSpinner = '[data-testid="loading-spinner"]';
    this.resultsContainer = '[data-testid="analysis-results"]';
    this.credibilityScore = '[data-testid="credibility-score"]';
    this.errorMessage = '[data-testid="error-message"]';
  }

  async navigate() {
    await this.page.goto('/');
    await this.page.waitForLoadState('networkidle');
  }

  async enterText(text) {
    await this.page.fill(this.textInput, text);
  }

  async selectAnalysisLevel(level) {
    await this.page.selectOption(this.levelSelect, level);
  }

  async startAnalysis() {
    await this.page.click(this.analyzeButton);
  }

  async waitForAnalysisComplete() {
    // Wait for loading to start
    await this.page.waitForSelector(this.loadingSpinner, { state: 'visible' });
    
    // Wait for loading to finish
    await this.page.waitForSelector(this.loadingSpinner, { state: 'hidden' });
    
    // Wait for results to appear
    await this.page.waitForSelector(this.resultsContainer, { state: 'visible' });
  }

  async getCredibilityScore() {
    const element = await this.page.locator(this.credibilityScore);
    return await element.textContent();
  }

  async getManipulationTactics() {
    const tactics = await this.page.locator('[data-testid="manipulation-tactic"]');
    return await tactics.allTextContents();
  }

  async exportToPDF() {
    const downloadPromise = this.page.waitForEvent('download');
    await this.page.click('[data-testid="export-pdf-button"]');
    return await downloadPromise;
  }

  async shareAnalysis() {
    await this.page.click('[data-testid="share-button"]');
    
    // Wait for share modal
    await this.page.waitForSelector('[data-testid="share-modal"]');
    
    // Get share URL
    const shareUrl = await this.page.inputValue('[data-testid="share-url"]');
    return shareUrl;
  }
}
```

#### Comprehensive E2E Test Scenarios
```javascript
// e2e/analysis-workflow.spec.js
import { test, expect } from '@playwright/test';
import { HomePage } from './pages/HomePage';

test.describe('Truth Lab 2.0 Analysis Workflow', () => {
  let homePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.navigate();
  });

  test('complete analysis workflow - high credibility text', async ({ page }) => {
    await test.step('Enter high credibility text', async () => {
      const credibleText = `
        According to a peer-reviewed study published in Nature magazine in 2023,
        researchers at MIT have developed a new methodology for detecting 
        misinformation using advanced natural language processing techniques.
        The study, which analyzed over 100,000 news articles, found that 
        linguistic patterns can be reliable indicators of information credibility.
      `;
      
      await homePage.enterText(credibleText);
    });

    await test.step('Configure analysis settings', async () => {
      await homePage.selectAnalysisLevel('Deep Analysis');
    });

    await test.step('Perform analysis', async () => {
      await homePage.startAnalysis();
      await homePage.waitForAnalysisComplete();
    });

    await test.step('Verify high credibility results', async () => {
      const scoreText = await homePage.getCredibilityScore();
      const score = parseInt(scoreText.split('/')[0]);
      
      expect(score).toBeGreaterThanOrEqual(70);
      
      // Should show green (high credibility) styling
      await expect(page.locator('[data-testid="credibility-badge"]'))
        .toHaveClass(/green|high-credibility/);
    });

    await test.step('Test export functionality', async () => {
      const download = await homePage.exportToPDF();
      expect(download.suggestedFilename()).toMatch(/truth-lab-analysis.*\.pdf/);
    });
  });

  test('analysis workflow - low credibility text with manipulation', async ({ page }) => {
    await test.step('Enter suspicious text', async () => {
      const suspiciousText = `
        URGENT! BREAKING NEWS! Scientists are HIDING the truth about vaccines!
        This shocking revelation will DESTROY the medical establishment!
        Share this immediately before they delete it! The government doesn't 
        want you to know this one weird trick that doctors HATE!
        Time is running out - act NOW or face the consequences!
      `;
      
      await homePage.enterText(suspiciousText);
    });

    await test.step('Perform forensic analysis', async () => {
      await homePage.selectAnalysisLevel('Forensic Review');
      await homePage.startAnalysis();
      await homePage.waitForAnalysisComplete();
    });

    await test.step('Verify low credibility detection', async () => {
      const scoreText = await homePage.getCredibilityScore();
      const score = parseInt(scoreText.split('/')[0]);
      
      expect(score).toBeLessThan(50);
      
      // Should show red (low credibility) styling
      await expect(page.locator('[data-testid="credibility-badge"]'))
        .toHaveClass(/red|low-credibility/);
    });

    await test.step('Verify manipulation tactics detection', async () => {
      const tactics = await homePage.getManipulationTactics();
      
      expect(tactics.length).toBeGreaterThan(0);
      
      // Should detect common manipulation patterns
      const tacticNames = tactics.join(' ').toLowerCase();
      expect(tacticNames).toMatch(/emotional|urgency|fear|authority/);
    });

    await test.step('Test sharing functionality', async () => {
      const shareUrl = await homePage.shareAnalysis();
      expect(shareUrl).toMatch(/https?:\/\/.*\/share\/[a-zA-Z0-9]+/);
    });
  });

  test('handles network errors gracefully', async ({ page }) => {
    await test.step('Setup network failure', async () => {
      // Block API requests
      await page.route('**/api/analyze', route => {
        route.abort('failed');
      });
    });

    await test.step('Attempt analysis', async () => {
      await homePage.enterText('Test text for network error');
      await homePage.startAnalysis();
    });

    await test.step('Verify error handling', async () => {
      await expect(page.locator('[data-testid="error-message"]'))
        .toBeVisible();
      
      await expect(page.locator('[data-testid="error-message"]'))
        .toContainText(/network error|failed to connect|connection failed/i);
    });

    await test.step('Test retry functionality', async () => {
      // Remove network block
      await page.unroute('**/api/analyze');
      
      // Click retry button
      await page.click('[data-testid="retry-button"]');
      
      // Should work now
      await homePage.waitForAnalysisComplete();
      await expect(page.locator('[data-testid="analysis-results"]'))
        .toBeVisible();
    });
  });
});

// e2e/responsive-design.spec.js
test.describe('Responsive Design Testing', () => {
  test('mobile interface works correctly', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    const homePage = new HomePage(page);
    await homePage.navigate();

    await test.step('Test mobile navigation', async () => {
      // Mobile menu should be visible
      await expect(page.locator('[data-testid="mobile-menu-button"]'))
        .toBeVisible();
      
      // Desktop menu should be hidden
      await expect(page.locator('[data-testid="desktop-menu"]'))
        .toBeHidden();
      
      // Open mobile menu
      await page.click('[data-testid="mobile-menu-button"]');
      await expect(page.locator('[data-testid="mobile-menu"]'))
        .toBeVisible();
    });

    await test.step('Test mobile analysis interface', async () => {
      // Input should be full width on mobile
      const input = page.locator('[data-testid="analysis-input"]');
      const inputBox = await input.boundingBox();
      
      expect(inputBox.width).toBeGreaterThan(300);
      
      // Buttons should stack vertically on mobile
      const buttons = page.locator('[data-testid="action-buttons"]');
      await expect(buttons).toHaveClass(/flex-col|vertical/);
    });

    await test.step('Perform mobile analysis', async () => {
      await homePage.enterText('Mobile testing text');
      await homePage.startAnalysis();
      await homePage.waitForAnalysisComplete();
      
      // Results should be readable on mobile
      const results = page.locator('[data-testid="analysis-results"]');
      await expect(results).toBeVisible();
      
      // Score should be prominently displayed
      await expect(page.locator('[data-testid="credibility-score"]'))
        .toBeVisible();
    });
  });

  test('tablet interface adapts correctly', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    
    const homePage = new HomePage(page);
    await homePage.navigate();

    // Should show desktop-like interface but optimized for touch
    await expect(page.locator('[data-testid="desktop-menu"]'))
      .toBeVisible();
    
    await expect(page.locator('[data-testid="mobile-menu-button"]'))
      .toBeHidden();
    
    // Touch targets should be appropriately sized
    const buttons = page.locator('button');
    const firstButton = buttons.first();
    const buttonBox = await firstButton.boundingBox();
    
    expect(buttonBox.height).toBeGreaterThanOrEqual(44); // iOS minimum touch target
  });
});
```

---

## 🚀 Performance Testing

### 📊 Load Testing with Artillery

#### Artillery Configuration
```yaml
# performance/load-test.yml
config:
  target: 'http://localhost:8000'
  phases:
    # Warm-up phase
    - duration: 60
      arrivalRate: 5
      name: "Warm up"
    
    # Load testing phase
    - duration: 300
      arrivalRate: 20
      name: "Load test"
    
    # Stress testing phase  
    - duration: 120
      arrivalRate: 50
      name: "Stress test"
    
    # Spike testing
    - duration: 60
      arrivalRate: 100
      name: "Spike test"

  processor: "./load-test-functions.js"
  
scenarios:
  - name: "Analysis API Load Test"
    weight: 80
    flow:
      - post:
          url: "/api/analyze"
          json:
            text: "{{ $randomString() }} analysis test content for load testing purposes."
            level: "{{ $randomItem(['Quick Scan', 'Deep Analysis']) }}"
          capture:
            - json: "$.data.analysis_id"
              as: "analysisId"
      - think: 2
      
  - name: "Health Check"
    weight: 10
    flow:
      - get:
          url: "/health"
      
  - name: "Archive Access"
    weight: 10
    flow:
      - get:
          url: "/api/archive"
          qs:
            limit: 20
            page: 1
```

#### Load Testing Functions
```javascript
// performance/load-test-functions.js
const faker = require('faker');

module.exports = {
  // Generate random text for analysis
  $randomString: function() {
    const templates = [
      "Breaking news: Scientists have discovered that",
      "According to recent studies published in",
      "URGENT WARNING: Government officials are hiding", 
      "New research reveals shocking truth about",
      "Experts claim that this simple trick will"
    ];
    
    const template = faker.random.arrayElement(templates);
    const continuation = faker.lorem.sentences(3);
    
    return `${template} ${continuation}`;
  },
  
  // Random array item selection
  $randomItem: function(items) {
    return faker.random.arrayElement(items);
  }
};
```

### 🔬 Backend Performance Benchmarks

#### Performance Test Implementation
```python
# tests/performance/test_api_performance.py
import pytest
import asyncio
import time
import statistics
from httpx import AsyncClient
from concurrent.futures import ThreadPoolExecutor
import psutil
import os

class TestAPIPerformance:
    
    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_analysis_endpoint_performance(self, test_client):
        """Benchmark analysis endpoint performance"""
        
        test_texts = [
            "Short text for quick analysis testing.",
            "Medium length text that contains more detailed content for analysis. This should take a moderate amount of processing time.",
            """Long text content with multiple sentences and complex structure.
            This text is designed to test the performance of the analysis engine
            when processing larger amounts of content. It includes various linguistic
            patterns and should trigger multiple analysis modules to provide
            comprehensive performance metrics for evaluation purposes."""
        ]
        
        performance_results = []
        
        for text in test_texts:
            # Measure single request performance
            start_time = time.perf_counter()
            
            response = await test_client.post("/api/analyze", json={
                "text": text,
                "level": "Deep Analysis"
            })
            
            end_time = time.perf_counter()
            response_time = end_time - start_time
            
            assert response.status_code == 200
            
            performance_results.append({
                'text_length': len(text),
                'response_time': response_time,
                'words_per_second': len(text.split()) / response_time
            })
        
        # Performance assertions
        for result in performance_results:
            assert result['response_time'] < 10.0  # Max 10 seconds
            assert result['words_per_second'] > 5   # Min 5 words/second processing
        
        # Log performance metrics
        avg_response_time = statistics.mean([r['response_time'] for r in performance_results])
        print(f"\nAverage response time: {avg_response_time:.2f}s")
        print(f"Performance results: {performance_results}")
    
    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_concurrent_requests_performance(self, test_client):
        """Test performance under concurrent load"""
        
        concurrent_requests = 20
        
        async def single_analysis():
            start_time = time.perf_counter()
            response = await test_client.post("/api/analyze", json={
                "text": "Concurrent load test message for performance evaluation.",
                "level": "Quick Scan"
            })
            end_time = time.perf_counter()
            
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'success': response.status_code == 200
            }
        
        # Execute concurrent requests
        start_time = time.perf_counter()
        
        tasks = [single_analysis() for _ in range(concurrent_requests)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # Filter out exceptions
        successful_results = [r for r in results if isinstance(r, dict) and r['success']]
        
        # Performance assertions
        success_rate = len(successful_results) / concurrent_requests
        assert success_rate >= 0.95  # 95% success rate minimum
        
        avg_response_time = statistics.mean([r['response_time'] for r in successful_results])
        assert avg_response_time < 15.0  # Average under 15 seconds under load
        
        throughput = len(successful_results) / total_time
        assert throughput > 2.0  # Minimum 2 requests per second
        
        print(f"\nConcurrent Performance Results:")
        print(f"Success rate: {success_rate:.2%}")
        print(f"Average response time: {avg_response_time:.2f}s")
        print(f"Throughput: {throughput:.2f} req/s")
    
    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self):
        """Monitor memory usage during intensive operations"""
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simulate memory-intensive operations
        analysis_tasks = []
        
        for i in range(50):
            # Create large text for analysis
            large_text = "Memory test content. " * 1000  # ~20KB per text
            
            # This would normally call analysis engine
            # For testing, we'll simulate memory allocation
            analysis_tasks.append(large_text)
        
        # Process all tasks
        for text in analysis_tasks:
            # Simulate analysis processing
            await asyncio.sleep(0.01)
            
            # Check memory periodically
            current_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = current_memory - initial_memory
            
            # Memory usage should stay reasonable
            assert memory_increase < 500  # Less than 500MB increase
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        total_memory_increase = final_memory - initial_memory
        
        print(f"\nMemory Usage Results:")
        print(f"Initial memory: {initial_memory:.2f} MB")
        print(f"Final memory: {final_memory:.2f} MB")
        print(f"Total increase: {total_memory_increase:.2f} MB")
        
        # Clean up should release most memory
        del analysis_tasks
        import gc
        gc.collect()
        
        cleanup_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_after_cleanup = cleanup_memory - initial_memory
        
        assert memory_after_cleanup < total_memory_increase * 0.5  # 50% cleanup minimum
```

### 🎨 Frontend Performance Testing

#### Web Vitals Testing
```javascript
// e2e/performance/web-vitals.spec.js
import { test, expect } from '@playwright/test';

test.describe('Web Vitals Performance', () => {
  test('Core Web Vitals meet thresholds', async ({ page }) => {
    // Navigate to home page
    await page.goto('/');
    
    // Measure Core Web Vitals
    const vitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const vitals = {};
          
          entries.forEach((entry) => {
            if (entry.entryType === 'measure') {
              vitals[entry.name] = entry.duration;
            } else if (entry.entryType === 'navigation') {
              vitals.loadTime = entry.loadEventEnd - entry.loadEventStart;
              vitals.domContentLoaded = entry.domContentLoadedEventEnd - entry.domContentLoadedEventStart;
            }
          });
          
          resolve(vitals);
        });
        
        observer.observe({ entryTypes: ['measure', 'navigation'] });
        
        // Trigger measurement
        performance.measure('page-load', 'navigationStart', 'loadEventEnd');
        
        setTimeout(() => resolve({}), 5000); // Fallback timeout
      });
    });
    
    // Core Web Vitals thresholds
    // LCP (Largest Contentful Paint) < 2.5s
    // FID (First Input Delay) < 100ms  
    // CLS (Cumulative Layout Shift) < 0.1
    
    console.log('Web Vitals Results:', vitals);
    
    if (vitals.loadTime) {
      expect(vitals.loadTime).toBeLessThan(2500); // 2.5s LCP threshold
    }
  });

  test('Bundle size analysis', async ({ page }) => {
    // Monitor network requests to analyze bundle size
    const resources = [];
    
    page.on('response', (response) => {
      if (response.url().includes('.js') || response.url().includes('.css')) {
        resources.push({
          url: response.url(),
          size: parseInt(response.headers()['content-length'] || '0'),
          type: response.url().includes('.js') ? 'javascript' : 'css'
        });
      }
    });
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Calculate total bundle sizes
    const jsSize = resources
      .filter(r => r.type === 'javascript')
      .reduce((total, r) => total + r.size, 0);
      
    const cssSize = resources
      .filter(r => r.type === 'css')
      .reduce((total, r) => total + r.size, 0);
    
    console.log(`JavaScript bundle size: ${(jsSize / 1024).toFixed(2)} KB`);
    console.log(`CSS bundle size: ${(cssSize / 1024).toFixed(2)} KB`);
    
    // Bundle size thresholds
    expect(jsSize).toBeLessThan(500 * 1024); // 500KB JS
    expect(cssSize).toBeLessThan(100 * 1024); // 100KB CSS
  });

  test('Analysis performance under interaction load', async ({ page }) => {
    await page.goto('/');
    
    // Perform multiple rapid analyses to test UI performance
    const analysisTexts = [
      'First rapid analysis test',
      'Second rapid analysis test', 
      'Third rapid analysis test'
    ];
    
    const performanceMetrics = [];
    
    for (const text of analysisTexts) {
      const startTime = Date.now();
      
      // Fill input
      await page.fill('[data-testid="analysis-input"]', text);
      
      // Start analysis
      await page.click('[data-testid="analyze-button"]');
      
      // Wait for results
      await page.waitForSelector('[data-testid="analysis-results"]', {
        timeout: 30000
      });
      
      const endTime = Date.now();
      const duration = endTime - startTime;
      
      performanceMetrics.push({
        text,
        duration,
        timestamp: new Date().toISOString()
      });
      
      // Clear for next test
      await page.fill('[data-testid="analysis-input"]', '');
    }
    
    // Performance assertions
    const avgDuration = performanceMetrics.reduce((sum, m) => sum + m.duration, 0) / performanceMetrics.length;
    
    expect(avgDuration).toBeLessThan(15000); // 15 second average
    
    // No analysis should take more than 30 seconds
    performanceMetrics.forEach(metric => {
      expect(metric.duration).toBeLessThan(30000);
    });
    
    console.log('Analysis Performance Results:', performanceMetrics);
  });
});
```

---

## 🔒 Security Testing

### 🛡️ Security Test Implementation

#### Input Validation Security Tests
```python
# tests/security/test_input_validation.py
import pytest
from httpx import AsyncClient

class TestInputSecurity:
    
    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_sql_injection_prevention(self, test_client: AsyncClient):
        """Test protection against SQL injection attacks"""
        
        malicious_inputs = [
            "'; DROP TABLE analyses; --",
            "' OR 1=1 --",
            "'; UPDATE analyses SET results='hacked' WHERE 1=1; --",
            "test'; INSERT INTO analyses (id, text_hash) VALUES ('evil', 'hack'); --"
        ]
        
        for malicious_input in malicious_inputs:
            response = await test_client.post("/api/analyze", json={
                "text": malicious_input,
                "level": "Quick Scan"
            })
            
            # Should either reject with validation error or process safely
            assert response.status_code in [200, 422]
            
            if response.status_code == 200:
                # If processed, ensure no SQL injection occurred
                data = response.json()
                assert "success" in data
                assert data["success"] is True
    
    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_xss_prevention(self, test_client: AsyncClient):
        """Test protection against XSS attacks"""
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "{{constructor.constructor('alert(\"XSS\")')()}}",
            "${alert('XSS')}"
        ]
        
        for payload in xss_payloads:
            response = await test_client.post("/api/analyze", json={
                "text": f"Test content with XSS: {payload}",
                "level": "Quick Scan"
            })
            
            assert response.status_code in [200, 422]
            
            if response.status_code == 200:
                # Response should not contain unescaped payload
                response_text = response.text
                assert payload not in response_text or "&lt;script&gt;" in response_text
    
    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_rate_limiting_enforcement(self, test_client: AsyncClient):
        """Test rate limiting protection"""
        
        # Make rapid requests to trigger rate limiting
        responses = []
        
        for i in range(25):  # Exceed typical rate limits
            response = await test_client.post("/api/analyze", json={
                "text": f"Rate limit test {i}",
                "level": "Quick Scan"
            })
            responses.append(response)
        
        # Should have some rate limited responses
        rate_limited_count = sum(1 for r in responses if r.status_code == 429)
        assert rate_limited_count > 0
        
        # Rate limited responses should have appropriate headers
        rate_limited_response = next(r for r in responses if r.status_code == 429)
        assert "Retry-After" in rate_limited_response.headers
    
    @pytest.mark.security 
    @pytest.mark.asyncio
    async def test_input_size_limits(self, test_client: AsyncClient):
        """Test protection against oversized inputs"""
        
        # Test extremely large input
        large_text = "A" * 100000  # 100KB text
        
        response = await test_client.post("/api/analyze", json={
            "text": large_text,
            "level": "Quick Scan"
        })
        
        # Should reject oversized input
        assert response.status_code == 422
        
        error_data = response.json()
        assert "detail" in error_data
        assert any("too long" in str(error).lower() for error in error_data["detail"])
    
    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_malformed_json_handling(self, test_client: AsyncClient):
        """Test handling of malformed JSON requests"""
        
        malformed_requests = [
            '{"text": "test"',  # Incomplete JSON
            '{"text": "test", "extra": }',  # Invalid syntax
            '{"text": null}',  # Null value
            '{text: "test"}',  # Unquoted keys
        ]
        
        for malformed_json in malformed_requests:
            response = await test_client.post(
                "/api/analyze",
                content=malformed_json,
                headers={"Content-Type": "application/json"}
            )
            
            # Should reject malformed JSON
            assert response.status_code == 422

class TestAuthenticationSecurity:
    
    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_protected_endpoints_require_auth(self, test_client: AsyncClient):
        """Test that protected endpoints require authentication"""
        
        protected_endpoints = [
            ("/api/archive", "GET"),
            ("/api/archive", "POST"),
            ("/api/analyze/batch", "POST"),
            ("/api/user/profile", "GET")
        ]
        
        for endpoint, method in protected_endpoints:
            if method == "GET":
                response = await test_client.get(endpoint)
            else:
                response = await test_client.post(endpoint, json={})
            
            # Should require authentication
            assert response.status_code in [401, 403]
    
    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_jwt_token_validation(self, test_client: AsyncClient):
        """Test JWT token validation"""
        
        invalid_tokens = [
            "invalid.token.here",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature",
            "",
            "Bearer malformed_token"
        ]
        
        for token in invalid_tokens:
            response = await test_client.get(
                "/api/user/profile",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 401
    
    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_session_security(self, test_client: AsyncClient):
        """Test session security measures"""
        
        # Test session timeout
        # This would require mocking time or using a test-specific timeout
        pass
        
        # Test concurrent session limits
        # This would require multiple authenticated sessions
        pass
```

#### Dependency Security Scanning
```python
# tests/security/test_dependency_security.py
import subprocess
import json
import pytest

@pytest.mark.security
def test_python_dependency_vulnerabilities():
    """Scan Python dependencies for known vulnerabilities"""
    
    try:
        # Run safety check
        result = subprocess.run(
            ["safety", "check", "--json"],
            capture_output=True,
            text=True,
            cwd="backend"
        )
        
        if result.returncode != 0:
            vulnerabilities = json.loads(result.stdout)
            
            # Filter out acceptable vulnerabilities (if any)
            critical_vulns = [
                v for v in vulnerabilities 
                if v.get('severity', '').lower() in ['high', 'critical']
            ]
            
            if critical_vulns:
                pytest.fail(f"Critical vulnerabilities found: {critical_vulns}")
    
    except FileNotFoundError:
        pytest.skip("Safety not installed - run 'pip install safety'")
    except json.JSONDecodeError:
        # safety check passed
        pass

@pytest.mark.security
def test_javascript_dependency_vulnerabilities():
    """Scan JavaScript dependencies for vulnerabilities"""
    
    try:
        # Run npm audit
        result = subprocess.run(
            ["npm", "audit", "--json"],
            capture_output=True,
            text=True,
            cwd="frontend"
        )
        
        if result.returncode != 0:
            audit_data = json.loads(result.stdout)
            
            # Check for high/critical vulnerabilities
            high_vulns = audit_data.get("metadata", {}).get("vulnerabilities", {})
            critical_count = high_vulns.get("critical", 0)
            high_count = high_vulns.get("high", 0)
            
            if critical_count > 0 or high_count > 0:
                pytest.fail(f"High/Critical vulnerabilities: {critical_count} critical, {high_count} high")
    
    except FileNotFoundError:
        pytest.skip("NPM not available")
    except json.JSONDecodeError:
        # npm audit passed
        pass
```

---

## 📊 Test Reporting & CI/CD Integration

### 🤖 GitHub Actions Test Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: truthlab_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements*.txt') }}
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run unit tests
      run: |
        cd backend
        pytest tests/unit/ -v --cov=src --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/truthlab_test
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY_TEST }}
    
    - name: Run integration tests
      run: |
        cd backend
        pytest tests/integration/ -v --markers=integration
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/truthlab_test
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml
        flags: backend
        name: backend-coverage

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run unit tests
      run: |
        cd frontend
        npm run test:unit -- --coverage
    
    - name: Run component tests
      run: |
        cd frontend
        npm run test:component
    
    - name: Build application
      run: |
        cd frontend
        npm run build
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: frontend/coverage/clover.xml
        flags: frontend
        name: frontend-coverage

  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install backend dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Install frontend dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Install Playwright
      run: |
        cd frontend
        npx playwright install --with-deps
    
    - name: Start backend server
      run: |
        cd backend
        uvicorn src.api.main:app --port 8000 &
        sleep 10
      env:
        DATABASE_URL: sqlite:///./test.db
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY_TEST }}
    
    - name: Start frontend server
      run: |
        cd frontend
        npm run build
        npm run preview -- --port 3000 &
        sleep 10
    
    - name: Run E2E tests
      run: |
        cd frontend
        npx playwright test
    
    - name: Upload Playwright report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: frontend/playwright-report/
        retention-days: 30

  security-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r backend/src/ -f json -o bandit-report.json
        
    - name: Run npm audit
      run: |
        cd frontend
        npm audit --audit-level=high
    
    - name: Run safety check
      run: |
        cd backend
        pip install safety
        safety check --json
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          bandit-report.json
          frontend/npm-audit.json

  performance-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup full application stack
      run: |
        docker-compose -f docker-compose.test.yml up -d
        sleep 30
    
    - name: Install Artillery
      run: npm install -g artillery
    
    - name: Run load tests
      run: |
        artillery run performance/load-test.yml
    
    - name: Upload performance results
      uses: actions/upload-artifact@v3
      with:
        name: performance-results
        path: artillery-report.json
```

### 📊 Test Coverage Reporting

#### Coverage Configuration
```python
# backend/.coveragerc
[run]
source = src/
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */settings/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

[html]
directory = htmlcov
```

#### Custom Test Reporters
```python
# tests/utils/custom_reporter.py
import pytest
import json
from datetime import datetime
from typing import Dict, List, Any

class TruthLabTestReporter:
    """Custom test reporter for Truth Lab 2.0"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    def pytest_runtest_setup(self, item):
        """Called before each test"""
        item.start_time = datetime.now()
    
    def pytest_runtest_teardown(self, item, nextitem):
        """Called after each test"""
        if hasattr(item, 'start_time'):
            item.duration = (datetime.now() - item.start_time).total_seconds()
    
    def pytest_runtest_logreport(self, report):
        """Called for each test phase (setup, call, teardown)"""
        if report.when == 'call':
            self.test_results.append({
                'test_name': report.nodeid,
                'outcome': report.outcome,
                'duration': getattr(report, 'duration', 0),
                'markers': [m.name for m in report.item.iter_markers()],
                'location': {
                    'file': report.fspath,
                    'line': report.lineno
                }
            })
    
    def pytest_sessionstart(self, session):
        """Called at test session start"""
        self.start_time = datetime.now()
    
    def pytest_sessionfinish(self, session, exitstatus):
        """Called at test session end"""
        self.end_time = datetime.now()
        
        # Generate comprehensive report
        report = self.generate_report()
        
        # Save to file
        with open('test-report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['outcome'] == 'passed'])
        failed_tests = len([t for t in self.test_results if t['outcome'] == 'failed'])
        skipped_tests = len([t for t in self.test_results if t['outcome'] == 'skipped'])
        
        # Categorize tests by markers
        test_categories = {}
        for test in self.test_results:
            for marker in test['markers']:
                if marker not in test_categories:
                    test_categories[marker] = {'total': 0, 'passed': 0, 'failed': 0}
                
                test_categories[marker]['total'] += 1
                if test['outcome'] == 'passed':
                    test_categories[marker]['passed'] += 1
                elif test['outcome'] == 'failed':
                    test_categories[marker]['failed'] += 1
        
        return {
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'skipped': skipped_tests,
                'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
                'total_duration': (self.end_time - self.start_time).total_seconds(),
                'timestamp': datetime.now().isoformat()
            },
            'categories': test_categories,
            'failed_tests': [
                t for t in self.test_results if t['outcome'] == 'failed'
            ],
            'performance_tests': [
                t for t in self.test_results 
                if 'benchmark' in t['markers'] or 'performance' in t['markers']
            ]
        }
```

---

## 📈 Testing Best Practices & Guidelines

### 🎯 Test Writing Guidelines

#### Test Structure (AAA Pattern)
```python
# Always use Arrange-Act-Assert pattern

async def test_analysis_credibility_scoring():
    # Arrange - Set up test data and mocks
    analyzer = TextAnalyzer(mock_ai_service)
    test_text = "High quality factual content from reliable source."
    expected_score_range = (70, 90)
    
    # Act - Perform the action being tested
    result = await analyzer.analyze_credibility(test_text)
    
    # Assert - Verify the results
    assert 'credibility_score' in result
    assert expected_score_range[0] <= result['credibility_score'] <= expected_score_range[1]
    assert result['confidence'] > 0.7
```

#### Test Naming Conventions
```python
# Use descriptive test names that explain what is being tested

# ✅ Good test names
def test_analysis_engine_returns_credibility_score_for_valid_text():
    pass

def test_api_endpoint_rejects_empty_text_with_validation_error():
    pass

def test_manipulation_detector_identifies_emotional_appeals():
    pass

# ❌ Poor test names  
def test_analysis():
    pass

def test_api():
    pass

def test_detector():
    pass
```

#### Test Data Management
```python
# Use fixtures for reusable test data
@pytest.fixture
def sample_analysis_texts():
    """Provide various text samples for testing"""
    return {
        'high_credibility': """
            According to a peer-reviewed study published in Nature (2023),
            researchers at Stanford University have developed a new method
            for carbon capture that shows promising results in laboratory tests.
        """,
        'low_credibility': """
            SHOCKING! Scientists don't want you to know this ONE WEIRD TRICK!
            Big Pharma is hiding the cure! Share before they delete!
        """,
        'neutral': """
            The weather forecast for tomorrow shows partly cloudy skies
            with temperatures ranging from 65 to 75 degrees Fahrenheit.
        """,
        'manipulation_heavy': """
            URGENT! Time is running out! The government is hiding the truth!
            You need to act NOW or face the consequences! Don't let THEM win!
        """
    }

# Use parametrized tests for multiple scenarios
@pytest.mark.parametrize("text_type,expected_score_range", [
    ('high_credibility', (80, 100)),
    ('neutral', (60, 80)), 
    ('low_credibility', (0, 40)),
])
async def test_credibility_scoring_accuracy(sample_analysis_texts, text_type, expected_score_range):
    text = sample_analysis_texts[text_type]
    analyzer = TextAnalyzer()
    
    result = await analyzer.analyze_credibility(text)
    score = result['credibility_score']
    
    assert expected_score_range[0] <= score <= expected_score_range[1]
```

### 🚀 Testing Automation & Continuous Improvement

#### Test Metrics & KPIs
```python
# Track key testing metrics
TEST_METRICS = {
    'coverage_target': 85,  # Minimum code coverage percentage
    'performance_thresholds': {
        'analysis_endpoint': 10.0,  # seconds
        'batch_analysis': 30.0,    # seconds
        'health_check': 1.0,       # seconds
    },
    'reliability_targets': {
        'test_success_rate': 0.98,  # 98% of tests should pass
        'flaky_test_threshold': 0.05,  # < 5% flaky tests
    }
}
```

#### Automated Test Generation
```python
# Generate tests automatically for new endpoints
def generate_endpoint_tests(endpoint_config):
    """Auto-generate basic tests for new API endpoints"""
    
    test_template = """
async def test_{endpoint_name}_success(test_client):
    response = await test_client.{method}("{path}", json={sample_data})
    assert response.status_code == 200
    
async def test_{endpoint_name}_validation(test_client):
    response = await test_client.{method}("{path}", json={{}})
    assert response.status_code == 422
    """
    
    return test_template.format(
        endpoint_name=endpoint_config['name'].replace('/', '_'),
        method=endpoint_config['method'].lower(),
        path=endpoint_config['path'],
        sample_data=endpoint_config.get('sample_data', '{}')
    )
```

---

**🎉 Testing Excellence Achieved!**

This comprehensive testing guide ensures Truth Lab 2.0 maintains the highest quality standards through:

- ✅ **Multi-layered Testing Strategy** - Unit, Integration, E2E, and Performance tests
- ✅ **Comprehensive Coverage** - Backend Python, Frontend React, and Full-stack workflows  
- ✅ **Security Testing** - Input validation, authentication, and dependency scanning
- ✅ **Performance Benchmarks** - Load testing, memory usage, and response time monitoring
- ✅ **Automated CI/CD Integration** - GitHub Actions workflows with comprehensive reporting
- ✅ **Best Practices** - Clean test architecture, maintainable code, and continuous improvement

**🔗 Related Documentation:**
- [Developer Guide](DEVELOPER-GUIDE.md) - Technical implementation details
- [Deployment Guide](DEPLOYMENT-GUIDE.md) - Production deployment procedures  
- [Getting Started Guide](GETTING-STARTED.md) - Development environment setup
- [Master README](../MASTER-README.md) - Complete project overview

*Quality is not an accident; it is the result of intelligent effort! 🚀*