# Brain_tumor_detection

1. Abstract
Brain tumors are life-threatening and require accurate early diagnosis. This project leverages deep learning—specifically a VGG16-based Convolutional Neural Network—to classify brain tumors using MRI scans. A Flask-based web interface allows users to upload MRI images and receive real-time predictions with high confidence levels. Additional features include user authentication, a responsive dashboard, and model interpretability through visual reports.

2. Introduction
Medical imaging and AI have recently emerged as powerful allies in disease diagnosis. Brain tumors, if not detected early, can be fatal. Traditional diagnosis methods involve manual analysis of MRI scans, which is time-consuming and subjective. Our system automates this process using a CNN-based deep learning model and provides an intuitive frontend for interaction.

3. Objective
To design and train a robust CNN model for tumor classification.

To develop a secure web app for image upload and tumor prediction.

To allow users to interact with the system through login/signup authentication.

To present results with accuracy and confidence score for clinical use.

4. System Architecture
graphql
Copy
Edit


         ┌──────────────┐       ┌────────────┐
         │   MRI Image  │       │Login/Signup│
         └──────┬───────┘       └─────┬─────┘
                │                     │
                ▼                     ▼
         ┌────────────────────────────────┐
         │ Flask Web Interface (Frontend) │
         └────────────┬───────────────────┘
                      ▼
         ┌───────────────────────────────┐
         │  Pre-trained VGG16 CNN Model  │
         └────────────┬──────────────────┘
                      ▼
         ┌───────────────────────────────┐
         │  Output: Tumor Type + Score   │
         └───────────────────────────────┘

   
6. Technologies Used
Languages: Python, HTML, CSS

Frameworks: Flask, Keras, TensorFlow

Libraries: Pillow, Numpy, Matplotlib, Scikit-learn

Tools: Google Colab, VS Code, SQLite

Model: Pre-trained VGG16 with custom classification head

6. Dataset
Source: Kaggle/Open Access MRI Brain Tumor Dataset

Classes: glioma, pituitary, meningioma, notumor

Images: >3,000 images categorized across train/test

Preprocessing:

Resizing to 128x128

Augmentation: Brightness, contrast changes

Normalization: [0, 1] pixel scaling

7. Model Training
Base Model: VGG16 (ImageNet weights)

Modifications:

Flatten + Dense + Dropout layers

Fine-tuned last 3 convolutional layers

Loss Function: Sparse Categorical Crossentropy

Optimizer: Adam (lr = 0.0001)

Metrics: Accuracy, ROC AUC

Evaluation:

Classification Report

Confusion Matrix

ROC Curve

8. Web Application Features
Login/Signup Authentication

Image Upload Portal

Live Tumor Detection with Confidence Score

User-friendly Result Visualization

Secure File Storage in uploads/ Folder

9. Folder Structure
csharp
Copy
Edit
Brain_Tumor_Detection/

├── app.py                                        # Main Flask app

├── create_db.py                                 # Initialize user DB

├── models/                                     # Saved VGG16 model

├── templates/                                  # HTML templates

├── static/                                    # CSS/JS (optional)

├── uploads/                                  # Uploaded images

├── users.db                                 # SQLite DB

├── model_training.ipynb                    # Training notebook

11. Screenshots

📌 Include screenshots of:

Login/signup interface:

![image alt](https://github.com/Anibrata-Ghatak/Brain_tumor_detection/blob/main/Screenshot%202025-06-13%20161507.png)

![image alt](https://github.com/Anibrata-Ghatak/Brain_tumor_detection/blob/main/Screenshot%202025-06-13%20161630.png)

Image upload page

![image alt](https://github.com/Anibrata-Ghatak/Brain_tumor_detection/blob/main/Screenshot%202025-06-13%20161525.png)

Prediction output

![image alt](https://github.com/Anibrata-Ghatak/Brain_tumor_detection/blob/main/Screenshot%202025-06-13%20161609.png)

11. Conclusion
The proposed system effectively automates the diagnosis of brain tumors with promising accuracy using deep learning. It provides a practical interface that could be extended for use by radiologists or as a patient-side tool. Future enhancements could include PDF reports, history tracking, and integration with hospital systems.

12. Future Scope
Integration with hospital PACS systems.

Deploy on cloud (Heroku, AWS, GCP).

Add heatmap visualizations (Grad-CAM).

Implement patient record management.

13. References
https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset

https://keras.io

https://flask.palletsprojects.com

Research papers on brain tumor classification using CNNs
