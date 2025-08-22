#!/usr/bin/env python3
"""
Seed data script for BTDigg Clone
Populates the database with sample torrent data
"""

import sqlite3
import time
import random
from datetime import datetime, timedelta

# Sample torrent data
SAMPLE_TORRENTS = [
    {
        'info_hash': 'a1b2c3d4e5f6789012345678901234567890abcd',
        'title': 'Ubuntu 22.04.3 LTS Desktop (x64)',
        'size': 4567890123,
        'files': 1,
        'seeds': 1250,
        'peers': 89,
        'description': 'Official Ubuntu 22.04.3 LTS Desktop ISO for x64 architecture'
    },
    {
        'info_hash': 'b2c3d4e5f6789012345678901234567890abcde1',
        'title': 'Linux Mint 21.3 Cinnamon Edition',
        'size': 2345678901,
        'files': 1,
        'seeds': 890,
        'peers': 45,
        'description': 'Linux Mint 21.3 Cinnamon Edition ISO file'
    },
    {
        'info_hash': 'c3d4e5f6789012345678901234567890abcde12',
        'title': 'Debian 12.4.0 Netinst',
        'size': 345678901,
        'files': 1,
        'seeds': 567,
        'peers': 23,
        'description': 'Debian 12.4.0 Netinst ISO for network installation'
    },
    {
        'info_hash': 'd4e5f6789012345678901234567890abcde123',
        'title': 'Fedora Workstation 39 Live',
        'size': 2345678901,
        'files': 1,
        'seeds': 432,
        'peers': 67,
        'description': 'Fedora Workstation 39 Live ISO with GNOME desktop'
    },
    {
        'info_hash': 'e5f6789012345678901234567890abcde1234',
        'title': 'Arch Linux 2024.01.01',
        'size': 1234567890,
        'files': 1,
        'seeds': 789,
        'peers': 34,
        'description': 'Arch Linux 2024.01.01 ISO with latest packages'
    },
    {
        'info_hash': 'f6789012345678901234567890abcde12345',
        'title': 'OpenSUSE Tumbleweed Live',
        'size': 3456789012,
        'files': 1,
        'seeds': 234,
        'peers': 12,
        'description': 'OpenSUSE Tumbleweed Live ISO with KDE Plasma'
    },
    {
        'info_hash': '6789012345678901234567890abcde123456',
        'title': 'Manjaro Linux 23.1.2 KDE',
        'size': 4567890123,
        'files': 1,
        'seeds': 654,
        'peers': 78,
        'description': 'Manjaro Linux 23.1.2 with KDE Plasma desktop'
    },
    {
        'info_hash': '789012345678901234567890abcde1234567',
        'title': 'Elementary OS 7.1 Horus',
        'size': 2345678901,
        'files': 1,
        'seeds': 321,
        'peers': 56,
        'description': 'Elementary OS 7.1 Horus with Pantheon desktop'
    },
    {
        'info_hash': '89012345678901234567890abcde12345678',
        'title': 'Pop!_OS 22.04 LTS',
        'size': 3456789012,
        'files': 1,
        'seeds': 543,
        'peers': 43,
        'description': 'Pop!_OS 22.04 LTS with GNOME desktop and gaming optimizations'
    },
    {
        'info_hash': '9012345678901234567890abcde123456789',
        'title': 'Zorin OS 17 Pro',
        'size': 5678901234,
        'files': 1,
        'seeds': 876,
        'peers': 98,
        'description': 'Zorin OS 17 Pro with Windows-like interface'
    },
    {
        'info_hash': '012345678901234567890abcde1234567890',
        'title': 'Kali Linux 2024.1 Live',
        'size': 4567890123,
        'files': 1,
        'seeds': 765,
        'peers': 87,
        'description': 'Kali Linux 2024.1 Live ISO for penetration testing'
    },
    {
        'info_hash': '12345678901234567890abcde12345678901',
        'title': 'Parrot OS 5.3 Security',
        'size': 3456789012,
        'files': 1,
        'seeds': 432,
        'peers': 65,
        'description': 'Parrot OS 5.3 Security Edition for ethical hacking'
    },
    {
        'info_hash': '2345678901234567890abcde123456789012',
        'title': 'Tails 5.18 Live',
        'size': 1234567890,
        'files': 1,
        'seeds': 234,
        'peers': 32,
        'description': 'Tails 5.18 Live ISO for privacy and anonymity'
    },
    {
        'info_hash': '345678901234567890abcde1234567890123',
        'title': 'Whonix 17.0.4.0 Gateway',
        'size': 2345678901,
        'files': 1,
        'seeds': 123,
        'peers': 21,
        'description': 'Whonix 17.0.4.0 Gateway for anonymous browsing'
    },
    {
        'info_hash': '45678901234567890abcde12345678901234',
        'title': 'Qubes OS 4.1.2',
        'size': 6789012345,
        'files': 1,
        'seeds': 345,
        'peers': 54,
        'description': 'Qubes OS 4.1.2 with security by isolation'
    },
    {
        'info_hash': '5678901234567890abcde123456789012345',
        'title': 'Alpine Linux 3.19.0',
        'size': 123456789,
        'files': 1,
        'seeds': 567,
        'peers': 76,
        'description': 'Alpine Linux 3.19.0 minimal distribution'
    },
    {
        'info_hash': '678901234567890abcde1234567890123456',
        'title': 'Slackware 15.0',
        'size': 4567890123,
        'files': 1,
        'seeds': 234,
        'peers': 43,
        'description': 'Slackware 15.0 traditional Linux distribution'
    },
    {
        'info_hash': '78901234567890abcde12345678901234567',
        'title': 'Gentoo Linux 2024.01.01',
        'size': 2345678901,
        'files': 1,
        'seeds': 123,
        'peers': 32,
        'description': 'Gentoo Linux 2024.01.01 source-based distribution'
    },
    {
        'info_hash': '8901234567890abcde123456789012345678',
        'title': 'Void Linux 20240101',
        'size': 3456789012,
        'files': 1,
        'seeds': 345,
        'peers': 54,
        'description': 'Void Linux 20240101 rolling release distribution'
    },
    {
        'info_hash': '901234567890abcde1234567890123456789',
        'title': 'NixOS 23.11',
        'size': 2345678901,
        'files': 1,
        'seeds': 234,
        'peers': 43,
        'description': 'NixOS 23.11 declarative Linux distribution'
    }
]

