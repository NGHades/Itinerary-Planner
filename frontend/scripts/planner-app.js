// Global state management
let itineraryData = null;
let currentEditingActivity = null;

// DOM elements (will be initialized after DOM loads)
let loadingOverlay,
  destinationName,
  tripDates,
  daysGrid,
  activityList,
  activityModal,
  activityForm;

// Initialize the application
document.addEventListener("DOMContentLoaded", async () => {
  // Initialize DOM elements after DOM is ready
  loadingOverlay = document.getElementById("loadingOverlay");
  destinationName = document.getElementById("destination-name");
  tripDates = document.getElementById("trip-dates");
  daysGrid = document.getElementById("daysGrid");
  activityList = document.getElementById("activityList");
  activityModal = document.getElementById("activityModal");
  activityForm = document.getElementById("activityForm");

  console.log("DOM elements initialized:");
  console.log("loadingOverlay:", loadingOverlay);
  console.log("daysGrid:", daysGrid);
  console.log("destinationName:", destinationName);

  showLoading(true);

  // Check if we have search data from the home page
  const searchData = localStorage.getItem("searchData");
  let isNewItinerary = false;

  if (searchData) {
    const data = JSON.parse(searchData);
    console.log("Search data from home page:", data);
    isNewItinerary = true;

    // Update the destination and dates if available
    if (data.destination) {
      console.log(`Loading fresh itinerary for ${data.destination}`);
      // Show message that we're loading a fresh itinerary
      showMessage(
        `Loading your personalized itinerary for ${data.destination}...`,
        "info"
      );
    }

    // Clear the search data since we've used it
    localStorage.removeItem("searchData");
  }

  console.log("🚀 Starting app initialization...");

  try {
    await loadItineraryData();

    console.log("✅ Data loaded, starting render...");
    renderHeader();
    renderDayCards();
    renderActivitySidebar();
    setupEventListeners();
    console.log("✅ App initialization completed successfully!");

    // Show success message if this is a fresh itinerary
    if (isNewItinerary && itineraryData) {
      showMessage(
        `Your personalized itinerary for ${itineraryData.destination} is ready!`,
        "success"
      );
    }
  } catch (error) {
    console.error("❌ INITIALIZATION ERROR:", error);
    console.error("Error stack:", error.stack);
    console.error("Error occurred during app initialization");
    console.error("Timestamp:", new Date().toISOString());

    // More specific error handling
    if (error.message && error.message.includes("fetch")) {
      console.error("🌐 Network error detected");
      showError(
        "[NETWORK] Unable to connect to server. Please make sure the backend is running."
      );
    } else if (error.message && error.message.includes("JSON")) {
      console.error("📄 JSON parsing error detected");
      showError("[DATA] Invalid data format received. Please try again.");
    } else {
      console.error("🔍 Generic error detected");
      showError(
        `[INIT] Failed to load itinerary data: ${
          error.message || "Unknown error"
        }`
      );
    }
  } finally {
    showLoading(false);
  }
});

// Load itinerary data from JSON file or API
async function loadItineraryData() {
  console.log("Starting to load itinerary data...");

  try {
    // Load from API only (data now managed by backend)
    console.log("Fetching itinerary from API...");
    const response = await fetch("http://localhost:8080/api/itinerary");
    console.log("API response status:", response.status);

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    itineraryData = await response.json();

    // If there's an error in the data, handle it
    if (itineraryData.error) {
      throw new Error(itineraryData.error);
    }

    console.log("Loaded itinerary data:", itineraryData);
  } catch (error) {
    console.error("Error loading itinerary data:", error);
    console.log("Using fallback sample data...");
    // Fallback to sample data for development
    itineraryData = getSampleData();
    console.log("Sample data loaded:", itineraryData);
  }
}

// Render header information
function renderHeader() {
  console.log("renderHeader called");

  try {
    if (!destinationName || !tripDates) {
      console.error("Header DOM elements not found:", {
        destinationName,
        tripDates,
      });
      return;
    }

    if (itineraryData) {
      destinationName.textContent =
        itineraryData.destination || "Unknown Destination";

      if (itineraryData.days && itineraryData.days.length > 0) {
        const startDate = itineraryData.startDate || itineraryData.days[0].date;
        const endDate = itineraryData.days[itineraryData.days.length - 1].date;
        tripDates.textContent = `${startDate} - ${endDate}`;
      }
    }
    console.log("✅ Header rendered successfully");
  } catch (error) {
    console.error("Error in renderHeader:", error);
    throw error;
  }
}

