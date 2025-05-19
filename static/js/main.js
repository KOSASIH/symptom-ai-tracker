// SymptomAI Tracker - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const symptomForm = document.getElementById('symptom-form');
    const loadingIndicator = document.querySelector('.loading');
    const resultContainer = document.getElementById('result-container');
    const diagnosisResult = document.getElementById('diagnosis-result');
    
    // Handle form submission
    symptomForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading indicator
        loadingIndicator.style.display = 'block';
        resultContainer.style.display = 'none';
        
        // Create form data
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Format the diagnosis text with line breaks
                const formattedDiagnosis = data.diagnosis.replace(/\n/g, '<br>');
                
                // Display the results
                diagnosisResult.innerHTML = `
                    <div class="alert alert-info">
                        <p><strong>AI Assessment:</strong></p>
                        <p>${formattedDiagnosis}</p>
                    </div>
                    <div class="disclaimer">
                        <p>Note: This is an AI-generated assessment and should not replace professional medical advice. 
                        Please consult with a healthcare provider for proper diagnosis and treatment.</p>
                    </div>
                `;
                
                // If an image was provided and processed, show it
                if (data.input_data.image_path) {
                    diagnosisResult.innerHTML += `
                        <div class="mt-3">
                            <p><strong>Uploaded Image:</strong></p>
                            <img src="/${data.input_data.image_path}" alt="Uploaded medical image" class="img-fluid" style="max-height: 300px;">
                        </div>
                    `;
                }
                
                resultContainer.style.display = 'block';
                
                // Scroll to results
                resultContainer.scrollIntoView({ behavior: 'smooth' });
            } else {
                throw new Error(data.error || 'An error occurred during analysis');
            }
        } catch (error) {
            diagnosisResult.innerHTML = `
                <div class="alert alert-danger">
                    <p>Error: ${error.message}</p>
                </div>
            `;
            resultContainer.style.display = 'block';
        } finally {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
        }
    });
    
    // Preview image before upload
    const imageInput = document.getElementById('image');
    const imagePreviewContainer = document.createElement('div');
    imagePreviewContainer.className = 'mt-2 image-preview';
    imagePreviewContainer.style.display = 'none';
    
    // Insert the preview container after the image input
    imageInput.parentNode.insertBefore(imagePreviewContainer, imageInput.nextSibling);
    
    imageInput.addEventListener('change', function() {
        imagePreviewContainer.innerHTML = '';
        imagePreviewContainer.style.display = 'none';
        
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                imagePreviewContainer.innerHTML = `
                    <p>Image Preview:</p>
                    <img src="${e.target.result}" alt="Preview" class="img-thumbnail" style="max-height: 200px;">
                `;
                imagePreviewContainer.style.display = 'block';
            };
            
            reader.readAsDataURL(this.files[0]);
        }
    });
});