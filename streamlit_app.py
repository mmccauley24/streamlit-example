import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
import seaborn as sns
import datetime
import matplotlib.pyplot as plt
from ipywidgets import interact, Dropdown, widgets, VBox, HBox, Layout, interactive
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
pulps = pd.read_csv('CGC_GRADED_PULPS.csv')
pulps = pulps.drop(pulps.columns[-1], axis=1)
pulps_long = pd.melt(pulps, id_vars=['ComicID', 'Title', 'Issue_Num', 'Issue_Date', 'Issue_Year', 'Publisher'
                                     , 'Country', 'ArtComments', 'KeyComments', 'Label_Category'], 
        var_name='Grade_Category', value_name='Value')
pulps_long['Grade'] = pulps_long['Grade_Category'].str.replace('POP_', '').str.replace('_', '.').astype(float)
pulps_long.drop('Grade_Category', axis=1)


# Filter out rows with null issue years and null grades
filtered_data = pulps_long.dropna(subset=['Issue_Year', 'Grade'])

# Get unique comic book titles
unique_titles = pulps_long['Title'].unique()

# Define a function to filter data based on selected title and search term
def filter_data(title, search_term):
    filtered_data = pulps_long
    if title:
        filtered_data = filtered_data[filtered_data['Title'] == title]
    if search_term:
        search_term_lower = search_term.lower()
        filtered_data = filtered_data[(filtered_data['ArtComments'].str.lower().str.contains(search_term_lower, na=False)) | 
                                      (filtered_data['KeyComments'].str.lower().str.contains(search_term_lower, na=False))]
    return filtered_data

# Define a function to update the bar chart based on the selected titles and search term
def update_plot(title1, title2, search_term1, search_term2):
    filtered_data1 = filter_data(title1, search_term1)
    filtered_data2 = filter_data(title2, search_term2)
    if filtered_data1.empty and filtered_data2.empty:
        st.write("No data to display.")
        return
    
    # Calculate total value for each grade for title 1
    grade_totals1 = filtered_data1.groupby('Grade')['Value'].sum().reset_index(name='Total Value')
    
    # Calculate total value for each grade for title 2
    grade_totals2 = filtered_data2.groupby('Grade')['Value'].sum().reset_index(name='Total Value')
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    if not filtered_data1.empty:
        axes[0].bar(grade_totals1['Grade'], grade_totals1['Total Value'], width=0.4, color='skyblue', label=title1)
        axes[0].set_title(title1)
        axes[0].set_xlabel('Grade')
        axes[0].set_ylabel('Total Value')
        axes[0].set_xticks(np.arange(11))
        axes[0].legend()
    
    if not filtered_data2.empty:
        axes[1].bar(grade_totals2['Grade'], grade_totals2['Total Value'], width=0.4, color='orange', label=title2)
        axes[1].set_title(title2)
        axes[1].set_xlabel('Grade')
        axes[1].set_ylabel('Total Value')
        axes[1].set_xticks(np.arange(11))
        axes[1].legend()
    
    # Show plot
    st.pyplot(fig)

# Create widgets
col1, col2 = st.columns(2)

with col1:
    title_dropdown1 = st.selectbox('Title 1:', [''] + list(unique_titles), index=0)
    search_box1 = st.text_input('Search Term for Title 1:')
    st.text(" ")  # Add empty space for better alignment

with col2:
    title_dropdown2 = st.selectbox('Title 2:', [''] + list(unique_titles), index=0)
    search_box2 = st.text_input('Search Term for Title 2:')
    st.text(" ")  # Add empty space for better alignment

# Create button to update plot
if st.button('Update Plot'):
    update_plot(title_dropdown1, title_dropdown2, search_box1, search_box2)

# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# indices = np.linspace(0, 1, num_points)
# theta = 2 * np.pi * num_turns * indices
# radius = indices

# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# df = pd.DataFrame({
#     "x": x,
#     "y": y,
#     "idx": indices,
#     "rand": np.random.randn(num_points),
# })

# st.altair_chart(alt.Chart(df, height=700, width=700)
#     .mark_point(filled=True)
#     .encode(
#         x=alt.X("x", axis=None),
#         y=alt.Y("y", axis=None),
#         color=alt.Color("idx", legend=None, scale=alt.Scale()),
#         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
#     ))
