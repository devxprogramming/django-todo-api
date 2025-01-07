const API_URL_ENDPOINT = `https://django-todo-api-k89l.onrender.com/api/all-todos/`;

// Test getting data from the API

async function getTodos() {
    const response = await fetch(API_URL_ENDPOINT);
    const data = await response.json();
    console.log(data);
}