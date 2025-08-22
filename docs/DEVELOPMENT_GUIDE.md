# BTDigg Clone - Development Guide

## Table of Contents
1. [Overview](#overview)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Code Standards](#code-standards)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Contributing](#contributing)
9. [Release Process](#release-process)
10. [Troubleshooting](#troubleshooting)

## Overview

This guide covers the development setup, workflow, and contribution process for the BTDigg Clone project. It's designed for developers who want to contribute to or extend the application.

### Development Goals
- **Maintainability**: Clean, well-documented code
- **Extensibility**: Easy to add new features
- **Performance**: Fast and efficient operation
- **Security**: Secure by design
- **Testing**: Comprehensive test coverage

## Development Setup

### Prerequisites

#### Required Software
- **Python 3.11+**: Core development language
- **Git**: Version control
- **Docker**: Containerized development
- **SQLite**: Database (included with Python)
- **Node.js**: For frontend development (optional)

#### Recommended Tools
- **VS Code**: Code editor with Python extensions
- **PyCharm**: Python IDE
- **Postman**: API testing
- **SQLite Browser**: Database management

### Environment Setup

#### 1. Clone Repository
```bash
# Clone the repository
git clone <repository-url>
cd btdg

# Create development branch
git checkout -b feature/your-feature-name
```

#### 2. Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Install development dependencies
pip install -r backend/requirements-dev.txt
```

#### 3. Development Dependencies
Create `backend/requirements-dev.txt`:
```
# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0

# Code Quality
flake8==6.1.0
black==23.11.0
isort==5.12.0
mypy==1.7.1

# Development Tools
pre-commit==3.5.0
```

#### 4. Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### IDE Configuration

#### VS Code Settings
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv": true
    }
}
```

#### VS Code Extensions
- Python (Microsoft)
- Python Docstring Generator
- Python Test Explorer
- SQLite Viewer
- Docker

## Project Structure

### Directory Layout
```
btdg/
├── frontend/                 # Frontend application
│   ├── index.html           # Homepage
│   ├── search.html          # Search results
│   ├── recent.html          # Recent findings
│   ├── about.html           # About page
│   ├── styles.css           # CSS styles
│   ├── script.js            # JavaScript
│   └── logo.png             # Logo image
├── backend/                  # Backend application
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   ├── requirements-dev.txt # Development dependencies
│   ├── config.py            # Configuration
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   ├── utils/               # Utility functions
│   └── tests/               # Test files
├── db/                      # Database
│   ├── schema.sql           # Database schema
│   ├── seed_data.py         # Sample data
│   └── migrations/          # Database migrations
├── docs/                    # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── DEVELOPMENT_GUIDE.md
│   └── USAGE_GUIDE.md
├── infra/                   # Infrastructure
├── scripts/                 # Utility scripts
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose
├── .gitignore              # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks
├── README.md               # Main documentation
└── PROJECT_SUMMARY.md      # Project overview
```

### Code Organization

#### Backend Structure
```
backend/
├── app.py                  # Main application entry point
├── config.py               # Configuration management
├── models/
│   ├── __init__.py
│   ├── torrent.py          # Torrent model
│   └── search.py           # Search model
├── services/
│   ├── __init__.py
│   ├── search_service.py   # Search business logic
│   └── torrent_service.py  # Torrent business logic
├── utils/
│   ├── __init__.py
│   ├── database.py         # Database utilities
│   ├── formatters.py       # Data formatting
│   └── validators.py       # Input validation
└── tests/
    ├── __init__.py
    ├── test_app.py         # Application tests
    ├── test_search.py      # Search tests
    └── test_models.py      # Model tests
```

## Development Workflow

### 1. Feature Development

#### Create Feature Branch
```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new search feature"

# Push to remote
git push origin feature/new-feature
```

#### Development Process
1. **Plan**: Define feature requirements
2. **Design**: Create technical design
3. **Implement**: Write code with tests
4. **Test**: Run tests and manual testing
5. **Review**: Self-review and peer review
6. **Merge**: Merge to main branch

### 2. Code Review Process

#### Pull Request Template
Create `.github/pull_request_template.md`:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

#### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Error handling implemented

### 3. Git Workflow

#### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

#### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tool changes

#### Examples
```bash
git commit -m "feat(search): add advanced search filters"
git commit -m "fix(api): resolve pagination issue"
git commit -m "docs(readme): update installation instructions"
```

## Code Standards

### Python Standards

#### PEP 8 Compliance
```python
# Good
def search_torrents(query: str, page: int = 1) -> List[Dict]:
    """Search for torrents using the given query.
    
    Args:
        query: Search query string
        page: Page number (default: 1)
        
    Returns:
        List of torrent dictionaries
    """
    # Implementation
    pass

# Bad
def searchTorrents(query,page=1):
    # Implementation
    pass
```

#### Type Hints
```python
from typing import List, Dict, Optional, Union

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    pass

def get_torrent_by_hash(info_hash: str) -> Optional[Dict]:
    """Get torrent by info hash."""
    pass
```

#### Docstrings
```python
def search_torrents(query: str, page: int = 1, limit: int = 20) -> Dict:
    """Search for torrents in the database.
    
    This function performs a full-text search through the torrent database
    using SQLite FTS5. Results are paginated and ordered by date added.
    
    Args:
        query: Search query string (required)
        page: Page number for pagination (default: 1)
        limit: Number of results per page (default: 20, max: 100)
        
    Returns:
        Dictionary containing:
            - results: List of torrent dictionaries
            - total_results: Total number of matching results
            - page: Current page number
            - limit: Results per page
            
    Raises:
        ValueError: If query is empty or too long
        DatabaseError: If database operation fails
        
    Example:
        >>> results = search_torrents("ubuntu 22.04")
        >>> print(f"Found {results['total_results']} results")
    """
    pass
```

### Frontend Standards

#### HTML Standards
```html
<!-- Good -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BTDigg Clone - Search Results</title>
    <meta name="description" content="Search results for torrents">
</head>
<body>
    <main>
        <h1>Search Results</h1>
        <!-- Content -->
    </main>
</body>
</html>

<!-- Bad -->
<html>
<head>
<title>Results</title>
</head>
<body>
<div>Results</div>
</body>
</html>
```

#### CSS Standards
```css
/* Use BEM methodology */
.search-form {
    width: 600px;
    margin: 0 auto;
}

.search-form__input {
    width: 100%;
    padding: 10px;
}

.search-form__button {
    background: #0000cc;
    color: white;
}

.search-form__button--disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
```

#### JavaScript Standards
```javascript
// Use ES6+ features
const searchTorrents = async (query, page = 1) => {
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&p=${page}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Search failed:', error);
        throw error;
    }
};

// Use meaningful variable names
const formatFileSize = (bytes) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
};
```

## Testing

### Test Structure

#### Unit Tests
```python
# backend/tests/test_search.py
import pytest
from unittest.mock import Mock, patch
from backend.services.search_service import SearchService

class TestSearchService:
    def setup_method(self):
        self.search_service = SearchService()
    
    def test_search_with_valid_query(self):
        """Test search with valid query returns results."""
        query = "ubuntu 22.04"
        results = self.search_service.search(query)
        
        assert results is not None
        assert 'results' in results
        assert 'total_results' in results
    
    def test_search_with_empty_query(self):
        """Test search with empty query raises ValueError."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            self.search_service.search("")
    
    @patch('backend.services.search_service.get_db')
    def test_search_database_error(self, mock_get_db):
        """Test search handles database errors gracefully."""
        mock_get_db.side_effect = Exception("Database error")
        
        with pytest.raises(Exception, match="Database error"):
            self.search_service.search("test")
```

#### Integration Tests
```python
# backend/tests/test_integration.py
import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'
    
    with app.test_client() as client:
        with app.app_context():
            # Initialize test database
            init_test_db()
        yield client

def test_search_endpoint(client):
    """Test search endpoint returns correct response."""
    response = client.get('/api/search?q=ubuntu')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data
    assert 'total_results' in data

def test_health_endpoint(client):
    """Test health endpoint returns healthy status."""
    response = client.get('/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
```

### Running Tests

#### Test Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest backend/tests/test_search.py

# Run specific test function
pytest backend/tests/test_search.py::TestSearchService::test_search_with_valid_query

# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v
```

#### Test Configuration
Create `pytest.ini`:
```ini
[tool:pytest]
testpaths = backend/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### Test Coverage

#### Coverage Configuration
Create `.coveragerc`:
```ini
[run]
source = backend
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
```

## Debugging

### Debug Configuration

#### VS Code Debug Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "backend/app.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "justMyCode": true
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

### Debugging Techniques

#### Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def search_torrents(query: str) -> Dict:
    logger.debug(f"Searching for query: {query}")
    
    try:
        results = perform_search(query)
        logger.info(f"Found {len(results)} results for '{query}'")
        return results
    except Exception as e:
        logger.error(f"Search failed for '{query}': {e}")
        raise
```

#### Debugging with pdb
```python
import pdb

def complex_function():
    # Set breakpoint
    pdb.set_trace()
    
    # Or use breakpoint() in Python 3.7+
    breakpoint()
    
    # Continue with function
    result = some_complex_calculation()
    return result
```

### Performance Debugging

#### Profiling
```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Function to profile
    search_torrents("test query")
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

## Contributing

### Contribution Guidelines

#### Before Contributing
1. **Check Issues**: Look for existing issues or discussions
2. **Discuss**: Open an issue to discuss your proposed changes
3. **Fork**: Fork the repository to your account
4. **Branch**: Create a feature branch from main

#### Development Process
1. **Setup**: Follow the development setup guide
2. **Code**: Write clean, tested code
3. **Test**: Ensure all tests pass
4. **Document**: Update documentation as needed
5. **Commit**: Use conventional commit messages
6. **Push**: Push to your fork
7. **PR**: Create a pull request

#### Code Review Process
1. **Self Review**: Review your own code first
2. **Tests**: Ensure tests pass and coverage is adequate
3. **Documentation**: Update relevant documentation
4. **Submit**: Submit pull request with clear description
5. **Address Feedback**: Respond to review comments
6. **Merge**: Merge after approval

### Contribution Areas

#### Frontend Improvements
- UI/UX enhancements
- Responsive design improvements
- Accessibility features
- Performance optimizations

#### Backend Enhancements
- New API endpoints
- Performance improvements
- Security enhancements
- Database optimizations

#### Documentation
- API documentation updates
- Code documentation
- User guides
- Deployment guides

#### Testing
- Unit test coverage
- Integration tests
- Performance tests
- Security tests

## Release Process

### Version Management

#### Semantic Versioning
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

#### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Release notes prepared
- [ ] Docker image built and tested
- [ ] Deployment tested

### Release Steps

#### 1. Prepare Release
```bash
# Update version
git checkout main
git pull origin main

# Create release branch
git checkout -b release/v1.1.0

# Update version in files
# Update CHANGELOG.md
# Update version in app.py
```

#### 2. Test Release
```bash
# Run all tests
pytest

# Build Docker image
docker build -t btdig-clone:v1.1.0 .

# Test deployment
docker-compose up -d
curl http://localhost:5000/health
```

#### 3. Create Release
```bash
# Merge to main
git checkout main
git merge release/v1.1.0

# Create tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# Create GitHub release
# Upload assets
# Publish release notes
```

## Troubleshooting

### Common Development Issues

#### Environment Issues
```bash
# Python version mismatch
python3 --version
# Ensure Python 3.11+

# Virtual environment issues
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Permission issues
sudo chown -R $USER:$USER .
chmod +x scripts/*.sh
```

#### Database Issues
```bash
# Database locked
rm db/torrents.db
python backend/db/seed_data.py

# Migration issues
sqlite3 db/torrents.db ".schema"
python backend/db/seed_data.py
```

#### Docker Issues
```bash
# Clean Docker environment
docker system prune -a
docker volume prune

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Debug Commands
```bash
# Check application status
curl http://localhost:5000/health

# Check logs
docker-compose logs -f
tail -f logs/app.log

# Check database
sqlite3 db/torrents.db "SELECT COUNT(*) FROM torrents;"

# Check dependencies
pip list
pip check
```

---

## Quick Reference

### Development Commands
```bash
# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Run tests
pytest
pytest --cov=backend

# Run application
python backend/app.py
docker-compose up -d

# Code quality
black backend/
flake8 backend/
mypy backend/

# Pre-commit hooks
pre-commit run --all-files
```

### Useful Scripts
```bash
# Development setup script
./scripts/setup-dev.sh

# Test runner script
./scripts/run-tests.sh

# Code quality check script
./scripts/check-quality.sh

# Database reset script
./scripts/reset-db.sh
```

---

*This development guide covers all aspects of contributing to the BTDigg Clone project. For additional support, refer to the main README or create an issue on GitHub.*
