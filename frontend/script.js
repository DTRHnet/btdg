// BTDigg Clone JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('q');
    const languageSelect = document.getElementById('languageSelect');

    // Form validation
    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        if (!query) {
            e.preventDefault();
            searchInput.focus();
            return false;
        }
    });

    // Language selection
    languageSelect.addEventListener('change', function() {
        const selectedLang = this.value;
        // Store language preference in localStorage
        localStorage.setItem('preferredLanguage', selectedLang);
        
        // In a real implementation, this would redirect to a localized version
        // For now, we'll just show a message
        console.log('Language changed to:', selectedLang);
    });

    // Load saved language preference
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang) {
        languageSelect.value = savedLang;
    }

    // Search input enhancements
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && this.value.trim()) {
            searchForm.submit();
        }
    });

    // Auto-focus search input
    searchInput.focus();

    // Add loading state for form submission
    searchForm.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i>';
        submitBtn.disabled = true;
        
        // Reset button after a delay (in case of errors)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 5000);
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
        
        // Escape to clear search
        if (e.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.value = '';
            searchInput.blur();
        }
    });

    // Search suggestions (placeholder for future implementation)
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length > 2) {
            searchTimeout = setTimeout(() => {
                // In a real implementation, this would fetch search suggestions
                console.log('Search suggestion for:', query);
            }, 300);
        }
    });
});

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Search results rendering (for dynamic content)
function renderSearchResults(results, container) {
    container.innerHTML = '';
    
    if (results.length === 0) {
        container.innerHTML = '<div class="no-results">No results found</div>';
        return;
    }
    
    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.className = 'result-item';
        resultElement.innerHTML = `
            <div class="result-title">${result.title}</div>
            <div class="result-info">
                Size: ${formatFileSize(result.size)} | 
                Files: ${result.files} | 
                Added: ${formatDate(result.added)}
            </div>
            <a href="${result.magnet}" class="result-magnet">
                <i class="fa fa-magnet"></i> Magnet Link
            </a>
        `;
        container.appendChild(resultElement);
    });
}

// Export functions for use in other modules
window.BTDiggUtils = {
    formatFileSize,
    formatDate,
    renderSearchResults
};
