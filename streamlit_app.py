import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Read data
pulps = pd.read_csv('CGC_POPULATION.csv')

# Melt data
pulps_long = pd.melt(pulps, id_vars=['ComicID', 'Title', 'Issue_Num', 'Issue_Date', 'Issue_Year', 'Publisher',
                                      'Country', 'ArtComments', 'KeyComments', 'Label_Category'],
                     var_name='Grade_Category', value_name='Value')
pulps_long['Grade'] = pulps_long['Grade_Category'].str.replace('POP_', '').str.replace('_', '.').astype(float)
pulps_long.drop('Grade_Category', axis=1, inplace=True)

# Combine Title and Publisher into a new column
pulps_long['Title_Publisher'] = pulps_long['Title'] + ' | ' + pulps_long['Publisher']

# Get unique combinations of Title and Publisher
unique_title_publisher = pulps_long['Title_Publisher'].unique()

# Function to filter data based on selected title, publisher, issue number, and search term
def filter_data(title_publisher, issue_num, search_term):
    if title_publisher:
        title, publisher = split_title_publisher(title_publisher)
        filtered_data = pulps_long[(pulps_long['Title'] == title) & (pulps_long['Publisher'] == publisher)]
        if issue_num:
            filtered_data = filtered_data[filtered_data['Issue_Num'] == issue_num]
        if search_term:
            search_term_lower = search_term.lower()
            filtered_data = filtered_data[(filtered_data['ArtComments'].str.lower().str.contains(search_term_lower, na=False)) |
                                          (filtered_data['KeyComments'].str.lower().str.contains(search_term_lower, na=False))]
        return filtered_data
    else:
        return pulps_long

# Define function to split combined Title and Publisher
def split_title_publisher(combined_str):
    if not combined_str:
        return None, None
    elif ' | ' in combined_str:
        title, publisher = combined_str.split(' | ')
        return title.strip(), publisher.strip()
    else:
        # If the combination is not in the expected format, return None for both
        return None, None

# Define function to update the bar chart based on the selected title, publisher, issue number, and search term
def update_plot(title_publisher1, title_publisher2, issue_num1, issue_num2, search_term1, search_term2):
    filtered_data1 = filter_data(title_publisher1, issue_num1, search_term1)
    filtered_data2 = filter_data(title_publisher2, issue_num2, search_term2)
    
    if filtered_data1.empty and filtered_data2.empty:
        st.write("No data to display.")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    if not filtered_data1.empty:
        grade_totals1 = filtered_data1.groupby('Grade')['Value'].sum().reset_index(name='Total Value')
        axes[0].bar(grade_totals1['Grade'], grade_totals1['Total Value'], width=0.4, color='skyblue', label=title_publisher1)
        axes[0].set_title(title_publisher1, fontsize=20)
        axes[0].set_xlabel('Grade', fontsize=16)
        axes[0].set_ylabel('Total Value', fontsize=16)
        axes[0].set_xticks(np.arange(11))
        axes[0].legend()
    
    if not filtered_data2.empty:
        grade_totals2 = filtered_data2.groupby('Grade')['Value'].sum().reset_index(name='Total Value')
        axes[1].bar(grade_totals2['Grade'], grade_totals2['Total Value'], width=0.4, color='orange', label=title_publisher2)
        axes[1].set_title(title_publisher2, fontsize=20)
        axes[1].set_xlabel('Grade', fontsize=16)
        axes[1].set_ylabel('Total Value', fontsize=16)
        axes[1].set_xticks(np.arange(11))
        axes[1].legend()
    
    st.pyplot(fig)

# Create widgets
col1, col2 = st.columns(2)

with col1:
    title_dropdown1 = st.selectbox('Title 1:', [''] + list(unique_title_publisher))
    if title_dropdown1:
        title1, publisher1 = split_title_publisher(title_dropdown1)
        issue_num_dropdown1 = st.selectbox('Issue Num for Title 1:', [''] + pulps_long.loc[(pulps_long['Title'] == title1) & (pulps_long['Publisher'] == publisher1), 'Issue_Num'].unique())
    else:
        issue_num_dropdown1 = st.selectbox('Issue Num for Title 1:', [''])
    search_box1 = st.text_input('Search Term for Title 1:')

with col2:
    title_dropdown2 = st.selectbox('Title 2:', [''] + list(unique_title_publisher))
    if title_dropdown2:
        title2, publisher2 = split_title_publisher(title_dropdown2)
        issue_num_dropdown2 = st.selectbox('Issue Num for Title 2:', [''] + pulps_long.loc[(pulps_long['Title'] == title2) & (pulps_long['Publisher'] == publisher2), 'Issue_Num'].unique())
    else:
        issue_num_dropdown2 = st.selectbox('Issue Num for Title 2:', [''])
    search_box2 = st.text_input('Search Term for Title 2:')

# Update plot
update_plot(title_dropdown1, title_dropdown2, issue_num_dropdown1, issue_num_dropdown2, search_box1, search_box2)
