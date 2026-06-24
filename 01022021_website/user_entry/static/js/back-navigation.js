/**
 * back-navigation.js
 * 
 * Intercepts the browser Back button on authenticated pages and shows a logout confirmation modal.
 * Preserves session state if cancelled. Logs the user out if confirmed.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Only intercept if the user is authenticated. 
    // We can infer this by the presence of the logout link in the navbar.
    const logoutLink = document.querySelector('a.logout-link');
    
    if (logoutLink) {
        // We are on an authenticated page.

        // 1. Inject the Bootstrap Modal into the DOM
        const modalHtml = `
        <style>
          #logoutConfirmModal .modal-dialog { transform: none !important; }
        </style>
        <div class="modal" id="logoutConfirmModal" tabindex="-1" aria-labelledby="logoutConfirmModalLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
          <div class="modal-dialog" style="margin-top: 15vh;">
            <div class="modal-content" style="border: 1px solid rgba(173, 216, 255, 0.8); box-shadow: 0 8px 25px rgba(100, 150, 200, 0.2);">
              <div class="modal-header" style="background-color: #0f1623; border-bottom: 2px solid #FF7A3D;">
                <h5 class="modal-title" id="logoutConfirmModalLabel" style="font-family: 'Poppins', sans-serif; color: #ffffff !important; font-weight: 600; font-size: 1.35rem; letter-spacing: 0.5px;">Confirm Logout</h5>
              </div>
              <div class="modal-body" style="font-family: 'Open Sans', sans-serif; font-size: 1.1rem; padding: 2rem;">
                Do you want to logout?
              </div>
              <div class="modal-footer" style="border-top: none;">
                <button type="button" class="btn btn-outline-secondary" id="btnCancelLogout" style="min-width: 100px;">No</button>
                <button type="button" class="btn btn-primary" id="btnConfirmLogout" style="min-width: 100px; background-color: #FF7A3D; border-color: #FF7A3D;">Yes</button>
              </div>
            </div>
          </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // 2. Initialize Bootstrap Modal
        let logoutModal;
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            const modalEl = document.getElementById('logoutConfirmModal');
            logoutModal = new bootstrap.Modal(modalEl);
        }

        // 3. Create the "Trap" by pushing a dummy state
        // This ensures there is a forward state in history, so pressing back fires 'popstate' without leaving the page.
        window.history.pushState({ isBackTrap: true }, '');

        let isModalOpen = false;

        // 4. Listen for popstate (Back/Forward button press)
        window.addEventListener('popstate', function(event) {
            if (isModalOpen) {
                // Navigation locked. Restore the trap and ignore.
                window.history.pushState({ isBackTrap: true }, '');
                return;
            }

            isModalOpen = true;

            // Check if the modal exists, otherwise fallback to standard confirm
            if (logoutModal) {
                logoutModal.show();
            } else {
                if (confirm("Do you want to logout?")) {
                    window.location.href = logoutLink.href;
                } else {
                    isModalOpen = false;
                    // Reset the trap
                    window.history.pushState({ isBackTrap: true }, '');
                }
            }
        });

        // 5. Handle Modal Button Clicks
        document.getElementById('btnCancelLogout').addEventListener('click', function() {
            isModalOpen = false;
            if (logoutModal) logoutModal.hide();
            // Important: Push the state again to re-arm the trap!
            window.history.pushState({ isBackTrap: true }, '');
        });

        document.getElementById('btnConfirmLogout').addEventListener('click', function() {
            // User confirmed logout
            window.location.href = logoutLink.href;
        });
    }
});
