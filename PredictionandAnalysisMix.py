import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import uuid
import pickle
import seaborn as sns
from fpdf import FPDF
import csv
import re
from PredictionandAnalysisEnglish import visualizations, report

from sklearn.feature_extraction.text import TfidfVectorizer

# Generate a unique filename using uuid
unique_filename = str(uuid.uuid4())

def process_mix(filename):
    df=pd.read_csv(filename)
    scrapped_file_path =os.path.join('media','clean', unique_filename + '_clean'+ '.csv')
    df.to_csv(scrapped_file_path)
    visualizations(scrapped_file_path,unique_filename)
    feature_extraction_mix(scrapped_file_path)
    report(scrapped_file_path,unique_filename,'Mix (Urdu, Roman Urdu, English)')



def feature_extraction_mix(filename):
    df=pd.read_csv(filename)
    df['text'] = df['text'].fillna('')  # Replace np.nan with empty strings

    max_feature_num = 3000
    vectorizer = TfidfVectorizer(max_features=max_feature_num)
    vocab = vectorizer.fit(df.text)
    feature_extracted_data = TfidfVectorizer(max_features=max_feature_num, vocabulary=vectorizer.vocabulary_).fit_transform(df.text)
    # Loading model
    ensemble_model = pickle.load(open('media/models/ensemble_small.pkl','rb')) #give path of best model
    ensemble_model_pred=ensemble_model.predict(feature_extracted_data)
    
        # Count the occurrences of each class
    class_counts = np.bincount(ensemble_model_pred)

    # Calculate the percentage of each class
    total_samples = len(ensemble_model_pred)
    class_percentages = (class_counts / total_samples) * 100

    # Define the class labels for the x-axis
    class_labels = ['Class 0', 'Class 1']

    # Generate the x-axis indices based on the number of classes
    x_indices = np.arange(len(class_labels))

    # Create the bar plot
    plt.figure(figsize=(6,6))

    plt.bar(x_indices, class_counts, align='center')

    # Display the percentage of each class on the plot
    for i, count in enumerate(class_counts):
        plt.text(x_indices[i], count, f'{class_percentages[i]:.2f}%', ha='center', va='bottom')

    # Customize the plot
    plt.xticks(x_indices, class_labels)
    plt.xlabel('Predicted Classes')
    plt.ylabel('Count')
    plt.title('Bar Plot of Predicted Classes')
    image_path = os.path.join('media','report_images', unique_filename + '_BarPlot'+ '.png')
    plt.savefig(image_path)    
#feature_extraction_mix('media/scrapped/mix_small4.csv')