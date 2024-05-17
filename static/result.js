function saveImage(imageLink, imageDescription, dateTime) {
    // Send a POST request to the server with image data
    fetch('/save-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            image_url: imageLink,
            image_description: imageDescription,
            date_time: dateTime,
            image_link: imageLink
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/album';
        } else {
            alert('Failed to save image data.');
        }
    })
    .catch(error => console.error('Error saving image data:', error));
}
