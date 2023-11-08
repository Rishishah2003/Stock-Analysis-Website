import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import mplcursors
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas_datareader as pdr
import datetime as dt
pd.set_option("display.max_rows", 100)  # Display all columns
pd.set_option("display.max_columns", 100)  # Display all columns
import numpy as np
import plotly.express as px

def stock_name(name):
    name= name.upper()
    name= name.replace(" ","")
    n= name+'.NS'
    stock= yf.Ticker(n)
    return stock

na = 'RELIANCE'
x = stock_name(na)
class FinancialData:
    def __init__(self, income_statement, balance_sheet, cash_flow):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.cash_flow = cash_flow

    @staticmethod
    def transpose_data(data):
        return data.T

    def get_transposed_data(self):
        transposed_income_statement = self.transpose_data(self.income_statement)
        transposed_balance_sheet = self.transpose_data(self.balance_sheet)
        transposed_cash_flow = self.transpose_data(self.cash_flow)
        return transposed_income_statement, transposed_balance_sheet, transposed_cash_flow

financial_data = FinancialData(x.income_stmt, x.balance_sheet, x.cash_flow)
qtr_financial_data = FinancialData(x.quarterly_income_stmt, x.quarterly_balance_sheet, x.quarterly_cash_flow)

transposed_income_statement, transposed_balance_sheet, transposed_cash_flow = financial_data.get_transposed_data()
qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow = qtr_financial_data.get_transposed_data()

