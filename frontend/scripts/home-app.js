// Home page JavaScript functionality
document.addEventListener("DOMContentLoaded", function () {
  // Search form functionality
  const searchForm = document.getElementById("searchForm");
  searchForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const searchData = {
      destination: formData.get("destination"),
      startDate: formData.get("startDate"),
      returnDate: formData.get("returnDate"),
      adults: parseInt(formData.get("guests")) || 2, // Get from the actual form field
    };

    // Validate dates
    const startDate = new Date(searchData.startDate);
    const returnDate = new Date(searchData.returnDate);
    const today = new Date();

    // Set today to midnight for proper comparison (ignore time components)
    today.setHours(0, 0, 0, 0);
    startDate.setHours(0, 0, 0, 0);
    returnDate.setHours(0, 0, 0, 0);

    if (startDate < today) {
      showMessage("Start date cannot be in the past", "error");
      return;
    }

    if (returnDate <= startDate) {
      showMessage("Return date must be after start date", "error");
      return;
    }

    // Store search data and redirect to planner
    localStorage.setItem("searchData", JSON.stringify(searchData));

    // Show loading state
    const searchBtn = document.querySelector(".search-button");
    const originalText = searchBtn.textContent;
    searchBtn.textContent = "Planning...";
    searchBtn.disabled = true;

    // Calculate trip duration from dates
    const tripStartDate = new Date(searchData.startDate);
    const tripReturnDate = new Date(searchData.returnDate);
    const days = Math.ceil(
      (tripReturnDate - tripStartDate) / (1000 * 60 * 60 * 24)
    );

    // Call Flask API to generate itinerary
    fetch("http://localhost:8080/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        destination: searchData.destination,
        days: days,
        guests: {
          adults: searchData.adults,
        },
        startDate: searchData.startDate,
        endDate: searchData.returnDate,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((result) => {
        console.log("Itinerary generated successfully:", result);
        // Redirect to planner after successful generation
        // Check if we're in the pages directory or root
        const currentPath = window.location.pathname;
        if (currentPath.includes("/pages/")) {
          window.location.href = "planner.html";
        } else {
          window.location.href = "pages/planner.html";
        }
      })
      .catch((error) => {
        console.error("Error generating itinerary:", error);
        showMessage("Error generating itinerary. Please try again.", "error");
        searchBtn.textContent = originalText;
        searchBtn.disabled = false;
      });
  });

  // Set default dates (today and 3 days from now)
  const today = new Date();
  const threeDaysLater = new Date(today);
  threeDaysLater.setDate(today.getDate() + 3);

  document.getElementById("startDate").value = today
    .toISOString()
    .split("T")[0];
  document.getElementById("returnDate").value = threeDaysLater
    .toISOString()
    .split("T")[0];
});

// Message toast functionality
function showMessage(message, type = "info") {
  // Remove existing toast
  const existingToast = document.getElementById("messageToast");
  if (existingToast) {
    existingToast.remove();
  }

  // Create new toast
  const toast = document.createElement("div");
  toast.id = "messageToast";
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
  if (type === "success") {
    toast.style.background = "#10B981";
  } else if (type === "error") {
    toast.style.background = "#EF4444";
  } else {
    toast.style.background = "#3B82F6";
  }

  document.body.appendChild(toast);

  // Animate in
  setTimeout(() => {
    toast.style.transform = "translateX(0)";
  }, 100);

  // Auto-hide after 3 seconds
  setTimeout(() => {
    toast.style.transform = "translateX(100%)";
    setTimeout(() => {
      if (toast.parentNode) {
        toast.remove();
      }
    }, 300);
  }, 3000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

// Add loading animation to search form
function addLoadingState() {
  const searchBtn = document.querySelector(".search-btn");
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
const style = document.createElement("style");
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
