import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

data = pd.read_csv(r'C:\Harsh\Desktop\GradientIQ\Student Dataset.csv')  
data = data.drop(columns=['Unnamed: 13', 'Unnamed: 14', 'Ethnicity'], errors='ignore')

def calculate_cgpa_penalty(absences): 
    penalty = (absences // 15) * 0.01
    return penalty

data['CGPAPenalty'] = data['Absences'].apply(calculate_cgpa_penalty)
X = data[['Age', 'Gender', 'ParentalEducation', 
           'StudyTimeWeekly', 'Absences', 'Tutoring',
           'ParentalSupport', 'Extracurricular', 'Sports']]
y = data['CGPA'] - data['CGPAPenalty']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor()
model.fit(X_train, y_train)

joblib.dump(model, 'model.pkl')

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

accuracy = r2 * 100

importances = model.feature_importances_
feature_names = X.columns
print("\nFeature Importances After Applying Penalty:")
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")

print("\nCleaned dataset head:")
print(data.head())
print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')
print(f'Accuracy: {accuracy:.2f}%')
