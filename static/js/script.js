 // JavaScript untuk mengendalikan kamera dan input
 const startBtn = document.getElementById('startBtn');
 const stopBtn = document.getElementById('stopBtn');
 const video = document.getElementById('video');
 const textInput = document.getElementById('textInput');
 
 let mediaStream;

 // Mulai Kamera
 startBtn.addEventListener('click', () => {
     navigator.mediaDevices.getUserMedia({ video: true })
         .then((stream) => {
             mediaStream = stream;
             video.srcObject = stream;
             startBtn.disabled = true;
             stopBtn.disabled = false;
         })
         .catch((error) => {
             console.error("Kamera tidak dapat diakses: ", error);
         });
 });

 // Stop Kamera
 stopBtn.addEventListener('click', () => {
     if (mediaStream) {
         let tracks = mediaStream.getTracks();
         tracks.forEach(track => track.stop());
         video.srcObject = null;
     }
     startBtn.disabled = false;
     stopBtn.disabled = true;
 });