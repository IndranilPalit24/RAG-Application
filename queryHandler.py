import pandas as pd

class QueryHandler:
    def __init__(self, data_file):
        """
        Initializes the QueryHandler with sales or financial data.
        Args:
            data_file (str): Path to the CSV file containing sales/finance data.
        """
        self.data = pd.read_csv(data_file, encoding='ISO-8859-1')

    def get_sales_growth(self, quarter1, quarter2):
        """
        Calculates sales growth between two quarters.
        Args:
            quarter1 (str): The first quarter (e.g., 'Q1').
            quarter2 (str): The second quarter (e.g., 'Q2').
        Returns:
            str: Sales growth from quarter1 to quarter2.
        """
        try:
            sales_q1 = self.data[self.data['Quarter'] == quarter1]['Sales'].values[0]
            sales_q2 = self.data[self.data['Quarter'] == quarter2]['Sales'].values[0]
            growth = ((sales_q2 - sales_q1) / sales_q1) * 100
            return f"The sales growth from {quarter1} to {quarter2} is {growth:.2f}%."
        except Exception as e:
            return f"Error fetching sales growth: {e}"

    def get_sales_for_quarter(self, quarter):
        """
        Fetches sales for a given quarter.
        Args:
            quarter (str): The quarter for which sales data is requested.
        Returns:
            str: Sales data for the given quarter.
        """
        try:
            sales = self.data[self.data['Quarter'] == quarter]['Sales'].values[0]
            return f"The sales for {quarter} is {sales}."
        except Exception as e:
            return f"Error fetching sales for {quarter}: {e}"

    def get_finance_overview(self):
        """
        Provides an overview of the financial data.
        Returns:
            str: Financial overview based on available data.
        """
        try:
            total_revenue = self.data['Revenue'].sum()
            total_expense = self.data['Expense'].sum()
            profit = total_revenue - total_expense
            return (f"Total revenue is {total_revenue}, total expenses are {total_expense}, "
                    f"and the profit is {profit}.")
        except Exception as e:
            return f"Error fetching finance overview: {e}"
