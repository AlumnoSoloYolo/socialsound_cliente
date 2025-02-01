function togglePlay(button) {
    const audioId = button.dataset.audioId;
    const audio = document.getElementById(`audio-${audioId}`);
    const icon = button.querySelector('i');

    if (audio.paused) {
        audio.play();
        icon.classList.replace('fa-play', 'fa-pause');
    } else {
        audio.pause();
        icon.classList.replace('fa-pause', 'fa-play');
    }
}

// Inicializar los reproductores
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.cyber-audio-player').forEach(player => {
        const audio = player.querySelector('audio');
        const progressBar = player.querySelector('.cyber-progress');
        const progressContainer = player.querySelector('.cyber-progress-container');
        const currentTimeDisplay = player.querySelector('.cyber-current-time');
        const durationDisplay = player.querySelector('.cyber-duration');
        const volumeProgress = player.querySelector('.cyber-volume-progress');
        const volumeContainer = player.querySelector('.cyber-volume-container');
        const volumeIcon = player.querySelector('.cyber-volume-icon');

        // Formatear tiempo
        function formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = Math.floor(seconds % 60);
            return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
        }

        // Actualizar progreso
        audio.addEventListener('timeupdate', () => {
            const progress = (audio.currentTime / audio.duration) * 100;
            progressBar.style.width = `${progress}%`;
            currentTimeDisplay.textContent = formatTime(audio.currentTime);
        });

        // Actualizar duración
        audio.addEventListener('loadedmetadata', () => {
            durationDisplay.textContent = formatTime(audio.duration);
        });

        // Click en la barra de progreso
        progressContainer.addEventListener('click', (e) => {
            const rect = progressContainer.getBoundingClientRect();
            const percent = (e.clientX - rect.left) / rect.width;
            audio.currentTime = percent * audio.duration;
        });

        // Control de volumen
        volumeContainer.addEventListener('click', (e) => {
            if (e.target === volumeIcon) {
                if (audio.volume > 0) {
                    audio.volume = 0;
                    volumeIcon.classList.replace('fa-volume-up', 'fa-volume-mute');
                    volumeProgress.style.width = '0%';
                } else {
                    audio.volume = 1;
                    volumeIcon.classList.replace('fa-volume-mute', 'fa-volume-up');
                    volumeProgress.style.width = '100%';
                }
            } else {
                const rect = volumeContainer.querySelector('.cyber-volume-slider').getBoundingClientRect();
                const percent = (e.clientX - rect.left) / rect.width;
                audio.volume = Math.max(0, Math.min(1, percent));
                volumeProgress.style.width = `${percent * 100}%`;
                volumeIcon.className = 'fas ' + (
                    audio.volume === 0 ? 'fa-volume-mute' :
                        audio.volume < 0.5 ? 'fa-volume-down' : 'fa-volume-up'
                );
            }
        });
    });
});