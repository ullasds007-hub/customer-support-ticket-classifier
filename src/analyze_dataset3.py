import pandas as pd
from pathlib import Path

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

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET3_DIR = BASE_DIR / "data" / "raw" / "dataset3"

X_TRAIN_FILE = DATASET3_DIR / "X_train.csv"
X_TEST_FILE = DATASET3_DIR / "X_test.csv"
Y_TRAIN_FILE = DATASET3_DIR / "y_train.csv"
Y_TEST_FILE = DATASET3_DIR / "y_test.csv"

# --------------------------------------------------
# 2. Load files
# --------------------------------------------------

X_train_df = pd.read_csv(X_TRAIN_FILE)
X_test_df = pd.read_csv(X_TEST_FILE)

y_train_df = pd.read_csv(Y_TRAIN_FILE)
y_test_df = pd.read_csv(Y_TEST_FILE)

print("X_train shape:", X_train_df.shape)
print("X_test shape :", X_test_df.shape)
print("y_train shape:", y_train_df.shape)
print("y_test shape :", y_test_df.shape)

# --------------------------------------------------
# 3. Merge using id
# --------------------------------------------------

train_df = X_train_df.merge(
    y_train_df,
    on="id",
    how="inner"
)

test_df = X_test_df.merge(
    y_test_df,
    on="id",
    how="inner"
)

print("\nMerged train shape:", train_df.shape)
print("Merged test shape :", test_df.shape)

# --------------------------------------------------
# 4. Remove missing values
# --------------------------------------------------

train_df = train_df.dropna(
    subset=["text", "category_truth"]
).copy()

test_df = test_df.dropna(
    subset=["text", "category_truth"]
).copy()

# --------------------------------------------------
# 5. Prepare train/test data
# --------------------------------------------------

X_train = train_df["text"].astype(str)
y_train = train_df["category_truth"].astype(str)

X_test = test_df["text"].astype(str)
y_test = test_df["category_truth"].astype(str)

print("\nNumber of categories:", y_train.nunique())

print("\nTraining category distribution:")
print(y_train.value_counts())

# --------------------------------------------------
# 6. Build TF-IDF + Linear SVM model
# --------------------------------------------------

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
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

# --------------------------------------------------
# 7. Train
# --------------------------------------------------

print("\nTraining Dataset 3 model...")

model.fit(X_train, y_train)

# --------------------------------------------------
# 8. Predict
# --------------------------------------------------

predictions = model.predict(X_test)

# --------------------------------------------------
# 9. Evaluate
# --------------------------------------------------

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
print("DATASET 3 RESULT")
print("=" * 60)

print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall   : {recall * 100:.2f}%")
print(f"F1 Score : {f1 * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

# --------------------------------------------------
# 10. Compare with Dataset 2
# --------------------------------------------------

dataset2_accuracy = 86.01

print("\n" + "=" * 60)
print("DATASET COMPARISON")
print("=" * 60)

print(f"Dataset 2 Accuracy : {dataset2_accuracy:.2f}%")
print(f"Dataset 3 Accuracy : {accuracy * 100:.2f}%")

if accuracy * 100 > dataset2_accuracy:
    print("\nDataset 3 currently performs better.")
elif accuracy * 100 < dataset2_accuracy:
    print("\nDataset 2 currently performs better.")
else:
    print("\nBoth datasets currently have the same accuracy.")