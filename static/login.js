import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
// https://firebase.google.com/docs/web/setup#available-libraries

// Web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBYaMx7ZyNonUGtmLUl0UlZBlZ4I07ONTY",
    authDomain: "multicloud-9875c.firebaseapp.com",
    projectId: "multicloud-9875c",
    storageBucket: "multicloud-9875c.appspot.com",
    messagingSenderId: "406218095576",
    appId: "1:406218095576:web:91057e2c55816c526790ad"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const signupLink = document.querySelector('.login-sign-txt a');
signupLink.addEventListener("click", function(event) {
    // Prevent the default action of the link
    event.preventDefault();
    // Redirect to the signup page
    window.location.href = "/signup";
});

const submit = document.getElementById('submit');

submit.addEventListener("click",function(event){
    event.preventDefault()
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            window.location.href = "/cloudidentify";
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(errorMessage)
        });
})
