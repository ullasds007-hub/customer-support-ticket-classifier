from flask import Flask, request, jsonify, render_template
from pathlib import Path
import joblib
import sys

# --------------------------------------------------
# 1. Setup paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "models" / "best_category_model.pkl"

sys.path.append(str(BASE_DIR / "src"))

from priority_rules import assign_priority

# --------------------------------------------------
# 2. Create Flask app
# --------------------------------------------------

app = Flask(__name__)

# --------------------------------------------------
# 3. Load trained model
# --------------------------------------------------

model = joblib.load(MODEL_FILE)

# --------------------------------------------------
# 4. Frontend page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")

# --------------------------------------------------
# 5. Analyze ticket API
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze_ticket():
    data = request.get_json()

    if not data or "ticket" not in data:
        return jsonify({
            "error": "Ticket text is required"
        }), 400

    ticket_text = data["ticket"].strip()

    if not ticket_text:
        return jsonify({
            "error": "Ticket text cannot be empty"
        }), 400

    category = model.predict([ticket_text])[0]
    priority = assign_priority(ticket_text)

    return jsonify({
        "ticket": ticket_text,
        "category": category,
        "priority": priority
    })

# --------------------------------------------------
# 6. Run server
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)