# %%
class FinancialMetricsCalculator:
    def __init__(self, transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
                 qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow):
        self.income_statement = transposed_income_statement
        self.balance_sheet = transposed_balance_sheet
        self.cash_flow = transposed_cash_flow
        self.qtr_income_statement = qtr_transposed_income_statement
        self.qtr_balance_sheet = qtr_transposed_balance_sheet
        self.qtr_cash_flow = qtr_transposed_cash_flow

    def yoy_sales(self):
        url = 'https://www.screener.in/company/' + na + '/consolidated/'

        table = pd.read_html(url, skiprows=0)[1]

        t = table.T
        t.columns = t.iloc[0]
        t = t.drop(t.index[0])

        t.columns = t.columns.str.replace(r'\xa0\+', '', regex=True)

        years = t['Sales'].index.tolist()
        sales_values = t['Sales'].astype(float).tolist()

        sales_growth_rates = [0]  # Assuming the growth rate for the first year is 0
        for i in range(1, len(sales_values) - 1):  # Exclude the last year
            growth_rate = ((sales_values[i] - sales_values[i - 1]) / sales_values[i - 1]) * 100
            sales_growth_rates.append(growth_rate)

        results = []
        if years == 'TTM':
            for year, sales, growth_rate in zip(years[:-1], sales_values[:-1], sales_growth_rates):
                results.append(f"Year: {year}, Sales: {sales}, Sales Growth Rate: {growth_rate:.2f}%")
        else:
            for year, sales, growth_rate in zip(years, sales_values, sales_growth_rates):
                results.append(f"Year: {year}, Sales: {sales}, Sales Growth Rate: {growth_rate:.2f}%")
        return(results)
    

    def qoq_sales(self):
        url = 'https://www.screener.in/company/' + na + '/consolidated/'

        table = pd.read_html(url, skiprows=0)[0]

        t = table.T
        t.columns = t.iloc[0]
        t = t.drop(t.index[0])

        t.columns = t.columns.str.replace(r'\xa0\+', '', regex=True)

        years = t['Sales'].index.tolist()
        sales_values = t['Sales'].astype(float).tolist()

        sales_growth_rates = [0]  # Assuming the growth rate for the first year is 0
        for i in range(1, len(sales_values)):  # Exclude the last year
            growth_rate = ((sales_values[i] - sales_values[i - 1]) / sales_values[i - 1]) * 100
            sales_growth_rates.append(growth_rate)

        results = []
        for year, sales, growth_rate in zip(years, sales_values, sales_growth_rates):
            results.append(f"Year: {year}, Sales: {sales}, Sales Growth Rate: {growth_rate:.2f}%")
        return(results)
        
    def qoq_profit(self):
        url = 'https://www.screener.in/company/' + na + '/consolidated/'

        table = pd.read_html(url, skiprows=0)[0]

        t = table.T
        t.columns = t.iloc[0]
        t = t.drop(t.index[0])

        t.columns = t.columns.str.replace(r'\xa0\+', '', regex=True)

        years = t['Net Profit'].index.tolist()
        sales_values = t['Net Profit'].astype(float).tolist()

        sales_growth_rates = [0]  # Assuming the growth rate for the first year is 0
        for i in range(1, len(sales_values)):  # Exclude the last year
            growth_rate = ((sales_values[i] - sales_values[i - 1]) / sales_values[i - 1]) * 100
            sales_growth_rates.append(growth_rate)

        results = []
        for year, sales, growth_rate in zip(years, sales_values, sales_growth_rates):
            results.append(f"Year: {year}, Net Profit: {sales}, Net Profit Growth Rate: {growth_rate:.2f}%")
        return(results)
    
    def yoy_profit(self):
        url = 'https://www.screener.in/company/' + na + '/consolidated/'

        table = pd.read_html(url, skiprows=0)[1]

        t = table.T
        t.columns = t.iloc[0]
        t = t.drop(t.index[0])

        t.columns = t.columns.str.replace(r'\xa0\+', '', regex=True)

        years = t['Net Profit'].index.tolist()
        sales_values = t['Net Profit'].astype(float).tolist()

        sales_growth_rates = [0]  # Assuming the growth rate for the first year is 0
        for i in range(1, len(sales_values) - 1):  # Exclude the last year
            growth_rate = ((sales_values[i] - sales_values[i - 1]) / sales_values[i - 1]) * 100
            sales_growth_rates.append(growth_rate)

        results = []
        if years == 'TTM':
            for year, sales, growth_rate in zip(years[:-1], sales_values[:-1], sales_growth_rates):
                results.append(f"Year: {year}, Sales: {sales}, Sales Growth Rate: {growth_rate:.2f}%")
        else:
            for year, sales, growth_rate in zip(years, sales_values, sales_growth_rates):
                results.append(f"Year: {year}, Sales: {sales}, Sales Growth Rate: {growth_rate:.2f}%")
        return(results)
    
    def has_positive_roa(self):
        total_assets = self.balance_sheet['Total Assets'].iloc[0]
        net_income = self.income_statement['Net Income'].iloc[0]
        roa = (net_income / total_assets) * 100
        return roa > 0
    
    def roa(self):
        total_assets = self.balance_sheet['Total Assets'].iloc[0]
        net_income = self.income_statement['Net Income'].iloc[0]
        roa = (net_income / total_assets) * 100
        return roa

    def has_positive_operating_cashflow(self):
        operating_cashflow = self.cash_flow['Operating Cash Flow'].iloc[0]
        return operating_cashflow > 0

    def has_positive_cfo_greater_than_net_income(self):
        operating_cashflow = self.cash_flow['Operating Cash Flow'].iloc[0]
        net_income = self.income_statement['Net Income'].iloc[0]
        return operating_cashflow > net_income

    def yoy_borrowings(self):
        url = 'https://www.screener.in/company/' + na + '/consolidated/'

        table = pd.read_html(url, skiprows=0)[6]

        t = table.T
        t.columns = t.iloc[0]
        t = t.drop(t.index[0])

        t.columns = t.columns.str.replace(r'\xa0\+', '', regex=True)

        years = t['Borrowings'].index.tolist()
        borrowings_values = t['Borrowings'].astype(float).tolist()

        borrowings_growth_rates = [0]  # Assuming the growth rate for the first period is 0
        for i in range(1, len(borrowings_values)):  # Exclude the last period
            growth_rate = ((borrowings_values[i] - borrowings_values[i - 1]) / borrowings_values[i - 1]) * 100
            borrowings_growth_rates.append(growth_rate)

        results = []
        for year, borrowings, growth_rate in zip(years, borrowings_values, borrowings_growth_rates):
            results.append(f"Year: {year}, Borrowings: {borrowings}, Borrowings Growth Rate: {growth_rate:.2f}%")
        return results
    
    def promoter_holdings(self):
        url = 'https://www.screener.in/company/' + na + '/consolidated/'       
        hold=[]
        table= pd.read_html(url,skiprows=0)[9]
        t=table.T
        t.columns= t.iloc[0]
        t.drop(t.index[0],inplace= True)
        t.reset_index(drop=True)
        t.columns= t.columns.str.replace(r'\xa0\+','', regex=True)
        shareholders= t.columns
        h= t.tail(1)
        h= np.array(h)
        for i in range(len(shareholders)):
            x= h[0][i]
            x= x.strip("%")
            hold.append(x)
        hold= np.array(hold)
        l= len(hold)
        l= np.int64(l)
        l=l-1
        hold= hold[:l]
        shareholders=shareholders[:l]
        data = pd.DataFrame({'Shareholders': shareholders, 'Holdings': hold})
        return(data)
        
    def has_positive_current_ratio(self):
        current_assets = self.balance_sheet['Current Assets'].iloc[0]
        current_liabilities = self.balance_sheet['Current Liabilities'].iloc[0]
        current_ratio = current_assets / current_liabilities
        return current_ratio > 1
    
    def current_ratio(self):
        current_assets = self.balance_sheet['Current Assets'].iloc[0]
        current_liabilities = self.balance_sheet['Current Liabilities'].iloc[0]
        current_ratio = current_assets / current_liabilities
        return current_ratio

    def has_same_number_of_shares(self):
        current_year_shares = self.balance_sheet['Ordinary Shares Number'].iloc[0]
        previous_year_shares = self.balance_sheet['Ordinary Shares Number'].iloc[1]
        return current_year_shares == previous_year_shares

    def calculate_asset_turnover(self):
        total_sales = self.income_statement['Total Revenue'].iloc[0]
        average_total_assets = (self.balance_sheet['Total Assets'].iloc[0] + self.balance_sheet['Total Assets'].iloc[1]) / 2
        asset_turnover = total_sales / average_total_assets
        return asset_turnover

    def has_consistent_tax_percentage(self):
        current_year_tax_percentage = self.income_statement['Tax Provision'].iloc[0] / self.income_statement['Pretax Income'].iloc[0] * 100
        previous_year_tax_percentage = self.income_statement['Tax Provision'].iloc[1] / self.income_statement['Pretax Income'].iloc[1] * 100
        return abs(current_year_tax_percentage - previous_year_tax_percentage) <= 5

    def calculate_roe(self):
        net_income = self.income_statement['Net Income'].iloc[0]
        average_shareholders_equity = (self.balance_sheet['Stockholders Equity'].iloc[0] + self.balance_sheet['Stockholders Equity'].iloc[1]) / 2
        roe = (net_income / average_shareholders_equity) * 100
        return roe


