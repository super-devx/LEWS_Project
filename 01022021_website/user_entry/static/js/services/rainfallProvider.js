/**
 * rainfallProvider.js
 * 
 * Abstract data provider for rainfall telemetry.
 * Currently fetches live weather data from Open-Meteo API.
 * In the future, simply swap the URL with your actual sensor endpoint!
 */

export async function getRainfallData() {
    try {
        // [ REPLACE THIS URL WITH YOUR ACTUAL SENSOR URL IN THE FUTURE ]
        // Example: const response = await fetch('http://192.168.1.100/api/rainfall');
        const SENSOR_URL = 'https://api.open-meteo.com/v1/forecast?latitude=10.8505&longitude=76.2711&current=precipitation';
        
        const response = await fetch(SENSOR_URL);
        const data = await response.json();
        
        // [ UPDATE THIS EXTRACTION LOGIC BASED ON YOUR SENSOR'S JSON RESPONSE ]
        // For Open-Meteo, precipitation is located at data.current.precipitation
        const baseValue = data.current ? data.current.precipitation : 0;
        
        return {
            rainfallValue: parseFloat(baseValue.toFixed(1)),
            unit: "mm",
            timestamp: new Date().toISOString(),
            source: "live-weather-api"
        };
    } catch (error) {
        console.error("Failed to fetch rainfall data:", error);
        // Fallback gracefully so the UI doesn't break
        return {
            rainfallValue: 0,
            unit: "mm",
            timestamp: new Date().toISOString(),
            source: "fallback",
            error: true
        };
    }
}
