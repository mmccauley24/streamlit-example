import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
import seaborn as sns
import datetime
import matplotlib.pyplot as plt
from ipywidgets import interact, Dropdown, widgets, VBox, HBox, Layout, interactive

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

def plot_weighted_avg_grade_by_year(title):
    # Filter data by selected title
    if title != 'All':
        filtered_data_title = filtered_data[filtered_data['Title'] == title]
    else:
        filtered_data_title = filtered_data
    
    # Calculate weighted average grade by year
    weighted_avg_grade = filtered_data_title.groupby('Issue_Year').apply(lambda x: np.average(x['Grade'], weights=x['Value'])).reset_index()
    weighted_avg_grade.columns = ['Issue_Year', 'Weighted_Avg_Grade']
    
    # Calculate count of graded values per year
    graded_count = filtered_data_title.groupby('Issue_Year').size().reset_index(name='Graded_Count')
    
    # Merge weighted average grade and graded count
    plot_data = weighted_avg_grade.merge(graded_count, on='Issue_Year')
    
    # Create plot
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='Issue_Year', y='Weighted_Avg_Grade', size='Graded_Count', data=plot_data, sizes=(50, 2000), legend='brief', marker='o')
    plt.title('Weighted Average Grade by Year')
    plt.xlabel('Issue Year')
    plt.ylabel('Weighted Average Grade')
    plt.grid(True)
    st.pyplot()

# Get unique titles for dropdown options
titles = ['All'] + filtered_data['Title'].unique().tolist()

# Create Streamlit app
st.title('Weighted Average Grade by Year')
selected_title = st.selectbox('Select Title:', titles)
plot_weighted_avg_grade_by_year(selected_title)

"""
num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))
"""
