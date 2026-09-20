from flask import Flask, render_template, request, jsonify
import base64, os, time
from io import BytesIO
from PIL import Image
# Replace with your actual size prediction model
from Find_your_fit import predict_size 

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the HTML template for image capture and prediction."""
    return render_template('index.html')

UPLOAD_FOLDER = 'uploads'  # Path to save the uploaded images
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        #print(f"Data: {data}")
        image_data = data['imageData']
        #print(f"Image data: {image_data}")

        # Decode the base64 image data
        #image_bytes = base64.b64decode(image_data.split(',')[1])
        # Decode the base64 image data 
        image_bytes = base64.b64decode(image_data)
        # Try to open the image data with Pillow
        try:
            image = Image.open(BytesIO(image_bytes))
        except IOError:
            return jsonify({'error': 'Invalid image data format'}), 400 

        # Generate a unique filename
        filename = f"captured_image_{int(time.time())}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Save the image to the server
        image.save(filepath)

        return jsonify({'filename': filename}) 

    except Exception as e:
        print(f"Error during upload: {e}")
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        filename = data['filename']
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        
        print(f"File name: {filename}")
        print(f"Image Path: {image_path}")
                
        # Load the image
        #image = Image.open(image_path) 
        # Predict the size using your model
        predicted_size = predict_size(image_path) 

        return jsonify({'size': predicted_size})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

##@app.route('/result')
##def show_result():
##    predicted_size = request.args.get('size')
##    image_data = request.args.get('imageData')
##    return render_template('result.html', size=predicted_size, imageData=image_data)
##
if __name__ == '__main__':
    app.run(debug=True)
