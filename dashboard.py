import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt  # matplotlib for plotting graphs
import numpy as np 

#loading my dataset into a pandas DataFrame
url = "https://raw.githubusercontent.com/mk123x/Hate-Crimes-Dashboard-DSPL/main/Hate_Crimes_2017-2025.csv"
df = pd.read_csv(url)

#title for the Streamlit app
st.title("Hate Crime Incidents Trend Dashboard")

#markdown to describe the purpose of the dashboard and then some key stats

st.markdown("""
This interactive dashboard aims to help policymakers and researchers analyse trends in hate crimes in Austin, Texas from 2017 to 2025.
            
It visualises various aspects of hate crimes, such as incidents by offence, bias motivation, and victim age distribution.

Use the sidebar to filter by year, bias, offense type, and explore different aspects of hate crime incidents. If you don't want to use a filter, you can select "All" to view data for all available categories.

The layout of this dashboard is designed to be intuitive and easy to navigate.

Using the sidebar lets you quickly find and analyse data relevant to your needs. The clean and organised structure of the app helps you focus on the most important information, improving the experience of exploring different aspects of hate crimes in Austin.

If no data is available for the selected filters, an error message will appear.

---

### Key Statistics (2017-2025)

- **Total number of Hate Crime Incidents:** 265  
- **Victims Under 18:** 12  
- **Victims Over 18:** 268  
- **The most Common Offense:** Criminal Mischief  
- **The most Common Bias Motivation:** Anti-Black or African American
            
---
""")

# converting the 'Date of Incident' column to datetime format
df['Date of Incident'] = pd.to_datetime(df['Date of Incident'], errors='coerce')

#extracting the year and month from the 'Date of Incident' to use later for different visualisations
df['Year'] = df['Date of Incident'].dt.year
df['Month'] = df['Date of Incident'].dt.month_name()  

#the sidebar filters in my app interface
st.sidebar.title("Filters") #creating a sidebar with filters title
year_filter = st.sidebar.selectbox("Select Year", ['All'] + list(df['Year'].unique()))  # creating dropdown to select year
bias_filter = st.sidebar.selectbox("Select Bias", ['All'] + list(df['Bias'].unique())) #using selectbox function to create a dropdown menu to allows user interaction to select an option 
offense_type_filter = st.sidebar.selectbox("Select Offense Type", ['All'] + list(df['Offense(s)'].unique()))  
offense_location_filter = st.sidebar.selectbox("Select Offense Location", ['All'] + list(df['Offense Location'].unique())) 

#creating a copy of the original df to avoid making any changes to the original dataset
df_copy_for_filtering = df.copy()

#applying filters based on selections ignoring 'All' options
if year_filter != 'All':
    df_copy_for_filtering = df_copy_for_filtering[df_copy_for_filtering['Year'] == year_filter] #filters the data to only include the rows where the year column matches the year filter value, using if function so if the user select all no filter will be applied to the year column, and if they select something other than all then apply the filter
if bias_filter != 'All':
    df_copy_for_filtering = df_copy_for_filtering[df_copy_for_filtering['Bias'] == bias_filter]
if offense_type_filter != 'All':
    df_copy_for_filtering = df_copy_for_filtering[df_copy_for_filtering['Offense(s)'] == offense_type_filter]
if offense_location_filter != 'All':
    df_copy_for_filtering = df_copy_for_filtering[df_copy_for_filtering['Offense Location'] == offense_location_filter]

#function creating titles for visualisations based on the filters
def create_visualisation_title(filter_name, filter_value):
    if filter_value == 'All':
        return f"for All {filter_name}s" #if all is selected
    else:
        return f"for {filter_value} {filter_name}" #if something specific is selected that is not all

#checking if the df for filtering is empty after applying  filters
if df_copy_for_filtering.empty:
    #if theres no data in the selected filters it will display an error message to the user
    st.error("There is no data available for the selected filters. Please adjust your filter selections and try again.")
else:
    # if data is available, itll display this message summarising the filters
    st.markdown(
        f"Showing data where Bias: {bias_filter}, Year: {year_filter}, "
        f"Offence Type: {offense_type_filter}, and the Location of Offence: {offense_location_filter}"
    )

#visualisation 1- a line graph of the number of incidents over time using \n to create a new line
st.subheader(f"Number of Incidents Over Time \n"
             f"(Bias: {bias_filter}) \n"
             f"(Year: {year_filter}) \n"
             f"(Offence Type: {offense_type_filter}) \n"
             f"(Location: {offense_location_filter})")
#grouping by month and counting the number of incidents
incident_counts = df_copy_for_filtering.groupby('Month')['Incident Number'].count()
fig, ax = plt.subplots(figsize=(10, 5)) #creating the plot
ax.plot(incident_counts.index, incident_counts.values, marker='o', color='b')
#setting the title and labels
ax.set_title("Monthly Trend of Hate Crimes")
ax.set_xlabel('Month')
ax.set_ylabel('Number of Incidents')
plt.xticks(rotation=90)  # rotate the x axis labels for readability
# displaying the plot 
st.pyplot(fig)


