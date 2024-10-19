let currentPage = 0;
let images = [];

function loadMangaList() {
    fetch('/mangas')
        .then(response => response.json())
        .then(data => {
            const mangaListDiv = document.getElementById('manga-list');
            data.forEach(manga => {
                const mangaItem = document.createElement('div');
                mangaItem.innerText = manga.title;
                mangaItem.onclick = () => loadManga(manga.title);
                mangaListDiv.appendChild(mangaItem);
            });
        });
}

function loadManga(mangaTitle) {
    fetch(`/manga/${mangaTitle}`)
        .then(response => response.json())
        .then(data => {
            images = data;
            currentPage = 0;
            showImage();
            document.getElementById('manga-list').style.display = 'none';
            document.getElementById('manga-reader').style.display = 'block';
        });
}

function showImage() {
    if (images.length > 0) {
        document.getElementById("manga-image").src = images[currentPage];
    }
}

document.addEventListener('keydown', (event) => {
    if (event.key === "ArrowRight") {
        currentPage = (currentPage + 1) % images.length; // sağ ok
        showImage();
    } else if (event.key === "ArrowLeft") {
        currentPage = (currentPage - 1 + images.length) % images.length; // sol ok
        showImage();
    }
});

// Sayfa yüklendiğinde manga listesini yükle
window.onload = loadMangaList;
