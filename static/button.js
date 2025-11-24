document.addEventListener('DOMContentLoaded', function() {
    const shadow = document.querySelector('#shadow');
    const main = document.querySelector('#head_main');

    // Проверка: если элементы не найдены, выводим ошибку в консоль
    if (!shadow) {
        console.error('Элемент #shadow не найден!');
        return;
    }
    if (!main) {
        console.error('Элемент #head_main не найден!');
        return;
    }

    // Toggle по клику на shadow (оверлей)
    shadow.addEventListener('click', () => {
        main.classList.toggle('disp'); // Простой toggle: добавляет/убирает класс
        console.log('Клик на shadow: класс disp toggled'); // Для отладки (убери, если не нужно)
    });

    // Опционально: закрытие по Esc
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && main.classList.contains('disp')) {
            main.classList.remove('disp');
        }
    });
});
