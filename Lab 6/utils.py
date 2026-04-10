import os
import pandas as pd
from sklearn.model_selection import train_test_split

def load_disaster_dataset():
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "disaster_tweets.csv")
    
    # Download dataset if it doesn't exist
    if not os.path.exists(csv_path):
        print("Downloading Disaster Tweets dataset...")
        url = "https://raw.githubusercontent.com/sugatagh/Natural-Language-Processing-with-Disaster-Tweets/main/train.csv"
        df = pd.read_csv(url)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)
        
    # We only need the text and the target label
    df = df[['text', 'target']].rename(columns={'target': 'label'})
    
    # Split the data for training and testing
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    df_valid, df_test = train_test_split(df_test, test_size=0.5, random_state=42)
    
    # Hide the labels in the training set so Snorkel has to guess them
    df_train_unlabeled = df_train.copy()
    df_train_unlabeled['label'] = -1 
    
    return df_train_unlabeled, df_valid, df_test, df_train