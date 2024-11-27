!pip install -r requirements.txt

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.express import treemap
from wordcloud import WordCloud
# Main heading in centre of the page with a title "Unstop Market Trend Analytics"
st.title("Unstop Market Trend Analytics") 
# A small heading under it on centre of the page with a title "By Group 8 - BDA 2024"
st.header("By Group 8 - BDA 2024")
# A subheading under it on centre of the page with a title "BML Munjal University"
st.subheader("BML Munjal University")


# Load data
hackathon_data = pd.read_csv('../Preprocessed_files/cleaned_hackathons.csv')
job_data = pd.read_csv('../Preprocessed_files/cleaned_jobs.csv')

# Streamlit app
st.title("Data Visualizations for Hackathons and Jobs")

# Hackathons Section
st.header("Hackathons")

# Heatmap: Correlation Between Numeric Variables
st.subheader("1. Heatmap: Correlation Between Numeric Variables")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    hackathon_data[['Applied', 'Impressions', 'Application Deadline']].corr(),
    annot=True, cmap='viridis', linewidths=0.5, fmt=".2f", ax=ax
)
ax.set_title('Correlation Heatmap of Event Metrics', fontsize=18, fontweight='bold')
st.pyplot(fig)

# Bar Chart: Most Active Organizations
st.subheader("2. Bar Chart: Most Active Organizations")
org_counts = hackathon_data['Organisations'].value_counts().head(10)
fig = px.bar(
    org_counts, x=org_counts.values, y=org_counts.index, orientation='h',
    title='Top 10 Organizations Hosting Events', labels={'x': 'Number of Events', 'y': 'Organizations'}
)
st.plotly_chart(fig)

# Treemap: Event Categories
st.subheader("3. Treemap: Event Categories")
excluded_labels = ["undergraduate", "engineering students", "postgraduate", "all", "mba students", "school students", "awards"]
category_counts = (
    hackathon_data['Category']
    .str.split(', ')
    .explode()
    .str.strip()
    .loc[lambda x: ~x.str.lower().isin(excluded_labels)]
    .value_counts()
)
category_counts_df = category_counts.reset_index()
category_counts_df.columns = ['Category', 'Count']
fig = px.treemap(
    category_counts_df, path=['Category'], values='Count',
    title='Event Category Distribution (Filtered)', color='Count', color_continuous_scale='Viridis'
)
st.plotly_chart(fig)

