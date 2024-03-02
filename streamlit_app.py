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
    if not filtered_data1.empty:
        weighted_avg_grade1 = (filtered_data1['Grade'] * filtered_data1['Value']).sum() / filtered_data1['Value'].sum()
        weighted_avg_grade1 = round(weighted_avg_grade1, 2)
        total_graded1 = filtered_data1['Value'].sum()
    
    # Calculate total value for each grade for title 2
    grade_totals2 = filtered_data2.groupby('Grade')['Value'].sum().reset_index(name='Total Value')
    if not filtered_data2.empty:
        weighted_avg_grade2 = (filtered_data2['Grade'] * filtered_data2['Value']).sum() / filtered_data2['Value'].sum()
        weighted_avg_grade2 = round(weighted_avg_grade2, 2)
        total_graded2 = filtered_data2['Value'].sum()
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    if not filtered_data1.empty:
        axes[0].bar(grade_totals1['Grade'], grade_totals1['Total Value'], width=0.4, color='skyblue', label=title1)
        axes[0].set_title(title1)
        axes[0].set_xlabel('Grade')
        axes[0].set_ylabel('Total Value')
        axes[0].set_xticks(np.arange(11))
        axes[0].legend()
        axes[0].text(0.5, -0.25, f'Weighted Average Grade: {weighted_avg_grade1}', horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
        axes[0].text(0.5, -0.30, f'Total Graded: {total_graded1}', horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
    
    if not filtered_data2.empty:
        axes[1].bar(grade_totals2['Grade'], grade_totals2['Total Value'], width=0.4, color='orange', label=title2)
        axes[1].set_title(title2)
        axes[1].set_xlabel('Grade')
        axes[1].set_ylabel('Total Value')
        axes[1].set_xticks(np.arange(11))
        axes[1].legend()
        axes[1].text(0.5, -0.25, f'Weighted Average Grade: {weighted_avg_grade2}', horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
        axes[1].text(0.5, -0.30, f'Total Graded: {total_graded2}', horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
    
    # Show plot
    st.pyplot(fig)

# Default values for filters
default_title1 = 'Weird Tales'
default_title2 = 'Amazing Stories'

# Create widgets
col1, col2 = st.columns(2)

with col1:
    title_dropdown1 = st.selectbox('Title 1:', [''] + list(unique_titles), index=np.where(unique_titles == default_title1)[0][0], key='title1')
    search_box1 = st.text_input('Search Term for Title 1:', key='search1')

with col2:
    title_dropdown2 = st.selectbox('Title 2:', [''] + list(unique_titles), index=np.where(unique_titles == default_title2)[0][0], key='title2')
    search_box2 = st.text_input('Search Term for Title 2:', key='search2')

# Create button to update plot
if st.button('Update Plot'):
    update_plot(title_dropdown1, title_dropdown2, search_box1, search_box2)
