import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_option_menu import option_menu as op
import plotly.express as px
import requests
import json

def get_db_connection():
    connection = mysql.connector.connect(
        host = 'localhost',
        port = '3306',
        user = 'root',
        password = '1234',
        database = 'phonepe'
    )
    return connection

def fetch_all_data_from_table(query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

table1 = fetch_all_data_from_table("SELECT * FROM aggregated_insurance")
agg_insurance_df = pd.DataFrame(table1)

table2 = fetch_all_data_from_table("SELECT * FROM aggregated_transactions")
agg_transactions_df = pd.DataFrame(table2)

table3 = fetch_all_data_from_table("SELECT * FROM aggregated_user")
agg_user_df = pd.DataFrame(table3)

table4 = fetch_all_data_from_table("SELECT * FROM map_insurance")
map_insurance_df = pd.DataFrame(table4)

table5 = fetch_all_data_from_table("SELECT * FROM map_transaction")
map_transactions_df = pd.DataFrame(table5)

table6 = fetch_all_data_from_table("SELECT * FROM map_user")
map_user_df = pd.DataFrame(table6)

table7 = fetch_all_data_from_table("SELECT * FROM top_insurance")
top_insurance_df = pd.DataFrame(table7)

table8 = fetch_all_data_from_table("SELECT * FROM top_transaction")
top_transactions_df = pd.DataFrame(table8)

table9 = fetch_all_data_from_table("SELECT * FROM top_user")
top_user_df = pd.DataFrame(table9)

def main():    
    st.title("Phonepe Pulse Data Visualization and Exploration")
    st.markdown("""
    ## Project Overview
    This project aims to create a user-friendly tool for visualizing and exploring data from the Phonepe Pulse GitHub repository using Streamlit and Plotly. The main objectives include:
    
    - Extracting data from the Phonepe Pulse GitHub repository.
    - Transforming and cleaning the data.
    - Storing the data in a MySQL database.
    - Creating an interactive dashboard with geo-visualizations.
    - Providing various dropdown options for users to select different metrics.
    
    ## Technologies Used
    - **Python**
    - **Pandas**
    - **MySQL**
    - **mysql-connector-python**
    - **Streamlit**
    - **Plotly**
    
    ## Domain
    - Fintech
    
    ## Problem Statement
    The Phonepe Pulse GitHub repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data, process it, and visualize it in an interactive and user-friendly manner.
    """)
    
    st.markdown("""

    ## Dataset
    The dataset for this project is sourced from the [Phonepe Pulse GitHub repository](https://github.com/PhonePe/pulse#readme).
    """)

def agg_insurance_year(df, year):
    data = df[df['Year'] == year]
    data.reset_index(drop=True, inplace=True)
    group_data = data.groupby('States')[['Insurance_count', 'Insurance_amount']].sum()
    group_data.reset_index(inplace=True)
    return group_data

def agg_insurance_quarter(df, quarter):
    data = df[df['Quarter'] == quarter]
    data.reset_index(drop=True, inplace=True)
    group_data = data.groupby('States')[['Insurance_count', 'Insurance_amount']].sum()
    group_data.reset_index(inplace=True)
    return group_data

def display_visualizations(group_data, metric, title, color_scale, col):
    fig = px.bar(group_data, x='States', y=metric, title=title, width=600, height=600, color_discrete_sequence=color_scale)
    col.plotly_chart(fig)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data = json.loads(response.content)

    fig = px.choropleth(
        group_data, geojson=data, locations="States", 
        featureidkey='properties.ST_NM', color=metric, 
        color_continuous_scale='Sunsetdark', 
        range_color=(group_data[metric].min(), group_data[metric].max()), 
        hover_name="States", title=title, 
        fitbounds="locations", width=600, height=600
    )
    fig.update_geos(visible=False)
    col.plotly_chart(fig)

def agg_transaction_year(df, year):
    data = df[df['Year'] == year]
    data.reset_index(drop=True, inplace=True)
    group_data = data.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
    group_data.reset_index(inplace=True)
    return group_data

def agg_transaction_quarter(df, quarter):
    data = df[df['Quarter'] == quarter]
    data.reset_index(drop=True, inplace=True)
    group_data = data.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
    group_data.reset_index(inplace=True)
    return group_data



def Agg_user_year(df, year):
    data = df[df['Year']==year]
    data.reset_index(drop=True, inplace=True)

    group_data = data.groupby('States')[['Brand', 'Transaction_count']].sum()
    group_data.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(group_data, x='States', y='Brand', title=f'{year} Brand', width=600, height=600, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig1)
    with col2:
        fig2 = px.bar(group_data, x='States', y='Transaction_count', title=f'{year} Transaction Count', width=600, height=600, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig2)
    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)  
        data = json.loads(response.content)
        states = [feature['properties']['ST_NM'] for feature in data['features']]
        states.sort()

        fig3 = px.choropleth(group_data, geojson=data, locations="States", featureidkey='properties.ST_NM', color='Brand', color_continuous_scale='Sunsetdark', range_color=(group_data['Brand'].min(), group_data['Brand'].max()), hover_name="States", title=f"{year} Brand", fitbounds="locations", width=600, height=600)
        fig3.update_geos(visible= False)
        st.plotly_chart(fig3)
    with col2:
        fig4 = px.choropleth(group_data, geojson=data, locations="States", featureidkey='properties.ST_NM', color='Transaction_count', color_continuous_scale='Sunsetdark', range_color=(group_data['Transaction_count'].min(), group_data['Transaction_count'].max()), hover_name="States", title=f"{year} Transaction Count", fitbounds="locations", width=600, height=600)
        fig4.update_geos(visible= False)
        st.plotly_chart(fig4)
    return data
