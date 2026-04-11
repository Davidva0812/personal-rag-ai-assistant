# Movie Info App with Pygame


A simple movie information app built with **Pygame**, 
using the **OMDb API** to fetch data about movies 
based on the **city name** provided by the user with corresponding movie posters.

---

## **Features**
- Search for a movie by its **title**
- Display basic info:
  - Title
  - Year
  - IMDb rating
  - Director
  - Main actors
- Toggle between **Light** and **Dark mode**
- Poster image display (if available)

## **Requirements**
Ensure you have the following installed before running the script:
- **Python 3.x**
- **Pygame**
- **Requests library**

## **Installation**
To install the required dependencies, run:
```bash
pip install pygame requests
```

## **Screenshots**
![screenshot](screenshots/light_mode.png)
![screenshot](screenshots/dark_mode.png)

## **Example output**
Title: Inception
Year: 2010
IMDB Rating: 8.8
Director: Christopher Nolan
Actors: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page

## **Future Improvements**
- Improve the user interface with more details and interactive features.
- Add Search Suggestions / Autocomplete
- More Movie Details
- Favorites or Watchlist Feature
- Add unit tests with mocking: Implement unit tests that mock external dependencies like API calls, 
HTTP requests, and movie data to ensure faster, isolated, and more reliable tests.

## **License and Data source**
This app uses data from the OMDb API (http://www.omdbapi.com/), 
licensed under **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)**.
The API is used for non-commercial, educational purposes only.