# Bubble Plot: Impressions vs Applications
st.subheader("4. Bubble Plot: Impressions vs Applications")
hackathon_data['Application Deadline'] = pd.to_datetime(hackathon_data['Application Deadline'], errors='coerce')
hackathon_data['Application Deadline (days)'] = (hackathon_data['Application Deadline'] - hackathon_data['Application Deadline'].min()).dt.days
fig = px.scatter(
    hackathon_data, x="Impressions", y="Applied", size="Application Deadline (days)", color="Region",
    hover_name="Title", title="Impressions vs Applications (Bubble Plot by Region)", size_max=60,
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.update_layout(
    title_font_size=22, xaxis_title="Impressions", yaxis_title="Applications", legend_title="Region", template="plotly_white"
)
fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgray")
fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgray")
st.plotly_chart(fig)

# Pie Chart: Online vs Offline Events
st.subheader("5. Pie Chart: Online vs Offline Events")
region_counts = hackathon_data['Region'].value_counts()
fig = px.pie(
    values=region_counts.values, names=region_counts.index, title='Online vs Offline Events',
    color_discrete_sequence=['#ff9999', '#66b3ff']
)
st.plotly_chart(fig)

# Word Cloud: Event Categories
st.subheader("6. Word Cloud: Event Categories")
text = " ".join(hackathon_data['Category'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='tab10', contour_width=1, contour_color='black').generate(text)
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
ax.set_title('Word Cloud of Event Categories', fontsize=18, fontweight='bold')
st.pyplot(fig)

# Time Series: Events Over Time
st.subheader("7. Time Series: Events Over Time")
hackathon_data['Uploaded On'] = pd.to_datetime(hackathon_data['Uploaded On'], errors='coerce')
monthly_counts = hackathon_data['Uploaded On'].dt.to_period('M').value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=monthly_counts.index.astype(str), y=monthly_counts.values, marker='o', color='blue', ax=ax)
ax.set_title('Trend of Uploaded Events Over Time', fontsize=18, fontweight='bold')
ax.set_xlabel('Month', fontsize=14)
ax.set_ylabel('Number of Events', fontsize=14)
ax.tick_params(axis='x', rotation=45)
ax.grid()
st.pyplot(fig)

# 3D Scatter Plot: Impressions vs Applications with Application Deadline
st.subheader("8. 3D Scatter Plot: Impressions vs Applications with Application Deadline")
fig = go.Figure(
    data=go.Scatter3d(
        x=hackathon_data['Impressions'], y=hackathon_data['Applied'], z=hackathon_data['Application Deadline (days)'],
        mode='markers', marker=dict(size=10, color=hackathon_data['Application Deadline (days)'], colorscale='Viridis', opacity=0.8),
        text=hackathon_data['Title']
    )
)
fig.update_layout(
    title="3D Scatter: Impressions vs Applications vs Deadline",
    scene=dict(xaxis_title='Impressions', yaxis_title='Applications', zaxis_title='Application Deadline (days)'),
    template='plotly_white'
)
st.plotly_chart(fig)

# Sunburst Chart: Hierarchical Breakdown of Categories and Regions
st.subheader("9. Sunburst Chart: Hierarchical Breakdown of Categories and Regions")
fig = px.sunburst(
    hackathon_data, path=['Region', 'Category'], values='Impressions', color='Impressions',
    color_continuous_scale='Blues', title="Sunburst Chart: Event Categories by Region"
)
fig.update_layout(title_font_size=22)
st.plotly_chart(fig)

# Heatmap of Application Trends Over Time
st.subheader("10. Heatmap of Application Trends Over Time")
hackathon_data['Uploaded Month'] = hackathon_data['Uploaded On'].dt.to_period('M')
heatmap_data = hackathon_data.groupby(['Uploaded Month', 'Region'])['Applied'].sum().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5, ax=ax)
ax.set_title('Applications Trends by Month and Region', fontsize=18, fontweight='bold')
ax.set_xlabel('Region', fontsize=14)
ax.set_ylabel('Month', fontsize=14)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Jobs Section
st.header("Jobs")

# Job Opportunities by Company
st.subheader("1. Job Opportunities by Company")
top_companies = job_data['Company'].value_counts().head(10)
fig = px.bar(
    top_companies, x=top_companies.values, y=top_companies.index, orientation='h',
    title='Top 10 Companies by Job Opportunities', labels={'x': 'Number of Opportunities', 'y': 'Company'},
    color=top_companies.values, color_continuous_scale='cividis'
)
st.plotly_chart(fig)

# Jobs by Location
st.subheader("2. Jobs by Location")
location_counts = job_data['Location'].value_counts().head(10)
fig = px.pie(
    values=location_counts.values, names=location_counts.index, title='Top 10 Locations for Job Opportunities',
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig)

# Eligibility Criteria Analysis
st.subheader("3. Eligibility Criteria Analysis")
eligibility_counts = job_data['Eligibility'].str.split(',').explode().value_counts()
top_eligibility = eligibility_counts.head(10)
fig = px.bar(
    top_eligibility, x=top_eligibility.values, y=top_eligibility.index, orientation='h',
    title='Top 10 Eligibility Criteria for Job Opportunities', labels={'x': 'Number of Opportunities', 'y': 'Eligibility Criteria'},
    color=top_eligibility.values, color_continuous_scale='viridis'
)
st.plotly_chart(fig)

