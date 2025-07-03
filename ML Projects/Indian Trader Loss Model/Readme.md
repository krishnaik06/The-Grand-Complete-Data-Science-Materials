
# 📊 Indian Trader Loss Prediction Model

A beginner-friendly regression model built using **scikit-learn** to predict the **loss percentage** faced by Indian retail investors, based on their investment behavior, platform choices, and emotional responses. This notebook is part of a learning project and uses a **synthetic dataset** that mimics real-world trading behavior among Indian investors.

---

## 🚀 Project Highlights

* 📁 Dataset: [Indian Trader Loss Dataset](https://www.kaggle.com/datasets/) (synthetic, 300 samples)
* ⚙️ Model: `GradientBoostingRegressor` via scikit-learn
* 🔄 Pipeline: Preprocessing (Ordinal + OneHot Encoding) + Regression
* 🎯 Target: `Loss_Percentage` (continuous output)
* 🧠 Use case: Behavioral finance, risk profiling, investor education

---

## 📥 Features Used

| Feature                      | Type        | Description                             |
| ---------------------------- | ----------- | --------------------------------------- |
| `Age_Group`                  | Ordinal     | Age bracket of the trader               |
| `Investment_Type`            | Categorical | Type of investment (e.g. Stock, Crypto) |
| `Investment_Amount_INR`      | Numeric     | Amount invested in INR                  |
| `Holding_Period`             | Ordinal     | Duration for which asset was held       |
| `Platform_Used`              | Categorical | Trading platform used (e.g. Zerodha)    |
| `Source_of_Advice`           | Categorical | Source of investment recommendation     |
| `Reason_for_Loss`            | Categorical | User-reported reason for loss           |
| `Recovery_Action`            | Categorical | What action was taken after the loss    |
| `Emotional_State_After_Loss` | Categorical | Self-assessed state after facing a loss |
| `Loss_Year`                  | Numeric     | Year the loss occurred                  |

---

## 🧪 Model Performance

* **Mean Absolute Error (MAE):** \~20%
* **R² Score:** Negative (indicates room for improvement on small dataset)

> Note: This is a **baseline educational model**, and performance can improve with tuning and real-world data.

---

## 💡 Example Usage

```python
sample_input = {
    "Age_Group": "20-30",
    "Investment_Type": "Crypto",
    "Investment_Amount_INR": 50000,
    "Holding_Period": "1-3 Months",
    "Platform_Used": "WazirX",
    "Source_of_Advice": "YouTube Influencer",
    "Reason_for_Loss": "High Volatility",
    "Recovery_Action": "Invested Again",
    "Emotional_State_After_Loss": "Anxious",
    "Loss_Year": 2023
}

# Preprocess and predict
predicted_loss = model.predict(pd.DataFrame([sample_input]))
print(f"Predicted Loss Percentage: {predicted_loss[0]:.2f}%")
```

---

## 📌 Use Cases

* 🧠 Behavioral finance research
* 📈 Retail trader profiling tools
* 🎓 Educational ML demos for finance domain
* 🔄 Risk estimation tools for trading apps

---

## 🧰 Requirements

```bash
pip install pandas scikit-learn numpy
```

---

## ⚖️ License

This project uses **synthetic, non-sensitive data** and is open for learning, experimentation, and portfolio showcase. Attribution appreciated if reused.


