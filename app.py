import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page configuration
st.set_page_config(page_title='Employee Attrition Dashboard', layout='wide')

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("EA.csv")

df = load_data()

# Title
st.title("🧠 Employee Attrition Dashboard")

# Intro
st.markdown("""
This dashboard provides in-depth insights into employee attrition trends.
Use filters, sliders, and tabs to explore the key metrics that influence workforce retention.
""")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
age = st.sidebar.slider("Select Age Range", int(df.Age.min()), int(df.Age.max()), (25, 45))
dept = st.sidebar.multiselect("Select Department(s)", df['Department'].unique(), default=list(df['Department'].unique()))

# Filter data
filtered_df = df[(df['Age'] >= age[0]) & (df['Age'] <= age[1]) & (df['Department'].isin(dept))]

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Deep Dive", "🎛️ Interactive Filters"])

# ---- TAB 1: OVERVIEW ----
with tab1:
    st.subheader("Attrition Breakdown")
    st.write("This chart shows the number of employees who have left vs stayed.")
    st.bar_chart(filtered_df['Attrition'].value_counts())

    st.subheader("Department-wise Attrition")
    st.write("Understand which departments have high attrition.")
    fig = px.histogram(filtered_df, x="Department", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Education Field vs Attrition")
    fig = px.histogram(filtered_df, x="EducationField", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Gender-wise Attrition")
    fig = px.histogram(filtered_df, x="Gender", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# ---- TAB 2: DEEP DIVE ----
with tab2:
    st.subheader("Boxplot: Monthly Income by Attrition")
    st.write("Visualize income distribution among employees who left vs stayed.")
    fig = px.box(filtered_df, x="Attrition", y="MonthlyIncome", color="Attrition")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Heatmap: Correlation Matrix")
    st.write("Understand relationships between numerical variables.")
    numeric_df = filtered_df.select_dtypes(include='number')
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(corr, annot=False, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("Total Working Years vs Age")
    fig = px.scatter(filtered_df, x="Age", y="TotalWorkingYears", color="Attrition", size="MonthlyIncome")
    st.plotly_chart(fig, use_container_width=True)

# ---- TAB 3: INTERACTIVE FILTERS ----
with tab3:
    st.subheader("Interactive Table")
    st.write("Browse employees matching the current filter criteria.")
    st.dataframe(filtered_df)

    st.subheader("Job Role vs Attrition")
    fig = px.histogram(filtered_df, x="JobRole", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Years at Company Distribution")
    fig = px.histogram(filtered_df, x="YearsAtCompany", color="Attrition")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Attrition by Business Travel")
    fig = px.histogram(filtered_df, x="BusinessTravel", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Created for HR Directors and Stakeholders | SP Jain GMBA Project")
