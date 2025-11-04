# WanderTrip Search Button Data Flow

This document outlines the complete data flow from when a user clicks the Search button until the generated itinerary is displayed on planner.html.

## Overview Flow Chart

```
[User Clicks Search] → [Frontend Validation] → [API Call] → [Backend Processing] → [AI Generation] → [Data Storage] → [Planner Display]
```

## Detailed Data Flow

### 1. Frontend: Search Button Click (home-app.js)

**File:** `frontend/scripts/home-app.js`

**Function:** Search Form Event Listener

```javascript
searchForm.addEventListener("submit", function (e) {
```

**Data Processing:**

- Prevents default form submission
- Extracts form data:
  - `destination` (string)
  - `startDate` (YYYY-MM-DD)
  - `returnDate` (YYYY-MM-DD)
  - `adults` (integer from guests dropdown)

**Validation:**

- Checks start date is not in the past
- Ensures return date is after start date
- Calculates trip duration in days

**Local Storage:**

```javascript
localStorage.setItem("searchData", JSON.stringify(searchData));
```

### 2. Frontend: API Call to Backend

**Endpoint:** `POST http://localhost:8080/api/generate`

**Request Payload:**

```json
{
  "destination": "Paris",
  "days": 5,
  "guests": {
    "adults": 2
  },
  "startDate": "2025-02-07",
  "endDate": "2025-02-12"
}
```

### 3. Backend: API Endpoint Handler

**File:** `backend/main.py`

**Function:** `generate_new_itinerary()`

**Data Processing:**

- Extracts request JSON data
- Sets defaults:
  - `pace = 'moderate'`
  - `has_car = True`
- Derives month from start date
- Logs all processing steps

### 4. Backend: Geographic Data Gathering

**File:** `backend/utils/geocoding.py`

**Function:** `geocode_city(destination)`

```python
lat, lon = geocode_city(destination)
```

**API Call:** OpenTripMap Geocoding API

- **Input:** City name (e.g., "Paris")
- **Output:** Latitude and longitude coordinates

**File:** `backend/utils/poi_service.py`

**Function:** `get_pois(lat, lon)`

```python
pois = get_pois(lat, lon)
```

**API Call:** OpenTripMap POI API

- **Input:** Coordinates, radius (5000m), limit (10)
- **Output:** List of Points of Interest with names and types

### 5. Backend: AI Prompt Generation

**File:** `backend/itinerary_service.py`

**Function:** `build_prompt(destination, startDate, endDate, guestCount, pois)`

**Prompt Structure:**

```
Create a {days}-day travel itinerary for {destination} in {month}.
Traveler count: {guestCount} people.
Suggested POIs include: {poi_list}.

IMPORTANT: Return your response as a valid JSON object with the following structure:
{
  "destination": "{destination}",
  "startDate": "Feb 7, 2025",
  "days": [
    {
      "dayNumber": 1,
      "date": "Feb 7, 2025",
      "periods": {
        "morning": [...activities...],
        "afternoon": [...activities...],
        "evening": [...activities...]
      }
    }
  ],
  "additionalActivities": [...extra activities...]
}
```

### 6. Backend: AI Generation

**File:** `backend/itinerary_service.py`

**Function:** `generate_itinerary(prompt)`

**AI Model:** Google Gemini 1.5 Flash

```python
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(f"You are a travel itinerary planner. {prompt}")
```

**Response Processing:**

- Cleans markdown formatting (removes `json, `)
- Parses JSON response
- Handles errors with fallback data structure

### 7. Backend: Data Storage

**File:** `backend/main.py`

**Data Enhancement:**

```python
itinerary_json['userInputs'] = {
    'destination': destination,
    'days': days,
    'adults': adults,
    'startDate': start_date,
    'endDate': end_date
}
```

**Storage:**

- Saves to `backend/data/itinerary_data.json`
- Returns JSON response to frontend

### 8. Frontend: Navigation to Planner

**File:** `frontend/scripts/home-app.js`

**Success Handler:**

```javascript
.then((result) => {
    console.log("Itinerary generated successfully:", result);
    // Redirect to planner
    window.location.href = "planner.html";
})
```

### 9. Planner Page: Data Loading

**File:** `frontend/scripts/planner-app.js`

**Initialization:**

```javascript
document.addEventListener("DOMContentLoaded", async () => {
  // Check for search data
  const searchData = localStorage.getItem("searchData");

  // Load itinerary data
  await loadItineraryData();

  // Render components
  renderHeader();
  renderDayCards();
  renderActivitySidebar();
});
```

**Data Loading:**

```javascript
async function loadItineraryData() {
  const response = await fetch("http://localhost:8080/api/itinerary");
  itineraryData = await response.json();
}
```

### 10. Planner Page: UI Rendering

**Components Rendered:**

1. **Header:** Destination name and trip dates
2. **Day Cards:** Daily itinerary with morning/afternoon/evening activities
3. **Activity Sidebar:** Additional activities for drag-and-drop

## Data Structures

### Search Form Data

```javascript
{
  destination: "Paris",
  startDate: "2025-02-07",
  returnDate: "2025-02-12",
  adults: 2
}
```

### API Request Data

```javascript
{
  destination: "Paris",
  days: 5,
  guests: { adults: 2 },
  startDate: "2025-02-07",
  endDate: "2025-02-12"
}
```

### POI Data

```javascript
[
  { name: "Eiffel Tower", type: "monument" },
  { name: "Louvre Museum", type: "museum" },
  { name: "Notre Dame", type: "historic" },
];
```

### Generated Itinerary Data

```javascript
{
  destination: "Paris",
  startDate: "Feb 7, 2025",
  days: [
    {
      dayNumber: 1,
      date: "Feb 7, 2025",
      periods: {
        morning: [
          {
            time: "08:00",
            activity: "Breakfast at local café",
            description: "Start your day with croissants and coffee",
            id: "day1_morning_0"
          }
        ],
        afternoon: [...],
        evening: [...]
      }
    }
  ],
  additionalActivities: [
    {
      id: "extra_activity_0",
      activity: "Shopping at Champs-Élysées",
      description: "Browse luxury boutiques and department stores",
      duration: "2-3 hours",
      type: "additional"
    }
  ],
  userInputs: {
    destination: "Paris",
    days: 5,
    adults: 2,
    startDate: "2025-02-07",
    endDate: "2025-02-12"
  }
}
```

## Error Handling

### Frontend Validation Errors

- Date validation (past dates, invalid ranges)
- Form field validation
- Display toast messages to user

### Backend API Errors

- Geocoding failures (fallback coordinates)
- POI service failures (empty POI list)
- AI generation failures (fallback data structure)
- JSON parsing errors (error response)

### Frontend Loading Errors

- API unavailable (fallback to sample data)
- Malformed response data (error display)
- Network timeouts (retry mechanism)

## Performance Considerations

- **API Calls:** Sequential (geocoding → POI → AI generation)
- **Caching:** POI data could be cached by location
- **Loading States:** UI feedback during AI generation (15-30 seconds)
- **Fallbacks:** Sample data when APIs fail

## Security Considerations

- **API Keys:** Stored in backend .env file only
- **CORS:** Enabled for localhost development
- **Input Validation:** Date ranges, destination format
- **Error Messages:** Generic messages to avoid information leakage
