import streamlit as st
import pandas as pd


# Load the dataset
@st.cache_data
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

    return df, disease_columns


df, disease_columns = load_data()

st.title("COVID-19 Cases Data Dashboard")

# Filters
column1, column2 = st.columns(2)

# Filter by Sex
with column1:
    sex_filter = st.selectbox(
        "Filter by Sex:", ["All"] + list(df["SEX"].dropna().unique())
    )
    if sex_filter != "All":
        df = df[df["SEX"] == sex_filter]

# Filter by Nationality
with column2:
    nationality_filter = st.selectbox(
        "Filter by Nationality:", ["All"] + list(df["NATIONALITY"].dropna().unique())
    )
    if nationality_filter != "All":
        df = df[df["NATIONALITY"] == nationality_filter]

# Filter by Disease
selected_diseases = st.multiselect("Filter by Disease:", disease_columns)
if selected_diseases:
    for disease in selected_diseases:
        df = df[df[disease] == "YES"]

# Display filtered results
if not df.empty:
    st.write("### Filtered Results:")
    st.dataframe(df)
else:
    st.warning("No data found for the selected filters.")

# Basic Visualizations
st.bar_chart(df["OUTCOME"].value_counts())
st.pie_chart(df["SEX"].value_counts())
