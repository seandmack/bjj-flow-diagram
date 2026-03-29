// Firebase Configuration (compat SDK — no bundler needed)
const firebaseConfig = {
    apiKey: "AIzaSyBrZl9gRMSeTgWJVVXyt-QrPQSpRE6h1n0",
    authDomain: "bjj-flow-diagram.firebaseapp.com",
    projectId: "bjj-flow-diagram",
    storageBucket: "bjj-flow-diagram.firebasestorage.app",
    messagingSenderId: "846274772015",
    appId: "1:846274772015:web:b2d8a4b9c331166dc85ada",
    measurementId: "G-TVFZCVSE0X"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();
