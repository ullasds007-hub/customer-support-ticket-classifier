import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CM_FILE = BASE_DIR / "results" / "category_confusion_matrix.csv"
OUTPUT_FILE = BASE_DIR / "results" / "category_confusion_matrix.png"

# --------------------------------------------------
# 2. Load confusion matrix
# --------------------------------------------------

cm_df = pd.read_csv(CM_FILE, index_col=0)

labels = cm_df.columns.tolist()
cm = cm_df.values

# --------------------------------------------------
# 3. Create plot
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 8))

image = ax.imshow(cm)

ax.set_title("Support Ticket Category Confusion Matrix")
ax.set_xlabel("Predicted Category")
ax.set_ylabel("Actual Category")

ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))

ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_yticklabels(labels)

# Show numbers inside each cell
for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )

fig.colorbar(image)

plt.tight_layout()

# --------------------------------------------------
# 4. Save image
# --------------------------------------------------

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

print("Confusion matrix image saved to:")
print(OUTPUT_FILE)

plt.show()