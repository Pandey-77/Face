# Real-time Face Blur Webcam Application

A Python-based web application that uses webcam access to detect and blur faces in real-time for privacy protection.

## Features

- **Real-time face detection** using OpenCV's Haar Cascade classifiers
- **Automatic face blurring** with adjustable blur strength
- **Modern web interface** with responsive design
- **Privacy-focused** - all processing happens locally
- **Cross-platform** - works on Windows, macOS, and Linux

## Requirements

- Python 3.7+
- Webcam access
- Modern web browser with WebRTC support

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Click "Start Camera" to begin webcam access
2. Grant camera permissions when prompted
3. The application will automatically detect faces and blur them
4. Adjust the blur strength using the slider
5. Click "Stop Camera" to end the session

## How It Works

1. **Frontend**: HTML5 video captures webcam feed
2. **Processing**: JavaScript sends frames to Python backend
3. **Detection**: OpenCV detects faces using Haar Cascade classifiers
4. **Blurring**: Gaussian blur is applied to detected face regions
5. **Display**: Processed frames are sent back and displayed in real-time

## Technical Details

- **Face Detection**: Uses OpenCV's pre-trained Haar Cascade classifier
- **Blur Effect**: Gaussian blur with adjustable kernel size
- **Frame Rate**: ~15 FPS for optimal performance
- **Image Format**: JPEG with 85% quality for efficient transmission

## Privacy

- All processing happens locally on your machine
- No data is sent to external servers
- Camera feed is not recorded or stored
- Face detection data is not saved

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Troubleshooting

**Camera not working?**
- Ensure camera permissions are granted
- Check if another application is using the camera
- Try refreshing the page

**Poor performance?**
- Close other applications using the camera
- Reduce browser window size
- Lower the blur strength setting

**No faces detected?**
- Ensure good lighting
- Face the camera directly
- Move closer to the camera