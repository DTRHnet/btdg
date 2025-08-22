# BTDigg Clone - Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Search Features](#search-features)
4. [Navigation](#navigation)
5. [Advanced Features](#advanced-features)
6. [Troubleshooting](#troubleshooting)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [Mobile Usage](#mobile-usage)

## Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for initial setup
- Docker (for containerized deployment)

### Quick Start
1. **Start the application**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

3. **Verify it's working**:
   You should see the BTDigg homepage with a search form and logo.

## Basic Usage

### Homepage
The homepage (`/`) provides:
- **Search Form**: Main search interface
- **Logo**: BTDigg branding
- **Navigation Links**: Access to different sections
- **Language Selector**: Choose your preferred language

### Search Interface
1. **Enter Search Terms**: Type keywords in the search box
2. **Submit Search**: Click the search button or press Enter
3. **View Results**: Browse through search results
4. **Navigate Pages**: Use pagination controls

### Search Results
Each result displays:
- **Title**: Torrent name (clickable)
- **File Information**: Size, number of files, date added
- **Peer Information**: Seeds and peers count
- **Magnet Link**: Direct download link
- **Hash**: Torrent hash for verification

## Search Features

### Basic Search
- **Keywords**: Search for specific terms
- **Partial Matches**: Find torrents containing your keywords
- **Case Insensitive**: Searches work regardless of case

### Search Tips
- **Use Specific Terms**: "ubuntu 22.04" vs "linux"
- **Include File Types**: "pdf", "iso", "mp4"
- **Add Categories**: "movie", "software", "music"

### Search Examples
```
ubuntu 22.04 lts
linux mint cinnamon
debian netinst
fedora workstation
arch linux iso
```

### Advanced Search (Future Enhancement)
- **File Size Filters**: Specify minimum/maximum size
- **Date Range**: Search by upload date
- **Category Filters**: Filter by content type
- **Seed Count**: Minimum number of seeds

## Navigation

### Main Pages
1. **Home** (`/`): Main search interface
2. **Search Results** (`/search`): Display search results
3. **Recent Findings** (`/recent.html`): Latest torrents
4. **About** (`/about/`): Project information

### Navigation Elements
- **Search Form**: Available on all pages
- **Logo**: Returns to homepage
- **Navigation Links**: Bottom of each page
- **Breadcrumbs**: Page location indicators

### Language Support
Available languages:
- **English** (en): Default language
- **Français** (fr): French
- **Português do Brasil** (pt): Brazilian Portuguese
- **简体中文** (cn): Simplified Chinese
- **Русский** (ru): Russian

## Advanced Features

### RSS Feed
- **URL**: `http://localhost:5000/rss.xml`
- **Content**: Latest 100 torrents
- **Format**: Standard RSS 2.0
- **Usage**: Add to RSS reader

### OpenSearch Integration
- **URL**: `http://localhost:5000/opensearchdescription.xml`
- **Browser Integration**: Add to browser search engines
- **Direct Search**: Search from browser address bar

### API Access
- **Search API**: `GET /api/search?q=<query>`
- **Health Check**: `GET /health`
- **JSON Response**: Machine-readable data

### Magnet Links
- **Direct Download**: Click magnet links to start download
- **Torrent Client**: Opens in your default torrent client
- **Hash Verification**: Use hash for verification

## Troubleshooting

### Common Issues

#### Application Won't Start
**Problem**: Docker container fails to start
**Solution**:
```bash
# Check Docker status
docker ps -a

# View logs
docker-compose logs

# Rebuild container
docker-compose down
docker-compose up --build
```

#### Search Not Working
**Problem**: No search results returned
**Solution**:
1. Check database initialization
2. Verify sample data is loaded
3. Try different search terms
4. Check application logs

#### Page Not Loading
**Problem**: Browser shows error or blank page
**Solution**:
1. Verify application is running
2. Check port 5000 is accessible
3. Clear browser cache
4. Try different browser

#### Database Issues
**Problem**: Database errors or missing data
**Solution**:
```bash
# Reinitialize database
cd backend
python db/seed_data.py

# Check database file
ls -la db/torrents.db
```

### Error Messages

#### "No results found"
- Try different search terms
- Check spelling
- Use broader keywords
- Verify database has data

#### "Search failed"
- Check application logs
- Restart the application
- Verify database connection

#### "Page not found"
- Check URL spelling
- Verify application is running
- Clear browser cache

## Keyboard Shortcuts

### Global Shortcuts
- **Ctrl/Cmd + K**: Focus search box
- **Escape**: Clear search box
- **Enter**: Submit search

### Navigation Shortcuts
- **Alt + Home**: Go to homepage
- **Alt + R**: Go to recent findings
- **Alt + A**: Go to about page

### Search Results
- **Tab**: Navigate between results
- **Space**: Select result
- **Enter**: Open magnet link

## Mobile Usage

### Responsive Design
- **Touch-Friendly**: Large touch targets
- **Mobile-Optimized**: Responsive layout
- **Fast Loading**: Optimized for mobile networks

### Mobile Features
- **Touch Search**: Easy search input
- **Swipe Navigation**: Touch gestures
- **Mobile View**: Optimized display

### Mobile Tips
- **Use Landscape**: Better viewing on tablets
- **Bookmark Pages**: Save frequently used pages
- **Add to Home Screen**: Quick access

## Performance Tips

### Search Optimization
- **Use Specific Terms**: More specific searches are faster
- **Avoid Wildcards**: Use exact terms when possible
- **Limit Results**: Use pagination for large result sets

### Browser Optimization
- **Clear Cache**: Regular cache clearing
- **Disable Extensions**: Test without browser extensions
- **Use Incognito**: Test in private browsing mode

### Network Optimization
- **Stable Connection**: Ensure reliable internet
- **Local Network**: Use local deployment for testing
- **CDN**: Use CDN for production deployment

## Security Considerations

### Safe Usage
- **Verify Sources**: Check torrent authenticity
- **Use Antivirus**: Scan downloaded files
- **Legal Compliance**: Respect copyright laws
- **VPN Usage**: Consider using VPN for privacy

### Privacy Protection
- **No Logging**: Application doesn't log personal data
- **Anonymous Access**: No registration required
- **Secure Connections**: Use HTTPS in production

## Support and Help

### Getting Help
1. **Check Documentation**: Review this guide
2. **Application Logs**: Check Docker logs
3. **GitHub Issues**: Report bugs on GitHub
4. **Community**: Join discussion forums

### Reporting Issues
When reporting issues, include:
- **Browser**: Browser type and version
- **Operating System**: OS and version
- **Error Message**: Exact error text
- **Steps to Reproduce**: Detailed reproduction steps
- **Expected Behavior**: What should happen

### Feature Requests
- **GitHub Issues**: Submit feature requests
- **Detailed Description**: Explain the feature
- **Use Cases**: Provide usage scenarios
- **Priority**: Indicate importance level

---

## Quick Reference

### URLs
- **Homepage**: `http://localhost:5000/`
- **Search**: `http://localhost:5000/search?q=<query>`
- **Recent**: `http://localhost:5000/recent.html`
- **About**: `http://localhost:5000/about/`
- **RSS**: `http://localhost:5000/rss.xml`
- **API**: `http://localhost:5000/api/search?q=<query>`
- **Health**: `http://localhost:5000/health`

### Commands
```bash
# Start application
docker-compose up --build

# Stop application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up --build --force-recreate
```

### Search Examples
- `linux ubuntu 22.04`
- `movie 2024 hd`
- `software windows 11`
- `music album 2024`
- `ebook pdf programming`

---

*This usage guide covers all aspects of using the BTDigg clone application. For technical details, see the API documentation and README files.*
