import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "all_tickets_processed_improved_v3.csv"
)

MODEL_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("Original dataset shape:", df.shape)

# Keep only useful columns
df = df[["Document", "Topic_group"]].copy()

# Remove missing rows
df = df.dropna()

# Remove duplicate ticket texts
df = df.drop_duplicates(subset=["Document"])

print("Cleaned dataset shape:", df.shape)

print("\nCategories:")
print(df["Topic_group"].value_counts())

# --------------------------------------------------
# 3. Input and target
# --------------------------------------------------

X = df["Document"].astype(str)
y = df["Topic_group"].astype(str)

# --------------------------------------------------
# 4. Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples :", len(X_test))

# --------------------------------------------------
# 5. Models
# --------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=3000,
        class_weight="balanced"
    ),

    "Linear SVM": LinearSVC(
        class_weight="balanced"
    ),

    "Naive Bayes": MultinomialNB()
}

results = []

best_model = None
best_model_name = None
best_f1 = -1
best_predictions = None

# --------------------------------------------------
# 6. Train all models
# --------------------------------------------------

for model_name, classifier in models.items():

    print("\n" + "=" * 60)
    print("Training:", model_name)
    print("=" * 60)

    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                max_features=40000,
                min_df=2,
                max_df=0.95,
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            classifier
        )
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

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

    print(f"Accuracy : {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall   : {recall * 100:.2f}%")
    print(f"F1 Score : {f1 * 100:.2f}%")

    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })

    if f1 > best_f1:
        best_f1 = f1
        best_model = pipeline
        best_model_name = model_name
        best_predictions = predictions

# --------------------------------------------------
# 7. Model comparison
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False
)

print("\n" + "=" * 60)
print("FINAL MODEL COMPARISON")
print("=" * 60)

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy": lambda x: f"{x * 100:.2f}%",
            "Precision": lambda x: f"{x * 100:.2f}%",
            "Recall": lambda x: f"{x * 100:.2f}%",
            "F1 Score": lambda x: f"{x * 100:.2f}%"
        }
    )
)

# --------------------------------------------------
# 8. Best model detailed report
# --------------------------------------------------

print("\nBest model:", best_model_name)
print(f"Best weighted F1 score: {best_f1 * 100:.2f}%")

report = classification_report(
    y_test,
    best_predictions,
    zero_division=0
)

print("\nClassification Report:")
print(report)

# --------------------------------------------------
# 9. Save best model
# --------------------------------------------------

MODEL_FILE = MODEL_DIR / "best_category_model.pkl"

joblib.dump(best_model, MODEL_FILE)

print("\nBest model saved to:")
print(MODEL_FILE)

# --------------------------------------------------
# 10. Save comparison results
# --------------------------------------------------

RESULTS_FILE = RESULTS_DIR / "category_model_comparison.csv"

results_df.to_csv(
    RESULTS_FILE,
    index=False
)

print("\nModel comparison saved to:")
print(RESULTS_FILE)

# --------------------------------------------------
# 11. Save classification report
# --------------------------------------------------

REPORT_FILE = RESULTS_DIR / "category_classification_report.txt"

with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write("BEST MODEL\n")
    file.write(best_model_name + "\n\n")

    file.write("WEIGHTED F1 SCORE\n")
    file.write(f"{best_f1 * 100:.2f}%\n\n")

    file.write("CLASSIFICATION REPORT\n")
    file.write(report)

print("\nClassification report saved to:")
print(REPORT_FILE)

# --------------------------------------------------
# 12. Save confusion matrix data
# --------------------------------------------------

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    best_predictions,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

CM_FILE = RESULTS_DIR / "category_confusion_matrix.csv"

cm_df.to_csv(CM_FILE)

print("\nConfusion matrix saved to:")
print(CM_FILE)