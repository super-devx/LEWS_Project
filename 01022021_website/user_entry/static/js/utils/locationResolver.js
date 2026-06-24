/**
 * locationResolver.js
 * 
 * Dynamic location resolver. Decouples the UI from knowing the active location.
 */

export function getActiveLocation() {
    // Priority 1: Check URL search parameters (e.g., ?location=himachal)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('location')) {
        const urlLoc = urlParams.get('location').toLowerCase();
        return urlLoc;
    }
    
    // Priority 2: Check localStorage
    const storedLoc = localStorage.getItem('activeLocation');
    if (storedLoc) {
        return storedLoc.toLowerCase();
    }
    
    // Priority 3: Fallback default
    return 'kerala';
}
