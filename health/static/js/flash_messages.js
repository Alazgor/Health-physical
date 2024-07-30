// flash_messages.js

// Функция для скрытия flash сообщений через определенное время
function hideFlashMessages() {
    setTimeout(function() {
        var messages = document.getElementsByClassName('flash-message');
        for (var i = 0; i < messages.length; i++) {
            messages[i].style.display = 'none';
        }
    }, 5000); // set up time in millisec, when messages are shows
}

// Calling functions when pages are loading
window.onload = function() {
    hideFlashMessages();
};
