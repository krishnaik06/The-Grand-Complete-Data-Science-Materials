# Climate Change Alert System
## Overview
The Climate Change Alert System is a Streamlit-based application designed to analyze global temperature data, identify unusual changes, and provide time series forecasting using LSTM (Long Short-Term Memory) neural networks. This project aims to raise awareness of potential climate anomalies by detecting significant deviations from historical temperature trends.

Prerequisites
Before running the application, ensure that you have the required Python packages installed. You can install them using the following command:

```
pip install streamlit matplotlib seaborn scikit-learn tensorflow pandas
```
## Project Structure
- app.py: The main Python script containing the Streamlit application and the implementation of data analysis, anomaly detection, and time series forecasting.

- GlobalTemperatures.csv: The dataset containing global temperature records is used for analysis.

- trained_lstm_model.h5: The trained LSTM model saved in Hierarchical Data Format (HDF5).

- climate_change_alert.log: Log file capturing errors and informational messages during the application's execution.

## Running the Application
To run the Climate Change Alert System, execute the following command in your terminal:

```
streamlit run climate_change_alert.py
```
Access the application in your web browser by navigating to the provided local address.

## Usage
- <strong>Parameters Sidebar:</strong> Adjust the Z-Score Threshold, Sequence Length for Forecasting, Batch Size for LSTM, and the number of Epochs using interactive sliders.

- <strong> Submit Button:</strong> Click the "Submit" button to trigger the analysis and forecasting based on the selected parameters.

- <strong>Alerts and Visualizations:</strong> The application displays alerts for unusual changes in global temperatures and provides visualizations, including Z-Score plots and additional temperature-related charts.

- <strong>Time Series Forecasting:</strong> The LSTM model is trained and evaluated on the provided global temperature dataset, and the results, including evaluation metrics and visualizations, are presented.

## Error Handling
The application logs errors and information to the climate_change_alert.log file. If any issues occur during execution, consult this log for diagnostic information.

## Contributing
Contributions to enhance the functionality, fix bugs, or improve the code structure are welcome. Feel free to open issues or pull requests.