// Render day cards
function renderDayCards() {
  console.log("renderDayCards called");
  console.log("itineraryData:", itineraryData);
  console.log("daysGrid element:", daysGrid);

  try {
    if (!daysGrid) {
      console.error("daysGrid element not found");
      return;
    }

    daysGrid.innerHTML = "";

    if (!itineraryData) {
      console.log("No itinerary data available");
      daysGrid.innerHTML = "<p>No itinerary data available.</p>";
      return;
    }

    if (!itineraryData.days || itineraryData.days.length === 0) {
      console.log("No days found in itinerary data");
      daysGrid.innerHTML = "<p>No days found in itinerary.</p>";
      return;
    }

    console.log("Rendering", itineraryData.days.length, "day cards");
    itineraryData.days.forEach((day, index) => {
      console.log(`Creating day card ${index + 1}:`, day);
      const dayCard = createDayCard(day);
      daysGrid.appendChild(dayCard);
    });

    console.log("✅ Day cards rendering complete");
  } catch (error) {
    console.error("Error in renderDayCards:", error);
    throw error;
  }
}

// Create a day card element
function createDayCard(day) {
  const dayCard = document.createElement("div");
  dayCard.className = "day-card";
  dayCard.dataset.dayNumber = day.dayNumber;

  dayCard.innerHTML = `
        <div class="day-header">
            <div class="day-number">Day ${day.dayNumber}</div>
            <div class="day-date">${day.date}</div>
            <div class="calendar-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
            </div>
        </div>
        <div class="day-content">
            ${createTimePeriods(day.periods, day.dayNumber)}
        </div>
    `;

  return dayCard;
}

// Create time periods (morning, afternoon, evening)
function createTimePeriods(periods, dayNumber) {
  const periodNames = ["morning", "afternoon", "evening"];
  const periodIcons = {
    morning: "☀️",
    afternoon: "🌤️",
    evening: "🌙",
  };

  return periodNames
    .map((periodName) => {
      const activities = periods[periodName] || [];

      return `
            <div class="time-period">
                <div class="period-header ${periodName}">
                    <div class="period-icon"></div>
                    <span>${
                      periodName.charAt(0).toUpperCase() + periodName.slice(1)
                    }</span>
                </div>
                <div class="activities-list" 
                     data-day="${dayNumber}" 
                     data-period="${periodName}"
                     ondrop="handleDrop(event)" 
                     ondragover="handleDragOver(event)"
                     ondragleave="handleDragLeave(event)">
                    ${activities
                      .map((activity) => createScheduledActivity(activity))
                      .join("")}
                </div>
            </div>
        `;
    })
    .join("");
}

// Create scheduled activity element
function createScheduledActivity(activity) {
  return `
        <div class="scheduled-activity" data-activity-id="${activity.id}" onclick="editActivity('${activity.id}')">
            <div class="activity-time">${activity.time}</div>
            <div class="activity-name">${activity.activity}</div>
            <div class="activity-description">${activity.description}</div>
            <div class="activity-actions">
                <button class="action-btn" onclick="event.stopPropagation(); editActivity('${activity.id}')" title="Edit">
                    ✏️
                </button>
                <button class="action-btn" onclick="event.stopPropagation(); removeActivity('${activity.id}')" title="Remove">
                    🗑️
                </button>
            </div>
        </div>
    `;
}

// Render activity sidebar
function renderActivitySidebar() {
  activityList.innerHTML = "";

  if (
    !itineraryData.additionalActivities ||
    itineraryData.additionalActivities.length === 0
  ) {
    activityList.innerHTML = "<p>No additional activities available.</p>";
    return;
  }

  itineraryData.additionalActivities.forEach((activity) => {
    const activityElement = createDraggableActivity(activity);
    activityList.appendChild(activityElement);
  });
}

// Create draggable activity element
function createDraggableActivity(activity) {
  const activityDiv = document.createElement("div");
  activityDiv.className = "activity-item";
  activityDiv.draggable = true;
  activityDiv.dataset.activityId = activity.id;

  activityDiv.innerHTML = `
        <div class="activity-name">${activity.activity}</div>
        <div class="activity-description">${activity.description}</div>
        <div class="activity-duration">${activity.duration || "1-2 hours"}</div>
    `;

  // Add drag event listeners
  activityDiv.addEventListener("dragstart", handleDragStart);
  activityDiv.addEventListener("dragend", handleDragEnd);

  return activityDiv;
}

