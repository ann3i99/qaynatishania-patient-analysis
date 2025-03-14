import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    df = pd.read_csv("dataset.csv")
    df.columns = map(str.upper, df.columns)

    # Convert and map categorical values
    mapping = {
        "SEX": {1: "FEMALE", 2: "MALE", 99: "UNKNOWN"},
        "HOSPITALIZED": {
            1: "YES",
            2: "NO",
            97: "DOES NOT APPLY",
            98: "IGNORED",
            99: "UNKNOWN",
        },
        "INTUBATED": {
            1: "YES",
            2: "NO",
            97: "DOES NOT APPLY",
            98: "IGNORED",
            99: "UNKNOWN",
        },
        "PREGNANCY": {
            1: "YES",
            2: "NO",
            97: "DOES NOT APPLY",
            98: "IGNORED",
            99: "UNKNOWN",
        },
        "SPEAKS_NATIVE_LANGUAGE": {
            1: "YES",
            2: "NO",
            97: "DOES NOT APPLY",
            98: "IGNORED",
            99: "UNKNOWN",
        },
        "TOBACCO": {
            1: "YES",
            2: "NO",
            97: "DOES NOT APPLY",
            98: "IGNORED",
            99: "UNKNOWN",
        },
        "ANOTHER CASE": {
            1: "YES",
            2: "NO",
            97: "DOES NOT APPLY",
            98: "IGNORED",
            99: "UNKNOWN",
        },
        "ICU": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "OUTCOME": {1: "POSITIVE", 2: "NEGATIVE", 97: "PENDING"},
        "NATIONALITY": {1: "MEXICAN", 2: "FOREIGN", 97: "UNKNOWN"},
    }

    disease_columns = [
        "DIABETES",
        "COPD",
        "ASTHMA",
        "INMUSUPR",
        "HYPERTENSION",
        "PNEUMONIA",
        "CARDIOVASCULAR",
        "OBESITY",
        "CHRONIC_KIDNEY",
        "TOBACCO",
        "OTHER_DISEASE",
    ]

    for column, map_values in mapping.items():
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
            df[column] = df[column].map(map_values)

    for column in disease_columns:
        if column in df.columns:
            df[column] = df[column].map(
                {1: "YES", 2: "NO", 97: "N/A", 98: "IGNORED", 99: "UNKNOWN"}
            )

    return df

df = load_data()
df['ADMISSION DATE'] = pd.to_datetime(df['ADMISSION DATE'])

pre_chosen_categories = ['PNEUMONIA', 'SEX', 'HOSPITALIZED', 'INTUBATED']

st.sidebar.title("Time Series Analysis")
# choose one of the pre-chosen categories
chosen_category = st.sidebar.selectbox("Select category", pre_chosen_categories)

# Summarize data for the chosen category
summarized_data = df.groupby('ADMISSION DATE')[chosen_category].value_counts().unstack().fillna(0)
summarized_data = summarized_data.reset_index()

# Create line chart
fig = px.line(summarized_data, x='ADMISSION DATE', y=summarized_data.columns[1:], title=f'Line Chart of {chosen_category} Admission Over Time')

# Display line chart
st.plotly_chart(fig)

# Display dataframe
# st.write(df)