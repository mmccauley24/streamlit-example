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
# CGC Pulp Analytics

Filter by titles or search for art/key comments and press Update Plot to compare the current pulp census of CGC graded books!

Brought to you by RarePulps and Fanalytics

"""
# pulps = pd.read_csv('CGC_GRADED_PULPS.csv')
pulps = pd.read_csv('CGC_POPULATION.csv')

pulps = pulps.drop(pulps.columns[-1], axis=1)
pulps_long = pd.melt(pulps, id_vars=['ComicID', 'Title', 'Issue_Num', 'Issue_Date', 'Issue_Year', 'Publisher'
                                     , 'Country', 'ArtComments', 'KeyComments', 'Label_Category'], 
        var_name='Grade_Category', value_name='Value')
pulps_long['Grade'] = pulps_long['Grade_Category'].str.replace('POP_', '').str.replace('_', '.').astype(float)
pulps_long.drop('Grade_Category', axis=1)


# Combine Title and Publisher into a new column
pulps_long['Title_Publisher'] = pulps_long['Title'] + ' | ' + pulps_long['Publisher']

# Get unique combinations of Title and Publisher
unique_title_publisher = pulps_long['Title_Publisher'].unique()

# Function to split combined Title and Publisher
def split_title_publisher(combined_str):
    if not combined_str:
        return None, None
    elif ' | ' in combined_str:
        title, publisher = combined_str.split(' | ')
        return title.strip(), publisher.strip()
    else:
        # If the combination is not in the expected format, return None for both
        return None, None

# Define function to filter data based on selected title_publisher, issue number, and search term
def filter_data(title_publisher, issue_num, search_term):
    title, publisher = split_title_publisher(title_publisher)
    filtered_data = pulps_long[(pulps_long['Title'] == title) & (pulps_long['Publisher'] == publisher)]
    if issue_num:
        filtered_data = filtered_data[filtered_data['Issue_Num'] == issue_num]
    if search_term:
        search_term_lower = search_term.lower()
        filtered_data = filtered_data[(filtered_data['ArtComments'].str.lower().str.contains(search_term_lower, na=False)) | 
                                      (filtered_data['KeyComments'].str.lower().str.contains(search_term_lower, na=False))]
    return filtered_data

# Define function to update the bar chart based on the selected title_publisher, issue number, and search term
def update_plot(title_publisher1, title_publisher2, issue_num1, issue_num2, search_term1, search_term2):
    filtered_data1 = filter_data(title_publisher1, issue_num1, search_term1)
    filtered_data2 = filter_data(title_publisher2, issue_num2, search_term2)
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
        axes[0].bar(grade_totals1['Grade'], grade_totals1['Total Value'], width=0.4, color='skyblue', label=title_publisher1)
        axes[0].set_title(title_publisher1, fontsize=20)
        axes[0].set_xlabel('Grade', fontsize=16)
        axes[0].set_ylabel('Total Value', fontsize=16)
        axes[0].set_xticks(np.arange(11))
        axes[0].legend()
        axes[0].text(0.5, -0.25, f'Weighted Average Grade: {weighted_avg_grade1}', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
        axes[0].text(0.5, -0.30, f'Total Graded: {total_graded1}', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
    
    if not filtered_data2.empty:
        axes[1].bar(grade_totals2['Grade'], grade_totals2['Total Value'], width=0.4, color='orange', label=title_publisher2)
        axes[1].set_title(title_publisher2, fontsize=20)
        axes[1].set_xlabel('Grade', fontsize=16)
        axes[1].set_ylabel('Total Value', fontsize=16)
        axes[1].set_xticks(np.arange(11))
        axes[1].legend()
        axes[1].text(0.5, -0.25, f'Weighted Average Grade: {weighted_avg_grade2}', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
        axes[1].text(0.5, -0.30, f'Total Graded: {total_graded2}', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
    
    # Show plot
    st.pyplot(fig)

# Create widgets
col1, col2 = st.columns(2)

with col1:
    title_dropdown1 = st.selectbox('Title 1:', [''] + list(unique_title_publisher), key='title1')
    if title_dropdown1:
        title1, publisher1 = split_title_publisher(title_dropdown1)    
        filtered_issue_nums1 = pulps_long[(pulps_long['Title'] == title1) & (pulps_long['Publisher'] == publisher1)]['Issue_Num'].unique()
        issue_num_dropdown1 = st.selectbox('Issue Num for Title 1:', [''] + list(filtered_issue_nums1), key='issue_num1')
  # issue_num_dropdown1 = st.selectbox('Issue Num for Title 1:', [''], key='issue_num1')
    search_box1 = st.text_input('Search Term for Title 1:', key='search1')



with col2:
    title_dropdown2 = st.selectbox('Title 2:', [''] + list(unique_title_publisher), key='title2')
    if title_dropdown2:
        title2, publisher2 = split_title_publisher(title_dropdown2)    
        filtered_issue_nums2 = pulps_long[(pulps_long['Title'] == title2) & (pulps_long['Publisher'] == publisher2)]['Issue_Num'].unique()
        issue_num_dropdown2 = st.selectbox('Issue Num for Title 2:', [''] + list(filtered_issue_nums1), key='issue_num2')
    # issue_num_dropdown2 = st.selectbox('Issue Num for Title 2:', [''], key='issue_num2')
    search_box2 = st.text_input('Search Term for Title 2:', key='search2')

# Update plot
update_plot(title_dropdown1, title_dropdown2, issue_num_dropdown1, issue_num_dropdown2, search_box1, search_box2)
