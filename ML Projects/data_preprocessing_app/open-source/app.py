import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import sys
import os

# Ensure module path and import your data_tool
sys.path.append(os.path.dirname(__file__))
from data_tool import read_data, preview, preprocess_data, data_metrics_and_visualise

st.set_page_config(page_title="Data Toolkit", layout="wide")
st.title("🧠 Data Preprocessing Web App")

uploaded_file = st.file_uploader("Upload a dataset", type=["csv", "xlsx", "json", "sql", "parquet"])

if uploaded_file:
    with open("temp_upload" + Path(uploaded_file.name).suffix, "wb") as f:
        f.write(uploaded_file.getvalue())
    filepath = f.name

    st.success(f"Loaded file: {uploaded_file.name}")
    task = st.selectbox("Choose Task", ["Preview", "Clean", "Visualize", "Transform"])

    if "processed_df" not in st.session_state:
        st.session_state.processed_df = read_data(filepath)

    if task == "Preview":
        head, tail = preview(filepath)
        st.subheader("Head")
        st.write(head)
        st.subheader("Tail")
        st.write(tail)

        csv = st.session_state.processed_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Dataset", csv, "original_data.csv", "text/csv")

    elif task == "Clean":
        st.subheader("Cleaning Options")
        df = st.session_state.processed_df
        drop_cols = st.multiselect("Columns to Drop", df.columns.tolist())
        drop_null = st.checkbox("Drop Null Values")
        fill_zero = st.checkbox("Fill Null with Zero")
        column_to_clean = st.selectbox("Column to Clean (remove non-alphanum)", [None] + df.columns.tolist())
        address_col = st.selectbox("Address Column (Replace String)", [None] + df.columns.tolist())
        old_str = st.text_input("Old String to Replace")
        new_str = st.text_input("New String Value")

        if st.button("Clean Data"):
            st.session_state.processed_df = preprocess_data(
                st.session_state.processed_df,
                drop_cols=drop_cols,
                drop_null=drop_null,
                fill_null_with_zero=fill_zero,
                column_to_clean=column_to_clean if column_to_clean != "None" else None,
                address_col_to_standardize=address_col if address_col != "None" else None,
                old_str=old_str or None,
                new_str=new_str or None,
            )
            st.dataframe(st.session_state.processed_df.head())

            csv = st.session_state.processed_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Cleaned Data", csv, "cleaned_data.csv", "text/csv")

    elif task == "Visualize":
        st.subheader("Visualization Options")
        df = st.session_state.processed_df

        numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
        selected_columns = st.multiselect("Select numeric columns to visualize", numeric_columns, default=numeric_columns)

        chart_type = st.selectbox("Chart Type", ["Boxplot", "Histogram"])

    if st.button("Show Plots"):
        if not selected_columns:
            st.warning("Please select at least one numeric column to visualize.")
        else:
            with st.spinner("Generating plots..."):
                for col in selected_columns:
                    st.write(f"### {chart_type} for `{col}`")

                    fig, ax = plt.subplots()
                    if chart_type == "Boxplot":
                        ax.boxplot(df[col].dropna(), vert=False)
                    elif chart_type == "Histogram":
                        ax.hist(df[col].dropna(), bins=30)

                    ax.set_title(f"{chart_type} for {col}")
                    st.pyplot(fig)
                    plt.clf()

            csv = df[selected_columns].to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Visualized Data", csv, "visualized_data.csv", "text/csv")


    elif task == "Transform":
        st.subheader("Transformation Options")
        df = st.session_state.processed_df
        label_cols = st.multiselect("Label Encode Columns", df.select_dtypes(include="object").columns.tolist())
        one_hot_cols = st.multiselect("One-Hot Encode (Pandas)", df.select_dtypes(include="object").columns.tolist())
        one_hot_sklearn_cols = st.multiselect("One-Hot Encode (Scikit-learn)", df.select_dtypes(include="object").columns.tolist())
        scale = st.checkbox("Standard Scale Data")
        anomaly_col = st.selectbox("Column for Anomaly Removal", [None] + df.select_dtypes(include="number").columns.tolist())

        if st.button("Transform Data"):
            st.session_state.processed_df = preprocess_data(
                st.session_state.processed_df,
                label_encode_cols=label_cols,
                one_hot_encode_cols=one_hot_cols,
                one_hot_encode_cols_sklearn=one_hot_sklearn_cols,
                scale=scale,
                anomaly_col_train=anomaly_col if anomaly_col != "None" else None,
            )

            st.dataframe(st.session_state.processed_df.head())

            csv = st.session_state.processed_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Transformed Data", csv, "transformed_data.csv", "text/csv")
