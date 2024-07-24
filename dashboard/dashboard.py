import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
file_path = 'dashboard/batik_exp_fixed.csv'
df = pd.read_csv(file_path)

# Sidebar with logo and filters
st.sidebar.image("dashboard/logobatik2.jpg", use_column_width=True)
st.sidebar.title("Filters")
year_range = st.sidebar.slider('Select Year Range', int(df['Tahun'].min()), int(df['Tahun'].max()), (int(df['Tahun'].min()), int(df['Tahun'].max())))

# Filter the dataset based on selected year range
filtered_df = df[(df['Tahun'] >= year_range[0]) & (df['Tahun'] <= year_range[1])]

css_styles = """
<style>
    .element-container:nth-child(1) {
        background-color: #DEB887; /* Light brown*/
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* Remove the box style for the sidebar image */
    .sidebar .stImage {
        box-shadow: none;
        border-radius: 0;
    }
</style>
"""
# Insert CSS styles into the Streamlit app
st.markdown(css_styles, unsafe_allow_html=True)

# Define CSS styles for the sidebar image
css_styles_sidebar = """
<style>
    .sidebar .stImage img {
        border-radius: 10px; /* Adjust the border-radius as needed */
    }
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# Title of the app
st.title("Indonesian Batik Export in 2010 - 2021 Analysis Dashboard")

# Metrics for the dashboard
col1, col2, col3 = st.columns(3)

with col1:
    total_countries = filtered_df['Negara'].nunique()
    st.metric('Total Destination Countries', total_countries)

with col2:
    total_export_value = filtered_df['Nilai'].sum()
    st.metric('Total Export Value (USD)', f"${total_export_value:,.2f}")

with col3:
    total_export_weight = filtered_df['Berat'].sum()
    st.metric('Total Export Weight (Kg)', f"{total_export_weight:,.2f} Kg")

# Define a custom color scale with shades of brown
custom_color_scale = [
    [0.0, "#FFF8DC"],    # Lightest brown (cornsilk)
    [0.2, "#DEB887"],    # Light brown (burlywood)
    [0.4, "#D2B48C"],    # Medium brown (tan)
    [0.6, "#A0522D"],    # Dark brown (sienna)
    [0.8, "#8B4513"],    # Darker brown (saddle brown)
    [1.0, "#5D4037"]     # Darkest brown (sienna)
]

# Menghapus baris dengan nilai yang hilang
filtered_df = filtered_df.dropna()

# Choropleth map of export destination countries by value
st.subheader("💰 Export Destination Countries by Value 🌎")
fig_value = px.choropleth(filtered_df,
                          locations='Iso-3',
                          color='Nilai',
                          hover_name='Negara',
                          color_continuous_scale=custom_color_scale,
                          range_color=(0, filtered_df['Nilai'].max()),
                          title='Export Destination Countries by Value',
                          labels={'Nilai': 'Value (USD)'})
st.plotly_chart(fig_value)

# Top 10 countries by export value with year filter
st.subheader("Top 10 Countries by Export Value 💰")
top10_value = filtered_df.groupby('Negara')['Nilai'].sum().nlargest(10).reset_index()
fig_value = px.bar(top10_value,
                   x='Nilai',
                   y='Negara',
                   orientation='h',
                   title='Top 10 Countries by Export Value',
                   color_discrete_sequence=['#8B4513'],
                   labels={'Nilai' : 'Value (USD)', 'Negara' : 'Country'})
st.plotly_chart(fig_value)

# Choropleth map of export destination countries by weight
st.subheader("⚖️ Export Destination Countries by Weight 🌎")
fig_weight = px.choropleth(filtered_df,
                          locations='Iso-3',
                          color='Berat',
                          hover_name='Negara',
                          color_continuous_scale=custom_color_scale,
                          range_color=(0, filtered_df['Berat'].max()),
                          title='Export Destination Countries by Value',
                          labels={'Berat': 'Weight (Kg)'})
st.plotly_chart(fig_weight)

# Top 10 countries by export weight with year filter
st.subheader("Top 10 Countries by Export Weight ⚖️")
top10_weight = filtered_df.groupby('Negara')['Berat'].sum().nlargest(10).reset_index()
fig_weight = px.bar(top10_weight,
                    x='Berat',
                    y='Negara',
                    orientation='h',
                    title='Top 10 Countries by Export Weight',
                    color_discrete_sequence=['#8B4513'],
                    labels={'Berat' : 'Weight (Kg)', 'Negara' : 'Country'})
st.plotly_chart(fig_weight)

# Line chart of total Batik export weight per year
st.subheader("Total Batik Export Weight per Year 📈")
annual_weight = df.groupby('Tahun')['Berat'].sum().reset_index()
fig_annual_weight = px.line(annual_weight,
                            x='Tahun',
                            y='Berat',
                            title='Total Batik Export Weight per Year',
                            color_discrete_sequence=['#8B4513'],
                            labels={'Tahun' : 'Year', 'Berat' : 'Weight (Kg)'})
st.plotly_chart(fig_annual_weight)

# Line chart of total Batik export value per year
st.subheader("Total Batik Export Value per Year 📉")
annual_value = df.groupby('Tahun')['Nilai'].sum().reset_index()
fig_annual_value = px.line(annual_value,
                           x='Tahun',
                           y='Nilai',
                           title='Total Batik Export Value per Year',
                           color_discrete_sequence=['#8B4513'],
                           labels={'Tahun' : 'Year', 'Nilai' : 'Value (USD)'})
st.plotly_chart(fig_annual_value)

# Line chart comparing total Batik export weight and value per year
st.subheader("🔎 Comparison of Total Batik Export Weight and Value per Year 📊")

# Calculate the aggregated data for weight and value per year
annual_weight_value = df.groupby('Tahun')[['Berat', 'Nilai']].sum().reset_index()

# Reshape the data to long format for easier plotting
annual_weight_value_long = pd.melt(annual_weight_value, id_vars='Tahun', value_vars=['Berat', 'Nilai'])

# Create the bar chart
fig_comparison = px.bar(annual_weight_value_long,
                        x='Tahun',
                        y='value',
                        color='variable', 
                        barmode='group',
                        title='Comparison of Total Batik Export Weight and Value per Year',
                        color_discrete_map={'Berat': '#DEB887', 'Nilai': '#8B4513'},
                        labels={'value': 'Total (USD)', 'variable': 'Category', 'Tahun': 'Year'})

st.plotly_chart(fig_comparison)
