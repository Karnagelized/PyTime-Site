// Ограничиваем длину до 6 символов
function limitLength(input) {
    if (input.value.length > 6) {
        input.value = input.value.slice(0, 6);
    }
    
    // Удаляем все нецифровые символы
    input.value = input.value.replace(/\D/g, '');
}


// Блокировка ввода нецифровых символов
document.addEventListener('DOMContentLoaded', function() {
    const codeInput = document.querySelector('.verify-code-input');
    
    codeInput.addEventListener('keypress', function(e) {
        // Разрешаем только цифры
        if (e.key < '0' || e.key > '9') {
            e.preventDefault();
        }
    });
    
    codeInput.addEventListener('input', function() {
        // Автоматическое ограничение длины
        if (this.value.length > 6) {
            this.value = this.value.slice(0, 6);
        }
    });
    
    codeInput.addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('text');
        const digitsOnly = pastedData.replace(/\D/g, '').slice(0, 6);
        this.value = digitsOnly;
    });
});
