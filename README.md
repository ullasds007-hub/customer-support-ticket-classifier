# Support Ticket Classification & Prioritization

## Project Overview

This project was developed for Future Interns Machine Learning Task 2.

The goal is to build a system that can:

- Read customer/IT support ticket text
- Automatically classify tickets into categories
- Assign priority as High, Medium, or Low
- Evaluate the classification model using ML metrics
- Help support teams reduce manual ticket sorting

---

## Dataset

For category classification, the project uses the Future Interns recommended:

**IT Service Ticket Classification Dataset (Kaggle)**

The main dataset file used is:

`all_tickets_processed_improved_v3.csv`

Important columns:

- `Document` → ticket text
- `Topic_group` → ticket category

The dataset contains categories such as:

- Access
- Administrative rights
- HR Support
- Hardware
- Internal Project
- Miscellaneous
- Purchase
- Storage

---

## Model Approach

### Category Classification

Ticket text is converted into numerical features using:

**TF-IDF (Term Frequency - Inverse Document Frequency)**

The following models were compared:

- Linear SVM
- Logistic Regression
- Multinomial Naive Bayes

The best model was:

**Linear SVM**

Final performance:

- Accuracy: 85.78%
- Precision: 85.83%
- Recall: 85.78%
- Weighted F1 Score: 85.79%

---

## Priority Assignment

The selected category dataset does not contain priority labels.

Therefore, priority is assigned using a rule-based priority engine based on keywords and issue severity.

Examples:

- Server/system/network down → High
- Password reset/access request → Medium
- General informational requests → Low

Priority levels:

- High
- Medium
- Low

---

## System Workflow

```text
Support Ticket Text
        |
        +----------------------+
        |                      |
        v                      v
      TF-IDF             Priority Rules
        |                      |
        v                      v
    Linear SVM          High / Medium / Low
        |
        v
 Ticket Category