/**
 * rainfallEngine.js
 * 
 * Logic to process rainfall data and compute thresholds for the Rainfall Analysis Gauge.
 */

export const RAINFALL_ZONES = {
    LOW: { min: 0, max: 20, label: "LOW RAINFALL", color: "#4ade80" },
    MODERATE: { min: 20, max: 50, label: "MODERATE", color: "#facc15" },
    HEAVY: { min: 50, max: 100, label: "HEAVY RAIN", color: "#fb923c" },
    EXTREME: { min: 100, max: Infinity, label: "EXTREME", color: "#ef4444" }
};

export function updateRainfallUI(data) {
    if (!data) return;
    
    const score = data.rainfallValue;
    
    // Determine Zone
    let statusText = "UNKNOWN";
    let color = "#cbd5e1"; // default gray
    
    // We cap the display score to something reasonable so the needle doesn't spin wildly.
    // For visual mapping, let's say 0-120 maps to the gauge.
    const maxVisualScale = 120;
    const displayScore = Math.max(0, Math.min(maxVisualScale, score));
    
    if (score >= RAINFALL_ZONES.EXTREME.min) {
        statusText = RAINFALL_ZONES.EXTREME.label;
        color = RAINFALL_ZONES.EXTREME.color;
    } else if (score >= RAINFALL_ZONES.HEAVY.min) {
        statusText = RAINFALL_ZONES.HEAVY.label;
        color = RAINFALL_ZONES.HEAVY.color;
    } else if (score >= RAINFALL_ZONES.MODERATE.min) {
        statusText = RAINFALL_ZONES.MODERATE.label;
        color = RAINFALL_ZONES.MODERATE.color;
    } else {
        statusText = RAINFALL_ZONES.LOW.label;
        color = RAINFALL_ZONES.LOW.color;
    }
    
    // Update Score Values
    const scoreValueEl = document.getElementById('rainfall-score-value');
    const scoreStatusEl = document.getElementById('rainfall-score-status');
    const unitEl = document.getElementById('rainfall-score-unit');
    
    if (scoreValueEl) scoreValueEl.innerText = score.toFixed(1);
    if (scoreStatusEl) scoreStatusEl.innerText = statusText;
    if (unitEl) unitEl.innerText = data.unit;
    
    if (scoreValueEl) scoreValueEl.style.color = color;
    if (scoreStatusEl) scoreStatusEl.style.color = color;

    // Gauge Fill Animation
    const gaugeFill = document.getElementById('rainfall-gauge-fill');
    if (gaugeFill) {
        const circumference = 565.48; // PI * R (180)
        const offset = circumference - ((displayScore / maxVisualScale) * circumference);
        
        setTimeout(() => {
            gaugeFill.style.strokeDashoffset = offset;
            gaugeFill.style.stroke = color;
        }, 100);
    }

    // Needle Rotation Animation
    const gaugeNeedle = document.getElementById('rainfall-gauge-needle');
    if (gaugeNeedle) {
        // Range is from -90deg (0) to 90deg (maxVisualScale)
        const rotation = -90 + ((displayScore / maxVisualScale) * 180);
        
        setTimeout(() => {
            gaugeNeedle.style.transform = `rotate(${rotation}deg)`;
        }, 100);
    }

    // Radar Beacon Update
    const radarBeacon = document.getElementById('rainfall-radar-beacon');
    if (radarBeacon) {
        radarBeacon.style.background = `${color}33`; // 20% opacity
    }
    
    const beaconRings = document.querySelectorAll('.rainfall-beacon-ring');
    beaconRings.forEach(ring => {
        ring.style.borderColor = color;
    });
}
