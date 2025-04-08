// Script básico de JavaScript (puedes expandirlo según sea necesario)

// Ejemplo: Prevenir el envío del formulario si los campos están vacíos
document.querySelector('form').addEventListener('submit', function(event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (username === "" || password === "") {
        alert("Por favor, complete todos los campos.");
        event.preventDefault(); // Previene el envío del formulario
    }
});

// Ejemplo de una posible función para mostrar un mensaje al usuario al enviar el formulario
function showMessage(message, type) {
    const messageContainer = document.createElement('div');
    messageContainer.textContent = message;
    messageContainer.className = type === 'success' ? 'success-message' : 'error-message';
    document.body.appendChild(messageContainer);
}
