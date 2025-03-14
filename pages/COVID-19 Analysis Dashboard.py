import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="COVID-19 Analysis Dashboard", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df.columns = map(str.upper, df.columns)

    # Convert and map categorical values
    mapping = {
        "SEX": {1: "FEMALE", 2: "MALE", 99: "UNKNOWN"},
        "HOSPITALIZED": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "INTUBATED": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "PREGNANCY": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "SPEAKS_NATIVE_LANGUAGE": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "TOBACCO": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "ANOTHER CASE": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "ICU": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
        "OUTCOME": {1: "POSITIVE", 2: "NEGATIVE", 97: "PENDING"},
        "NATIONALITY": {1: "MEXICAN", 2: "FOREIGN", 97: "UNKNOWN"},
    }

    disease_columns = [
        "DIABETES", "COPD", "ASTHMA", "INMUSUPR", "HYPERTENSION",
        "PNEUMONIA", "CARDIOVASCULAR", "OBESITY", "CHRONIC_KIDNEY",
        "TOBACCO", "OTHER_DISEASE",
    ]

    for column, map_values in mapping.items():
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
            df[column] = df[column].map(map_values)

    for column in disease_columns:
        if column in df.columns:
            df[column] = df[column].map({1: "YES", 2: "NO", 97: "N/A", 98: "IGNORED", 99: "UNKNOWN"})

    return df, disease_columns

df, disease_columns = load_data()

# Sidebar for global filters
st.sidebar.title("Global Filters")
sex_filter = st.sidebar.selectbox("Filter by Sex:", ["All"] + list(df["SEX"].dropna().unique()))
nationality_filter = st.sidebar.selectbox("Filter by Nationality:", ["All"] + list(df["NATIONALITY"].dropna().unique()))
selected_diseases = st.sidebar.multiselect("Filter by Disease:", disease_columns)

# Apply filters
filtered_df = df.copy()
if sex_filter != "All":
    filtered_df = filtered_df[filtered_df["SEX"] == sex_filter]
if nationality_filter != "All":
    filtered_df = filtered_df[filtered_df["NATIONALITY"] == nationality_filter]
if selected_diseases:
    for disease in selected_diseases:
        filtered_df = filtered_df[filtered_df[disease] == "YES"]

# Main content
st.title("COVID-19 Analysis Dashboard")

# Create tabs for different analyses
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Age Distribution", 
    "Disease Impact", 
    "Patient Demographics",
    "Hospital Statistics",
    "Outcome Analysis"
])

# Tab 1: Age Distribution Analysis
with tab1:
    st.header("Age Distribution Analysis")
    
    # Age bins and distribution
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
    filtered_df["Age Group"] = pd.cut(filtered_df["AGE"], bins=bins, labels=labels, right=True)
    age_distribution = filtered_df["Age Group"].value_counts().sort_index()
    
    # Interactive chart type selection
    chart_type = st.radio("Select Chart Type:", ["Bar", "Line", "Area"], horizontal=True)
    
    chart_data = pd.DataFrame({"Cases": age_distribution})
    if chart_type == "Bar":
        st.bar_chart(chart_data)
    elif chart_type == "Line":
        st.line_chart(chart_data)
    else:
        st.area_chart(chart_data)

# Tab 2: Disease Impact Analysis
with tab2:
    st.header("Disease Impact Analysis")
    
    # Filter deceased patients
    deceased_df = filtered_df[filtered_df["DATE_OF_DEATH"].notna()]
    
    # Calculate disease counts
    disease_counts = {}
    for disease in disease_columns:
        disease_counts[disease] = len(deceased_df[deceased_df[disease] == "YES"])
    
    disease_data = pd.DataFrame({
        "Disease": list(disease_counts.keys()),
        "Deaths": list(disease_counts.values())
    }).sort_values("Deaths", ascending=True)
    
    st.bar_chart(data=disease_data.set_index("Disease"))

# Tab 3: Patient Demographics
with tab3:
    st.header("Patient Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        gender_dist = filtered_df["SEX"].value_counts()
        st.subheader("Gender Distribution")
        fig_gender = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title="Gender Distribution"
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Nationality distribution
        nationality_dist = filtered_df["NATIONALITY"].value_counts()
        st.subheader("Nationality Distribution")
        st.bar_chart(nationality_dist)

# Tab 4: Hospital Statistics
with tab4:
    st.header("Hospital Statistics")
    
    # Get intubation counts
    intubation_counts = filtered_df["INTUBATED"].value_counts()
    
    # Create enhanced bar chart using Plotly Express
    fig = px.bar(
        x=intubation_counts.index,
        y=intubation_counts.values,
        title="Number of Patients Requiring Intubation",
        labels={"x": "Intubation Status", "y": "Number of Patients"},
        color=intubation_counts.values,
        color_continuous_scale="RdBu",  # Similar to coolwarm
        text=intubation_counts.values  # Add value labels on bars
    )
    
    # Customize the layout
    fig.update_layout(
        title=dict(
            text="Number of Patients Requiring Intubation",
            x=0.5,
            font=dict(
                size=20,
                family="Arial, bold"  # Using Arial bold font instead of font-weight
            )
        ),
        xaxis_title_font=dict(size=14, family="Arial, bold"),
        yaxis_title_font=dict(size=14, family="Arial, bold"),
        xaxis_tickfont=dict(size=12),
        yaxis_tickfont=dict(size=12),
        yaxis_gridcolor="rgba(0,0,0,0.1)",
        showlegend=False,
        height=600
    )
    
    # Customize bar appearance
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=14, color="black", family="Arial Bold"),
        texttemplate="%{text:,.0f}",  # Format with commas
        marker_line_color="black",
        marker_line_width=1.2
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Show percentage metrics
    col1, col2 = st.columns(2)
    with col1:
        icu_percentage = len(filtered_df[filtered_df["ICU"] == "YES"]) / len(filtered_df) * 100
        st.metric("ICU Cases", f"{icu_percentage:.1f}%")
    
    with col2:
        intubated_percentage = len(filtered_df[filtered_df["INTUBATED"] == "YES"]) / len(filtered_df) * 100
        st.metric("Intubated Cases", f"{intubated_percentage:.1f}%")

# Tab 5: Outcome Analysis
with tab5:
    st.header("Outcome Analysis")
    
    # Outcome distribution
    outcome_dist = filtered_df["OUTCOME"].value_counts()
    
    # Interactive chart selection
    chart_style = st.selectbox("Select Chart Style:", ["Pie Chart", "Bar Chart"])
    
    if chart_style == "Pie Chart":
        fig_outcome = px.pie(
            values=outcome_dist.values,
            names=outcome_dist.index,
            title="Outcome Distribution"
        )
        st.plotly_chart(fig_outcome, use_container_width=True)
    else:
        st.bar_chart(outcome_dist)
    
    # Show outcome percentages
    total_cases = len(filtered_df)
    for outcome, count in outcome_dist.items():
        percentage = (count / total_cases) * 100
        st.metric(f"{outcome} Cases", f"{percentage:.1f}%", f"{count:,} cases")
