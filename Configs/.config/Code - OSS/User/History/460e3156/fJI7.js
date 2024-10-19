const image = document.getElementById('cover'),
    title = document.getElementById('music-title'),
    artist = document.getElementById('music-artist'),
    currentTimeEl = document.getElementById('current-time'),
    durationEl = document.getElementById('duration'),
    progress = document.getElementById('progress'),
    playerProgress = document.getElementById('player-progress'),
    prevBtn = document.getElementById('prev'),
    nextBtn = document.getElementById('next'),
    playBtn = document.getElementById('play'),
    background = document.getElementById('bg-img'),
    searchInput = document.getElementById('search'),
    searchResults = document.getElementById('search-results');



    const darkLightBtn = document.querySelector('.dark-light');
    let isDarkMode = false; // Varsayılan olarak light mode
    
    darkLightBtn.addEventListener('click', () => {
        // Body'deki tema sınıfını değiştir
        document.body.classList.toggle('dark-mode');
        document.body.classList.toggle('light-mode');
        
        // Tema modunu değiştir
        isDarkMode = !isDarkMode;
    
        // İkonu değiştir
        if (isDarkMode) {
            darkLightBtn.classList.replace('fa-moon', 'fa-sun'); // Güneş ikonu
        } else {
            darkLightBtn.classList.replace('fa-sun', 'fa-moon'); // Ay ikonu
        }
    });
    
const music = new Audio();
const songs = [
    {
        path: '../static/assets/the-charmers-call.mp3',
        displayName: 'The Charmer\'s Call',
        cover: '../static/assets/the-charmers-call.jpg',
        artist: 'Hanu Dixit',
    },
    {
        path: '../static/assets/you-will-never-see-me-coming.mp3',
        displayName: 'You Will Never See Me Coming',
        cover: '../static/assets/you-will-never-see-me-coming.jpg',
        artist: 'NEFFEX',
    },
    {
        path: '../static/assets/intellect.mp3',
        displayName: 'Intellect',
        cover: '../static/assets/intellect.jpg',
        artist: 'Yung Logos',
    }
];

/*fetch('/get-songs')
    .then(response => response.json())
    .then(data => {
        songs = data;
        console.log(songs);
    })
    .catch(error => {
        console.error(error);
    })
*/


let musicIndex = 0;
let isPlaying = false;



searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    searchResults.innerHTML = '';

    // songs dizisinde döngü yap
    songs.forEach(song => {
        // Şarkının adı veya sanatçısı arama sorgusunu içeriyorsa
        if (song.displayName.toLowerCase().includes(query) || song.artist.toLowerCase().includes(query)) {
            // Uygun olanları listeye ekle
            const li = document.createElement('li');
            li.textContent = `${song.displayName} - ${song.artist}`; // Şarkı adı ve sanatçıyı göster
            li.addEventListener('click', () => { // Tıklandığında müziği yükle
                loadMusic(song);
                playMusic();
                searchResults.innerHTML = ''; // Sonuçları temizle
                searchInput.value = ''; // Arama inputunu temizle
                searchResults.style.display = 'none'; // Gizle
            });
            searchResults.appendChild(li); // Listeye ekle
        }
    });

    // Eğer arama kutusu boşsa sonuçları gizle
    if (query === '') {
        searchResults.style.display = 'none'; // Arama kutusu boşsa sonuçları gizle
    } else if (searchResults.children.length === 0) {
        searchResults.style.display = 'none'; // Eşleşme yoksa sonuçları gizle
    } else {
        searchResults.style.display = 'block'; // Eşleşme varsa göster
    }
});




function togglePlay() {
    if (isPlaying) {
        pauseMusic();
    } else {
        playMusic();
    }
}

function playMusic() {
    isPlaying = true;
    // Change play button icon
    playBtn.classList.replace('fa-play', 'fa-pause');
    // Set button hover title
    playBtn.setAttribute('title', 'Pause');
    music.play();
}

function pauseMusic() {
    isPlaying = false;
    // Change pause button icon
    playBtn.classList.replace('fa-pause', 'fa-play');
    // Set button hover title
    playBtn.setAttribute('title', 'Play');
    music.pause();
}

function loadMusic(song) {
    music.src = song.path;
    title.textContent = song.displayName;
    artist.textContent = song.artist;
    image.src = song.cover;
    background.src = song.cover;
}

function downloadMusic() {
    const link = document.createElement('a'); // Yeni bir bağlantı elementi oluştur
    link.href = music.src; // Müziğin kaynak yolunu ayarla
    link.download = songs[musicIndex].displayName + '.mp3'; // İndirme dosyasının ismini belirle
    document.body.appendChild(link); // Bağlantıyı belgeye ekle
    link.click(); // Bağlantıya tıkla
    document.body.removeChild(link); // Bağlantıyı belge üzerinden kaldır
}

document.getElementById('download').addEventListener('click', downloadMusic);

function changeMusic(direction) {
    musicIndex = (musicIndex + direction + songs.length) % songs.length;
    loadMusic(songs[musicIndex]);
    playMusic();
}

function updateProgressBar() {
    const { duration, currentTime } = music;
    const progressPercent = (currentTime / duration) * 100;
    progress.style.width = `${progressPercent}%`;

    const formatTime = (time) => String(Math.floor(time)).padStart(2, '0');
    durationEl.textContent = `${formatTime(duration / 60)}:${formatTime(duration % 60)}`;
    currentTimeEl.textContent = `${formatTime(currentTime / 60)}:${formatTime(currentTime % 60)}`;
}

function setProgressBar(e) {
    const width = playerProgress.clientWidth;
    const clickX = e.offsetX;
    music.currentTime = (clickX / width) * music.duration;
}

playBtn.addEventListener('click', togglePlay);
prevBtn.addEventListener('click', () => changeMusic(-1));
nextBtn.addEventListener('click', () => changeMusic(1));
music.addEventListener('ended', () => changeMusic(1));
music.addEventListener('timeupdate', updateProgressBar);
playerProgress.addEventListener('click', setProgressBar);

loadMusic(songs[musicIndex]);