# Job Status Distribution
st.subheader("4. Job Status Distribution")
status_counts = job_data['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
fig = px.pie(
    status_counts, values='Count', names='Status', title='Job Status Distribution', hole=0.4,
    color_discrete_sequence=px.colors.sequential.Greens
)
st.plotly_chart(fig)

# Sunburst Chart of Job Opportunities by Company and Status
st.subheader("5. Sunburst Chart of Job Opportunities by Company and Status")
fig = px.sunburst(
    job_data, path=['Company', 'Status'], values='Applied', title='Sunburst Chart of Job Opportunities by Company and Status',
    template='plotly_white'
)
st.plotly_chart(fig)

# Heatmap of Job Applications by Location and Opportunity Type
st.subheader("6. Heatmap of Job Applications by Location and Opportunity Type")
heatmap_data = job_data.groupby(['Location', 'Opportunity Type'])['Applied'].sum().reset_index()
fig = px.density_heatmap(
    heatmap_data, x='Location', y='Opportunity Type', z='Applied', title='Heatmap of Job Applications by Location and Opportunity Type',
    color_continuous_scale='Viridis'
)
fig.update_layout(xaxis_title='Location', yaxis_title='Opportunity Type', template='plotly_white')
st.plotly_chart(fig)

# Treemap of Job Opportunities by Company and Opportunity Type
st.subheader("7. Treemap of Job Opportunities by Company and Opportunity Type")

# Clean and preprocess data
job_data['Uploaded On'] = pd.to_datetime(job_data['Uploaded On'])
job_data['Application Deadline'] = pd.to_datetime(job_data['Application Deadline'], errors='coerce')
job_data['Impressions'] = pd.to_numeric(job_data['Impressions'], errors='coerce')
job_data['Applied'] = pd.to_numeric(job_data['Applied'], errors='coerce')

# Drop rows with NaN values in critical columns
job_data.dropna(subset=['Company', 'Opportunity Type', 'Applied'], inplace=True)

# Create a treemap of job opportunities by company and opportunity type
fig = px.treemap(
    job_data, path=['Company', 'Opportunity Type'], values='Applied',
    title='Treemap of Job Opportunities by Company and Opportunity Type',
    template='plotly_white'
)
st.plotly_chart(fig)

# Word Cloud for Job Positions
st.subheader("8. Word Cloud for Job Positions")
position_text = ' '.join(job_data['Position'].tolist())
wordcloud_positions = WordCloud(width=800, height=400, background_color='white').generate(position_text)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud_positions, interpolation='bilinear')
ax.axis('off')
ax.set_title('Word Cloud for Job Positions', fontsize=16)
st.pyplot(fig)

# Word Cloud for Companies
st.subheader("9. Word Cloud for Companies")
company_text = ' '.join(job_data['Company'].tolist())
wordcloud_companies = WordCloud(width=800, height=400, background_color='white').generate(company_text)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud_companies, interpolation='bilinear')
ax.axis('off')
ax.set_title('Word Cloud for Companies', fontsize=16)
st.pyplot(fig)

# Word Cloud for Eligibility Criteria
st.subheader("10. Word Cloud for Eligibility Criteria")

# Generate a word cloud for eligibility criteria
eligibility_text = ' '.join(job_data['Eligibility'].dropna().tolist())
wordcloud_eligibility = WordCloud(width=800, height=400, background_color='white').generate(eligibility_text)

# Display the word cloud for eligibility criteria
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud_eligibility, interpolation='bilinear')
ax.axis('off')  # Turn off axis
ax.set_title('Word Cloud for Eligibility Criteria', fontsize=16)
st.pyplot(fig)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud

# Load the dataset
internship_data = pd.read_csv("../Preprocessed_files/cleaned_internship.csv")

# Preprocessing steps
# Convert date columns to datetime format
internship_data['Uploaded On'] = pd.to_datetime(internship_data['Uploaded On'], errors='coerce')

# Drop unnecessary or empty columns
data_cleaned = internship_data.drop(columns=['Location', 'Link'])

# Check for missing values and handle them
# We'll drop rows with missing numerical values for simplicity
data_cleaned = data_cleaned.dropna(subset=['Impressions', 'Applied', 'Application Deadline'])

# Setting plot style
sns.set_theme(style="whitegrid", palette="muted")

# Streamlit app
st.title("Internship Data Visualizations")

# Visualization 1: Top 10 internship roles by impressions and applications
st.subheader("1. Top 10 Internship Roles by Impressions and Applications")
top_roles = data_cleaned.groupby('Position')[['Impressions', 'Applied']].sum().sort_values(by='Impressions', ascending=False).head(10)
fig, ax1 = plt.subplots(figsize=(12, 6))
top_roles.plot(kind='bar', ax=ax1)
plt.title('Top 10 Internship Roles by Impressions and Applications', fontsize=16)
plt.xlabel('Internship Role', fontsize=12)
plt.ylabel('Counts', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

# Visualization 2: Companies posting the most internships
st.subheader("2. Top 10 Companies by Number of Internships Posted")
top_companies = data_cleaned['Company'].value_counts().head(10)
fig, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_companies.values, y=top_companies.index, palette="viridis", ax=ax2)
plt.title('Top 10 Companies by Number of Internships Posted', fontsize=16)
plt.xlabel('Number of Internships', fontsize=12)
plt.ylabel('Company', fontsize=12)
plt.tight_layout()
st.pyplot(fig)

