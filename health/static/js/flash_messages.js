// flash_messages.js

// Функция для скрытия flash сообщений через определенное время
function hideFlashMessages() {
    setTimeout(function() {
        var messages = document.getElementsByClassName('flash-message');
        for (var i = 0; i < messages.length; i++) {
            messages[i].style.display = 'none';
        }
    }, 5000); // Установите время в миллисекундах, через которое сообщения исчезнут (здесь 5000 миллисекунд = 5 секунд)
}

// Вызываем функцию при загрузке страницы
window.onload = function() {
    hideFlashMessages();
};
