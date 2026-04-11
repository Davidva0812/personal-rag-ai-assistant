# 🌤️ Dynamic Weather Forecast App

A modern, responsive, and bilingual weather application that provides real-time weather data and a 5-day forecast. The app features a dynamic UI that adapts its background based on current weather conditions.

![Weather App Preview](screenshots/screenshot.png)

## 🚀 Features

- **🌍 Bilingual Support:** Seamlessly switch between **English** and **Hungarian** languages.
- **🖼️ Dynamic Backgrounds:** The background image automatically changes based on the weather condition (Clear, Clouds, Rain, Snow, etc.).
- **📍 Geolocation API:** Get local weather instantly with a single click using your browser's location.
- **📅 5-Day Forecast:** Detailed upcoming weather breakdown (midday snapshots).
- **🎨 Reactive UI:** Temperature-based color coding for the main weather card.
- **⚠️ Robust Error Handling:** Graceful management of "City not found," API errors, and denied location permissions.
  To run this project, you need to add your own API key in script.js.

## 🛠️ Tech Stack

- **HTML5** - Semantic structure.
- **CSS3** - Custom styling with Glassmorphism effects and transitions.
- **JavaScript (ES6+)** - Fetch API, Async/Await, and Geolocation.
- **OpenWeatherMap API** - Real-time data source.

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Davidva0812/weather-app.git](https://github.com/your-username/weather-app.git)
    ```
2.  **Get your API Key:**
    Sign up at [OpenWeatherMap](https://openweathermap.org/) and generate a free API key.
3.  **Configure the key:**
    Open `script.js` and paste your key into the `apiKey` variable:
    ```javascript
    const apiKey = "YOUR_API_KEY_HERE";
    ```
4.  **Launch:**
    Open `index.html` in your favorite browser.

## 📖 How It Works

1.  **Search:** Type a city name in the input field.
2.  **Location Button:** Click the 📍 icon to use your current GPS coordinates.
3.  **Language Switch:** Click the **HU/EN** button in the top right corner to change the language on the fly.
4.  **Weather States:**
    - **Clear Sky** ☀️ -> Sunny landscape background.
    - **Clouds** ☁️ -> Overcast/Cloudy background.
    - **Rain/Drizzle** 🌧️ -> Rainy/Moody background.
    - **Snow** ❄️ -> Snowy/Winter background.
    - **Thunderstorm** ⚡ -> Lightning/Storm background.

## 🛠️ Development Highlights

- **Dictionary Logic:** Implemented a central `translations` object for easy maintenance of bilingual strings.
- **Conditional Styling:** Created a `getBackgroundColor` function to map temperature ranges to visual cues (blue for cold, orange/red for heat).
- **Data Filtering:** Used `.filter()` on the 40-slot forecast array to extract only midday data for a clean 5-day view.

## ⚖️ License and Data source

This project uses weather data from the OpenWeather API. Data usage is governed by OpenWeather’s Terms of Service and Privacy Policy. The data is used under a free-tier plan for non-commercial, educational purposes.

---
Developed by David Varga
