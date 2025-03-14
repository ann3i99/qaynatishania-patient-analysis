import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Disease Correlations", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df.columns = map(str.upper, df.columns)

    disease_columns = [
        "DIABETES", "COPD", "ASTHMA", "INMUSUPR", "HYPERTENSION",
        "PNEUMONIA", "CARDIOVASCULAR", "OBESITY", "CHRONIC_KIDNEY",
        "TOBACCO", "OTHER_DISEASE",
    ]

    # Map disease values
    for column in disease_columns:
        if column in df.columns:
            df[column] = df[column].map({1: "YES", 2: "NO", 97: "N/A", 98: "IGNORED", 99: "UNKNOWN"})
    
    # Map ICU values
    df["ICU"] = df["ICU"].map({1: "YES", 2: "NO", 97: "N/A", 98: "IGNORED", 99: "UNKNOWN"})

    return df, disease_columns

df, disease_columns = load_data()

st.title("Disease Correlation Analysis")

# Sidebar controls
st.sidebar.header("Visualization Controls")

# Feature selection
selected_features = st.sidebar.multiselect(
    "Select diseases to analyze:",
    disease_columns + ["ICU"],
    default=["DIABETES", "PNEUMONIA", "ICU", "CARDIOVASCULAR"]
)

# Correlation settings
correlation_threshold = st.sidebar.slider(
    "Minimum correlation strength:",
    min_value=0.0,
    max_value=1.0,
    value=0.1,
    step=0.05,
    help="Show only correlations stronger than this value"
)

# Visual settings
color_scheme = st.sidebar.selectbox(
    "Color scheme:",
    ["RdBu_r", "Viridis", "Plasma", "Magma", "Inferno"],
    help="Select color scheme for the heatmap"
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Correlation Heatmap")
    
    if len(selected_features) < 2:
        st.warning("Please select at least 2 features to show correlations.")
    else:
        # Convert categorical to numeric
        disease_numeric_df = df.copy()
        for col in disease_columns + ["ICU"]:
            if col in disease_numeric_df.columns:
                disease_numeric_df[col] = disease_numeric_df[col].map({"YES": 1, "NO": 0})

        # Compute correlation matrix for selected features
        correlation_matrix = disease_numeric_df[selected_features].corr()

        # Apply threshold masking
        if correlation_threshold > 0:
            mask = abs(correlation_matrix) >= correlation_threshold
            correlation_matrix = correlation_matrix.where(mask, None)

        # Create heatmap
        fig = px.imshow(
            correlation_matrix,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            color_continuous_scale=color_scheme,
            labels=dict(color="Correlation"),
            aspect="auto"
        )

        # Update layout
        fig.update_layout(
            title="Disease and ICU Admission Correlations",
            xaxis_title="Features",
            yaxis_title="Features",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Key Insights")
    
    if len(selected_features) >= 2:
        # Find strongest correlations
        correlations = []
        for i in range(len(selected_features)):
            for j in range(i + 1, len(selected_features)):
                corr_value = correlation_matrix.iloc[i, j]
                if corr_value is not None:  # Check for masked values
                    correlations.append({
                        "Feature 1": selected_features[i],
                        "Feature 2": selected_features[j],
                        "Correlation": corr_value
                    })

        if correlations:
            correlations_df = pd.DataFrame(correlations)
            correlations_df = correlations_df.sort_values("Correlation", key=abs, ascending=False)

            # Display top correlations
            st.subheader("Strongest Correlations")
            for _, row in correlations_df.iterrows():
                correlation_strength = abs(row["Correlation"])
                if correlation_strength >= correlation_threshold:
                    st.metric(
                        f"{row['Feature 1']} vs {row['Feature 2']}",
                        f"{row['Correlation']:.3f}",
                        delta="Strong" if correlation_strength >= 0.5 else "Moderate"
                    )

            # Additional statistics
            st.subheader("Statistics")
            st.write(f"Number of strong correlations (≥0.5): {len(correlations_df[abs(correlations_df['Correlation']) >= 0.5])}")
            st.write(f"Number of moderate correlations (0.3-0.5): {len(correlations_df[(abs(correlations_df['Correlation']) >= 0.3) & (abs(correlations_df['Correlation']) < 0.5)])}")
        else:
            st.info("No correlations meet the threshold criteria.")