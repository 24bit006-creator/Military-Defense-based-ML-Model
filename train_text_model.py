import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = os.path.join("dataset", "dispatches.csv")
MODEL_PATH = os.path.join("models", "text_threat_pipeline.pkl")

def train():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    print(f"[*] Loading tactical dispatch dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # Map classes: 1 for hostile, 0 for routine
    df['label'] = df['category'].str.strip().str.lower().map({'hostile': 1, 'routine': 0})
    df.dropna(subset=['label'], inplace=True)
    df['label'] = df['label'].astype(int)

    print(f"[*] Total Dispatches: {len(df)} | Hostile: {(df['label'] == 1).sum()} | Routine: {(df['label'] == 0).sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label'], test_size=0.25, random_state=42, stratify=df['label']
    )

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
    ])

    print("[*] Training Tactical Dispatch Classifier...")
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"[+] Text Model Accuracy on evaluation split: {acc * 100:.2f}%")
    print(classification_report(y_test, preds, target_names=["Routine (0)", "Hostile (1)"]))

    os.makedirs("models", exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"[+] Saved model pipeline to: {MODEL_PATH}")

if __name__ == "__main__":
    train()
