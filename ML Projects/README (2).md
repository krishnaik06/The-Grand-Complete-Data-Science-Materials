# 🧠 Stroke Risk Prediction using Machine Learning

### 📊 EDA | ⚖️ SMOTE | 🤖 Model Comparison (90% Accuracy)

---

## 📌 Overview

Stroke is one of the leading causes of death and disability worldwide. Early prediction can significantly improve patient outcomes.

This project builds a **machine learning pipeline** to predict the likelihood of stroke using healthcare data such as age, glucose level, BMI, and medical history.

It includes **data preprocessing, exploratory data analysis (EDA), class imbalance handling using SMOTE, and comparison of multiple ML models**.

---

## 🎯 Objectives

* Perform **Exploratory Data Analysis (EDA)** to understand patterns
* Identify **key factors influencing stroke risk**
* Handle **imbalanced dataset using SMOTE**
* Train and compare multiple **machine learning models**
* Evaluate performance and generate **actionable insights**

---

## 📂 Dataset

* Source: Kaggle Stroke Prediction Dataset
* Total Records: **5110** 
* Features include:

  * Age
  * Gender
  * Hypertension
  * Heart Disease
  * Average Glucose Level
  * BMI
  * Smoking Status
  * Work Type
  * Residence Type

---

## 🔍 Exploratory Data Analysis (EDA)

Key visualizations performed:

* Age vs Stroke relationship
* Glucose level distribution
* BMI distribution
* Work type vs stroke
* Smoking status impact
* Correlation heatmap

📊 Insights:

* Higher age increases stroke risk
* High glucose levels show strong correlation
* Heart disease & hypertension significantly impact stroke probability

---

## 🛠️ Data Preprocessing

* Handled missing values (BMI filled with median) 
* Dropped irrelevant columns (ID)
* Encoded categorical variables
* Applied **One-Hot Encoding**
* Feature scaling & transformation

---

## ⚖️ Handling Imbalanced Data

The dataset was highly imbalanced:

* Stroke cases were very low compared to non-stroke cases 

👉 Solution:

* Applied **SMOTE (Synthetic Minority Oversampling Technique)**
* Balanced dataset improved model learning

---

## 🤖 Machine Learning Models Used

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier
* XGBoost Classifier

---

## 📈 Model Performance

| Model               | Accuracy   |
| ------------------- | ---------- |
| Logistic Regression | ~84.5%     |
| Decision Tree       | ~88.1%     |
| Random Forest       | **~90.8%** |
| XGBoost             | **~90.7%** |

📌 Best Models:

* Random Forest
* XGBoost 

---

## 🧪 Sample Prediction

The system can predict:

* Stroke occurrence (0 or 1)
* Probability of stroke risk

Example output:

```
Random Forest → Stroke: 0, Probability: 0.03
XGBoost → Stroke: 0, Probability: 0.00
```

---

## 🚀 Key Achievements

✔ Built an **end-to-end ML pipeline**
✔ Successfully handled **class imbalance using SMOTE**
✔ Compared multiple models effectively
✔ Achieved **~90% accuracy**
✔ Generated **interpretable predictions**

---

## 🔮 Future Improvements

* Hyperparameter tuning for better performance
* Use larger real-world datasets
* Deploy using **Streamlit / Flask**
* Add more medical features for accuracy improvement 

---

## 🛠️ Tech Stack

* Python 🐍
* Pandas & NumPy
* Matplotlib & Seaborn
* Scikit-learn
* XGBoost
* Imbalanced-learn (SMOTE)

---

## 📁 Project Structure

```
├── data/
├── notebooks/
├── models/
├── README.md
```

---

## 📌 How to Run

```bash
# Clone the repository
git clone https://github.com/your-username/stroke-prediction-ml.git

# Navigate to project folder
cd stroke-prediction-ml

# Install dependencies
pip install -r requirements.txt

# Run notebook
jupyter notebook
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub and share your feedback!

---


* Optimize README for **recruiters (placement-focused)**
* Add **badges + GitHub profile branding** 🚀
