# Travel Itinerary Planner

A modern, interactive travel itinerary planner that generates personalized travel schedules using AI and provides a drag-and-drop interface for customization.

## Features

- 🤖 **AI-Powered Itinerary Generation**: Uses Google's Gemini AI to create detailed travel itineraries
- 🏛️ **Beautiful UI**: Inspired by travel aesthetics with landmark illustrations and elegant typography
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🖱️ **Drag & Drop Interface**: Easily move activities between sidebar and schedule
- ⏰ **Time Management**: Visual time slots for morning, afternoon, and evening activities
- ✏️ **Editable Activities**: Click to edit activity details, times, and descriptions
- 💾 **Auto-Save**: Changes are automatically saved when using the API
- 🗺️ **POI Integration**: Incorporates real tourist attractions using OpenTripMap API

## Project Structure

```
Itinerary-Planner/
├── frontend/
│   ├── index.html          # Main HTML structure
│   ├── styles.css          # Complete styling with travel theme
│   ├── app.js             # JavaScript functionality
│   └── itinerary_data.json # Generated itinerary data
├── itinerary.py           # AI itinerary generation script
├── app.py                 # Flask API server (optional)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
cd Itinerary-Planner

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Keys Configuration

Create a `.env` file in the root directory with your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENTRIPMAP_API_KEY=your_opentripmap_api_key_here
```

**Get API Keys:**
- **Gemini API**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- **OpenTripMap API**: Visit [OpenTripMap](https://opentripmap.io/docs)

### 3. Generate Initial Data

```bash
# Generate sample itinerary data
python itinerary.py
```

This will create `frontend/itinerary_data.json` with AI-generated itinerary data.

### 4. Run the Application

You have two options:

#### Option A: Simple Static Server
```bash
cd frontend
python -m http.server 8000
```
Visit: http://localhost:8000

#### Option B: Full API Server (Recommended)
```bash
# Install additional dependencies
pip install flask flask-cors

# Start the API server
python app.py

# In another terminal, serve the frontend
cd frontend
python -m http.server 8000
```

## Usage Guide

### Basic Navigation

1. **View Itinerary**: The main area shows day cards with morning, afternoon, and evening sections
2. **Browse Activities**: The left sidebar contains additional activities you can add
3. **Drag & Drop**: Drag activities from the sidebar to any time period in the day cards
4. **Edit Activities**: Click on any scheduled activity to edit its details
5. **Time Management**: Activities are automatically sorted by time within each period

### Customization Features

- **Edit Activity Details**: Click any activity to modify time, name, and description
- **Remove Activities**: Use the delete button on activities or in the edit modal
- **Reorder Activities**: The system automatically sorts activities by time
- **Add New Activities**: Drag from the sidebar or edit existing ones

### Responsive Design

- **Desktop**: Full sidebar and day cards layout
- **Tablet**: Adjusts to smaller screens with flexible grid
- **Mobile**: Stacks sidebar below day cards, optimizes for touch interaction

## Technical Details

### Frontend Architecture

- **Pure JavaScript**: No frameworks required, vanilla JS for maximum compatibility
- **CSS Grid & Flexbox**: Modern layout techniques for responsive design
- **Drag & Drop API**: HTML5 native drag and drop implementation
- **Local Storage**: Automatic saving when API is available

### Backend Features

- **AI Integration**: Gemini AI generates contextual, location-specific itineraries
- **POI Discovery**: OpenTripMap API finds real attractions near the destination
- **JSON Output**: Structured data format for easy frontend consumption
- **Error Handling**: Graceful fallbacks when APIs are unavailable

### Design Philosophy

- **Travel-Themed**: Visual elements inspired by famous landmarks
- **User-Centric**: Intuitive drag-and-drop interface
- **Accessible**: High contrast, readable fonts, keyboard navigation
- **Modern**: Clean design with subtle animations and shadows

## Customization Options

### Modify Destinations
Edit `itinerary.py` variables:
```python
destination = "Your City"
days = 3
pace = "moderate"  # slow, moderate, fast
has_car = True
month = "Your Month"
```

### Styling Changes
- Colors: Modify CSS custom properties in `:root`
- Fonts: Update font imports in HTML head
- Layout: Adjust grid layouts in CSS

### API Customization
- Add new endpoints in `app.py`
- Modify AI prompts in `itinerary.py`
- Integrate additional APIs for hotels, restaurants, etc.

## Browser Support

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!

## Troubleshooting

### Common Issues

1. **No itinerary data**: Run `python itinerary.py` to generate data
2. **API errors**: Check your `.env` file has valid API keys
3. **CORS issues**: Use the Flask server instead of static files
4. **Drag not working**: Ensure you're using a modern browser with JavaScript enabled

### Development Tips

- Check browser console for JavaScript errors
- Verify JSON data format in `itinerary_data.json`
- Test with sample data if APIs are unavailable
- Use browser dev tools to inspect network requests