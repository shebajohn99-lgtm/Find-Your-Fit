#!/usr/bin/env python
# coding: utf-8

# In[3]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from skimage import io, color, filters, feature
import os
import cv2, warnings
import numpy as np
import matplotlib.pyplot as plt

# --- Predict Dress Size for a New Image ---
def predict_size(new_image):
    image_folder = 'Front image'
    images, labels = load_and_preprocess_images(image_folder)

    # --- Encode Dress Sizes (Map labels to numerical values) ---
    le = LabelEncoder()
    y = le.fit_transform(labels)

    # --- Split Data into Training and Testing Sets ---
    X_train, X_test, y_train, y_test = train_test_split(images, y, test_size=0.2, random_state=42)

    # --- Create and Train the Model ---
    model = RandomForestClassifier(n_estimators=100, random_state=42) 
    model.fit(X_train, y_train)

    # --- Make Predictions ---
    y_pred = model.predict(X_test)

    # --- Evaluate Model Accuracy ---
    accuracy = accuracy_score(y_test, y_pred)
    #print("Accuracy:", accuracy)
    #new_image_path = "Front image/woman7.jpg"
    new_image_features = extract_features(new_image)
    print("New image:", new_image)
    print("New image features:", new_image_features)
    predicted_size = le.inverse_transform(model.predict([new_image_features]))[0]
    print("Predicted Dress Size:", predicted_size)
    return predicted_size

# --- Sample Data Preparation (Replace with your actual data) ---
# Assuming you have a list of image filenames and corresponding dress sizes
#image_filenames = ['image1.jpg', 'image2.jpg', 'image3.jpg', ...]
#dress_sizes = ['S', 'M', 'L', ...] 

# --- Feature Extraction using scikit-image ---
def extract_features(image_path):
    """
    Extracts features from an image using scikit-image.

    Args:
        image_path: Path to the image file.

    Returns:
        A NumPy array containing the extracted features.
    """
    img = io.imread(image_path) 
   
    img_gray = color.rgb2gray(img) 
    
    #features = []
# Suppress the warning (not recommended)
    warnings.filterwarnings("ignore", message="Applying `local_binary_pattern` to floating-point images")
    # Extract features (example: edges, local binary patterns)
    edges = filters.sobel(img_gray)
    lbp = feature.local_binary_pattern(img_gray, P=8, R=1, method='uniform') 
    
    # Calculate feature statistics (mean, standard deviation, etc.)
    edge_mean = np.mean(edges)
    edge_std = np.std(edges)
    lbp_hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 59 + 3), range=(0, 59)) 

    # Combine features into a single array
    features = np.array([edge_mean, edge_std])  # Create an array with edge_mean and edge_std
    features = np.concatenate((features, lbp_hist))  # Concatenate with lbp_hist
    return features

# --- Create Feature Vectors ---
# features = []
# for filename in image_filenames:
#     features.append(extract_features(filename))
# features = np.array(features)

# Function to load and preprocess images
def load_and_preprocess_images(image_folder):
    images = []
    labels = []
    
    for filename in os.listdir(image_folder):
        img_path = os.path.join(image_folder, filename)
        if is_hidden(img_path):
            print("hidden file")
        elif os.path.isfile(img_path) and not is_hidden(img_path):
            features = extract_features(img_path)
            label = classify_image_size(img_path)  # Use a simple classification rule or a pre-trained model
        
            images.append(features)
            labels.append(label)
    
    return np.array(images), np.array(labels)

# Skip hidden files
def is_hidden(file):
    return file.startswith('.')

# Classify images
def classify_image_size(image_path):
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    # Define size thresholds (adjust as needed)
    small_threshold = 300
    medium_threshold = 700
  
    if width < small_threshold:
        return "S"
    elif width < medium_threshold:
        return "M"
    else:
        return "L"

# image_folder = 'Front image'
# images, labels = load_and_preprocess_images(image_folder)

# # --- Encode Dress Sizes (Map labels to numerical values) ---
# le = LabelEncoder()
# y = le.fit_transform(labels)

# # --- Split Data into Training and Testing Sets ---
# X_train, X_test, y_train, y_test = train_test_split(images, y, test_size=0.2, random_state=42)

# # --- Create and Train the Model ---
# model = RandomForestClassifier(n_estimators=100, random_state=42) 
# model.fit(X_train, y_train)

# # --- Make Predictions ---
# y_pred = model.predict(X_test)

# # --- Evaluate Model Accuracy ---
# accuracy = accuracy_score(y_test, y_pred)
# #print("Accuracy:", accuracy)




# In[ ]:





# In[ ]:




