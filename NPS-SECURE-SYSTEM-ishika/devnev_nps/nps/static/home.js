document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('surveyForm').addEventListener('submit', function (event) {
        event.preventDefault();

        // Get the CSRF token from the form
        var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        // Prepare the form data
        var formData = new FormData(document.getElementById('surveyForm'));

        // Append the CSRF token to the form data
        formData.append('csrfmiddlewaretoken', csrf_token);

        // Send the AJAX request
        fetch('/save_survey/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Handle the response as needed
            // For example, you can redirect to a thank-you page
            window.location.href = '/thank_you/';
        })
        .catch(error => console.error('Error:', error));
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
