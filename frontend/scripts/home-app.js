// Home page JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // People selector functionality
    const peopleSelector = document.getElementById('peopleSelector');
    const peopleDisplay = document.getElementById('peopleDisplay');
    const peopleDropdown = document.getElementById('peopleDropdown');
    const doneBtn = document.getElementById('doneBtn');
    const adultsCount = document.getElementById('adultsCount');
    const childrenCount = document.getElementById('childrenCount');
    
    let adults = 2;
    let children = 0;
    
    // Toggle people dropdown
    peopleDisplay.addEventListener('click', function() {
        peopleDropdown.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!peopleSelector.contains(e.target)) {
            peopleDropdown.classList.remove('active');
        }
    });
    
    // Counter buttons functionality
    document.querySelectorAll('.counter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action;
            const target = this.dataset.target;
            
            if (target === 'adults') {
                if (action === 'increase') {
                    adults = Math.min(adults + 1, 10);
                } else if (action === 'decrease') {
                    adults = Math.max(adults - 1, 1);
                }
                adultsCount.textContent = adults;
            } else if (target === 'children') {
                if (action === 'increase') {
                    children = Math.min(children + 1, 8);
                } else if (action === 'decrease') {
                    children = Math.max(children - 1, 0);
                }
                childrenCount.textContent = children;
            }
            
            updatePeopleDisplay();
        });
    });
    
    // Done button functionality
    doneBtn.addEventListener('click', function() {
        peopleDropdown.classList.remove('active');
    });
    
    // Update people display text
    function updatePeopleDisplay() {
        const adultsText = adults === 1 ? '1 Adult' : `${adults} Adults`;
        const childrenText = children === 0 ? '0 Children' : 
                           children === 1 ? '1 Child' : `${children} Children`;
        peopleDisplay.value = `${adultsText} • ${childrenText}`;
    }
    
    // Search form functionality
    const searchForm = document.getElementById('searchForm');
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const searchData = {
            destination: formData.get('destination'),
            startDate: formData.get('startDate'),
            returnDate: formData.get('returnDate'),
            adults: adults,
            children: children
        };
        
        // Validate dates
        const startDate = new Date(searchData.startDate);
        const returnDate = new Date(searchData.returnDate);
        const today = new Date();
        
        if (startDate < today) {
            showMessage('Start date cannot be in the past', 'error');
            return;
        }
        
        if (returnDate <= startDate) {
            showMessage('Return date must be after start date', 'error');
            return;
        }
        
        // Store search data and redirect to planner
        localStorage.setItem('searchData', JSON.stringify(searchData));
        
        // Show loading state
        const searchBtn = document.querySelector('.search-btn');
        const originalText = searchBtn.textContent;
        searchBtn.textContent = 'Planning...';
        searchBtn.disabled = true;
        
        // Simulate planning process and redirect
        setTimeout(() => {
            window.location.href = 'planner.html';
        }, 1500);
    });
    
    // Set default dates (today and 3 days from now)
    const today = new Date();
    const threeDaysLater = new Date(today);
    threeDaysLater.setDate(today.getDate() + 3);
    
    document.getElementById('startDate').value = today.toISOString().split('T')[0];
    document.getElementById('returnDate').value = threeDaysLater.toISOString().split('T')[0];
    
    // Itinerary card interactions
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.itinerary-card');
            const title = card.querySelector('.card-title').textContent;
            
            // Animate button
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Show message (in a real app, this would navigate to the itinerary)
            showMessage(`Opening "${title}" itinerary...`, 'info');
            
            // Simulate navigation delay
            setTimeout(() => {
                // In a real app, navigate to the specific itinerary
                console.log(`Viewing itinerary: ${title}`);
            }, 1000);
        });
    });
    
    // Add hover effects to nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href.startsWith('#')) {
                e.preventDefault();
                showMessage('Page coming soon!', 'info');
            }
        });
    });
    
    // Profile avatar interaction
    document.querySelector('.profile-avatar').addEventListener('click', function() {
        showMessage('Profile menu coming soon!', 'info');
    });
});

// Message toast functionality
function showMessage(message, type = 'info') {
    // Remove existing toast
    const existingToast = document.getElementById('messageToast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create new toast
    const toast = document.createElement('div');
    toast.id = 'messageToast';
    toast.className = `message-toast ${type}`;
    toast.textContent = message;
    
    // Add styles for toast
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 2000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        max-width: 300px;
        font-size: 0.9rem;
    `;
    
    // Set background color based on type
    if (type === 'success') {
        toast.style.background = '#10B981';
    } else if (type === 'error') {
        toast.style.background = '#EF4444';
    } else {
        toast.style.background = '#3B82F6';
    }
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 3000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading animation to search form
function addLoadingState() {
    const searchBtn = document.querySelector('.search-btn');
    if (searchBtn) {
        searchBtn.innerHTML = `
            <span style="display: inline-flex; align-items: center; gap: 0.5rem;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2"></path>
                </svg>
                Planning...
            </span>
        `;
    }
}

// Add CSS for loading animation
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .message-toast {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);