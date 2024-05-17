document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const startCameraBtn = document.getElementById('start-camera');
    const capturePhotoBtn = document.getElementById('capture-photo');
    const uploadPhotoBtn1 = document.getElementById('upload-photo');
    const photoNameInput = document.getElementById('photo-name');
    const fileInput = document.querySelector('input[type="file"]');
    const fileUploadForm = document.getElementById('file-upload-form');
    const uploadFileBtn = document.getElementById('upload-file-btn');
    const message = document.getElementById('message');
    
    let stream = null;
    let isCameraStarted = false;

    // Start camera function
    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            isCameraStarted = true;
            startCameraBtn.disabled = true;
            capturePhotoBtn.disabled = false;
            uploadPhotoBtn1.disabled = true;
            photoNameInput.disabled = false;
            uploadFileBtn.disabled = true;
        } catch (err) {
            console.error('Error accessing webcam:', err);
        }
    }

    // Capture photo function
    function capturePhoto() {
        uploadPhotoBtn1.disabled = false;
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        video.srcObject.getTracks().forEach(track => track.stop());
        capturePhotoBtn.disabled = true;
        startCameraBtn.disabled = false;
    }

    // Function to upload photo
    function uploadPhoto() {
        const dataUrl = canvas.toDataURL('image/jpeg');
        const imageData = dataUrl.split(',')[1];
        const fileName = photoNameInput.value || 'camera-photo.jpg';

        fetch('/upload', {
            method: 'POST',
            body: JSON.stringify({ image: imageData, filename: fileName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(handleFileUploadResponse) // Handle the response
        .catch(error => console.error('Error uploading photo:', error));
    }

    startCameraBtn.addEventListener('click', startCamera);
    capturePhotoBtn.addEventListener('click', capturePhoto);
    uploadPhotoBtn1.addEventListener('click', uploadPhoto);

    // Add change event listener to the file input
    fileInput.addEventListener('change', () => {
        // Check if a file is selected
        if (fileInput.files.length > 0) {
            // Enable the upload button
            uploadFileBtn.disabled = false;
        } else {
            // No file selected, disable the upload button
            uploadFileBtn.disabled = true;
        }
    });
    
    // Event listener for "Upload File" button click
    uploadFileBtn.addEventListener('click', function(event) {
        // Prevent the form from being submitted when the button is clicked
        event.preventDefault();
        // Trigger the form submission manually
        const formData = new FormData(fileUploadForm);
        uploadFile(formData);
    });

    // Function to handle file upload response and redirect to result.html
    function handleFileUploadResponse(response) {
        if (response.ok) {
            console.log('File uploaded successfully');
            showMessage();
            // Optionally, clear canvas and photo name input
            canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
            photoNameInput.value = '';
            document.getElementById('file-upload-form').reset();
            // Redirect to process-result route
            window.location.href = '/process-result';
        } else {
            console.error('Failed to upload file');
        }
    }

    // Function to upload file
    function uploadFile(formData) {
        fetch('/upload-file', {
            method: 'POST',
            body: formData,
        })
        .then(handleFileUploadResponse) // Handle the response
        .catch(error => console.error('Error uploading file:', error));
    }

    // Function to show message
    function showMessage() {
        message.style.display = 'block';
    }

    // Automatically start camera when the page loads
    if (!isCameraStarted) {
        startCamera();
    }
});