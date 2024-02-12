
import pandas as pd 
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Life Expectancy :)",
                   page_icon="chart_with_upwards_trend",
                   layout="wide")


st.header('Life Expectancy Analysis')
st.write(f"In this case study we are going to analyse Life Expectancy Dataset from Kaggle.We are going to compare Male and Female Life expectancy gap in each country with its increase population.")

dataset_link="https://www.kaggle.com/datasets/saimondahal/life-expectancy-trends-for-males-and-females"

st.write(f"Given below is the dataset from the Kaggle ({dataset_link}) on which we are going to work")
life_exp_df=pd.read_csv("life_expectancy.csv")

st.write("\n\n\n")
st.write("")


left_column,right_column = st.columns(2)
with left_column:
    st.subheader("Dataframe")

with right_column:
    st.subheader("Specification of Datframe")



#Drop Id from the life_exp_dataframe
life_exp_df=life_exp_df.drop(life_exp_df.columns[0],axis=1)

unique_country_list=life_exp_df['Country'].unique().tolist()

left_column,right_column = st.columns(2)
#for dataframe vizualization 
with left_column:
    #updated dataframe
    st.dataframe(life_exp_df)
#for dataframe specification 
with right_column:
    
    st.write("")# for optimal gap
    #country
    #total number of country present in dataframe
    total_country = life_exp_df.groupby('Country').size().count()
    #total_country = life_exp_df.groupby[]'Country'].nunique()
    st.write(f"Country :- Total number of countries present in the given dataset are {total_country} .")
    
    #Country code
    st.write(f"Country Code :-For uniquely identify country.Same unique values as country i.e. {total_country} .")

    #Year
    min_year=life_exp_df['Year'].min()# minimun year in dataset
    max_year = life_exp_df['Year'].max()# maximun year in dataset
    st.write(f"Year :- The given dataset holds the data from year {min_year} to {max_year} .")

    #Female Life Expectancy 
    min_female_exp = life_exp_df['Female Life Expectancy'].min()#minimum value in Female Life Expectancy column
    max_female_exp = life_exp_df['Female Life Expectancy'].max()#maximum value in Female Life Expectancy column
    st.write(f"Female Life Expectancy  :- The values of this column ranges from {min_female_exp} to { max_female_exp} .")

    #Male Life Expectancy 
    min_male_exp = life_exp_df['Male Life Expectancy'].min()#minimum value in Female Life Expectancy column
    max_male_exp = life_exp_df['Male Life Expectancy'].max()#maximum value in Female Life Expectancy column
    st.write(f"Male Life Expectancy  :- The values of this column ranges from {min_male_exp} to { max_male_exp} .")

    #Population 
    st.write(f"Population  :- This column holds values of countrie's population for each year .")

    #Life Expectancy Gap
    neg_value = life_exp_df.loc[life_exp_df['Life Expectancy Gap'] < 0, 'Life Expectancy Gap'].count()
    pos_value = life_exp_df.loc[life_exp_df['Life Expectancy Gap'] > 0, 'Life Expectancy Gap'].count()
    st.write(f"Life Expectancy Gap :- Life expectancy gap column holds {round(neg_value)} negative value and {round(pos_value)} positive values for {total_country} over the year .")


st.markdown('---')

#Subheading for graph 
st.header("Analysing the Population vs Life Expectancy gap of a country ")
st.write("")

# Function which on passing country name returns object fig which holds animated graph of countries life exp gap vs population
def individual_(country):
    temp_df=life_exp_df[life_exp_df['Country']==country]
    x_min = temp_df['Population'].min()-temp_df['Population'].min()/25
    x_max = temp_df['Population'].max()+temp_df['Population'].max()/25

    y_min = temp_df['Life Expectancy Gap'].min()-3
    y_max = temp_df['Life Expectancy Gap'].max()+3

    fig=px.scatter(temp_df,x='Population',y='Life Expectancy Gap',range_x=[x_min,x_max],range_y=[y_min,y_max],size=temp_df['Population'],color='Country',
                   animation_frame='Year',animation_group='Country',title=f"Country's Population vs Life Expectancy Gap")
    
    return fig

unique_country = life_exp_df['Country'].unique()