def Agg_user_quarter(df, quarter):
    data = df[df['Quarter']==quarter]
    data.reset_index(drop=True, inplace=True)

    group_data = data.groupby('States')[['Brand', 'Transaction_count']].sum()
    group_data.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(group_data, x='States', y='Brand', title=f'{data['Year'].min()} and {quarter} Brand', width=600, height=600, color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig1)
    with col2:
        fig2 = px.bar(group_data, x='States', y='Transaction_count', title=f'{data['Year'].min()} and {quarter} Transaction Count', width=600, height=600, color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig2)
    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)  
        data = json.loads(response.content)
        states = [feature['properties']['ST_NM'] for feature in data['features']]
        states.sort()

        fig3 = px.choropleth(group_data, geojson=data, locations="States", 
                             featureidkey='properties.ST_NM', 
                             color='Transaction_amount', 
                             color_continuous_scale='Sunsetdark', 
                             range_color=(group_data['Brand'].min(), group_data['Brand'].max()), 
                             hover_name="States", 
                             title=f"{quarter} Brand", 
                             fitbounds="locations", width=600, height=600)
        fig3.update_geos(visible= False)
        st.plotly_chart(fig3)
    with col2:
        fig4 = px.choropleth(group_data, geojson=data, locations="States", 
                             featureidkey='properties.ST_NM', 
                             color='Transaction_count', 
                             color_continuous_scale='Sunsetdark', 
                             range_color=(group_data['Transaction_count'].min(), group_data['Transaction_count'].max()), 
                             hover_name="States", 
                             title=f"{quarter} Transaction Count", 
                             fitbounds="locations", width=600, height=600)
        fig4.update_geos(visible= False)
        st.plotly_chart(fig4)
    return data
def bar_pie_chart(df, x, y, state, year, quarter):
    bar_fig = px.bar(df, x=x, y=y, title= f'{x} vs {y} in {state} (Y {year} Q {quarter})')
    bar_fig.update_layout(xaxis_type='category')
    st.plotly_chart(bar_fig)
    pie_fig = px.pie(df, names=x, values=y,title=f'{y} for {x} in {state} ({year} Q{quarter})')
    st.plotly_chart(pie_fig)

def create_charts(df, x, y1, y2=None, prefix=""):
    col1, col2, col3 = st.columns(3)
    with col1:
        state = st.selectbox('Select State', df['State'].unique(), key=f'{prefix}_state')
    with col2:
        year = st.slider('Select Year', df['Year'].min(), df['Year'].max(), df['Year'].min(), key=f'{prefix}_year1')
    with col3:
        quarter = st.slider('Select Quarter', df['Quarter'].min(), df['Quarter'].max(), df['Quarter'].min(), key=f'{prefix}_quarter1')
    filtered_df = df[(df['Year']== year) & (df['Quarter']== quarter) & (df['State']== state)]

    if(y2):
        col1, col2 = st.columns(2)
        with col1:
            bar_pie_chart(filtered_df, x, y1, state, year, quarter)
        with col2:
            bar_pie_chart(filtered_df, x, y2, state, year, quarter)
    else:
        bar_pie_chart(filtered_df, x, y1, state, year, quarter)

