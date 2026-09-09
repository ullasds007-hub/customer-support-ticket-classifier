import pandas as pd
import re
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "customer_support_tickets.csv"
PROCESSED_FILE = BASE_DIR / "data" / "processed" / "cleaned_tickets.csv"

# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(RAW_FILE)

print("Original dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

# --------------------------------------------------
# 3. Keep only required columns
# --------------------------------------------------

required_columns = [
    "Ticket Subject",
    "Ticket Description",
    "Ticket Type",
    "Ticket Priority"
]

df = df[required_columns].copy()

# --------------------------------------------------
# 4. Remove rows with missing important values
# --------------------------------------------------

df = df.dropna(
    subset=[
        "Ticket Subject",
        "Ticket Description",
        "Ticket Type",
        "Ticket Priority"
    ]
)

# --------------------------------------------------
# 5. Combine subject + description
# --------------------------------------------------

df["text"] = (
    df["Ticket Subject"].astype(str)
    + " "
    + df["Ticket Description"].astype(str)
)

# --------------------------------------------------
# 6. Text cleaning function
# --------------------------------------------------

def clean_text(text):
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Keep letters and spaces only
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


df["clean_text"] = df["text"].apply(clean_text)

# --------------------------------------------------
# 7. Convert priority into task-required classes
# --------------------------------------------------

priority_mapping = {
    "Critical": "High",
    "High": "High",
    "Medium": "Medium",
    "Low": "Low"
}

df["priority"] = df["Ticket Priority"].map(priority_mapping)

# Rename category column
df["category"] = df["Ticket Type"]

# --------------------------------------------------
# 8. Remove empty cleaned text
# --------------------------------------------------

df = df[df["clean_text"].str.len() > 0]

# --------------------------------------------------
# 9. Remove duplicate ticket texts
# --------------------------------------------------

df = df.drop_duplicates(subset=["clean_text"])

# --------------------------------------------------
# 10. Keep final useful columns
# --------------------------------------------------

final_df = df[
    [
        "clean_text",
        "category",
        "priority"
    ]
].copy()

# --------------------------------------------------
# 11. Save processed dataset
# --------------------------------------------------

PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

final_df.to_csv(PROCESSED_FILE, index=False)

# --------------------------------------------------
# 12. Show results
# --------------------------------------------------

print("\nCleaned dataset shape:", final_df.shape)

print("\nCategory counts:")
print(final_df["category"].value_counts())

print("\nPriority counts:")
print(final_df["priority"].value_counts())

print("\nCleaned dataset saved to:")
print(PROCESSED_FILE)