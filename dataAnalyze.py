# pylint: disable=import-error
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class SalesDataHandler:
    def __init__(self, file_path):
        try:
            # Specify encoding to handle different formats
            self.data = pd.read_csv(file_path, encoding='ISO-8859-1')  # or 'latin1'
        except Exception as e:
            print(f"Error loading sales data: {e}")
 
    def get_sales_growth(self, quarter):
        # Implement logic to calculate sales growth for the requested quarter
        try:
            sales_data = self.data[self.data['Quarter'] == quarter]
            # Perform the growth calculation
            growth = (sales_data['Sales'].iloc[-1] - sales_data['Sales'].iloc[0]) / sales_data['Sales'].iloc[0] * 100
            return growth
        except Exception as e:
            print(f"Error calculating sales growth: {e}")
            return None
       
    def plot_sales_by_quarter(self):
        sales_by_quarter = self.data.groupby('Quarter')['Sales'].sum()
        fig, ax = plt.subplots()
        sales_by_quarter.plot(kind='bar', ax=ax)
        st.pyplot(fig)


