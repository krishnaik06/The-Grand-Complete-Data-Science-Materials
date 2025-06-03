GradientIQ is a Machine Learning project that evaluates factors such as study hours, tutoring, absences for a specific semester, parental support, extracurricular activities, and sports to deliver a comprehensive SGPA prediction. Beyond predictions, it offers visual insights and actionable feedback, empowering students to maximize their academic efforts. 📊

💡 Key Features:

High-Accuracy Predictions: Delivers SGPA insights with 95% accuracy.
Visual Analysis: Provides a pie chart of input data and a comparison graph showing recommended study time (min. 15 hours) vs. actual study time, helping students set study goals for success.# Student Performance Prediction System

## 🎯 Features

- **CGPA Prediction**: Accurate prediction using Gradient Boosting Regressor
- **Smart Penalty System**: Automatic CGPA adjustment based on attendance patterns
- **Interactive Visualizations**: 
  - Pie charts showing factor distribution
  - Bar charts comparing recommended vs actual study time
- **Personalized Suggestions**: Tailored recommendations based on input data
- **Grade Classification**: Automatic grade assignment (A+ to F)
- **Responsive Web Interface**: Clean, user-friendly design

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn, Gradient Boosting Regressor
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Model Persistence**: joblib
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker

## 📊 Model Details

- **Algorithm**: Gradient Boosting Regressor
- **Features**: Age, Gender, Parental Education, Study Time, Absences, Tutoring, Parental Support, Extracurricular Activities, Sports
- **Penalty System**: Reduces CGPA by 0.01 for every 15 absences
- **Performance Metrics**: Tracked via MAE, MSE, and R² score

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshhrawte/GradientIQ.git
   cd GradientIQ
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model** (if model.pkl doesn't exist)
   ```bash
   python trainmodel.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   ```
   Open your browser and navigate to http://localhost:5000
   ```

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t student-performance-app .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 student-performance-app
   ```

## 📁 Project Structure

```
student-performance-prediction/
│
├── app.py                 # Main Flask application
├── trainmodel.py          # Model training script
├── model.pkl              # Trained model (generated)
├── Student Dataset.csv    # Training dataset
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── templates/
│   ├── index.html        # Home page
│   ├── first.html        # Alternative landing page
│   └── result.html       # Prediction results page
│
└── static/
    ├── css/              # Stylesheets
    ├── js/               # JavaScript files
    └── images/           # Static images
```

## 🎮 Usage

1. **Navigate to the home page**
2. **Fill in the student information form**:
   - Age
   - Gender (0: Female, 1: Male)
   - Parental Education Level (0-4 scale)
   - Weekly Study Time (hours)
   - Number of Absences
   - Tutoring (0: No, 1: Yes)
   - Parental Support (0: No, 1: Yes)
   - Extracurricular Activities (0: No, 1: Yes)
   - Sports Participation (0: No, 1: Yes)

3. **Click "Predict CGPA"**
4. **View results including**:
   - Predicted CGPA
   - Letter Grade
   - Personalized suggestions
   - Interactive charts

## 📈 Model Performance

The Gradient Boosting Regressor model provides:
- High accuracy in CGPA prediction
- Feature importance analysis
- Robust handling of various input combinations
- Penalty-adjusted predictions for realistic outcomes

## 🎯 Suggestions Algorithm

The system provides intelligent suggestions based on:
- **Study Time**: Recommends minimum 12 hours/week
- **Attendance**: Alerts for high absence rates (>20)
- **Support Systems**: Suggests tutoring and parental support
- **Extracurricular Balance**: Encourages well-rounded development
- **Physical Activity**: Promotes sports participation

## 🔧 Customization

### Adding New Features
1. Update the dataset with new columns
2. Modify `trainmodel.py` to include new features
3. Update the web form in `templates/index.html`
4. Adjust the prediction logic in `app.py`

### Modifying Suggestions
Edit the suggestion logic in the `predict()` function in `app.py`

### Changing Visualizations
Modify the `create_pie_chart()` and `create_comparison_graph()` functions

## 📋 Requirements

```
Flask==2.3.3
pandas==2.0.3
scikit-learn==1.3.0
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
joblib==1.3.2
```

## 🐳 Docker Configuration

The included Dockerfile creates a lightweight container with:
- Python 3.9 base image
- All required dependencies
- Proper port exposure
- Optimized for production deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset contributors
- scikit-learn community
- Flask framework developers
- Open source community

## 📞 Contact

Your Name - harshrawte.dev@gmail.com

Project Link: [https://github.com/harshhrawte/GradientIQ.git](https://github.com/harshhrawte/GradientIQ.git)

---

⭐ **Star this repository if you found it helpful!**
Personalized Feedback: Offers guidance on areas for improvement, like:
"Increase your study time to at least 12 to 15 hours per week for a decent SGPA" (study hours include college assignments, self-study, and any college-related tasks or homework).
"Too many absences? Try to manage your schedule better."
"Consider tutoring to boost performance."
