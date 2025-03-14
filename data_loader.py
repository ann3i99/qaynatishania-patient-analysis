import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df.columns = map(str.upper, df.columns)

    # Convert and map categorical values
    mapping = {
        "SEX": {1: "FEMALE", 2: "MALE", 99: "UNKNOWN"},
        "HOSPITALIZED": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "INTUBATED": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "TOBACCO": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "PNEUMONIA": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    }

    disease_columns = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR", "HYPERTENSION", 
                       "PNEUMONIA", "CARDIOVASCULAR", "OBESITY", "CHRONIC_KIDNEY", "TOBACCO", "OTHER_DISEASE"]

    for column, map_values in mapping.items():
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
            df[column] = df[column].map(map_values)

    for column in disease_columns:
        if column in df.columns:
            df[column] = df[column].map({1: "YES", 2: "NO", 97: "N/A", 98: "IGNORED", 99: "UNKNOWN"})

    return df, disease_columns