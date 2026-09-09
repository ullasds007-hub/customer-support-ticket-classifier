import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "all_tickets_processed_improved_v3.csv"
)

df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

# Keep only required columns
df = df[["Document", "Topic_group"]].copy()

# Remove missing rows
df = df.dropna()

# Remove duplicate documents
df = df.drop_duplicates(subset=["Document"])

print("\nAfter cleaning:", df.shape)

print("\nNumber of categories:")
print(df["Topic_group"].nunique())

print("\nCategory distribution:")
print(df["Topic_group"].value_counts())

X = df["Document"].astype(str)
y = df["Topic_group"].astype(str)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=30000,
            min_df=2,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LinearSVC()
    )
])

print("\nTraining Linear SVM...")

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

precision = precision_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

print("\n" + "=" * 60)
print("DATASET 2 RESULT")
print("=" * 60)

print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall   : {recall * 100:.2f}%")
print(f"F1 Score : {f1 * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))