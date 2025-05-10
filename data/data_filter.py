import os
import pandas as pd
from PIL import Image
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np


dataset_path = "C:/Users/38978/Downloads/archive/sample_0/sample_0_venom_nonvenom.csv"

# Load the entire dataset
full_dataset = pd.read_csv(dataset_path)

# Specify the number of train and test samples you want
num_train_samples = 5000
num_test_samples = 1000

# Get the indices for the random subset of samples
all_indices = np.arange(len(full_dataset))
train_indices = np.random.choice(all_indices, size=num_train_samples, replace=False)
test_indices = np.setdiff1d(all_indices, train_indices, assume_unique=True)[:num_test_samples]

# Create train and test datasets
train_dataset = full_dataset.iloc[train_indices]
test_dataset = full_dataset.iloc[test_indices]

# Save train and test datasets to CSV
train_dataset.to_csv("C:/Users/38978/Downloads/train_dataset.csv", index=False)
test_dataset.to_csv("C:/Users/38978/Downloads/test_dataset.csv", index=False)

if __name__ == '__main__':
    print(len(train_dataset))