#!/usr/bin/env python3
"""
BTDigg Clone - BitTorrent DHT Search Engine
Backend Flask Application
"""

import os
import time
import sqlite3
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
           static_folder='../frontend',
           template_folder='../frontend')
CORS(app)

# Configuration
app.config['DATABASE'] = '../db/torrents.db'
app.config['RESULTS_PER_PAGE'] = 20
app.config['MAX_SEARCH_LENGTH'] = 100

def get_db():
    """Get database connection"""
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with tables"""
    with app.app_context():
        db = get_db()
        with app.open_resource('../db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 Bytes"
    size_names = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def format_date(timestamp):
    """Format timestamp to readable date"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def generate_magnet_link(info_hash, title):
    """Generate magnet link from info hash and title"""
    return f"magnet:?xt=urn:btih:{info_hash}&dn={title}"

def search_torrents(query, page=1, limit=None):
    """Search torrents in database"""
    if limit is None:
        limit = app.config['RESULTS_PER_PAGE']
    
    offset = (page - 1) * limit
    
    db = get_db()
    
    # Simple full-text search using SQLite FTS
    search_query = """
        SELECT 
            info_hash,
            title,
            size,
            files,
            added,
            seeds,
            peers,
            description
        FROM torrents 
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY added DESC
        LIMIT ? OFFSET ?
    """
    
    search_term = f"%{query}%"
    cursor = db.execute(search_query, (search_term, search_term, limit, offset))
    results = cursor.fetchall()
    
    # Get total count
    count_query = """
        SELECT COUNT(*) as count 
        FROM torrents 
        WHERE title LIKE ? OR description LIKE ?
    """
    cursor = db.execute(count_query, (search_term, search_term))
    total_count = cursor.fetchone()['count']
    
    # Format results
    formatted_results = []
    for row in results:
        formatted_results.append({
            'hash': row['info_hash'],
            'title': row['title'],
            'size': row['size'],
            'size_formatted': format_file_size(row['size']),
            'files': row['files'],
            'added': row['added'],
            'added_formatted': format_date(row['added']),
            'seeds': row['seeds'],
            'peers': row['peers'],
            'description': row['description'],
            'magnet': generate_magnet_link(row['info_hash'], row['title'])
        })
    
    return formatted_results, total_count

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/search')
def search():
    """Search endpoint"""
    query = request.args.get('q', '').strip()
    page = int(request.args.get('p', 1))
    
    if not query:
        return render_template('index.html')
    
    if len(query) > app.config['MAX_SEARCH_LENGTH']:
        return render_template('index.html', error="Search query too long")
    
    start_time = time.time()
    
    try:
        results, total_count = search_torrents(query, page)
        search_time = round(time.time() - start_time, 3)
        
        # Calculate pagination
        results_per_page = app.config['RESULTS_PER_PAGE']
        total_pages = (total_count + results_per_page - 1) // results_per_page
        
        # Generate page range for pagination
        page_range = []
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)
        
        for p in range(start_page, end_page + 1):
            page_range.append(p)
        
        pagination = {
            'current_page': page,
            'total_pages': total_pages,
            'page_range': page_range,
            'has_prev': page > 1,
            'has_next': page < total_pages
        }
        
        return render_template('search.html',
                             query=query,
                             results=results,
                             total_results=total_count,
                             search_time=search_time,
                             pagination=pagination)
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return render_template('search.html',
                             query=query,
                             results=[],
                             total_results=0,
                             search_time=0,
                             error="Search failed")

@app.route('/api/search')
def api_search():
    """API search endpoint"""
    query = request.args.get('q', '').strip()
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', app.config['RESULTS_PER_PAGE']))
    
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        results, total_count = search_torrents(query, page, limit)
        return jsonify({
            'query': query,
            'results': results,
            'total_results': total_count,
            'page': page,
            'limit': limit
        })
    except Exception as e:
        logger.error(f"API search error: {e}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/recent.html')
def recent():
    """Recent findings page"""
    try:
        db = get_db()
        cursor = db.execute("""
            SELECT 
                info_hash,
                title,
                size,
                files,
                added,
                seeds,
                peers
            FROM torrents 
            ORDER BY added DESC 
            LIMIT 50
        """)
        results = cursor.fetchall()
        
        formatted_results = []
        for row in results:
            formatted_results.append({
                'hash': row['info_hash'],
                'title': row['title'],
                'size': row['size'],
                'size_formatted': format_file_size(row['size']),
                'files': row['files'],
                'added': row['added'],
                'added_formatted': format_date(row['added']),
                'seeds': row['seeds'],
                'peers': row['peers'],
                'magnet': generate_magnet_link(row['info_hash'], row['title'])
            })
        
        return render_template('recent.html', results=formatted_results)
    
    except Exception as e:
        logger.error(f"Recent page error: {e}")
        return render_template('recent.html', results=[])

@app.route('/about/')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/rss.xml')
def rss():
    """RSS feed"""
    try:
        db = get_db()
        cursor = db.execute("""
            SELECT 
                info_hash,
                title,
                size,
                added,
                description
            FROM torrents 
            ORDER BY added DESC 
            LIMIT 100
        """)
        results = cursor.fetchall()
        
        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>BTDigg DHT Search Engine</title>
        <link>https://btdig.com</link>
        <description>BitTorrent DHT search engine which analyses the DHT network in real-time</description>
        <language>en</language>
        <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}</lastBuildDate>
"""
        
        for row in results:
            magnet_link = generate_magnet_link(row['info_hash'], row['title'])
            rss_content += f"""
        <item>
            <title>{row['title']}</title>
            <link>{magnet_link}</link>
            <description>Size: {format_file_size(row['size'])} | Added: {format_date(row['added'])}</description>
            <pubDate>{datetime.fromtimestamp(row['added']).strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>
            <guid>{row['info_hash']}</guid>
        </item>"""
        
        rss_content += """
    </channel>
</rss>"""
        
        return rss_content, 200, {'Content-Type': 'application/rss+xml'}
    
    except Exception as e:
        logger.error(f"RSS error: {e}")
        return "RSS feed unavailable", 500

@app.route('/opensearchdescription.xml')
def opensearch():
    """OpenSearch description"""
    opensearch_xml = """<?xml version="1.0" encoding="UTF-8"?>
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
</OpenSearchDescription>"""
    
    return opensearch_xml, 200, {'Content-Type': 'application/opensearchdescription+xml'}

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        db = get_db()
        cursor = db.execute("SELECT COUNT(*) as count FROM torrents")
        count = cursor.fetchone()['count']
        return jsonify({
            'status': 'healthy',
            'torrent_count': count,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(app.config['DATABASE']):
        init_db()
        logger.info("Database initialized")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