# Visualization 3: Status Breakdown
st.subheader("3. Internship Status Distribution")
status_count = data_cleaned['Status'].value_counts()
fig, ax3 = plt.subplots(figsize=(6, 6))
ax3.pie(status_count, labels=status_count.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
plt.title('Internship Status Distribution', fontsize=16)
plt.tight_layout()
st.pyplot(fig)

# Visualization 4: Most common eligibility criteria
st.subheader("4. Most Common Eligibility Criteria")
eligibility_split = data_cleaned['Eligibility'].str.split(', ', expand=True).stack().value_counts().head(10)
fig, ax4 = plt.subplots(figsize=(12, 6))
sns.barplot(y=eligibility_split.index, x=eligibility_split.values, palette="mako", ax=ax4)
plt.title('Most Common Eligibility Criteria', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Eligibility Criteria', fontsize=12)
plt.tight_layout()
st.pyplot(fig)

# Visualization 5: Heatmap for numerical columns
st.subheader("5. Correlation Heatmap")
numerical_cols = data_cleaned[['Impressions', 'Applied', 'Application Deadline']]
fig, ax5 = plt.subplots(figsize=(8, 6))
sns.heatmap(numerical_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax5)
plt.title('Correlation Heatmap', fontsize=16)
plt.tight_layout()
st.pyplot(fig)

# Visualization 6: Word Cloud for Internship Positions
st.subheader("6. Word Cloud of Internship Positions")
positions = ' '.join(data_cleaned['Position'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(positions)
fig, ax6 = plt.subplots(figsize=(10, 5))
ax6.imshow(wordcloud, interpolation='bilinear')
ax6.axis('off')
plt.title('Word Cloud of Internship Positions', fontsize=16)
plt.tight_layout()
st.pyplot(fig)

# Visualization 7: Treemap for Company-wise Activity
st.subheader("7. Treemap of Top 15 Companies by Internship Posts")
company_counts = data_cleaned['Company'].value_counts().head(15).reset_index()
company_counts.columns = ['Company', 'Post Count']
fig = px.treemap(
    company_counts,
    path=['Company'],
    values='Post Count',
    title="Treemap of Top 15 Companies by Internship Posts",
    color='Post Count',
    color_continuous_scale='Viridis',
    hover_data={'Post Count': True}
)
fig.update_traces(
    textinfo="label+value+percent entry",
    marker=dict(cornerradius=5)
)
fig.update_layout(
    title_font_size=16,
    margin=dict(t=50, l=25, r=25, b=25),
    template="plotly_white"
)
st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
internship_Scraped_data = pd.read_csv('../scraped_internships.csv')

# Streamlit app
st.title("Internship Data Visualizations")

# Visualization 8: Bubble Chart for Impressions, Applications, and Deadline
st.subheader("8. Bubble Chart: Impressions vs Applications (Bubble Size: Deadline)")
bubble_data = internship_Scraped_data[['Impressions', 'Applied', 'Application Deadline']].dropna()
bubble_data['Deadline (days)'] = pd.to_numeric(bubble_data['Application Deadline'], errors='coerce')

# Drop rows with NaN values in 'Deadline (days)'
bubble_data = bubble_data.dropna(subset=['Deadline (days)'])

fig = px.scatter(
    bubble_data,
    x='Impressions',
    y='Applied',
    size='Deadline (days)',
    color='Deadline (days)',
    hover_data=['Impressions', 'Applied', 'Deadline (days)'],
    title="Bubble Chart: Impressions vs Applications (Bubble Size: Deadline)",
    color_continuous_scale=px.colors.sequential.Viridis
)

fig.update_layout(
    xaxis_title="Impressions",
    yaxis_title="Applications",
    template="plotly_white",
    coloraxis_colorbar=dict(title="Deadline (days)")
)

st.plotly_chart(fig)

# Visualization 9: Sunburst Chart for Eligibility Breakdown
st.subheader("9. Sunburst Chart of Eligibility Criteria")
eligibility_hierarchy = data_cleaned['Eligibility'].str.split(', ', expand=True).stack().value_counts()
sunburst_data = pd.DataFrame({
    'Eligibility': eligibility_hierarchy.index,
    'Count': eligibility_hierarchy.values
})
fig = px.sunburst(
    sunburst_data, path=['Eligibility'], values='Count',
    color='Count', color_continuous_scale='viridis', title='Sunburst Chart of Eligibility Criteria'
)
st.plotly_chart(fig)
