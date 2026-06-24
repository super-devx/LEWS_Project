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
