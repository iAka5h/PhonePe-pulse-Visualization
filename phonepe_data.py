import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import json
from PIL import Image

# Dataframe Creation

#sql connection
mydb=pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             port=3306,
                             database = "phonepe_data")
cursor= mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands",
                                               "Transaction_count", "Percentage"))

#map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

map_insurance= pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District",
                                               "Transaction_count", "Transaction_amount"))

#map_transction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

map_transaction= pd.DataFrame(table5, columns=("States", "Years", "Quarter", "District",
                                               "Transaction_count", "Transaction_amount"))

#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

map_user= pd.DataFrame(table6, columns=("States", "Years", "Quarter", "District",
                                               "RegisteredUser", "AppOpens"))

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

top_user= pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes",
                                               "RegisteredUsers"))


def Transaction_amount_count_Y(df, year):

    tacy= df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(fig_count)


    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):
    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    
    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

            
def Aggre_Tran_Transaction_type(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                            width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                            width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)


# Aggre_User_analysis_1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title=  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


#Map_insurance_district
def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "District", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "District", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

# top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)

#sql connection
def top_chart_transaction_amount(table_name):
    mydb=pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             port=3306,
                             database = "phonepe_data")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


#sql connection
def top_chart_transaction_count(table_name):
    mydb=pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             port=3306,
                             database = "phonepe_data")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



#sql connection
def top_chart_registered_user(table_name, state):
    mydb=pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             port=3306,
                             database = "phonepe_data")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_appopens(table_name, state):
    mydb=pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             port=3306,
                             database = "phonepe_data")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))


    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:

        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_users(table_name):
    mydb=pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             port=3306,
                             database = "phonepe_data")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registeredusers"))
    
    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registeredusers"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


###==============================================Streamlit Part============================================###

st.set_page_config(layout="wide")
select= option_menu(None,
                        options=["HOME", "EXPLORE DATA", "INSIGHTS", "DATA APIs"],
                        icons = ["house","bar-chart","toggles","at"],
                        default_index=0,
                        orientation="horizontal",
                        styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#6F36AD"}}
                        )



