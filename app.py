from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import threading
import time

app = Flask(__name__)

class FaceBlurProcessor:
    def __init__(self):
        # Load the face detection classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.blur_strength = 15
        
    def detect_and_blur_faces(self, frame):
        """Detect faces in the frame and apply blur effect"""
        try:
            # Convert frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Apply blur to each detected face
            for (x, y, w, h) in faces:
                # Extract face region
                face_region = frame[y:y+h, x:x+w]
                
                # Apply Gaussian blur
                blurred_face = cv2.GaussianBlur(face_region, (self.blur_strength, self.blur_strength), 0)
                
                # Replace the face region with blurred version
                frame[y:y+h, x:x+w] = blurred_face
                
                # Optional: Draw rectangle around detected face (for debugging)
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            return frame, len(faces)
            
        except Exception as e:
            print(f"Error in face detection: {e}")
            return frame, 0

# Global processor instance
processor = FaceBlurProcessor()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Process a single frame from the webcam"""
    try:
        from flask import request
        
        # Get the image data from the request
        data = request.get_json()
        image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Convert PIL image to OpenCV format
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Process the frame
        processed_frame, face_count = processor.detect_and_blur_faces(frame)
        
        # Convert back to RGB for web display
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(processed_frame)
        
        # Convert to base64
        buffer = BytesIO()
        pil_image.save(buffer, format='JPEG', quality=85)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'image': f'data:image/jpeg;base64,{img_str}',
            'faces_detected': face_count
        })
        
    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/set_blur', methods=['POST'])
def set_blur():
    """Adjust blur strength"""
    try:
        from flask import request
        data = request.get_json()
        blur_value = int(data.get('blur', 15))
        
        # Ensure blur value is odd and within reasonable range
        blur_value = max(1, min(51, blur_value))
        if blur_value % 2 == 0:
            blur_value += 1
            
        processor.blur_strength = blur_value
        
        return jsonify({'success': True, 'blur_strength': blur_value})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)