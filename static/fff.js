function openModal() {
    document.getElementById('myModal').style.display = 'block';
    var img = document.getElementById('myImage');
    var modalImg = document.getElementById('img01');
    modalImg.src = img.src;  // Копируем src
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

// Закрытие по клику на фон или ESC
window.onclick = function(event) {
    var modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

function openModal(imgSrc, title) {
    document.getElementById('img01').src = imgSrc;
    document.getElementById('gf').innerHTML = title;
    document.getElementById('myModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

// Закрытие модала при клике вне изображения (опционально)
window.onclick = function(event) {
    var modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
