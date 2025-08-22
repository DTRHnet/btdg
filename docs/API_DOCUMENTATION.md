# BTDigg Clone - API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Endpoints](#endpoints)
5. [Response Formats](#response-formats)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Examples](#examples)
9. [SDK Examples](#sdk-examples)

## Overview

The BTDigg Clone API provides programmatic access to torrent search functionality. The API is RESTful and returns JSON responses for machine-readable data.

### Features
- **Search API**: Full-text search through torrent database
- **Health Monitoring**: Application status and statistics
- **RSS Feed**: Syndication feed for latest torrents
- **OpenSearch**: Browser search engine integration

### API Version
- **Current Version**: v1.0
- **Status**: Stable
- **Base URL**: `http://localhost:5000` (development)

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

**Note**: For production deployments, consider implementing API key authentication for rate limiting and usage tracking.

## Base URL

### Development
```
http://localhost:5000
```

### Production
```
https://your-domain.com
```

## Endpoints

### 1. Search API

#### GET /api/search

Search for torrents using full-text search.

**URL Parameters:**
- `q` (required): Search query string
- `p` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 20, max: 100)

**Example Request:**
```bash
curl "http://localhost:5000/api/search?q=ubuntu&p=1&limit=10"
```

**Response Format:**
```json
{
  "query": "ubuntu",
  "results": [
    {
      "hash": "a1b2c3d4e5f6789012345678901234567890abcd",
      "title": "Ubuntu 22.04.3 LTS Desktop (x64)",
      "size": 4567890123,
      "size_formatted": "4.26 GB",
      "files": 1,
      "added": 1704067200,
      "added_formatted": "2024-01-01 12:00:00",
      "seeds": 1250,
      "peers": 89,
      "description": "Official Ubuntu 22.04.3 LTS Desktop ISO for x64 architecture",
      "magnet": "magnet:?xt=urn:btih:a1b2c3d4e5f6789012345678901234567890abcd&dn=Ubuntu+22.04.3+LTS+Desktop+(x64)"
    }
  ],
  "total_results": 15,
  "page": 1,
  "limit": 10
}
```

**Response Fields:**
- `query`: Original search query
- `results`: Array of torrent objects
- `total_results`: Total number of matching results
- `page`: Current page number
- `limit`: Results per page

**Torrent Object Fields:**
- `hash`: Torrent info hash (40 character hex string)
- `title`: Torrent title/name
- `size`: File size in bytes
- `size_formatted`: Human-readable file size
- `files`: Number of files in torrent
- `added`: Unix timestamp when added
- `added_formatted`: Human-readable date
- `seeds`: Number of seeders
- `peers`: Number of peers
- `description`: Torrent description
- `magnet`: Magnet link for download

### 2. Health Check API

#### GET /health

Check application health and get system statistics.

**Example Request:**
```bash
curl "http://localhost:5000/health"
```

**Response Format:**
```json
{
  "status": "healthy",
  "torrent_count": 20,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Response Fields:**
- `status`: Application status ("healthy" or "unhealthy")
- `torrent_count`: Total number of torrents in database
- `timestamp`: Current server timestamp (ISO 8601)

**Error Response:**
```json
{
  "status": "unhealthy",
  "error": "Database connection failed",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 3. RSS Feed

#### GET /rss.xml

Get RSS feed of latest torrents.

**Example Request:**
```bash
curl "http://localhost:5000/rss.xml"
```

**Response Format:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>BTDigg DHT Search Engine</title>
        <link>https://btdig.com</link>
        <description>BitTorrent DHT search engine which analyses the DHT network in real-time</description>
        <language>en</language>
        <lastBuildDate>Mon, 01 Jan 2024 12:00:00 +0000</lastBuildDate>
        <item>
            <title>Ubuntu 22.04.3 LTS Desktop (x64)</title>
            <link>magnet:?xt=urn:btih:a1b2c3d4e5f6789012345678901234567890abcd&dn=Ubuntu+22.04.3+LTS+Desktop+(x64)</link>
            <description>Size: 4.26 GB | Added: 2024-01-01 12:00:00</description>
            <pubDate>Mon, 01 Jan 2024 12:00:00 +0000</pubDate>
            <guid>a1b2c3d4e5f6789012345678901234567890abcd</guid>
        </item>
    </channel>
</rss>
```

### 4. OpenSearch Description

#### GET /opensearchdescription.xml

Get OpenSearch description for browser integration.

**Example Request:**
```bash
curl "http://localhost:5000/opensearchdescription.xml"
```

**Response Format:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
    <ShortName>BTDigg</ShortName>
    <Description>BitTorrent DHT search engine which analyses the DHT network in real-time</Description>
    <Tags>torrent search bittorrent dht</Tags>
    <Contact>admin@btdig.com</Contact>
    <Url type="application/rss+xml" template="https://btdig.com/rss.xml"/>
    <Url type="text/html" template="https://btdig.com/search?q={searchTerms}"/>
    <Url type="application/x-suggestions+json" template="https://btdig.com/suggest?q={searchTerms}"/>
    <LongName>BTDigg DHT Search Engine</LongName>
    <Image height="64" width="64" type="image/png">https://btdig.com/logo.png</Image>
    <Query role="example" searchTerms="linux"/>
    <Developer>BTDigg Team</Developer>
    <Attribution>Search results from BTDigg DHT Search Engine</Attribution>
    <SyndicationRight>open</SyndicationRight>
    <AdultContent>false</AdultContent>
    <Language>en</Language>
    <OutputEncoding>UTF-8</OutputEncoding>
    <InputEncoding>UTF-8</InputEncoding>
</OpenSearchDescription>
```

## Response Formats

### Success Response
All successful API responses follow this format:
```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Error Response
Error responses follow this format:
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Error Handling

### HTTP Status Codes

- **200 OK**: Request successful
- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Codes

| Code | Description |
|------|-------------|
| `INVALID_QUERY` | Search query is invalid or too long |
| `QUERY_REQUIRED` | Search query parameter is missing |
| `INVALID_PAGE` | Page number is invalid |
| `INVALID_LIMIT` | Limit parameter is invalid |
| `DATABASE_ERROR` | Database connection or query error |
| `INTERNAL_ERROR` | Internal server error |

### Error Examples

**Missing Query Parameter:**
```json
{
  "status": "error",
  "error": {
    "code": "QUERY_REQUIRED",
    "message": "Query parameter 'q' is required",
    "details": "Please provide a search query"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Invalid Page Number:**
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_PAGE",
    "message": "Page number must be positive",
    "details": "Page parameter must be >= 1"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Rate Limiting

Currently, the API does not implement rate limiting. However, for production use, consider implementing:

- **Rate Limits**: Requests per minute/hour
- **API Keys**: Authentication for tracking
- **Throttling**: Gradual response slowdown
- **Quotas**: Daily/monthly limits

### Recommended Limits
- **Anonymous**: 100 requests/hour
- **Authenticated**: 1000 requests/hour
- **Burst**: 10 requests/minute

## Examples

### JavaScript (Fetch API)

**Basic Search:**
```javascript
async function searchTorrents(query, page = 1, limit = 20) {
  const url = `http://localhost:5000/api/search?q=${encodeURIComponent(query)}&p=${page}&limit=${limit}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    
    if (response.ok) {
      return data;
    } else {
      throw new Error(data.error.message);
    }
  } catch (error) {
    console.error('Search failed:', error);
    throw error;
  }
}

// Usage
searchTorrents('ubuntu 22.04')
  .then(results => {
    console.log(`Found ${results.total_results} results`);
    results.results.forEach(torrent => {
      console.log(`${torrent.title} (${torrent.size_formatted})`);
    });
  })
  .catch(error => {
    console.error('Error:', error.message);
  });
```

**Health Check:**
```javascript
async function checkHealth() {
  try {
    const response = await fetch('http://localhost:5000/health');
    const data = await response.json();
    
    console.log(`Status: ${data.status}`);
    console.log(`Torrents: ${data.torrent_count}`);
    return data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
}
```

### Python (Requests)

**Basic Search:**
```python
import requests
import json

def search_torrents(query, page=1, limit=20):
    url = "http://localhost:5000/api/search"
    params = {
        'q': query,
        'p': page,
        'limit': limit
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Search failed: {e}")
        raise

# Usage
try:
    results = search_torrents('ubuntu 22.04')
    print(f"Found {results['total_results']} results")
    
    for torrent in results['results']:
        print(f"{torrent['title']} ({torrent['size_formatted']})")
        
except Exception as e:
    print(f"Error: {e}")
```

**Health Check:**
```python
def check_health():
    try:
        response = requests.get('http://localhost:5000/health')
        response.raise_for_status()
        data = response.json()
        
        print(f"Status: {data['status']}")
        print(f"Torrents: {data['torrent_count']}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Health check failed: {e}")
        raise
```

### cURL Examples

**Search for Linux distributions:**
```bash
curl "http://localhost:5000/api/search?q=linux&p=1&limit=5"
```

**Search with specific terms:**
```bash
curl "http://localhost:5000/api/search?q=ubuntu+22.04+lts&p=1&limit=10"
```

**Get health status:**
```bash
curl "http://localhost:5000/health"
```

**Get RSS feed:**
```bash
curl "http://localhost:5000/rss.xml"
```

## SDK Examples

### Node.js SDK

```javascript
class BTDiggAPI {
  constructor(baseURL = 'http://localhost:5000') {
    this.baseURL = baseURL;
  }
  
  async search(query, page = 1, limit = 20) {
    const url = `${this.baseURL}/api/search`;
    const params = new URLSearchParams({
      q: query,
      p: page.toString(),
      limit: limit.toString()
    });
    
    const response = await fetch(`${url}?${params}`);
    return response.json();
  }
  
  async health() {
    const response = await fetch(`${this.baseURL}/health`);
    return response.json();
  }
  
  async rss() {
    const response = await fetch(`${this.baseURL}/rss.xml`);
    return response.text();
  }
}

// Usage
const api = new BTDiggAPI();
api.search('ubuntu').then(console.log);
```

### Python SDK

```python
import requests
from typing import Dict, List, Optional

class BTDiggAPI:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def search(self, query: str, page: int = 1, limit: int = 20) -> Dict:
        """Search for torrents"""
        url = f"{self.base_url}/api/search"
        params = {'q': query, 'p': page, 'limit': limit}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def health(self) -> Dict:
        """Check application health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def rss(self) -> str:
        """Get RSS feed"""
        response = requests.get(f"{self.base_url}/rss.xml")
        response.raise_for_status()
        return response.text

# Usage
api = BTDiggAPI()
results = api.search('ubuntu 22.04')
print(f"Found {results['total_results']} results")
```

## Best Practices

### Request Optimization
1. **Use Specific Queries**: More specific searches return better results
2. **Implement Pagination**: Use page and limit parameters for large result sets
3. **Cache Responses**: Cache frequently requested data
4. **Handle Errors**: Implement proper error handling

### Response Processing
1. **Validate Responses**: Check response status and data structure
2. **Handle Pagination**: Process results page by page
3. **Format Data**: Convert timestamps and file sizes as needed
4. **Error Recovery**: Implement retry logic for failed requests

### Security Considerations
1. **Validate Input**: Sanitize user input before sending requests
2. **Use HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Implement client-side rate limiting
4. **Error Handling**: Don't expose sensitive information in error messages

---

## API Changelog

### v1.0 (Current)
- Initial API release
- Search functionality
- Health monitoring
- RSS feed
- OpenSearch integration

### Future Versions
- Authentication system
- Advanced search filters
- Real-time updates
- WebSocket support
- Analytics endpoints

---

*This API documentation covers all available endpoints and usage patterns. For additional support, refer to the main README or create an issue on GitHub.*
