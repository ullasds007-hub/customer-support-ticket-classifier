from pathlib import Path
import joblib

from priority_rules import assign_priority

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "best_category_model.pkl"

# --------------------------------------------------
# 2. Load trained category model
# --------------------------------------------------

model = joblib.load(MODEL_FILE)

print("Support Ticket Classifier")
print("-" * 40)

# --------------------------------------------------
# 3. Take ticket from user
# --------------------------------------------------

ticket_text = input("Enter support ticket: ").strip()

if not ticket_text:
    print("Ticket text cannot be empty.")
    raise SystemExit

# --------------------------------------------------
# 4. Predict category
# --------------------------------------------------

category = model.predict([ticket_text])[0]

# --------------------------------------------------
# 5. Assign priority
# --------------------------------------------------

priority = assign_priority(ticket_text)

# --------------------------------------------------
# 6. Display result
# --------------------------------------------------

print("\n" + "=" * 40)
print("TICKET ANALYSIS")
print("=" * 40)

print("Ticket   :", ticket_text)
print("Category :", category)
print("Priority :", priority)