import streamlit as st
import pandas as pd
import plotly.express as px



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

# Age Group Analysis
st.title("COVID-19 Age Group Analysis")

# Define age bins and labels
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = [
    "0-10",
    "11-20",
    "21-30",
    "31-40",
    "41-50",
    "51-60",
    "61-70",
    "71-80",
    "81-90",
    "91-100",
]

# Categorize AGE into bins
df["Age Group"] = pd.cut(df["AGE"], bins=bins, labels=labels, right=True)

# Count cases per age group
age_distribution = df["Age Group"].value_counts().sort_index()

# Create two columns for the analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Interactive Age Group Selection")
    # Dropdown for age group selection with counts
    selected_group = st.selectbox(
        "Select an Age Group:",
        options=labels,
        format_func=lambda x: f"{x} ({age_distribution.get(x, 0)} cases)",
    )

    # Show detailed statistics for selected group
    if selected_group in age_distribution.index:
        total_cases = age_distribution.sum()
        group_cases = age_distribution[selected_group]
        percentage = (group_cases / total_cases) * 100

        st.metric(
            label=f"Cases in {selected_group}",
            value=f"{group_cases:,}",
            delta=f"{percentage:.1f}% of total",
        )
    else:
        st.warning(f"No cases found in age group {selected_group}")

with col2:
    st.subheader("Most Affected Age Groups")
    # Show top 3 most affected age groups
    top_3_groups = age_distribution.nlargest(3)
    for age_group, count in top_3_groups.items():
        percentage = (count / age_distribution.sum()) * 100
        st.metric(
            label=f"#{list(top_3_groups.index).index(age_group) + 1}: {age_group}",
            value=f"{count:,} cases",
            delta=f"{percentage:.1f}% of total",
        )

