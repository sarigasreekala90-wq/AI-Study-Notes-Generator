/**
 * AI Study Notes Generator - Main JavaScript File
 * Handles all interactive features including password toggle, character counter, 
 * notes actions, search, and UI interactions.
 */

// ========== UTILITY FUNCTIONS ==========

/**
 * Show a toast notification message
 * @param {string} message - The message to display
 * @param {string} type - The type of message ('success', 'error', 'info')
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-message toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Trigger animation
    void toast.offsetWidth;
    toast.classList.add('show');
    
    // Remove after 2 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

/**
 * Show loading indicator
 */
function showLoading() {
    const loader = document.getElementById('loadingIndicator');
    if (loader) {
        loader.classList.add('show');
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loader = document.getElementById('loadingIndicator');
    if (loader) {
        loader.classList.remove('show');
    }
}

/**
 * Collect all note text from the output card
 * @returns {string} - All note content as text
 */
function collectNoteText() {
    const outputCard = document.querySelector('.output-card');
    if (!outputCard) return '';
    
    let textToCopy = '';
    const sections = outputCard.querySelectorAll('.note-section');
    
    sections.forEach(section => {
        const heading = section.querySelector('.section-heading');
        const content = section.querySelector('p');
        if (heading && content) {
            textToCopy += heading.textContent + '\n';
            textToCopy += content.textContent + '\n\n';
        }
    });
    
    return textToCopy.trim();
}

// ========== PASSWORD TOGGLE ==========

/**
 * Initialize password visibility toggle buttons
 * Allows users to show/hide password fields
 */
function initPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Find the associated password input
            const fieldId = this.getAttribute('data-password-toggle');
            const input = document.getElementById(fieldId);
            
            if (!input) return;
            
            // Toggle password/text type
            if (input.type === 'password') {
                input.type = 'text';
                this.textContent = 'Hide';
            } else {
                input.type = 'password';
                this.textContent = 'Show';
            }
        });
    });
}

// ========== CHARACTER COUNTER ==========

/**
 * Initialize character counter for topic input
 * Displays current character count and prevents exceeding max length
 */
function initCharacterCounter() {
    const topicInput = document.getElementById('topic');
    const charCount = document.getElementById('charCount');
    
    if (!topicInput || !charCount) return;
    
    // Update counter on input
    topicInput.addEventListener('input', function() {
        charCount.textContent = this.value.length;
    });
    
    // Set initial count
    charCount.textContent = topicInput.value.length;
}

// ========== COPY NOTES ACTION ==========

/**
 * Copy all generated notes to clipboard
 */
function initCopyButton() {
    const copyBtn = document.getElementById('copyBtn');
    if (!copyBtn) return;
    
    copyBtn.addEventListener('click', async function() {
        const text = collectNoteText();
        if (!text) {
            showToast('No notes to copy', 'error');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(text);
            showToast('✓ Notes copied to clipboard!', 'success');
        } catch (err) {
            showToast('Failed to copy notes', 'error');
        }
    });
}

// ========== DOWNLOAD NOTES ACTION ==========

/**
 * Download generated notes as a .txt file
 * Filename is based on the topic name
 */
function initDownloadButton() {
    const downloadBtn = document.getElementById('downloadBtn');
    if (!downloadBtn) return;
    
    downloadBtn.addEventListener('click', function() {
        const text = collectNoteText();
        if (!text) {
            showToast('No notes to download', 'error');
            return;
        }
        
        // Get topic name and create safe filename
        const titleElement = document.querySelector('.output-card .card-title');
        const topic = titleElement ? titleElement.textContent.trim() : 'notes';
        const safeFilename = topic
            .replace(/[^a-z0-9\-\s]/gi, '') // Remove special characters
            .replace(/\s+/g, '_') // Replace spaces with underscores
            .toLowerCase();
        
        // Create and download file
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${safeFilename}.txt`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        showToast('✓ Notes downloaded!', 'success');
    });
}

// ========== DELETE NOTE ACTION ==========

/**
 * Initialize delete button with confirmation dialog
 */
function initDeleteButton() {
    const deleteBtn = document.getElementById('deleteBtn');
    const modal = document.getElementById('deleteConfirmModal');
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    const cancelBtn = document.getElementById('cancelDeleteBtn');
    
    if (!deleteBtn || !modal || !confirmBtn || !cancelBtn) return;
    
    // Show confirmation modal when delete is clicked
    deleteBtn.addEventListener('click', function() {
        modal.style.display = 'flex';
    });
    
    // Cancel delete action
    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            this.style.display = 'none';
        }
    });
    
    // Confirm delete action
    confirmBtn.addEventListener('click', async function() {
        const noteId = deleteBtn.getAttribute('data-note-id');
        if (!noteId) return;
        
        showLoading();
        
        try {
            const response = await fetch('/api/delete_note', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: parseInt(noteId) })
            });
            
            if (response.ok) {
                hideLoading();
                showToast('✓ Note deleted successfully!', 'success');
                // Refresh page after a short delay
                setTimeout(() => location.reload(), 500);
            } else {
                hideLoading();
                const data = await response.json();
                showToast(data.error || 'Failed to delete note', 'error');
            }
        } catch (err) {
            hideLoading();
            showToast('Error deleting note', 'error');
        }
        
        modal.style.display = 'none';
    });
}

// ========== SEARCH FUNCTIONALITY ==========

/**
 * Initialize search for topics
 * Filters recent topics based on search query
 */
function initSearchTopics() {
    const searchInput = document.getElementById('searchInput');
    const topicsList = document.getElementById('topicsList');
    
    if (!searchInput || !topicsList) return;
    
    searchInput.addEventListener('input', async function() {
        const query = this.value.trim().toLowerCase();
        
        if (query.length < 2) {
            // If query is too short, reload original list
            const topicItems = topicsList.querySelectorAll('.topic-item');
            topicItems.forEach(item => item.style.display = '');
            return;
        }
        
        // Filter existing items
        const topicItems = topicsList.querySelectorAll('.topic-item');
        topicItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? '' : 'none';
        });
    });
}

// ========== FORM HANDLING ==========

/**
 * Initialize form submission with validation
 */
function initFormHandling() {
    const generateForm = document.getElementById('generateForm');
    if (!generateForm) return;
    
    generateForm.addEventListener('submit', function(e) {
        const topicInput = document.getElementById('topic');
        if (topicInput && !topicInput.value.trim()) {
            e.preventDefault();
            showToast('Please enter a topic', 'error');
            topicInput.focus();
        }
    });
}

// ========== INITIALIZATION ==========

/**
 * Initialize all functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initPasswordToggle();
    initCharacterCounter();
    initCopyButton();
    initDownloadButton();
    initDeleteButton();
    initSearchTopics();
    initFormHandling();
    
    // Focus first input in forms
    const authForm = document.querySelector('.auth-form');
    if (authForm) {
        const firstInput = authForm.querySelector('input');
        if (firstInput) {
            firstInput.focus();
        }
    }
});
