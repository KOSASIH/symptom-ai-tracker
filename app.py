from flask import Flask, render_template, request, jsonify
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor
from PIL import Image
import io
import base64

app = Flask(__name__)

# Configuration
MODEL_ID = "Bio-Medical-MultiModal-Llama-3-8B-V1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Create directories for uploads
os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'uploads'), exist_ok=True)

# Initialize model and tokenizer
try:
    print(f"Attempting to load model {MODEL_ID}...")
    # For demo purposes, we'll use a fallback approach since we might not have the actual model
    # In a real implementation, you would use:
    # tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    # model = AutoModelForCausalLM.from_pretrained(MODEL_ID).to(DEVICE)
    # processor = AutoProcessor.from_pretrained(MODEL_ID)
    
    # For now, we'll set these to None to use our demo mode
    model = None
    tokenizer = None
    processor = None
    print(f"Using demo mode (model not available)")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    tokenizer = None
    processor = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get text input
        text_input = request.form.get('symptoms', '')
        
        # Get image if provided
        image = None
        image_path = None
        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            image = Image.open(image_file)
            
            # Save the image
            image_filename = f"upload_{os.urandom(8).hex()}.jpg"
            image_path = os.path.join('static', 'uploads', image_filename)
            image.save(os.path.join(os.path.dirname(__file__), image_path))
        
        # Get biometric data
        heart_rate = request.form.get('heart_rate', '')
        blood_pressure = request.form.get('blood_pressure', '')
        temperature = request.form.get('temperature', '')
        
        # Combine all inputs
        prompt = f"Patient symptoms: {text_input}\n"
        if heart_rate:
            prompt += f"Heart rate: {heart_rate} bpm\n"
        if blood_pressure:
            prompt += f"Blood pressure: {blood_pressure} mmHg\n"
        if temperature:
            prompt += f"Body temperature: {temperature} °C\n"
        
        # If model is loaded, use it for prediction
        if model and tokenizer:
            if image:
                # Process multimodal input (text + image)
                inputs = processor(text=prompt, images=image, return_tensors="pt").to(DEVICE)
                output = model.generate(**inputs, max_length=500)
                result = processor.decode(output[0], skip_special_tokens=True)
            else:
                # Process text-only input
                inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
                output = model.generate(**inputs, max_length=500)
                result = tokenizer.decode(output[0], skip_special_tokens=True)
        else:
            # Demo response for testing
            result = generate_demo_diagnosis(text_input, heart_rate, blood_pressure, temperature, image is not None)
        
        return jsonify({
            'diagnosis': result,
            'input_data': {
                'symptoms': text_input,
                'heart_rate': heart_rate,
                'blood_pressure': blood_pressure,
                'temperature': temperature,
                'image_provided': image is not None,
                'image_path': image_path
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_demo_diagnosis(symptoms, heart_rate, blood_pressure, temperature, has_image):
    """Generate a demo diagnosis for testing purposes"""
    
    # Simple keyword matching for demo purposes
    keywords = {
        'headache': 'Your headache symptoms could be related to tension headaches, migraines, or sinus issues. ',
        'fever': 'The presence of fever suggests your body is fighting an infection. ',
        'cough': 'Your cough could be due to a respiratory infection, allergies, or irritation. ',
        'rash': 'The skin rash might indicate an allergic reaction, infection, or autoimmune condition. ',
        'fatigue': 'Fatigue can be caused by various factors including stress, poor sleep, anemia, or viral infections. ',
        'pain': 'The pain you\'re experiencing could be related to inflammation, injury, or underlying medical conditions. ',
        'nausea': 'Nausea can be caused by digestive issues, infections, or medication side effects. ',
        'dizziness': 'Dizziness might be related to inner ear problems, low blood pressure, or dehydration. '
    }
    
    # Start with a general response
    response = "Based on the information provided, here's my assessment:\n\n"
    
    # Add specific responses based on symptoms
    matched = False
    for keyword, explanation in keywords.items():
        if keyword.lower() in symptoms.lower():
            response += explanation
            matched = True
    
    if not matched:
        response += "Your symptoms require further evaluation to determine a specific cause. "
    
    # Add biometric data analysis
    if heart_rate:
        try:
            hr = float(heart_rate)
            if hr > 100:
                response += "Your heart rate is elevated, which could indicate stress, anxiety, or infection. "
            elif hr < 60:
                response += "Your heart rate is lower than average, which could be normal for athletes or indicate certain conditions. "
            else:
                response += "Your heart rate is within normal range. "
        except:
            pass
    
    if temperature:
        try:
            temp = float(temperature)
            if temp > 38:
                response += "You have a fever, which is often a sign that your body is fighting an infection. "
            elif temp > 37.5:
                response += "You have a slight elevation in temperature, which could be the beginning of a fever. "
            else:
                response += "Your body temperature is within normal range. "
        except:
            pass
    
    if blood_pressure:
        response += "Your blood pressure reading has been noted in the assessment. "
    
    if has_image:
        response += "The image you provided has been analyzed as part of this assessment. "
    
    # Add possible diagnoses
    response += "\n\nPossible conditions to consider based on your symptoms include:\n"
    
    if 'headache' in symptoms.lower() and 'fever' in symptoms.lower():
        response += "- Viral infection (such as influenza)\n- COVID-19\n- Sinusitis\n"
    elif 'cough' in symptoms.lower() and 'fever' in symptoms.lower():
        response += "- Bronchitis\n- Pneumonia\n- COVID-19\n- Common cold\n"
    elif 'rash' in symptoms.lower():
        response += "- Allergic reaction\n- Eczema\n- Contact dermatitis\n- Viral exanthem\n"
    else:
        response += "- Common cold\n- Seasonal allergies\n- Stress-related condition\n- Viral infection\n"
    
    # Add disclaimer
    response += "\n\nIMPORTANT: This is a simulated AI assessment for demonstration purposes only. " \
               "It is not a medical diagnosis. Please consult with a qualified healthcare professional " \
               "for proper evaluation, diagnosis, and treatment of your condition."
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)