if select == "HOME":
          
    st.title(":violet[PhonePe Pulse Data Visualization and Exploration]")
    st.subheader("**A User-Friendly Tool Using Streamlit and Plotly**")
    st.write("---")
        
    col1,col2= st.columns(2)
    with col1:
        st.subheader("**:violet[Project Overview]**")
        st.markdown("**PhonePe Pulse is a data analytics initiative by PhonePe, one of india's leading digital payment plotforms. The Project provides insights into digital payment trends accross India using data collected from PhonePe transactions.**")
        st.markdown("**:violet[Domain :] FinTech**")
        st.markdown("**:violet[Technologies Used :] Github cloning, Python Scripting, MySQL, mysql-connector-python, Streamlit and Plotly**")
        st.write("This project inspired from [PhonePe Pulse](https://www.phonepe.com/pulse/explore/transaction/2022/4/) ", " Data source:","[Git Hub](https://github.com/PhonePe/pulse.git)")
        st.info("Amount and Count values are in Indian Rupee(INR ₹)",icon="ℹ️")

    with col2:
        st.image(Image.open(r"H:\Python\PhonePe Project\PhonePe-Logo.wine.png"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(Image.open(r"H:\Python\PhonePe Project\col1.png"))
    with col2:
        st.video(r"H:\Python\PhonePe Project\pulse-video.mp4")
    with col3:
        st.image(Image.open(r"H:\Python\PhonePe Project\col3.png"))

# EXPLORE DATA TAB
elif select == "EXPLORE DATA":
    st.title(':violet[ANALYSIS]')
    select = option_menu(None,
                         options=["Aggregated Analysis", "Map Analysis", "Top Analysis"],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                   "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})
    # AGGREGATED ANALYSIS TAB
    if select == "Aggregated Analysis":
        tab1, tab2 = st.tabs(["TRANSACTION","USER"])

        # TRANSACTION TAB
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                in_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_tr_yr')
            with col2:
                in_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_tr_qtr')
            with col3:
                in_tr_tr_typ = st.selectbox('**Select Transaction type**',
                                            ('Recharge & bill payments', 'Peer-to-peer payments',
                                             'Merchant payments', 'Financial Services', 'Others'), key='in_tr_tr_typ')
            # SQL Query
            # Transaction Analysis bar chart query
            cursor.execute(
                f"SELECT States, Transaction_amount FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_tab_qry_rslt = cursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(np.array(in_tr_tab_qry_rslt), columns=['States', 'Transaction_amount'])
            df_in_tr_tab_qry_rslt1 = df_in_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_tr_tab_qry_rslt) + 1)))

            # Transaction Analysis table query
            cursor.execute(
                f"SELECT States, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt),
                                                      columns=['States', 'Transaction_count', 'Transaction_amount'])
            df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt) + 1)))

            # Total Transaction Amount table query
            cursor.execute(
                f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_am_qry_rslt = cursor.fetchall()
            df_in_tr_am_qry_rslt = pd.DataFrame(np.array(in_tr_am_qry_rslt), columns=['Total', 'Average'])
            df_in_tr_am_qry_rslt1 = df_in_tr_am_qry_rslt.set_index(['Average'])

            # Total Transaction Count table query
            cursor.execute(
                f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_co_qry_rslt = cursor.fetchall()
            df_in_tr_co_qry_rslt = pd.DataFrame(np.array(in_tr_co_qry_rslt), columns=['Total', 'Average'])
            df_in_tr_co_qry_rslt1 = df_in_tr_co_qry_rslt.set_index(['Average'])

            # GEO VISUALISATION
            # Drop a State column from df_in_tr_tab_qry_rslt
            df_in_tr_tab_qry_rslt.drop(columns=['States'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()
            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'States': state_names_tra})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_tra['Transaction_amount'] = df_in_tr_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_tra.to_csv('State_trans.csv', index=False)
            # Read csv
            df_tra = pd.read_csv('State_trans.csv')
            # Geo plot
            fig_tra = px.choropleth(
                df_tra,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='States', color='Transaction_amount',
                color_continuous_scale='thermal', title='Transaction Analysis')
            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_tra, use_container_width=True)

            # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
            df_in_tr_tab_qry_rslt1['States'] = df_in_tr_tab_qry_rslt1['States'].astype(str)
            df_in_tr_tab_qry_rslt1['Transaction_amount'] = df_in_tr_tab_qry_rslt1['Transaction_amount'].astype(float)
            df_in_tr_tab_qry_rslt1_fig = px.bar(df_in_tr_tab_qry_rslt1, x='States', y='Transaction_amount',
                                                color='Transaction_amount', color_continuous_scale='thermal',
                                                title='Transaction Analysis Chart', height=700, )
            df_in_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_in_tr_tab_qry_rslt1_fig, use_container_width=True)

            # -------  /  All India Total Transaction calculation Table   /   ----  #
            st.header(':violet[Total calculation]')

            col4, col5 = st.columns(2)
            with col4:
                st.subheader(':violet[Transaction Analysis]')
                st.dataframe(df_in_tr_anly_tab_qry_rslt1)
            with col5:
                st.subheader(':violet[Transaction Amount]')
                st.dataframe(df_in_tr_am_qry_rslt1)
                st.subheader(':violet[Transaction Count]')
                st.dataframe(df_in_tr_co_qry_rslt1)

        # USER TAB
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                in_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_us_yr')
            with col2:
                in_us_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_us_qtr')

            # SQL Query

            # User Analysis Bar chart query
            cursor.execute(f"SELECT States , SUM(Transaction_count) FROM aggregated_user WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY States;")
            in_us_tab_qry_rslt = cursor.fetchall()
            df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=['States', 'User Count'])
            df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt) + 1)))

            # Total User Count table query
            cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_user WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}';")
            in_us_co_qry_rslt = cursor.fetchall()
            df_in_us_co_qry_rslt = pd.DataFrame(np.array(in_us_co_qry_rslt), columns=['Total', 'Average'])
            df_in_us_co_qry_rslt1 = df_in_us_co_qry_rslt.set_index(['Average'])



            # GEO VISUALIZATION FOR USER

            # Drop a State column from df_in_us_tab_qry_rslt
            df_in_us_tab_qry_rslt.drop(columns=['States'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()
            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'States': state_names_use})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['User Count'] = df_in_us_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_use.to_csv('State_user.csv', index=False)
            # Read csv
            df_use = pd.read_csv('State_user.csv')
            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='States', color='User Count',
                color_continuous_scale='thermal', title='User Analysis')
            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_use, use_container_width=True)

            # ----   /   All India User Analysis Bar chart   /     -------- #
            df_in_us_tab_qry_rslt1['States'] = df_in_us_tab_qry_rslt1['States'].astype(str)
            df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)
            df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1, x='States', y='User Count', color='User Count',
                                                color_continuous_scale='thermal', title='User Analysis Chart',
                                                height=700, )
            df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_in_us_tab_qry_rslt1_fig, use_container_width=True)

            # -----   /   All India Total User calculation Table   /   ----- #
            st.header(':violet[Total calculation]')

            col3, col4 = st.columns(2)
            with col3:
                st.subheader(':violet[User Analysis]')
                st.dataframe(df_in_us_tab_qry_rslt1)
            with col4:
                st.subheader(':violet[User Count]')
                st.dataframe(df_in_us_co_qry_rslt1)

    # MAP ANALYSIS TAB
    if select == "Map Analysis":
        tab3 ,tab4 = st.tabs(["TRANSACTION","USER"])

        #TRANSACTION TAB FOR STATE
        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st_tr_st = st.selectbox('**Select State**', (
                'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
                'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh',
                'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'), key='st_tr_st')
            with col2:
                st_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_tr_yr')
            with col3:
                st_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')


            # SQL QUERY

            #Transaction Analysis bar chart query
            cursor.execute(f"SELECT Transaction_type, Transaction_amount FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
            st_tr_tab_bar_qry_rslt = cursor.fetchall()
            df_st_tr_tab_bar_qry_rslt = pd.DataFrame(np.array(st_tr_tab_bar_qry_rslt),
                                                        columns=['Transaction_type', 'Transaction_amount'])
            df_st_tr_tab_bar_qry_rslt1 = df_st_tr_tab_bar_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_tr_tab_bar_qry_rslt) + 1)))



            # Transaction Analysis table query
            cursor.execute(f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
            st_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_st_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt),
                                                        columns=['Transaction_type', 'Transaction_count',
                                                                'Transaction_amount'])
            df_st_tr_anly_tab_qry_rslt1 = df_st_tr_anly_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_tr_anly_tab_qry_rslt) + 1)))

            # Total Transaction Amount table query
            cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
            st_tr_am_qry_rslt = cursor.fetchall()
            df_st_tr_am_qry_rslt = pd.DataFrame(np.array(st_tr_am_qry_rslt), columns=['Total', 'Average'])
            df_st_tr_am_qry_rslt1 = df_st_tr_am_qry_rslt.set_index(['Average'])

            # Total Transaction Count table query
            cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Years ='{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
            st_tr_co_qry_rslt = cursor.fetchall()
            df_st_tr_co_qry_rslt = pd.DataFrame(np.array(st_tr_co_qry_rslt), columns=['Total', 'Average'])
            df_st_tr_co_qry_rslt1 = df_st_tr_co_qry_rslt.set_index(['Average'])



            # -----    /   State wise Transaction Analysis bar chart   /   ------ #

            df_st_tr_tab_bar_qry_rslt1['Transaction_type'] = df_st_tr_tab_bar_qry_rslt1['Transaction_type'].astype(str)
            df_st_tr_tab_bar_qry_rslt1['Transaction_amount'] = df_st_tr_tab_bar_qry_rslt1['Transaction_amount'].astype(
                float)
            df_st_tr_tab_bar_qry_rslt1_fig = px.bar(df_st_tr_tab_bar_qry_rslt1, x='Transaction_type',
                                                    y='Transaction_amount', color='Transaction_amount',
                                                    color_continuous_scale='thermal',
                                                    title='Transaction Analysis Chart', height=500, )
            df_st_tr_tab_bar_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig, use_container_width=True)

            # ------  /  State wise Total Transaction calculation Table  /  ---- #
            st.header(':violet[Total calculation]')

            col4, col5 = st.columns(2)
            with col4:
                st.subheader(':violet[Transaction Analysis]')
                st.dataframe(df_st_tr_anly_tab_qry_rslt1)
            with col5:
                st.subheader(':violet[Transaction Amount]')
                st.dataframe(df_st_tr_am_qry_rslt1)
                st.subheader(':violet[Transaction Count]')
                st.dataframe(df_st_tr_co_qry_rslt1)

