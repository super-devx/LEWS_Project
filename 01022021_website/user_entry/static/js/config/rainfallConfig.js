/**
 * rainfallConfig.js
 * 
 * Centralized configuration layer for location-based rainfall data APIs.
 * Add new locations here without touching the dashboard or service logic.
 */

export const LOCATION_CONFIG = {
    kerala: {
        rainfallApi: "https://api.open-meteo.com/v1/forecast?latitude=10.8505&longitude=76.2711&current=precipitation",
        name: "Kerala"
    },
    himachal: {
        rainfallApi: "https://api.open-meteo.com/v1/forecast?latitude=31.1048&longitude=77.1734&current=precipitation",
        name: "Himachal Pradesh"
    },
    uttarakhand: {
        rainfallApi: "https://api.open-meteo.com/v1/forecast?latitude=30.0668&longitude=79.0193&current=precipitation",
        name: "Uttarakhand"
    }
};

/**
 * Standardized API Adapter
 * 
 * Isolates the JSON extraction logic. If future hardware sensors return a 
 * different JSON structure, modify ONLY this function.
 */
export function extractRainfallValue(response) {
    if (!response) return 0;
    
    // Open-Meteo Structure
    if (response.current && response.current.precipitation !== undefined) {
        return response.current.precipitation;
    }
    
    // Example Future Sensor Structure
    if (response.sensor && response.sensor.value !== undefined) {
        return response.sensor.value;
    }

    if (response.rainfall && response.rainfall.amount !== undefined) {
        return response.rainfall.amount;
    }

    return 0; // Safe default
}