# %%
class StockHealth():
    def __init__(self, financial_metrics_calculator):
        self.financial_metrics_calculator = financial_metrics_calculator
    
    def analyze_stock_health(self):
        health_score = 0
        if self.financial_metrics_calculator.has_positive_roa():  # Use correct attribute name here
            health_score += 15
        print(health_score)

financial_metrics_calculator = FinancialMetricsCalculator(
    transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
    qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow
)
stock_health = StockHealth(financial_metrics_calculator)



# %%
class SalesVisualizer:
    def __init__(self, financial_metrics_calculator):
        self.financial_metrics_calculator = financial_metrics_calculator

    def plot_yoy_sales_growth(self):
        yoy_sales_data = self.financial_metrics_calculator.yoy_sales()
        yoy_sales_data = yoy_sales_data[1:]
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        sales_growth_rates = [float(data.split(',')[2].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=sales_growth_rates, mode='markers+lines', marker=dict(size=12),
                                 line=dict(color='white', width=2)))
        fig.update_layout(title='YoY Sales Growth Rate Over Years', xaxis_title='Year', yaxis_title='YoY Sales Growth Rate (%)',
                          xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_yoy_sales(self):
        yoy_sales_data = self.financial_metrics_calculator.yoy_sales()
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        sales_growth = [float(data.split(',')[1].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=sales_growth, marker_color='white'))
        fig.update_layout(title='YoY Sales Over Years', xaxis_title='Year', yaxis_title='YoY Sales (%)',
                          xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_yoy_profit(self):
        yoy_sales_data = self.financial_metrics_calculator.yoy_profit()
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        profit_growth = [float(data.split(',')[1].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=profit_growth, marker_color='white'))
        fig.update_layout(title='YoY Profit Over Years', xaxis_title='Year', yaxis_title='YoY Profit (%)',
                          xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_yoy_profit_growth(self):
        yoy_sales_data = self.financial_metrics_calculator.qoq_profit()
        yoy_sales_data = yoy_sales_data[1:]
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        profit_growth_rates = [float(data.split(',')[2].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=profit_growth_rates, mode='markers+lines', marker=dict(size=12),
                                 line=dict(color='white', width=2)))
        fig.update_layout(title='YoY Profit Growth Rate Over Years', xaxis_title='Year',
                          yaxis_title='YoY Profit Growth Rate (%)', xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_qoq_sales_growth(self):
        yoy_sales_data = self.financial_metrics_calculator.qoq_sales()
        yoy_sales_data = yoy_sales_data[1:]
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        sales_growth_rates = [float(data.split(',')[2].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=sales_growth_rates, mode='markers+lines', marker=dict(size=12),
                                 line=dict(color='white', width=2)))
        fig.update_layout(title='YoY Sales Growth Rate Over Years', xaxis_title='Year', yaxis_title='YoY Sales Growth Rate (%)',
                          xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_qoq_sales(self):
        yoy_sales_data = self.financial_metrics_calculator.qoq_sales()
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        sales_growth = [float(data.split(',')[1].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=sales_growth, marker_color='white'))
        fig.update_layout(title='YoY Sales Over Years', xaxis_title='Year', yaxis_title='YoY Sales (%)',
                          xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_qoq_profit(self):
        yoy_sales_data = self.financial_metrics_calculator.qoq_profit()
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        profit_growth = [float(data.split(',')[1].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=profit_growth, marker_color='white'))
        fig.update_layout(title='YoY Profit Over Years', xaxis_title='Year', yaxis_title='YoY Profit (%)',
                          xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_qoq_profit_growth(self):
        yoy_sales_data = self.financial_metrics_calculator.yoy_profit()
        yoy_sales_data = yoy_sales_data[1:]
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        profit_growth_rates = [float(data.split(',')[2].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=profit_growth_rates, mode='markers+lines', marker=dict(size=12),
                                 line=dict(color='white', width=2)))
        fig.update_layout(title='YoY Profit Growth Rate Over Years', xaxis_title='Year',
                          yaxis_title='YoY Profit Growth Rate (%)', xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_yoy_borrowings_growth(self):
        yoy_sales_data = self.financial_metrics_calculator.yoy_borrowings()
        yoy_sales_data = yoy_sales_data[1:]
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        profit_growth_rates = [float(data.split(',')[2].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=profit_growth_rates, mode='markers+lines', marker=dict(size=12),
                                 line=dict(color='white', width=2)))
        fig.update_layout(title='YoY Profit Growth Rate Over Years', xaxis_title='Year',
                          yaxis_title='YoY Profit Growth Rate (%)', xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()

    def plot_yoy_borrowings(self):
        yoy_sales_data = self.financial_metrics_calculator.yoy_borrowings()
        years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
        profit_growth = [float(data.split(',')[1].split(': ')[1].strip('%')) for data in yoy_sales_data]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=years, y=profit_growth, marker_color='white'))
        fig.update_layout(title='YoY Profit Over Years', xaxis_title='Year', yaxis_title='YoY Profit (%)',
                          xaxis=dict(tickangle=45,showgrid = False), yaxis = dict(showgrid = False), template='plotly_dark')
        fig.show()
    
    def plot_promoter_holdings(self):
        yoy_promoters = self.financial_metrics_calculator.promoter_holdings()
        fig = px.pie(yoy_promoters, names='Shareholders', values='Holdings')

        # Customize the appearance of the pie chart
        fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1])  # Adjust pull for a 3D effect
        fig.update_layout(
            showlegend=True,
            margin=dict(l=0, r=0, t=30, b=0),
            scene=dict(
                xaxis=dict(showticklabels=False, showgrid=False),
                yaxis=dict(showticklabels=False, showgrid=False),
                zaxis=dict(showticklabels=False, showgrid=False),
                bgcolor='black'  # Background color for the 3D scene
            ),
            paper_bgcolor='black',  # Background color
            font=dict(family='Arial', color='white'),  # Set a custom font and text color
            legend=dict(orientation='h', y=1.05),  # Legend position
        )

        fig.show()

class StockHealthCalculator:
    def __init__(self, financial_metrics_calculator):
        self.financial_metrics_calculator = financial_metrics_calculator

    def calculate_stock_health_score(self):
        score = 100  # Start with a base score of 100

        # Assign points based on metrics (adjust these points based on importance)
        points_dict = {
            'yoy_sales_growth': 10,
            'qoq_sales_growth': 10,
            'yoy_profit_growth': 10,
            'qoq_profit_growth': 10,
            'positive_roa': 5,
            'positive_operating_cashflow': 5,
            'positive_cfo_greater_than_net_income': 5,
            'decreasing_debt': 5,
            'positive_current_ratio': 5,
            'same_number_of_shares': 5,
            'asset_turnover': 5,
            'consistent_tax_percentage': 5,
            'roe': 10
        }

        # Deduct points for negative metrics
        if not self.financial_metrics_calculator.has_positive_roa():
            score -= points_dict['positive_roa']

        if not self.financial_metrics_calculator.has_positive_operating_cashflow():
            score -= points_dict['positive_operating_cashflow']

        if not self.financial_metrics_calculator.has_positive_cfo_greater_than_net_income():
            score -= points_dict['positive_cfo_greater_than_net_income']

        # Extract percentage growth for sales and profit
        yoy_sales_growth = max([float(year.split()[-1][:-1]) for year in self.financial_metrics_calculator.yoy_sales()[-5:]])
        qoq_sales_growth = max([float(year.split()[-1][:-1]) for year in self.financial_metrics_calculator.qoq_sales()[-5:]])
        yoy_profit_growth = max([float(year.split()[-1][:-1]) for year in self.financial_metrics_calculator.yoy_profit()[-5:]])
        qoq_profit_growth = max([float(year.split()[-1][:-1]) for year in self.financial_metrics_calculator.qoq_profit()[-5:]])

        # Deduct points based on growth rates
        score -= yoy_sales_growth * (points_dict['yoy_sales_growth'] / 100)
        score -= qoq_sales_growth * (points_dict['qoq_sales_growth'] / 100)
        score -= yoy_profit_growth * (points_dict['yoy_profit_growth'] / 100)
        score -= qoq_profit_growth * (points_dict['qoq_profit_growth'] / 100)

        # Deduct points for decreasing debt
        if float(self.financial_metrics_calculator.yoy_borrowings()[-1].split()[-1][:-1]) > 0:
            score -= points_dict['decreasing_debt']

        # Deduct points for negative current ratio
        if not self.financial_metrics_calculator.has_positive_current_ratio():
            score -= points_dict['positive_current_ratio']

        # Deduct points for different number of shares
        if not self.financial_metrics_calculator.has_same_number_of_shares():
            score -= points_dict['same_number_of_shares']

        # Deduct points for low asset turnover
        if self.financial_metrics_calculator.calculate_asset_turnover() < 1:
            score -= points_dict['asset_turnover']

        # Deduct points for inconsistent tax percentage
        if not self.financial_metrics_calculator.has_consistent_tax_percentage():
            score -= points_dict['consistent_tax_percentage']

        # Deduct points for low ROE
        roe = self.financial_metrics_calculator.calculate_roe()
        if roe < 10:
            score -= points_dict['roe']
        elif roe < 15:
            score -= points_dict['roe'] * 0.5

        return max(score, 0)  # Ensure the score is not negative


    def visualize_riskometer(self, risk_score):
        levels = [20, 40, 60, 80, 100]  # Levels indicating different risk categories
        colors = ['#00e047', '#248003', '#d9c000', '#d97000', '#8a0303']  # Colors for different risk levels

        # Assigning color based on risk score
        color = colors[0]
        for i in range(len(levels)):
            if 100-risk_score >= levels[i]:
                color = colors[i]

        # Creating the riskometer gauge chart
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=100-risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Level"},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': 'white'},
                'steps': [
                    {'range': [0, levels[0]], 'color': colors[0]},
                    {'range': [levels[0], levels[1]], 'color': colors[1]},
                    {'range': [levels[1], levels[2]], 'color': colors[2]},
                    {'range': [levels[2], levels[3]], 'color': colors[3]},
                    {'range': [levels[3], levels[4]], 'color': colors[4]}
                ],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.5,
                    'value': 100-risk_score
                }
            }
        ))

        # Customize layout for the riskometer
        fig.update_layout(
            font=dict(family="Arial, sans-serif"),
            width=400,
            height=300,
            margin=dict(t=80, b=0, l=40, r=40)
        )

        # Show the interactive riskometer graph
        fig.show()