# USER TAB FOR STATE
        with tab4:
            col5, col6 = st.columns(2)
            with col5:
                st_us_st = st.selectbox('**Select State**', (
                'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
                'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh',
                'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'), key='st_us_st')
            with col6:
                st_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_us_yr')
            # SQL QUERY

            # User Analysis Bar chart query
            cursor.execute(f"SELECT Quarter, SUM(Transaction_count) FROM aggregated_user WHERE States = '{st_us_st}' AND Years = '{st_us_yr}' GROUP BY Quarter;")
            st_us_tab_qry_rslt = cursor.fetchall()
            df_st_us_tab_qry_rslt = pd.DataFrame(np.array(st_us_tab_qry_rslt), columns=['Quarter', 'User Count'])
            df_st_us_tab_qry_rslt1 = df_st_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_us_tab_qry_rslt) + 1)))

            # Total User Count table query
            cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_user WHERE States = '{st_us_st}' AND Years = '{st_us_yr}';")
            st_us_co_qry_rslt = cursor.fetchall()
            df_st_us_co_qry_rslt = pd.DataFrame(np.array(st_us_co_qry_rslt), columns=['Total', 'Average'])
            df_st_us_co_qry_rslt1 = df_st_us_co_qry_rslt.set_index(['Average'])


            # -----   /   All India User Analysis Bar chart   /   ----- #
            df_st_us_tab_qry_rslt1['Quarter'] = df_st_us_tab_qry_rslt1['Quarter'].astype(int)
            df_st_us_tab_qry_rslt1['User Count'] = df_st_us_tab_qry_rslt1['User Count'].astype(int)
            df_st_us_tab_qry_rslt1_fig = px.bar(df_st_us_tab_qry_rslt1, x='Quarter', y='User Count', color='User Count',
                                                color_continuous_scale='thermal', title='User Analysis Chart',
                                                height=500, )
            df_st_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_st_us_tab_qry_rslt1_fig, use_container_width=True)

            # ------    /   State wise User Total User calculation Table   /   -----#
            st.header(':violet[Total calculation]')

            col3, col4 = st.columns(2)
            with col3:
                st.subheader(':violet[User Analysis]')
                st.dataframe(df_st_us_tab_qry_rslt1)
            with col4:
                st.subheader(':violet[User Count]')
                st.dataframe(df_st_us_co_qry_rslt1)

 # Top Analysis
    if select == "Top Analysis":
        tab5, tab6 = st.tabs(["TRANSACTION", "USER"])

        # Overall top transaction
        #TRANSACTION TAB
        with tab5:
            top_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='top_tr_yr')

            #SQL QUERY

            #Top Transaction Analysis bar chart query
            cursor.execute(
                f"SELECT States, SUM(Transaction_amount) As Transaction_amount FROM top_transaction WHERE Years = '{top_tr_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
            top_tr_tab_qry_rslt = cursor.fetchall()
            df_top_tr_tab_qry_rslt = pd.DataFrame(np.array(top_tr_tab_qry_rslt),
                                                  columns=['States', 'Top Transaction amount'])
            df_top_tr_tab_qry_rslt1 = df_top_tr_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_top_tr_tab_qry_rslt) + 1)))

            # Top Transaction Analysis table query
            cursor.execute(
                f"SELECT States, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transaction WHERE Years = '{top_tr_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
            top_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_top_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(top_tr_anly_tab_qry_rslt),
                                                       columns=['States', 'Top Transaction amount',
                                                                'Total Transaction count'])
            df_top_tr_anly_tab_qry_rslt1 = df_top_tr_anly_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_top_tr_anly_tab_qry_rslt) + 1)))



            # All India Transaction Analysis Bar chart
            df_top_tr_tab_qry_rslt1['States'] = df_top_tr_tab_qry_rslt1['States'].astype(str)
            df_top_tr_tab_qry_rslt1['Top Transaction amount'] = df_top_tr_tab_qry_rslt1[
                'Top Transaction amount'].astype(float)
            df_top_tr_tab_qry_rslt1_fig = px.bar(df_top_tr_tab_qry_rslt1, x='States', y='Top Transaction amount',
                                                 color='Top Transaction amount', color_continuous_scale='thermal',
                                                 title='Top Transaction Analysis Chart', height=600, )
            df_top_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_top_tr_tab_qry_rslt1_fig, use_container_width=True)


            #All India Total Transaction calculation Table
            st.header(':violet[Total calculation]')
            st.subheader('Top Transaction Analysis')
            st.dataframe(df_top_tr_anly_tab_qry_rslt1)

        # OVERALL TOP USER DATA
        # USER TAB
        with tab6:
            top_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='top_us_yr')

            #SQL QUERY

            #Top User Analysis bar chart query
            cursor.execute(f"SELECT States, SUM(RegisteredUsers) AS Top_user FROM top_user WHERE Years ='{top_us_yr}' GROUP BY States ORDER BY Top_user DESC LIMIT 10;")
            top_us_tab_qry_rslt = cursor.fetchall()
            df_top_us_tab_qry_rslt = pd.DataFrame(np.array(top_us_tab_qry_rslt), columns=['States', 'Total User count'])
            df_top_us_tab_qry_rslt1 = df_top_us_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_top_us_tab_qry_rslt) + 1)))



            #All India User Analysis Bar chart
            df_top_us_tab_qry_rslt1['States'] = df_top_us_tab_qry_rslt1['States'].astype(str)
            df_top_us_tab_qry_rslt1['Total User count'] = df_top_us_tab_qry_rslt1['Total User count'].astype(float)
            df_top_us_tab_qry_rslt1_fig = px.bar(df_top_us_tab_qry_rslt1, x='States', y='Total User count',
                                                 color='Total User count', color_continuous_scale='thermal',
                                                 title='Top User Analysis Chart', height=600, )
            df_top_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_top_us_tab_qry_rslt1_fig, use_container_width=True)

            #All India Total Transaction calculation Table
            st.header(':violet[Total calculation]')
            st.subheader('Total User Analysis')
            st.dataframe(df_top_us_tab_qry_rslt1)


