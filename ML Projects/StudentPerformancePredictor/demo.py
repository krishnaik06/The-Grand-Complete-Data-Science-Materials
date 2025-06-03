import pandas as pd
# Load dataset
data = pd.read_csv(r'C:\Harsh\Desktop\GradientIQ\Student Dataset.csv')  
# Print the entire dataset
print("Complete dataset:")
print(data)

# Print column names
print("\nColumn names:")
print(data.columns.tolist())

# Dropping unnecessary columns
data = data.drop(columns=['Unnamed: 13', 'Unnamed: 14'], errors='ignore')

# Check for data types and null counts
print("\nData Information:")
print(data.info())

# Optional: Print the first few rows of the cleaned dataset
print("\nCleaned dataset:")
print(data.head())
