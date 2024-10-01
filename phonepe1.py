import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import mysql.connector
import requests
import json



#DataFrame Creation
#SQL Connection

mydb=mysql.connector.connect(host="localhost",
                             user="root",
                             password="root",
                             port="3306",
                             database = "phonepe")
cursor=mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1, columns=("States", 
                                              "Years", 
                                              "Quarter",
                                              "Transaction_type", 
                                              "Transaction_count", 
                                              "Transaction_amount"))


#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2, columns=("States", 
                                              "Years", 
                                              "Quarter",
                                              "Transaction_type", 
                                              "Transaction_count", 
                                              "Transaction_amount"))


#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3, columns=("States", 
                                        "Years", 
                                        "Quarter",
                                        "Brands", 
                                        "Transaction_count", 
                                        "Percentage"))

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4, columns=("States", 
                                        "Years", 
                                        "Quarter",
                                        "Districts", 
                                        "Transaction_count", 
                                        "Transaction_amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5, columns=("States", 
                                        "Years", 
                                        "Quarter",
                                        "Districts", 
                                        "Transaction_count", 
                                        "Transaction_amount"))


#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6, columns=("States", 
                                        "Years", 
                                        "Quarter",
                                        "Districts", 
                                        "RegisteredUsers", 
                                        "AppOpens"))


#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7, columns=("States", 
                                        "Years", 
                                        "Quarter",
                                        "Pincodes", 
                                        "Tansaction_count", 
                                        "Tansaction_amount"))


#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8, columns=("States", 
                                        "Years", 
                                        "Quarter",
                                        "Pincodes", 
                                        "Tansaction_count", 
                                        "Tansaction_amount"))



#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9, columns=("States", 
                                        "Years", 
                                        "Quarter",
                                        "Pincodes", 
                                        "RegisteredUsers"))


def Transaction_amount_count_Y(df, year):

    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_amount=px.bar(tacyg, x="States", 
                      y="Transaction_amount", 
                      title=f"{year} - TRANSACTION AMOUNT",
                      color_discrete_sequence=px.colors.sequential.Aggrnyl)
    fig_amount.show()

    fig_count=px.bar(tacyg, x="States", 
                     y="Transaction_count", 
                     title=f"{year} - TRANSACTION COUNT",
                     color_discrete_sequence=px.colors.sequential.Bluered_r)
    fig_count.show()

#Streamlit Part

st.set_page_config(layout="wide")
st.title("PhonePe Data Visualization & Exploration")

with st.sidebar:
    select=option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select=="HOME":
    pass #fill at the end of the project

elif select=="DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    
    with tab1:
        method=st.radio("Select the method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method=="Insurance Analysis":

            years=st.slider("SELECT THE YEAR", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min())
            Transaction_amount_count_Y(Aggre_insurance, years)


        elif method=="Transaction Analysis":
            pass

        elif method=="User Analysis":
            pass



    with tab2:
        method2=st.radio("Select the method", ["Map Insurance", "Map Transaction", "Map User"])

        if method2=="Map Insurance":
            pass

        elif method2=="Map Transaction":
            pass

        elif method2=="Map User":
            pass



    with tab3:
        method3=st.radio("Select the method", ["Top Insurance", "Top Transaction", "Top User"])

        if method3=="Top Insurance":
            pass

        elif method3=="Top Transaction":
            pass

        elif method3=="Top User":
            pass

elif select=="TOP CHARTS":
    pass