def show_visualization(question):
    if question == "q1":
        df3 = agg_insurance_df.groupby('Year').sum().reset_index()[['Year', 'Insurance_count']]
        df4 = agg_insurance_df.groupby('Year').sum().reset_index()[['Year', 'Insurance_amount']]
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(df3, x='Year', y='Insurance_count', title='Total Insurance Count from 2018 to 2022')
            st.plotly_chart(fig1)
            st.dataframe(df3)
        with col2:
            fig2 = px.line(df4, x='Year', y='Insurance_amount', title='Total Insurance Amount from 2018 to 2022')
            st.plotly_chart(fig2)
            st.dataframe(df4)
    
    elif question == "q2":
        df5 = agg_transactions_df.groupby('States').sum().reset_index().sort_values(by='Transaction_count', ascending=False)[['States', 'Transaction_count']].head(10)
        fig = px.bar(df5, x='States', y='Transaction_count', title='States with Highest Transaction Counts')
        st.plotly_chart(fig)
        st.dataframe(df5)
    
    elif question == "q3":
        top_brands_df = agg_user_df.groupby('Brand').agg({'Transaction_count': 'sum'}).reset_index().sort_values('Transaction_count', ascending=False)
        fig = px.bar(top_brands_df, x='Brand', y='Transaction_count', title='Top Brands Used')
        st.plotly_chart(fig)
        st.dataframe(top_brands_df)
    
    elif question == "q4":
        df = map_insurance_df.groupby('State').apply(lambda df: df.loc[df['Transaction_amount'].idxmax()])[['State', 'District','Transaction_amount']]
        fig = px.bar(df, x='State', y='Transaction_amount', color='District', title='Districts with Highest Insurance Transactions in Each State')
        st.plotly_chart(fig)
        st.dataframe(df)
    
    elif question == "q5":
        df6 = map_transactions_df.groupby('State').sum().reset_index().sort_values('Transaction_count')[['State', 'Transaction_amount']].head(10)
        fig = px.bar(df6, x='State', y='Transaction_amount', title='Top 10 Districts of Lowest Transaction Amount')
        st.plotly_chart(fig)
        st.dataframe(df6)
    
    elif question == "q6":
        df2 = map_user_df.groupby('State').agg({'Registered_user': 'sum'}).reset_index().sort_values(by='Registered_user',ascending=False).head(10)
        fig = px.bar(df2, x='State', y='Registered_user', title='States with Most Registered Users')
        st.plotly_chart(fig)
        st.dataframe(df2)
    
    elif question == "q7":
        df8 = top_insurance_df.groupby('Pincode').sum().reset_index().sort_values(by='Transaction_amount', ascending=False)[['Pincode', 'Transaction_amount']].head(10)
        fig = px.bar(df8, x='Pincode', y='Transaction_amount', title='Pincode with Highest Transaction Amount')
        st.plotly_chart(fig)
        st.dataframe(df8)
    
    elif question == "q8":
        df9 = agg_transactions_df.groupby('States').sum().reset_index().sort_values(by='Transaction_amount', ascending=False)[['States', 'Transaction_amount']].head(10)
        fig = px.bar(df9, x='States', y='Transaction_amount', title='Top 10 States with Highest Transaction Amount')
        st.plotly_chart(fig)
        st.dataframe(df9)
    
    elif question == "q9":
        df10 = map_user_df.groupby('State').agg({'AppOpens': 'sum'}).reset_index().sort_values(by='AppOpens',ascending=False).head(10)
        fig = px.bar(df10, x='State', y='AppOpens', title='Top 10 States With AppOpens')
        st.plotly_chart(fig)
        st.dataframe(df10)
    
    elif question == "q10":
        df11 = map_transactions_df.groupby('State').sum().reset_index().sort_values(by='Transaction_amount')[['State', 'Transaction_amount']].head(50)
        fig = px.bar(df11, x='State', y='Transaction_amount', title='Top 50 Districts With Lowest Transaction Amount')
        st.plotly_chart(fig)
        st.dataframe(df11)


st.set_page_config(page_title="Phonepe Pulse Data Visualization", page_icon=":bar_chart:", layout="wide")