#visualisation 2- bar chart of the distribution of victims by age group
st.subheader(f"Age distribution of Victims \n"
             f"(Bias: {bias_filter}) \n"
             f"(Year: {year_filter}) \n"
             f"(Offence Type: {offense_type_filter}) \n"
             f"(Location: {offense_location_filter})")
#group by age group and count the number of incidents
age_group_counts = df_copy_for_filtering.groupby('Number of Victims under 18')['Incident Number'].count()

#using an if else function checking if the group has data to plot and plotting a bar chart else display a message in the dashbaord
if not age_group_counts.empty: #if the dataset is not empty then plot the graph
    fig, ax = plt.subplots()
    ax.bar(age_group_counts.index, age_group_counts.values, color='pink', alpha=0.7)
    ax.set_xlabel('Age Group (Victims under 18)')
    ax.set_ylabel('Number of Incidents')
    st.pyplot(fig)
else:
    st.write("There is no victim data available for the selected filter.")


#visualisation 3 bar chart of incidents by offence type
st.subheader(f"Incidents by Offence Type \n"
             f"(Bias: {bias_filter}) \n"
             f"(Year: {year_filter}) \n"
             f"(Offence Type: {offense_type_filter}) \n"
             f"(Location: {offense_location_filter})")
#counting the number of incidents for each offense type
offense_counts = df_copy_for_filtering['Offense(s)'].value_counts()
# using an if else function checking if the group has data to plot and plotting a bar chart else display a message in the dashbaord
if not offense_counts.empty: #if not empty
    fig, ax = plt.subplots()
    ax.bar(offense_counts.index, offense_counts.values, color='purple', alpha=0.7)
    ax.set_xlabel('Offense Type')
    ax.set_ylabel('Number of Incidents')
    plt.xticks(rotation=90)  # rotate x-axis labels for readability
    st.pyplot(fig)
else:
    st.write("There is no offence data available for the selected filter.")



#visualisation 4- bar chart of incidents by offender age group
st.subheader(f"Offender Age Group Distribution \n"
             f"(Bias: {bias_filter}) \n"
             f"(Year: {year_filter}) \n"
             f"(Offence Type: {offense_type_filter}) \n"
             f"(Location: {offense_location_filter})")

#group by offender age group and count the number of incidents
offender_age_group_counts = df_copy_for_filtering.groupby('Number of Offenders under 18')['Incident Number'].count()
#create a bar chart if there is data to plot otherwise displaying an error message
if not offender_age_group_counts.empty:
    fig, ax = plt.subplots()
    ax.bar(offender_age_group_counts.index, offender_age_group_counts.values, color='orange', alpha=0.7)
    ax.set_xlabel('Age Group (Offenders under 18)')
    ax.set_ylabel('Number of Incidents')
    st.pyplot(fig)
else:
    st.write("There is no offender data available for the selected filter.")


#visualisation 5 - plot of distribution of incidents by zip code
st.subheader(f"Hate Crime incidents by Zip Code \n"
             f"(Bias: {bias_filter}) \n"
             f"(Year: {year_filter}) \n"
             f"(Offence Type: {offense_type_filter}) \n"
             f"(Location: {offense_location_filter})")
fig, ax = plt.subplots(figsize=(10, 5)) 
zip_code_counts = df_copy_for_filtering['Zip Code'].value_counts()  # count the incidents by zip code
if not zip_code_counts.empty:  # using if else function and checking if there is any data to plot
    ax.bar(zip_code_counts.index.astype(str), zip_code_counts.values, color='red', alpha=0.7)  # plotting the bar chart
    ax.set_title(f"Incidents by Zip Code {create_visualisation_title('Bias', bias_filter)}") 
    ax.set_xlabel('Zip Code') 
    ax.set_ylabel('Number of Incidents') 
    plt.xticks(rotation=90)  # rotate the x-axis labels for readability
    st.pyplot(fig)  # display the plot on the dashboard
else: #else display this error message
    st.write("There is no zip code data available for the selected filter.")  #display a message if no data is available


#visualisation 6- plot a barchart of the breakdown of incidents by bias motivation
st.subheader(f"Bias Motivation Breakdown of the number of incidents \n"
             f"(Bias: {bias_filter}) \n"
             f"(Year: {year_filter}) \n"
             f"(Offence Type: {offense_type_filter}) \n"
             f"(Location: {offense_location_filter})")
fig, ax = plt.subplots(figsize=(10, 5)) 
bias_motivation_counts = df_copy_for_filtering['Bias'].value_counts()  # this counts the occurrences of each bias motivation
if not bias_motivation_counts.empty:  
    ax.bar(bias_motivation_counts.index, bias_motivation_counts.values, color='teal', alpha=0.7)  #plot bar chart
    ax.set_title(f"Bias Motivation Breakdown {create_visualisation_title('Bias', bias_filter)}")
    ax.set_xlabel('Bias Motivation')
    ax.set_ylabel('Number of Incidents') 
    plt.xticks(rotation=90) 
    st.pyplot(fig) 
else:
    st.write("There is no data on bias motivation available for the selected filter.")  # display a message if no data is available