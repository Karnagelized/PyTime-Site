function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
    .catch(err => console.error('Ошибка копирования: ', err));
}