with st.sidebar:
    select = op("Main Menu", ['Home', 'Explore Data', 'Top Charts'])

if select == 'Home':
    main()
if select == 'Explore Data':
    tab11, tab12, tab13 = st.tabs(['Aggregated Analysis', 'Map Analysis', 'Top Analysis'])
    
    with tab11:
        agg_method = st.radio("**Select the Analysis Method**", ['Aggregated Insurance Analysis', 'Aggregated Transaction Analysis' , 'Aggregated User Analysis'])
        if agg_method == 'Aggregated Insurance Analysis':
            col1, col2 = st.columns(2)
            with col1:
                year = st.slider('Select the Year', agg_insurance_df['Year'].min(), agg_insurance_df['Year'].max(), agg_insurance_df['Year'].min())
            with col2:
                quarter = st.slider('Select the Quarter', agg_insurance_df['Quarter'].min(), agg_insurance_df['Quarter'].max(), agg_insurance_df['Quarter'].min())
            
            agg_year_data = agg_insurance_year(agg_insurance_df, year)
            agg_quarter_data = agg_insurance_quarter(agg_insurance_df, quarter)
            
            tab1, tab2 = st.tabs(["Insurance Count", "Insurance Amount"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"### Visualizations for Insurance Count in {year}")
                    display_visualizations(agg_year_data, 'Insurance_count', f'{year} Insurance Count', px.colors.sequential.Bluered_r, col1)
                with col2:
                    st.write(f"### Visualizations for Insurance Count in Quarter {quarter}")
                    display_visualizations(agg_quarter_data, 'Insurance_count', f'{quarter} Quarter Insurance Count', px.colors.sequential.Cividis_r, col2)
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"### Visualizations for Insurance Amount in {year}")
                    display_visualizations(agg_year_data, 'Insurance_amount', f'{year} Insurance Amount', px.colors.sequential.Aggrnyl, col1)
                with col2:
                    st.write(f"### Visualizations for Insurance Amount in Quarter {quarter}")
                    display_visualizations(agg_quarter_data, 'Insurance_amount', f'{quarter} Quarter Insurance Amount', px.colors.sequential.Burg_r, col2)
        
        elif agg_method == 'Aggregated Transaction Analysis':
            col1, col2 = st.columns(2)
            with col1:
                year = st.slider('Select the Year', agg_transactions_df['Year'].min(), agg_transactions_df['Year'].max(), agg_transactions_df['Year'].min())
            with col2:
                quarter = st.slider('Select the Quarter', agg_transactions_df['Quarter'].min(), agg_transactions_df['Quarter'].max(), agg_transactions_df['Quarter'].min())
            
            agg_year_data = agg_transaction_year(agg_transactions_df, year)
            agg_quarter_data = agg_transaction_quarter(agg_transactions_df, quarter)
            
            tab1, tab2, tab3 = st.tabs(["Transaction Count", "Transaction Amount", "Transaction Type"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"### Visualizations for Transaction Count in {year}")
                    display_visualizations(agg_year_data, 'Transaction_count', f'{year} Transaction Count', px.colors.sequential.Bluered_r, col1)
                with col2:
                    st.write(f"### Visualizations for Transaction Count in Quarter {quarter}")
                    display_visualizations(agg_quarter_data, 'Transaction_count', f'{quarter} Quarter Transaction Count', px.colors.sequential.Cividis_r, col2)
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"### Visualizations for Transaction Amount in {year}")
                    display_visualizations(agg_year_data, 'Transaction_amount', f'{year} Transaction Amount', px.colors.sequential.Aggrnyl, col1)
                with col2:
                    st.write(f"### Visualizations for Transaction Amount in Quarter {quarter}")
                    display_visualizations(agg_quarter_data, 'Transaction_amount', f'{quarter} Quarter Transaction Amount', px.colors.sequential.Burg_r, col2)
            with tab3:
                st.title("Transaction Analysis by Type")
                grouped_df = agg_transactions_df.groupby('Transaction_type').sum().reset_index()
                col1, col2 = st.columns(2)
                with col1:
                    fig1 = px.bar(grouped_df, x='Transaction_type', y='Transaction_count', 
                                title='Transaction Count by Type', 
                                labels={'Transaction_type': 'Transaction Type', 'Transaction_count': 'Transaction Count'}, 
                                color='Transaction_type')
                    st.plotly_chart(fig1)
                    st.dataframe(grouped_df[['Transaction_type', 'Transaction_count']])

                with col2:
                    fig2 = px.bar(grouped_df, x='Transaction_type', y='Transaction_amount', 
                                title='Transaction Amount by Type', 
                                labels={'Transaction_type': 'Transaction Type', 'Transaction_amount': 'Transaction Amount'}, 
                                color='Transaction_type')
                    st.plotly_chart(fig2)
                    st.dataframe(grouped_df[['Transaction_type', 'Transaction_amount']])

        elif agg_method == 'Aggregated User Analysis':
            col1, col2, col3 = st.columns(3)
            with col1:
                au_state = st.selectbox('Select State', agg_user_df['States'].unique())
            with col2:
                au_year = st.slider('Select Year', agg_user_df['Year'].min(), agg_user_df['Year'].max(), agg_user_df['Year'].min())
            with col3:
                au_quarter = st.slider('Select Quarter', agg_user_df['Quarter'].min(), agg_user_df['Quarter'].max(), agg_user_df['Quarter'].min())
            filtered_df = agg_user_df[(agg_user_df['Year']== au_year) & (agg_user_df['Quarter']== au_quarter) & (agg_user_df['States']== au_state)]
            bar_fig = px.bar(filtered_df, x='Brand', y='Transaction_count', title= f'Transaction Count vs Brands in {au_state} (Y {au_year} Q {au_quarter})')
            st.plotly_chart(bar_fig)

            pie_fig = px.pie(filtered_df, names='Brand', values='Percentage', title= f'Market share of Brands in {au_state} (Y {au_year} Q {au_quarter})')
            st.plotly_chart(pie_fig)

            yq_df = agg_user_df[(agg_user_df['Year']== au_year) & (agg_user_df['Quarter']== au_quarter)]
            choropleth_df = yq_df.loc[yq_df.groupby('States')['Transaction_count'].idxmax()]
            choropleth_fig = px.choropleth(choropleth_df, geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
                                    locations='States', featureidkey='properties.ST_NM', color='Brand', title=f'Most Popular Brand in Each State (Y {au_year} Q{au_quarter})')
            choropleth_fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(choropleth_fig)
    with tab12:
        map_method = st.radio("**Select the Analysis Method**", ['Map Insurance Analysis', 'Map Transaction Analysis' , 'Map User Analysis'])
        if map_method == 'Map Insurance Analysis':
            create_charts(map_insurance_df, 'District', 'Transaction_count', 'Transaction_amount', prefix='map_ins')
        elif map_method == 'Map Transaction Analysis':
            create_charts(map_transactions_df, 'District', 'Transaction_count', 'Transaction_amount', prefix='map_trans')
        elif map_method == 'Map User Analysis':
            create_charts(map_user_df, 'District', 'Registered_user', 'App_opens', prefix='map_user')
    with tab13:
        top_method = st.radio("**Select the Analysis Method**", ['Top Insurance Analysis', 'Top Transaction Analysis' , 'Top User Analysis'])
        if top_method == 'Top Insurance Analysis':
            create_charts(top_insurance_df, 'Pincode','Transaction_count','Transaction_amount', prefix='top_ins')
        elif top_method == 'Top Transaction Analysis':
            create_charts(top_transactions_df, 'Pincode', 'Transaction_count', 'Transaction_amount', prefix='top_trans')
        elif top_method == 'Top User Analysis':
            create_charts(top_user_df, 'Pincode', 'Registered_user', prefix='top_user')
            
if select == 'Top Charts':
    st.title("Data Visualization for Insurance and Transactions")
    questions = {
        "How has the total insurance count and amount changed from 2018 to 2022?": "q1",
        "States with highest transaction counts": "q2",
        "Top brands used": "q3",
        "Districts with highest insurance transactions in each state": "q4",
        "Top 10 districts of lowest transaction amount": "q5",
        "States with most registered users": "q6",
        "Pincode with highest transaction amount": "q7",
        "Top 10 states with highest transaction amount": "q8",
        "Top 10 States With AppOpens": "q9",
        "Top 50 Districts With Lowest Transaction Amount" : "q10"
    }

    selected_question = st.selectbox("Select a question to visualize", list(questions.keys()))

    if selected_question:
        show_visualization(questions[selected_question])
