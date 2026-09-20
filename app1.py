from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from Find_your_fit import predict_size  # Import your prediction function


app = Flask(__name__)

@app.route('/')
def index():
    """Renders the HTML template for image capture and prediction."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles image upload, prediction, and returns the predicted size."""
    data = request.form
    image = data.get('image')
    print(f"File name: {image}") 
    if 'image' not in request.files:
        return jsonify({'error': 'No image'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

   
### Save the file and get the full path
##    upload_folder = os.path.join(app.root_path, 'uploads')
##    os.makedirs(upload_folder, exist_ok=True)  # Create the uploads directory if it doesn't exist
##    filename = file.filename
##    file_path = os.path.join(upload_folder, filename) 
##    file.save(file_path)
##
##    # Now you have the file path in the 'file_path' variable
##    print(f"File saved to: {file_path}") 
##    #file_path = './captured_image.jpg'  # Adjust path as needed
##    #file.save(file_path)
##
##    # Load the image using OpenCV
##    try:
##        img = cv2.imread(file_path) 
##    except Exception as e:
##        return jsonify({'error': f'Error loading image: {e}'}) 
##
##    # Predict the size using your model
##  
##    try:
##        predicted_size = predict_size(img)
##        return jsonify({'size': predicted_size}) 
##    except Exception as e:
##        return jsonify({'error': f'Error predicting size: {e}'})

    predicted_size = "Medium"  # Example
    return jsonify({'size': predicted_size})
##def result():
    """Renders the HTML template for image capture and prediction."""
    
   
    #return render_template('result.html', size=predicted_size) 


if __name__ == '__main__':
    app.run(debug=True)