def seed_database(db_path='../db/torrents.db'):
    """Seed the database with sample torrent data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get current timestamp
    current_time = int(time.time())
    
    print("Seeding database with sample torrent data...")
    
    for i, torrent in enumerate(SAMPLE_TORRENTS):
        # Add some time variation to the added timestamp
        added_time = current_time - random.randint(0, 30 * 24 * 3600)  # Random time within last 30 days
        
        cursor.execute("""
            INSERT OR IGNORE INTO torrents 
            (info_hash, title, size, files, added, seeds, peers, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            torrent['info_hash'],
            torrent['title'],
            torrent['size'],
            torrent['files'],
            added_time,
            torrent['seeds'],
            torrent['peers'],
            torrent['description']
        ))
        
        if cursor.rowcount > 0:
            print(f"Added: {torrent['title']}")
    
    # Update statistics
    cursor.execute("""
        UPDATE statistics SET 
        total_torrents = (SELECT COUNT(*) FROM torrents),
        total_size = (SELECT SUM(size) FROM torrents),
        total_files = (SELECT SUM(files) FROM torrents),
        active_seeds = (SELECT SUM(seeds) FROM torrents),
        active_peers = (SELECT SUM(peers) FROM torrents),
        last_updated = CURRENT_TIMESTAMP
        WHERE id = 1
    """)
    
    conn.commit()
    conn.close()
    
    print(f"Database seeded with {len(SAMPLE_TORRENTS)} sample torrents")

if __name__ == '__main__':
    seed_database()
