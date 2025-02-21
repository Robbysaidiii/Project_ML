from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Load model deteksi wajah dari OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Fungsi untuk menangkap video dan mendeteksi wajah
def generate_frames():
    camera = cv2.VideoCapture(0)  # 0 untuk kamera bawaan

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Konversi ke grayscale untuk deteksi wajah
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Gambar kotak merah di sekitar wajah
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Encode frame ke format JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Stream frame ke web
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route utama untuk tampilan web
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk streaming video
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
