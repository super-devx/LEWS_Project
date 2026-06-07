export const STATUS_RANGES = {
  GREEN: [0, 24],
  YELLOW: [25, 49],
  ORANGE: [50, 74],
  RED: [75, 100]
};

function generateMockScore() {
    const probability = Math.random();
    let score;

    if (probability < 0.60) {
        // Green (~60%)
        score = Math.floor(Math.random() * (24 - 0 + 1)) + 0;
    } else if (probability < 0.90) {
        // Yellow (~30%)
        score = Math.floor(Math.random() * (49 - 25 + 1)) + 25;
    } else if (probability < 0.98) {
        // Orange (~8%)
        score = Math.floor(Math.random() * (74 - 50 + 1)) + 50;
    } else {
        // Red (~2%)
        score = Math.floor(Math.random() * (100 - 75 + 1)) + 75;
    }

    return score;
}

export function getRiskScore() {
    return {
        score: generateMockScore(),
        confidence: 0.91,
        timestamp: new Date().toISOString()
    };
}
