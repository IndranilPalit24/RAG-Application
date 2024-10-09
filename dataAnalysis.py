import pandas as pd
import matplotlib.pyplot as plt 
import streamlit as st

class SalesDataHandler:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
    
    def get_sales_growth(self, quarter):
        # Implement logic to calculate sales growth for the requested quarter
        sales_q1 = self.data[self.data['Quarter'] == quarter]['Sales'].sum()
        sales_last_q = self.data[self.data['Quarter'] == f'Q{int(quarter[-1]) - 1}']['Sales'].sum()
        
        growth = ((sales_q1 - sales_last_q) / sales_last_q) * 100
        return growth
    
    def plot_sales_by_quarter(self):
        sales_by_quarter = self.data.groupby('Quarter')['Sales'].sum()
        fig, ax = plt.subplots()
        sales_by_quarter.plot(kind='bar', ax=ax)
        st.pyplot(fig)
