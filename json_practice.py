import json
x = {
  "destination": "Pasadena",
  "month": "November",
  "days": [
    {
      "day": 1,
      "activities": [
        {
          "name": "Old Pasadena Historic District",
          "type": "Shopping & Dining",
          "description": "Explore charming historic alleys, unique boutiques, and a variety of cafes and restaurants. Enjoy the architecture."
        },
        {
          "name": "Pasadena City Hall",
          "type": "Architectural Landmark",
          "description": "Admire the iconic Spanish Colonial Revival architecture, grand courtyard, and beautiful dome. A great spot for photos."
        },
        {
          "name": "The Gamble House",
          "type": "Historic Home & Architecture",
          "description": "Tour a masterpiece of American Arts and Crafts architecture by Greene & Greene. Check for available tour times and book in advance if possible."
        },
        {
          "name": "Dinner in Old Pasadena",
          "type": "Dining",
          "description": "Enjoy diverse culinary options, from casual eateries to upscale dining, in the vibrant Old Pasadena district."
        }
      ]
    },
    {
      "day": 2,
      "activities": [
        {
          "name": "The Huntington Library, Art Museum, and Botanical Gardens",
          "type": "Gardens, Art & Culture",
          "description": "Spend several hours exploring the vast botanical gardens (Japanese, Chinese, Desert, Rose), art galleries, and rare book collections. Plan for extensive walking."
        },
        {
          "name": "Lunch near The Huntington",
          "type": "Dining",
          "description": "Grab a meal at one of the cafes within The Huntington or a nearby restaurant in the San Marino area."
        },
        {
          "name": "Norton Simon Museum",
          "type": "Art Museum",
          "description": "Discover an impressive collection of European and Asian art spanning various periods, featuring works by masters like Degas, Van Gogh, and Picasso."
        },
        {
          "name": "South Lake Avenue Shopping & Dining",
          "type": "Shopping & Dining",
          "description": "Explore the upscale shops and department stores along South Lake Avenue, followed by dinner at one of its many restaurants."
        }
      ]
    },
    {
      "day": 3,
      "activities": [
        {
          "name": "Rose Bowl Stadium & Park",
          "type": "Landmark & Recreation",
          "description": "Drive by the iconic Rose Bowl Stadium, home of the Rose Bowl Game. Enjoy a leisurely walk or bike ride around the scenic surrounding park and Arroyo Seco."
        },
        {
          "name": "Pasadena Museum of History",
          "type": "Local History",
          "description": "Delve into the rich history of Pasadena and the San Gabriel Valley through rotating exhibits and permanent collections."
        },
        {
          "name": "Arlington Garden in Pasadena",
          "type": "Nature & Garden",
          "description": "Visit Pasadena's only botanical garden dedicated to water-wise plants. A peaceful, free-to-enter Mediterranean-climate garden."
        },
        {
          "name": "Farewell Dinner",
          "type": "Dining",
          "description": "Enjoy a final memorable meal at a Pasadena restaurant of your choice, perhaps trying a different cuisine or neighborhood."
        }
      ]
    }
  ]
}

y = json.dumps(x)
print(y["destination"])