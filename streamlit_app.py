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

# Define a function to update the bar chart based on the selected title and search term
def update_plot(title, search_term):
    filtered_data = filter_data(title, search_term)
    if filtered_data.empty:
        st.write("No data to display.")
        return
    
    # Calculate total value for each grade
    grade_totals = filtered_data.groupby('Grade')['Value'].sum().reset_index(name='Total Value')
    
    # Calculate weighted average grade
    weighted_avg_grade = (filtered_data['Grade'] * filtered_data['Value']).sum() / filtered_data['Value'].sum()
    weighted_avg_grade = round(weighted_avg_grade, 2)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(grade_totals['Grade'], grade_totals['Total Value'], color='skyblue')
    ax.set_xlabel('Grade')
    ax.set_ylabel('Total Value')
    ax.set_title('Total Value by Grade')
    ax.set_xticks(np.arange(11))
    
    # Add text for weighted average grade
    ax.text(0.5, -0.15, f'Weighted Average Grade: {weighted_avg_grade}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    
    # Show plot
    st.pyplot(fig)

# Create widgets
title_dropdown = st.selectbox('Title:', [''] + list(unique_titles), index=0)
search_box = st.text_input('Search Term:')

# Create button to update plot
if st.button('Update Plot'):
    update_plot(title_dropdown, search_box)


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