// Drag and drop handlers
function handleDragStart(e) {
  e.dataTransfer.setData("text/plain", e.target.dataset.activityId);
  e.target.classList.add("dragging");
}

function handleDragEnd(e) {
  e.target.classList.remove("dragging");
}

function handleDragOver(e) {
  e.preventDefault();
  e.currentTarget.classList.add("drag-over");
}

function handleDragLeave(e) {
  e.currentTarget.classList.remove("drag-over");
}

function handleDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove("drag-over");

  const activityId = e.dataTransfer.getData("text/plain");
  const dayNumber = e.currentTarget.dataset.day;
  const period = e.currentTarget.dataset.period;

  addActivityToSchedule(activityId, dayNumber, period);
}

// Add activity to schedule
function addActivityToSchedule(activityId, dayNumber, period) {
  // Find the activity in additional activities
  const activity = itineraryData.additionalActivities.find(
    (a) => a.id === activityId
  );

  if (!activity) {
    console.error("Activity not found:", activityId);
    return;
  }

  // Create new scheduled activity
  const newActivity = {
    id: `day${dayNumber}_${period}_${Date.now()}`,
    time: getNextAvailableTime(dayNumber, period),
    activity: activity.activity,
    description: activity.description,
  };

  // Find the day and add the activity
  const day = itineraryData.days.find((d) => d.dayNumber == dayNumber);
  if (day) {
    if (!day.periods[period]) {
      day.periods[period] = [];
    }
    day.periods[period].push(newActivity);

    // Sort activities by time
    day.periods[period].sort((a, b) => a.time.localeCompare(b.time));

    // Re-render the day card
    renderDayCards();

    // Remove activity from sidebar (optional - you might want to keep it for reuse)
    // removeActivityFromSidebar(activityId);
  }
}

// Get next available time slot
function getNextAvailableTime(dayNumber, period) {
  const timeSlots = {
    morning: ["08:00", "09:00", "10:00", "11:00"],
    afternoon: ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
    evening: ["18:00", "19:00", "20:00", "21:00"],
  };

  const day = itineraryData.days.find((d) => d.dayNumber == dayNumber);
  const existingTimes = day.periods[period]?.map((a) => a.time) || [];

  for (const time of timeSlots[period]) {
    if (!existingTimes.includes(time)) {
      return time;
    }
  }

  // If all slots are taken, return the last slot + 1 hour
  return timeSlots[period][timeSlots[period].length - 1];
}

// Activity editing functions
function editActivity(activityId) {
  const activity = findActivityById(activityId);
  if (!activity) {
    console.error("Activity not found:", activityId);
    return;
  }

  currentEditingActivity = activity;

  // Populate form
  document.getElementById("activityTime").value = activity.time;
  document.getElementById("activityName").value = activity.activity;
  document.getElementById("activityDescription").value = activity.description;

  // Show modal
  activityModal.classList.add("active");
}

function removeActivity(activityId) {
  if (confirm("Are you sure you want to remove this activity?")) {
    // Find and remove the activity
    for (const day of itineraryData.days) {
      for (const period in day.periods) {
        const index = day.periods[period].findIndex((a) => a.id === activityId);
        if (index !== -1) {
          day.periods[period].splice(index, 1);
          renderDayCards();
          return;
        }
      }
    }
  }
}

function findActivityById(activityId) {
  for (const day of itineraryData.days) {
    for (const period in day.periods) {
      const activity = day.periods[period].find((a) => a.id === activityId);
      if (activity) {
        return activity;
      }
    }
  }
  return null;
}

// Event listeners setup
function setupEventListeners() {
  try {
    console.log("Setting up event listeners...");

    // Check if required elements exist
    const modalClose = document.getElementById("modalClose");
    const cancelEdit = document.getElementById("cancelEdit");
    const deleteActivity = document.getElementById("deleteActivity");

    if (
      !modalClose ||
      !cancelEdit ||
      !deleteActivity ||
      !activityForm ||
      !activityModal
    ) {
      console.warn("Some modal elements not found:", {
        modalClose: !!modalClose,
        cancelEdit: !!cancelEdit,
        deleteActivity: !!deleteActivity,
        activityForm: !!activityForm,
        activityModal: !!activityModal,
      });
    }

    // Modal close
    if (modalClose) modalClose.addEventListener("click", closeModal);
    if (cancelEdit) cancelEdit.addEventListener("click", closeModal);

    // Form submission
    if (activityForm)
      activityForm.addEventListener("submit", handleActivitySave);

    // Delete button
    if (deleteActivity)
      deleteActivity.addEventListener("click", handleActivityDelete);

    // Close modal on overlay click
    if (activityModal) {
      activityModal.addEventListener("click", (e) => {
        if (e.target === activityModal) {
          closeModal();
        }
      });
    }

    console.log("✅ Event listeners setup completed");
  } catch (error) {
    console.error("Error in setupEventListeners:", error);
    throw error;
  }
}