#INSIGHTS TAB
elif select == "INSIGHTS":
        
        st.title(':violet[BASIC INSIGHTS]')
        st.subheader("The basic insights are derived from the Analysis of the Phonepe Pulse data. It provides a clear idea about the analysed data.")
        options = ["---SELECT---",
                "1. Top 10 states based on year and amount of transaction",
                "2. Least 10 states based on year and amount of transaction",
                "3. Top 10 States and Districts based on Registered Users",
                "4. Least 10 States and Districts based on Registered Users",
                "5. Top 10 Districts based on the Transaction Amount",
                "6. Least 10 Districts based on the Transaction Amount",
                "7. Top 10 Districts based on the Transaction count",
                "8. Least 10 Districts based on the Transaction count",
                "9. Top Transaction types based on the Transaction Amount",
                "10.Top 10 Mobile Brands based on the User count of transaction"]
        select = st.selectbox(":violet[Select the option]",options)

        #1
        if select == "1. Top 10 states based on year and amount of transaction":
            cursor.execute(
                "SELECT DISTINCT States,Years, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY States,Years ORDER BY Total_Transaction_Amount DESC LIMIT 10");

            data = cursor.fetchall()
            columns = ['States', 'Years', 'Transaction_amount']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Top 10 states based on amount of transaction")
                st.bar_chart(data=df, x="Transaction_amount", y="States")

        #2
        elif select == "2. Least 10 states based on year and amount of transaction":
            cursor.execute(
                "SELECT DISTINCT States,Years, SUM(Transaction_amount) as Total FROM top_transaction GROUP BY States, Years ORDER BY Total ASC LIMIT 10");
            data = cursor.fetchall()
            columns = ['States', 'Years', 'Transaction_amount']
            df = pd.DataFrame(data, columns=columns, index=range(1,len(data)+1))
            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Least 10 states based on amount of transaction")
                st.bar_chart(data=df, x="Transaction_amount", y="States")

        #3
        elif select == "3. Top 10 States and Districts based on Registered Users":
            cursor.execute("SELECT DISTINCT States, Pincodes, SUM(RegisteredUsers) AS Users FROM top_user GROUP BY States, Pincodes ORDER BY Users DESC LIMIT 10");
            data = cursor.fetchall()
            columns = ['States', 'Pincodes', 'RegisteredUsers']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Top 10 States and Districts based on Registered Users")
                st.bar_chart(data=df, x="RegisteredUsers", y="States")

        #4
        elif select == "4. Least 10 States and Districts based on Registered Users":
            cursor.execute("SELECT DISTINCT States, Pincodes, SUM(RegisteredUsers) AS Users FROM top_user GROUP BY States, Pincodes ORDER BY Users ASC LIMIT 10");
            data = cursor.fetchall()
            columns = ['States', 'Pincodes', 'RegisteredUsers']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Least 10 States and Districts based on Registered Users")
                st.bar_chart(data=df, x="RegisteredUsers", y="States")

        #5
        elif select == "5. Top 10 Districts based on the Transaction Amount":
            cursor.execute(
                "SELECT DISTINCT States, Districts, SUM(Transaction_Amount) AS Total FROM map_transaction GROUP BY States, Districts ORDER BY Total DESC LIMIT 10");
            data = cursor.fetchall()
            columns = ['States', 'Districts', 'Transaction_Amount']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Top 10 Districts based on Transaction Amount")
                st.bar_chart(data=df, x="Districts", y="Transaction_Amount")

        #6
        elif select == "6. Least 10 Districts based on the Transaction Amount":
            cursor.execute(
                "SELECT DISTINCT States, Districts, SUM(Transaction_amount) AS Total FROM map_transaction GROUP BY States, Districts ORDER BY Total ASC LIMIT 10");
            data = cursor.fetchall()
            columns = ['States', 'Districts', 'Transaction_amount']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Least 10 Districts based on Transaction Amount")
                st.bar_chart(data=df, x="Districts", y="Transaction_amount")

        #7
        elif select == "7. Top 10 Districts based on the Transaction count":
            cursor.execute(
                "SELECT DISTINCT States, Districts, SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY States, Districts ORDER BY Counts DESC LIMIT 10");
            data = cursor.fetchall()
            columns = ['States', 'Districts', 'Transaction_Count']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Top 10 Districts based on Transaction Count")
                st.bar_chart(data=df, x="Transaction_Count", y="Districts")

        #8
        elif select == "8. Least 10 Districts based on the Transaction count":
            cursor.execute(
                "SELECT DISTINCT States, Districts, SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY States, Districts ORDER BY Counts ASC LIMIT 10");
            data = cursor.fetchall()
            columns = ['States', 'Districts', 'Transaction_Count']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Top 10 Districts based on the Transaction Count")
                st.bar_chart(data=df, x="Transaction_Count", y="Districts")

        #9
        elif select == "9. Top Transaction types based on the Transaction Amount":
            cursor.execute(
                "SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM aggregated_transaction GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5");
            data = cursor.fetchall()
            columns = ['Transaction_type', 'Transaction_amount']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Top Transaction Types based on the Transaction Amount")
                st.bar_chart(data=df, x="Transaction_type", y="Transaction_amount")

        #10
        elif select == "10.Top 10 Mobile Brands based on the User count of transaction":
            cursor.execute(
                "SELECT DISTINCT Brands, SUM(Transaction_count) as Total FROM aggregated_user GROUP BY Brands ORDER BY Total DESC LIMIT 10");
            data = cursor.fetchall()
            columns = ['Brands', 'Transaction_count']
            df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

            col1, col2 = st.columns(2)
            with col1:
                st.write(df)
            with col2:
                st.title("Top 10 Mobile Brands based on User count of transaction")
                st.bar_chart(data=df , x="Transaction_count", y="Brands")

elif select == "DATA APIs":
    st.write("---")
    st.subheader(":violet[Introduction]")
    st.write(""" The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem. """)      
    st.write("---")
    st.subheader(":violet[GUIDE]")
    st.write("This data has been structured to provide details on data cuts of Transactions and Users on the Explore tab. [Link](https://www.phonepe.com/pulse/data-api/)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(Image.open(r"H:\Python\PhonePe Project\aggregated.png"))
    with col2:
        st.subheader("1️⃣ :violet[Aggregated]")
        st.subheader("Aggregated values of various payment categories as shown under Categories section")

    col3, col4 = st.columns(2)
    with col3:
        st.image(Image.open(r"H:\Python\PhonePe Project\map.png"))
    with col4:
        st.subheader("2️⃣ :violet[Map]")
        st.subheader("Total values at the State and District levels")

    col5, col6 = st.columns(2)
    with col5:
        st.image(Image.open(r"H:\Python\PhonePe Project\top.png"))
    with col6:
        st.subheader("3️⃣ :violet[Top]")
        st.subheader("Totals of top States / Districts / Postal Codes")    
    st.write("---")
    st.image(Image.open(r"H:\Python\PhonePe Project\last.png"))