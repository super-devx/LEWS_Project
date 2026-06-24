/**
 * rainfallProvider.js
 * 
 * Abstract data provider for rainfall telemetry.
 * Resolves location, fetches data, and uses an adapter to extract the value.
 */

import { LOCATION_CONFIG, extractRainfallValue } from '../config/rainfallConfig.js';

export async function getRainfallData(locationId) {
    try {
        // Fallback to kerala if no locationId is provided or config doesn't exist
        const configKey = LOCATION_CONFIG[locationId] ? locationId : 'kerala';
        const config = LOCATION_CONFIG[configKey];
        
        if (!config) {
            throw new Error(`Location ${locationId} not found in configuration.`);
        }

        const SENSOR_URL = config.rainfallApi;
        
        const response = await fetch(SENSOR_URL);
        
        if (!response.ok) {
            throw new Error(`API returned status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Use the adapter layer to extract the actual value safely
        const baseValue = extractRainfallValue(data);
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
            source: "live-weather-api",
            locationName: config.name
        };
    } catch (error) {
        console.error(`Failed to fetch rainfall data for ${locationId}:`, error);
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
