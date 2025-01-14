document.addEventListener("DOMContentLoaded", () => {
    
    const tokenExpiryTime = 14 * 60 * 1000; 
    let timer;
    let isUserActive = false; 

    // Refresh token function
    const refreshToken = () => {
        fetch('/refresh', {
            method: 'POST',
            credentials: 'include', // Ensures cookies are sent with the request
        })
        .then(response => {
            if (response.ok) {
                console.log("Token refreshed successfully.");
            } else {
                console.error("Failed to refresh token.");
            }
        })
        .catch(error => {
            console.error("Error during token refresh:", error);
        });
    };

    // Timer handler to check activity and refresh token if needed
    const handleTimer = () => {
        if (isUserActive) {
            console.log("User was active. Refreshing token...");
            refreshToken(); // Refresh the token if the user was active
        } else {
            console.log("User was not active. Token will not be refreshed.");
        }
        isUserActive = false; // Reset activity flag for the next period
        resetTimer(); // Start the next timer
    };


    const resetTimer = () => {
        clearTimeout(timer); // Clear any existing timer
        timer = setTimeout(handleTimer, tokenExpiryTime); // Set a new timer
    };

    
    const userActivityHandler = () => {
        isUserActive = true; 
    };

    
    ['mousemove', 'keydown', 'click', 'scroll', 'touchstart'].forEach(event => {
        window.addEventListener(event, userActivityHandler);
    });

    // Start the initial timer on page load
    resetTimer();
});
