import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from scipy.stats import zscore
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(filename='climate_change_alert.log', level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Function to convert 'dt' column to datetime format
def convert_to_datetime(data, column='dt'):
    data[column] = pd.to_datetime(data[column])
    return data

# Read datasets
try:
    df = pd.read_csv('GlobalTemperatures.csv', parse_dates=['dt'])
except FileNotFoundError:
    logger.error("Error: File not found. Please make sure the file path is correct.")
except pd.errors.EmptyDataError:
    logger.error("Error: The CSV file is empty or in an invalid format.")

# Convert 'dt' column to datetime format
df = convert_to_datetime(df)

global_temperatures_df = df.dropna(subset=['LandAverageTemperature'])

# Streamlit App
st.title('Climate Change Alert System')
st.header("Please submit the parameters to view the details")

# Default parameters
default_z_score_threshold = 2.0
default_sequence_length = 10
default_batch_size = 32
default_epochs = 50

# Check if session state variables are already initialized
try:
    if 'z_score_threshold' not in st.session_state:
        st.session_state.z_score_threshold = default_z_score_threshold
    if 'sequence_length' not in st.session_state:
        st.session_state.sequence_length = default_sequence_length
    if 'batch_size' not in st.session_state:
        st.session_state.batch_size = default_batch_size
    if 'epochs' not in st.session_state:
        st.session_state.epochs = default_epochs
except Exception as e:
    st.warning(f"Error initializing session state: {e}")

# Sidebar with interactive controls
st.sidebar.header('Parameters')
z_score_threshold = st.sidebar.slider('Z-Score Threshold', min_value=0.1, max_value=5.0, value=st.session_state.z_score_threshold)
sequence_length = st.sidebar.slider('Sequence Length for Forecasting', min_value=5, max_value=50, value=st.session_state.sequence_length)
batch_size = st.sidebar.slider('Batch Size for LSTM', min_value=16, max_value=128, value=st.session_state.batch_size)
epochs = st.sidebar.slider('Number of Epochs', min_value=10, max_value=100, value=st.session_state.epochs)
submit_button = st.sidebar.button('Submit')

# Convert the 'dt' column to datetime format
global_temperatures_df['dt'] = pd.to_datetime(global_temperatures_df['dt'])
global_aggregated = global_temperatures_df.resample('Y', on='dt').mean()

# Define a function to calculate z-scores
def calculate_z_scores(data):
    return zscore(data['LandAverageTemperature'])

# Define a function to identify unusual changes
def find_unusual_changes(data, z_scores, threshold):
    return data[abs(z_scores) > threshold]

# Handle button click
if submit_button:
    try:
        # Update session state variables
        st.session_state.z_score_threshold = z_score_threshold
        st.session_state.sequence_length = sequence_length
        st.session_state.batch_size = batch_size
        st.session_state.epochs = epochs
        # Call the calculate_z_scores function
        z_scores = calculate_z_scores(global_aggregated)

        # Call the find_unusual_changes function
        unusual_changes = find_unusual_changes(global_aggregated, z_scores, st.session_state.z_score_threshold)
        
        # Define a function to plot z-scores
        def plot_z_scores(data, z_scores, threshold):
            plt.figure(figsize=(10, 6))
            plt.plot(data.index, z_scores, label='Z-Scores')
            plt.axhline(y=threshold, color='r', linestyle='--', label='Alert Threshold')
            plt.axhline(y=-threshold, color='r', linestyle='--')
            plt.title('Z-Scores for Land Average Temperature')
            plt.xlabel('Year')
            plt.ylabel('Z-Score')
            plt.legend()
            st.pyplot(plt)
    except Exception as e:
        logger.error(f"Error processing data and generating alerts: {e}")

    # Call the plot_z_scores function
    try:
        plot_z_scores(global_aggregated, z_scores, st.session_state.z_score_threshold)
    except Exception as e:
        st.error(f"Error plotting Z-Scores: {e}")

    # Send alerts based on unusual changes
    if len(unusual_changes) > 0:
        st.warning(f"ALERT: {len(unusual_changes)} unusual changes detected in global temperatures.")
        st.write(unusual_changes)
    else:
        st.info("No unusual changes detected.")

    # Rest of your code for time series forecasting
    try:
        # Convert the 'dt' column to datetime format
        global_temperatures_df = global_temperatures_df.copy()
        global_temperatures_df['dt'] = pd.to_datetime(global_temperatures_df['dt'])

        # Calculate the z-score for the 'LandAverageTemperature'
        z_scores = zscore(global_aggregated['LandAverageTemperature'])

        # Define a z-score threshold for unusual changes (you can adjust this)
        threshold = st.session_state.z_score_threshold

        # Identify unusual changes based on the z-score
        unusual_changes = global_aggregated[abs(z_scores) > threshold]

        # Extract relevant features and target variable
        features = global_temperatures_df[['LandAverageTemperatureUncertainty', 'LandMaxTemperature', 'LandMinTemperatureUncertainty']]
        target = global_temperatures_df['LandAverageTemperature']

        # Ensure that your dataset is sorted by the datetime column
        global_temperatures_df = global_temperatures_df.sort_values('dt')

        # Normalize the data using Min-Max scaling
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(target.values.reshape(-1, 1))

        # Define a function to create sequences for time series forecasting
        def create_sequences(data, sequence_length):
            X, y = [], []
            for i in range(len(data) - sequence_length):
                X.append(data[i:i+sequence_length])
                y.append(data[i+sequence_length])
            return np.array(X), np.array(y)

        # Define hyperparameters
        sequence_length = st.session_state.sequence_length  # Adjust based on the desired sequence length
        batch_size = st.session_state.batch_size
        epochs = st.session_state.epochs  # Use the session state variable consistently

        # Create sequences for training
        X, y = create_sequences(scaled_data, sequence_length)

        # Split the data into training and testing sets
        train_size = int(len(X) * 0.8)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
        model.add(Dense(1))
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

        # Train the model
        try:
            model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)
        except Exception as e:
            st.error(f"Error during model training: {e}")
            logger.error(f"Error during model training: {e}")

        # Save the trained model
        model_save_path = "trained_lstm_model.h5"
        try:
            model.save(model_save_path)
            st.success(f"Model saved successfully to {model_save_path}")
        except Exception as e:
            st.error(f"Error saving the model: {e}")
            logger.error(f"Error saving the model: {e}")

        # Load the trained model
        loaded_model = None
        try:
            loaded_model = load_model(model_save_path)
            st.success("Model loaded successfully")
        except Exception as e:
            st.error(f"Error loading the model: {e}")

        # Make predictions on the testing set using the loaded model
        if loaded_model:
            loaded_y_pred = loaded_model.predict(X_test)
            loaded_y_pred_original = scaler.inverse_transform(loaded_y_pred)

            # Extract the original y_test values for evaluation
            y_test_original = scaler.inverse_transform(y_test)

            # Additional code for evaluation, visualization, etc.

            # Evaluation Metrics
            mae = mean_absolute_error(y_test_original, loaded_y_pred_original)
            rmse = np.sqrt(mean_squared_error(y_test_original, loaded_y_pred_original))

            st.subheader('Time Series Forecasting Evaluation Metrics')
            st.write("Mean Absolute Error (MAE):", mae)
            st.write("Root Mean Squared Error (RMSE):", rmse)

            # Additional Visualizations
            st.subheader('Additional Visualizations')

            # Multiple plots to show different aspects of the data
            def plot_additional_visualizations():
                fig, axes = plt.subplots(2, 2, figsize=(12, 8))

                axes[0, 0].plot(global_aggregated.index, global_aggregated['LandMaxTemperature'], label='LandMaxTemperature')
                axes[0, 0].set_title('LandMaxTemperature over Time')
                axes[0, 0].set_xlabel('Year')
                axes[0, 0].set_ylabel('Temperature')
                axes[0, 0].legend()

                axes[0, 1].plot(global_aggregated.index, global_aggregated['LandMinTemperature'], label='LandMinTemperature', color='orange')
                axes[0, 1].set_title('LandMinTemperature over Time')
                axes[0, 1].set_xlabel('Year')
                axes[0, 1].set_ylabel('Temperature')
                axes[0, 1].legend()

                axes[1, 0].plot(global_aggregated.index, global_aggregated['LandAndOceanAverageTemperature'], label='LandAndOceanAverageTemperature', color='green')
                axes[1, 0].set_title('LandAndOceanAverageTemperature over Time')
                axes[1, 0].set_xlabel('Year')
                axes[1, 0].set_ylabel('Temperature')
                axes[1, 0].legend()

                axes[1, 1].plot(global_aggregated.index, global_aggregated['LandAverageTemperatureUncertainty'], label='LandAverageTemperatureUncertainty', color='red')
                axes[1, 1].set_title('LandAverageTemperatureUncertainty over Time')
                axes[1, 1].set_xlabel('Year')
                axes[1, 1].set_ylabel('Uncertainty')
                axes[1, 1].legend()

                plt.tight_layout()
                st.pyplot(fig)

            plot_additional_visualizations()

            # Heatmap to visualize the correlation matrix of features
            correlation_matrix = global_temperatures_df.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title('Correlation Matrix of Features')
            st.pyplot(plt)

            # Line chart showing the original and predicted temperature values over time
            def plot_temperature_comparison():
                plt.figure(figsize=(12, 6))

                # Use the same index for both original and predicted values
                index_range = global_aggregated.index[-len(y_test_original):]

                # Flatten y_test_original if it's a 2D array
                y_test_original_flat = y_test_original.flatten()

                # Trim the index_range and y_test_original_flat to the minimum length
                min_length = min(len(index_range), len(y_test_original_flat))
                index_range_trimmed = index_range[-min_length:]
                y_test_original_flat_trimmed = y_test_original_flat[-min_length:]

                plt.plot(index_range_trimmed, y_test_original_flat_trimmed, label='Original Temperature', color='blue')
                plt.plot(index_range_trimmed, loaded_y_pred_original[-min_length:], label='Predicted Temperature', color='orange', linestyle='--')

                plt.title('Original vs Predicted Temperature over Time')
                plt.xlabel('Year')
                plt.ylabel('Temperature')
                plt.legend()
                st.pyplot(plt)

            plot_temperature_comparison()

    except Exception as e:
        st.error(f"Error during time series forecasting and additional visualizations: {e}")