# Custom CSS to reduce the width of the select box
custom_css = """
    <style>
        div[data-baseweb="select"] {
            max-width: 200px;  
        }
    </style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

left_column,right_column = st.columns(2)

#This column conatins animate graph
with right_column:
    selected_country=st.selectbox("Select country ",unique_country_list,index=unique_country_list.index("Algeria"))
    custom_width = 1000
    custom_height = 1000
    figure = individual_(selected_country)
    st.plotly_chart(figure, use_container_width=False, width=custom_width, height=custom_height)

#Implementaion of graph as case study
with left_column:
    st.write("")
    st.markdown(f"##### With the help of this graph we can easily visualize change in the Life expectancy gap with respect to the population over the year .")
    st.write("")
    st.markdown("#### -->Case Study of Algeria")
    st.markdown("##### If we study the case of Algeria we can easily see the change in life expectancy gap dering (1950 - 2020). On analysing the graph we observe a sudden decrease in Life Expectancy column around 1955 and again exponential increase in life expectancy gap around 1964 .")
    st.markdown("##### On further research we learned that during that period Algeria was on war.The Algerian War (also known as the Algerian Revolution or the Algerian War of Independence)[nb 1] was a major armed conflict between France and the Algerian National Liberation Front (FLN) from 1954 to 1962, which led to Algeria winning its independence from France.[33] An important decolonization war, it was a complex conflict characterized by guerrilla warfare and war crimes. ")

st.markdown("---")



st.header("Bar Graph ")
st.write("")
st.markdown("##### To make it more easier to read the changes in Female Life Expectancy, Male Life Expectancy and Life Expectancy Gap of the country over the year")
st.markdown("##### I have enabled log function for so that Life Expectancy Gap can be seen comparable to Female Life Expectancy and Male Life expectancy")
st.write("")
#function which works on life_exp_df to plot the graph for a country which is being passed in it
def plot_bar_(country):

    #dummy df
    plot_bar_df = life_exp_df[life_exp_df['Country'] == country]

    #pdropping all other column except country,country code and population
    plot_bar_df = plot_bar_df.drop(['Country', 'Country Code', 'Population'], axis=1)
    
    #Setting Year as index for dummy df
    plot_bar_df.set_index('Year', inplace=True)

    #Apeeding value on list based on if life expectancy gap is positive or negative
    PosNeg = []
    for i in plot_bar_df['Life Expectancy Gap']:
        if i < 0:
            PosNeg.append(0)
        else:
            PosNeg.append(1)
    
    #Entering new column to determine if life expectancy gap is postitive or negative
    plot_bar_df['PosNeg'] = PosNeg

    #coverting life expectancy values to absolute value for easier plotting
    plot_bar_df['Life Expectancy Gap'] = plot_bar_df['Life Expectancy Gap'].abs()

    #ploting bar graph
    fig = px.bar(plot_bar_df, x=plot_bar_df.index, y=(['Male Life Expectancy', 'Female Life Expectancy', 'Life Expectancy Gap']), barmode='group', title=country)
    fig.update_traces(marker=dict(color=plot_bar_df['PosNeg'].map({0: 'cyan', 1: 'purple'})), selector=dict(name='Life Expectancy Gap'))
    
    # Adjust width and height of the plot
    fig.update_layout(width=1800, height=600)

    return fig

import numpy as np

#Randomly selecting country



# Create the selectbox with default value
random_country = st.selectbox("Select country", unique_country_list, index=unique_country_list.index("India"))
figure = plot_bar_(random_country)
st.plotly_chart(figure)

st.markdown("---")



#comparision between any two  country
#header for the next para
st.header("Line chart for the comparision between two countries")
st.write("")
st.markdown("###### Plotting the comparision chart between two countries on the basis of female life expectancy, male life expectancy , life expectancy gap .")
st.write("")
#Displaying two select box in which user is going to select any two countries for comparision
selectd_country_1=st.selectbox("Select 1st country",unique_country_list,index=unique_country_list.index("India"))
selectd_country_2 = st.selectbox("Select 2nd country",unique_country_list, index=unique_country_list.index("China"))

#Function to plot line chart for comparision
def comparision_(country1,country2):

    #Dataframe of the selected countries
    dummy_df_1= life_exp_df[(life_exp_df['Country'] == country1) | (life_exp_df['Country'] == country2)]
    
    #Graph plot between female life expectancy vs year
    fig1 = px.line(dummy_df_1, x="Year", y="Female Life Expectancy", color="Country", hover_name="Country",log_y=True,title="Female Life Exp vs Year")
    #Graph plot between male life expectancy vs year
    fig2 = px.line(dummy_df_1, x="Year", y="Male Life Expectancy", color="Country", hover_name="Country",log_y=True,title="Male Life Exp vs Year")
    #Graph plot between life expectancy gap vs year 
    fig3 = px.line(dummy_df_1, x="Year", y="Life Expectancy Gap", color="Country", hover_name="Country",title="Life Exp Gapvs Year")

    #return figures
    return fig1,fig2,fig3

#figure1, figure2 ,figure3 holds the values after return 
figure1,  figure2, figure3 = comparision_(selectd_country_1,selectd_country_2)

#three column for displaying graph
left_column,middle_column,right_column=st.columns(3)

#Displaying graph in three column
with left_column:
    figure1
with middle_column:
    figure2
with right_column:
    figure3
    

st.markdown("##### We can easily see progress in Female life expectancy, Male life Expectancy and Life expectancy gap over the year")
st.markdown("*Female and Male life expectancy values for china in 1950 is not given in dataset*")

st.markdown("---")

# dummy = life_exp_df[life_exp_df['Country'] == "India"]
# st.plotly_chart(px.histogram(dummy,x="Year",y=["Male Life Expectancy","Female Life Expectancy"]))
st.header('Plot for male/female life expectancy of all country') 

def plot_mean_life_expectancy():
    # Group the DataFrame by year and calculate the mean life expectancy for males and females
    mean_life_exp_df = life_exp_df.groupby('Year').agg({'Male Life Expectancy': 'mean', 'Female Life Expectancy': 'mean'}).reset_index()
    
    # Plot the mean life expectancy using Plotly Express
    fig = px.line(mean_life_exp_df, x='Year', y=['Male Life Expectancy', 'Female Life Expectancy'], title='Mean Life Expectancy Over the Years')
    
    return fig

# Call the function to get the plot
figure = plot_mean_life_expectancy()

# Display the plot using Streamlit
st.plotly_chart(figure)

st.header("Ploting the histogram ")
st.write("")
selected_country_hist =st.selectbox('Select Country',unique_country_list)

def histo_country(country):

    
        dummy = life_exp_df[life_exp_df["Country"] == country].drop(['Country Code','Population'],axis=1)
        st.dataframe(dummy)

    

    
        st.plotly_chart(px.histogram(dummy,x='Year',y=['Female Life Expectancy','Male Life Expectancy'],title=f'Histograme of Male/Female Life Expectancy of {country}',nbins=145,barmode='group',width=1600,height=600))
    

histo_country(selected_country_hist)

#Plotting a bubble map using plotly express
st.markdown("---")

st.header("Visualizing the male life expectancy in world graph")

left_column,right_column = st.columns(2)

with left_column:
    df=life_exp_df

    df_sorted = df.sort_values('Year')

    fig = px.scatter_geo(df_sorted,
                    locations = 'Country',
                    locationmode = 'country names', 
                    color = 'Male Life Expectancy',
                    color_continuous_scale = 'viridis',
                    hover_name = 'Country',
                    size = "Male Life Expectancy",
                    projection = "natural earth",
                    animation_frame = 'Year',
                    title='Male Life Expectancy')

    #show plot
    st.plotly_chart(fig)

with right_column:
    df=life_exp_df

    df_sorted = df.sort_values('Year')

    fig = px.scatter_geo(df_sorted,
                    locations = 'Country',
                    locationmode = 'country names', 
                    color = 'Female Life Expectancy',
                    color_continuous_scale = 'viridis',
                    hover_name = 'Country',
                    size = "Female Life Expectancy",
                    projection = "natural earth",
                    animation_frame = 'Year',
                    title='Female Life Expectancy')

    #show plot
    st.plotly_chart(fig)








