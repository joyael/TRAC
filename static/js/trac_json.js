document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    document.getElementById('jsonForm').onsubmit = function(event) {
        event.preventDefault(); // Prevent the default form submission

        const jsonData = document.getElementById('jsonData').value;
        console.log(jsonData);
        console.log(document.getElementById('jsonForm').dataset.url);

        fetch(document.getElementById('jsonForm').dataset.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Change to application/json
                'X-CSRFToken':  csrftoken // Include CSRF token
            },
            body: JSON.stringify({ jsonData: jsonData }) // Wrap jsonData in an object
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('response').innerText = 'Error: ' + error;
        });
    };
});