function closeModal() {
  activityModal.classList.remove("active");
  currentEditingActivity = null;
}

function handleActivitySave(e) {
  e.preventDefault();

  if (!currentEditingActivity) return;

  const formData = new FormData(activityForm);

  currentEditingActivity.time = formData.get("time");
  currentEditingActivity.activity = formData.get("activity");
  currentEditingActivity.description = formData.get("description");

  renderDayCards();
  closeModal();

  // Auto-save the changes
  saveItinerary();
}

// Save itinerary data
async function saveItinerary() {
  try {
    const response = await fetch("http://localhost:8080/api/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(itineraryData),
    });

    if (response.ok) {
      console.log("Itinerary saved successfully");
      showMessage("Changes saved!", "success");
    } else {
      console.error("Failed to save itinerary");
      showMessage("Failed to save changes", "error");
    }
  } catch (error) {
    console.error("Error saving itinerary:", error);
    // Silently fail if API is not available
  }
}

function handleActivityDelete() {
  if (
    currentEditingActivity &&
    confirm("Are you sure you want to delete this activity?")
  ) {
    removeActivity(currentEditingActivity.id);
    closeModal();
  }
}

// Utility functions
function showLoading(show) {
  console.log("showLoading called with:", show);
  console.log("loadingOverlay element:", loadingOverlay);

  if (!loadingOverlay) {
    console.error("loadingOverlay element not found!");
    return;
  }

  if (show) {
    loadingOverlay.classList.add("active");
    console.log("Loading overlay shown");
  } else {
    loadingOverlay.classList.remove("active");
    console.log("Loading overlay hidden");
  }
}

function showError(message) {
  console.error("🚨 showError called with message:", message);
  showMessage(message, "error");
}

function showMessage(message, type = "info") {
  // Create or update message toast
  let toast = document.getElementById("messageToast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "messageToast";
    toast.className = "message-toast";
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.className = `message-toast ${type} active`;

  // Auto-hide after 3 seconds
  setTimeout(() => {
    toast.classList.remove("active");
  }, 3000);
}

// Sample data for fallback
function getSampleData() {
  return {
    destination: "Pasadena",
    startDate: "Feb 7, 2025",
    days: [
      {
        dayNumber: 1,
        date: "Feb 7, 2025",
        periods: {
          morning: [
            {
              time: "08:00",
              activity: "Breakfast and get ready",
              description: "Start the day with a hearty breakfast",
              id: "day1_morning_0",
            },
            {
              time: "10:00",
              activity: "Bus to First Destination ( Museum )",
              description: "Explore local history and culture",
              id: "day1_morning_1",
            },
          ],
          afternoon: [
            {
              time: "14:00",
              activity: "Lunch and get ready for the next destination",
              description: "Enjoy local cuisine",
              id: "day1_afternoon_0",
            },
            {
              time: "16:00",
              activity: "Bus to Second Destination ( Historic Building )",
              description: "Visit architectural landmarks",
              id: "day1_afternoon_1",
            },
          ],
          evening: [
            {
              time: "19:00",
              activity: "Stroll along the famous avenue",
              description: "Enjoy the evening atmosphere",
              id: "day1_evening_0",
            },
            {
              time: "20:00",
              activity: "Dinner in Barcelona Restaurant",
              description: "Taste authentic local cuisine",
              id: "day1_evening_1",
            },
          ],
        },
      },
    ],
    additionalActivities: [
      {
        id: "extra_activity_0",
        activity: "Shopping at Local Market",
        description: "Browse local crafts and souvenirs",
        duration: "1-2 hours",
        type: "additional",
      },
      {
        id: "extra_activity_1",
        activity: "Art Gallery Visit",
        description: "Explore contemporary and classical art",
        duration: "2-3 hours",
        type: "additional",
      },
      {
        id: "extra_activity_2",
        activity: "Coffee Shop Tour",
        description: "Discover local coffee culture",
        duration: "1 hour",
        type: "additional",
      },
    ],
  };
}
