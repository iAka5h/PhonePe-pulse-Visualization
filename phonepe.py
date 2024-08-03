import streamlit as st
from streamlit_option_menu import option_menu


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
            pass

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
