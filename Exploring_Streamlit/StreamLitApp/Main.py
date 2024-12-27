# nohup streamlit run '/Users/saisandeep/GitRepo/musical-eureka/Exploring_Streamlit/StreamLitApp/Main.py' > /dev/null 2>&1 &

import streamlit as st
import pandas as pd

st.sidebar.header("Filter Options")

temp = pd.read_csv(r'/Users/saisandeep/GitRepo/musical-eureka/Kaggle/Lending_Club/Data/accepted_2007_to_2018Q4.csv')
temp.head(100)
