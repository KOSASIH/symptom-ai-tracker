# SymptomAI Tracker

SymptomAI Tracker is a web application that uses multimodal data inputs (text, images, and biometrics) to assess symptoms and suggest potential diagnoses in real-time. It leverages the Bio-Medical-MultiModal-Llama-3-8B-V1 model for medical analysis.

## Features

- **Text-based Symptom Analysis**: Users can describe their symptoms in detail
- **Image Upload**: Supports uploading images of visible symptoms (rashes, injuries, etc.)
- **Biometric Data Integration**: Collects heart rate, blood pressure, and body temperature
- **Real-time Assessment**: Provides immediate analysis of symptoms and potential diagnoses
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **AI Model**: Bio-Medical-MultiModal-Llama-3-8B-V1 (based on Llama-3-8B-Instruct)
- **Image Processing**: PIL (Python Imaging Library)
- **Model Integration**: Hugging Face Transformers

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install flask transformers torch pillow
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Access the application at http://localhost:8080

## Usage

1. Enter your symptoms in the text area
2. Upload any relevant images (optional)
3. Enter biometric data (optional)
4. Click "Analyze Symptoms"
5. Review the AI-generated assessment

## Important Note

This application is for demonstration purposes only. The assessments provided should not be considered medical advice. Always consult with a qualified healthcare professional for proper diagnosis and treatment.

## Demo Mode

The application includes a demo mode that simulates AI responses when the actual model is not available. This allows for testing and demonstration without requiring the full model to be loaded.

## Project Structure

```
symptom_ai_tracker/
├── app.py                  # Main Flask application
├── templates/
│   └── index.html          # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css       # Custom CSS styles
│   ├── js/
│   │   └── main.js         # Frontend JavaScript
│   └── uploads/            # Directory for uploaded images
└── README.md               # Project documentation
```

## License

This project is for educational and demonstration purposes only.