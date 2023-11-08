import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
from django.shortcuts import render,redirect
import base64
from .financial_metrics import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,auth


# Create your views here.
def Home(request):
    return render(request, 'untitled-1.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # User authenticated, log them in
            auth.login(request, user)
            return redirect('index.html')  # Redirect to home page after successful login
        else:
            # Invalid login, show error message
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')

def Register(request):
    if request.method == 'POST':
        # Extract form data
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        # Validate form data
        if not (first_name and last_name and email and password and password_repeat):
            # Handle validation error, e.g., return an error message to the template
            return render(request, 'register.html', {'error': 'All fields are required'})

        if password != password_repeat:
            # Handle password mismatch error, e.g., return an error message to the template
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        # Create and save the user
        user = User.objects.create_user(username=username,first_name=first_name, email=email, password=password, last_name=last_name)
        user.save()
        print('User created')
        return redirect('index.html')
    else:
        return render(request, 'register.html')

def AboutUs(request):
    return render(request, 'untitled.html')

#def Index(request):
#    return render(request, 'index.html')

def stock_name(request):
    #name = name.upper()
    #name = name.replace(" ", "")
    #n = name + '.NS'
    #stock = yf.Ticker(n)
    n = 'RELIANCE.NS'
    return n

def stock_price(request):
    n = 'RELIANCE.NS'
    stock = yf.Ticker(n)
    stock_info = stock.history()
    last_quote = stock_info['Close'].iloc[-1]
    last_quote = round(last_quote, 2)

    # Process stock_info data as needed
    # ...
    return last_quote

def plot_yoy_sales_growth(request):
    # Perform necessary calculations to get yoy sales data
    financial_metrics_calculator = FinancialMetricsCalculator(transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
    qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow)  # Initialize your FinancialMetricsCalculator object with appropriate data
    yoy_sales_data = financial_metrics_calculator.yoy_sales()  # Replace with the actual method call to get yoy sales data

    # Extract years and sales growth rates from yoy_sales_data
    years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
    sales_growth_rates = [float(data.split(',')[2].split(': ')[1].strip('%')) for data in yoy_sales_data]

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=sales_growth_rates, mode='markers+lines', marker=dict(size=12),
                             line=dict(color='white', width=2)))
    fig.update_layout(title='YoY Sales Growth Rate Over Years', xaxis_title='Year', yaxis_title='YoY Sales Growth Rate (%)',
                      xaxis=dict(tickangle=45,showgrid=False), yaxis=dict(showgrid=False), template='plotly_dark')

    # Render the plot as a template variable
    plot_div = fig.to_html(full_html=False, default_height=330, default_width=600)

    # Render the template with the plot
    return plot_div

def plot_sales(request, period='yoy'):
    # Perform necessary calculations to get sales data
    financial_metrics_calculator = FinancialMetricsCalculator(transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
    qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow)  # Initialize your FinancialMetricsCalculator object with appropriate data

    if period == 'yoy':
        sales_data = financial_metrics_calculator.yoy_sales()  # Replace with the actual method call to get yoy sales data
    elif period == 'qoq':
        sales_data = financial_metrics_calculator.qoq_sales()  # Replace with the actual method call to get qoq sales data
    else:
        sales_data = []

    # Extract years and sales growth rates from sales_data
    years = [data.split(',')[0].split(': ')[1] for data in sales_data]
    sales_growth = [float(data.split(',')[1].split(': ')[1].strip('%')) for data in sales_data]

    # Create the Plotly figure with white background and grey bars
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=sales_growth, marker_color='#4682B4'))
    fig.update_layout(xaxis_title='Year', yaxis_title='Sales in Rs. (Cr)',
                      xaxis=dict(tickangle=45, showgrid=False), yaxis=dict(showgrid=False), template='plotly_white')

    # Convert the Plotly figure to HTML
    plot_div = fig.to_html(full_html=False, default_height=330, default_width=630)
    
    return plot_div


def plot_profit(request, period='yoy'):
    
    # Perform necessary calculations to get sales data
    financial_metrics_calculator = FinancialMetricsCalculator(transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
    qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow)  # Initialize your FinancialMetricsCalculator object with appropriate data

    if period == 'yoy':
        sales_data = financial_metrics_calculator.yoy_profit()  # Replace with the actual method call to get yoy sales data
    elif period == 'qoq':
        sales_data = financial_metrics_calculator.qoq_profit()  # Replace with the actual method call to get qoq sales data
    else:
        sales_data = []

    # Extract years and sales growth rates from sales_data
    years = [data.split(',')[0].split(': ')[1] for data in sales_data]
    sales_growth = [float(data.split(',')[1].split(': ')[1].strip('%')) for data in sales_data]

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=sales_growth, marker_color='#4682B4'))
    fig.update_layout(xaxis_title='Year', yaxis_title='Profit in Rs. (Cr)',
                      xaxis=dict(tickangle=45, showgrid=False), yaxis=dict(showgrid=False), template='plotly_white')

    # Convert the Plotly figure to HTML
    plot_div = fig.to_html(full_html=False, default_height=330, default_width=630)
    
    return plot_div
    

def stock_hist_with_volume(request):
    selected_period = "1y"  # Default period
    if request.method == "POST":
        selected_period = request.POST.get("period", "1mo")

    # Fetch stock data (replace 'RELIANCE.NS' with your desired stock symbol)
    stock_symbol = 'RELIANCE.NS'
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period=selected_period)

    # Create a subplot with price and volume
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Price', line=dict(color='green')), secondary_y=True)
    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color='blue'), secondary_y=False)

    # Update layout and display the chart
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price',  # Change this to 'Volume' if you want to show the volume on the primary y-axis
        yaxis2_title='Volume',
        template='plotly_white',  # Set plot theme to white background
        margin=dict(l=20, r=20, t=40, b=20),  # Adjust margins for better layout
        hovermode='x unified',  # Show hover info for all traces at the same x position
    )

    # Convert the Plotly figure to HTML
    plot_div = fig.to_html(full_html=False, default_height=330, default_width=630)

    # Create HTML form with toggle buttons
    toggle_form = """
    <form method="post">
        {% csrf_token %}
        <label>Select Time Period:</label>
        <input type="submit" name="period" value="1mo">
        <input type="submit" name="period" value="1y">
        <input type="submit" name="period" value="5y">
        <input type="submit" name="period" value="max">
    </form>
    """

    # Combine form and plot_div and return
    result_html = toggle_form + plot_div
    return result_html


def plot_promoter_holdings(request):
    # Initialize your FinancialMetricsCalculator object with appropriate data
    financial_metrics_calculator = FinancialMetricsCalculator(transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
    qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow)

    yoy_promoters = financial_metrics_calculator.promoter_holdings()

    # Create the pie chart using Plotly Express
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
        paper_bgcolor='white',  # Background color
        font=dict(family='Arial', color='black'),  # Set a custom font and text color
        legend=dict(orientation='h', y=1.2),  # Legend position
    )

    # Convert the Plotly figure to HTML
    plot_div = fig.to_html(full_html=False, default_height=330, default_width=630)

    return plot_div

def plot_yoy_borrowings_growth(request):
    # Initialize your FinancialMetricsCalculator object with appropriate data
    financial_metrics_calculator = FinancialMetricsCalculator(
        transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
        qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow
    )

    yoy_sales_data = financial_metrics_calculator.yoy_borrowings()
    yoy_sales_data = yoy_sales_data[1:]
    years = [data.split(',')[0].split(': ')[1] for data in yoy_sales_data]
    profit_growth_rates = [float(data.split(',')[2].split(': ')[1].strip('%')) for data in yoy_sales_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=profit_growth_rates, mode='markers+lines', marker=dict(size=12),
                             line=dict(color='#4682B4', width=2)))
    fig.update_layout(xaxis_title='Year',
                      yaxis_title='YoY Borrowings Rate (%)', xaxis=dict(tickangle=45, showgrid=False),
                      yaxis=dict(showgrid=False), template='plotly_white')

    # Convert the Plotly figure to div for rendering in the template
    plot_div = fig.to_html(full_html=False, default_height=330, default_width=630)

    # Pass the plot_div to the template
    return plot_div


def riskometer(request):
    financial_metrics_calculator = FinancialMetricsCalculator(
        transposed_income_statement, transposed_balance_sheet, transposed_cash_flow,
        qtr_transposed_income_statement, qtr_transposed_balance_sheet, qtr_transposed_cash_flow
    )

    # Pass the financial_metrics_calculator instance to StockHealthCalculator constructor
    stock_health_calculator_instance = StockHealthCalculator(financial_metrics_calculator)
    # Calculate risk score by calling the method on the instance
    risk_score = stock_health_calculator_instance.calculate_stock_health_score()

    
    # Create the riskometer chart
    levels = [20, 40, 60, 80, 100]
    colors = ['#00e047', '#248003', '#d9c000', '#d97000', '#8a0303']

    color = colors[0]
    for i in range(len(levels)):
        if 100 - risk_score >= levels[i]:
            color = colors[i]

    chart = go.Figure()
    chart.add_trace(go.Indicator(
        mode="gauge+number",
        value=100 - risk_score,
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
                'value': 100 - risk_score
            }
        }
    ))

    chart_layout = {
        'font': dict(family="Arial, sans-serif"),
        'width': 600,
        'height': 320,
        'margin': dict(t=80, b=0, l=40, r=40)
    }

    chart.update_layout(chart_layout)
    riskometer_div = chart.to_html(full_html=False)

    return riskometer_div


def current_ratio(request):
    current_ratio = financial_metrics_calculator.current_ratio()
    return round(current_ratio,2)

def asset_turnover(request):
    asset_turnover = financial_metrics_calculator.calculate_asset_turnover()
    return round(asset_turnover,2)

def roe(request):
    roe = financial_metrics_calculator.calculate_roe()
    return round(roe,2)

def roa(request):
    roa = financial_metrics_calculator.roa()
    return round(roa,2)

def roe(request):
    roe = financial_metrics_calculator.calculate_roe()
    return round(roe,2)


    
def index(request):
    # Get data from both functions
    yoy_sales_plot = plot_sales(request)
    stockname = stock_name(request)
    stock_last_quote = stock_price(request)
    stock_hist_1mo = stock_hist_with_volume(request)
    yoy_profit_plot = plot_profit(request)
    plot_promoter = plot_promoter_holdings(request)
    plot_borrowings = plot_yoy_borrowings_growth(request)
    stock_health = riskometer(request)
    current_ratio1 = current_ratio(request)
    asset_turnover1 = asset_turnover(request)
    roa1 = roa(request)
    roe1 = roe(request)

    # Create a context dictionary with the data
    context = {
        'yoy_sales_plot': yoy_sales_plot,
        'stock_last_quote': stock_last_quote,
        'stock_hist_1mo_w_volume': stock_hist_1mo,
        'yoy_profit_plot': yoy_profit_plot,
        'plot_promoter': plot_promoter,
        'stock_name' : stockname,
        'plot_borrowings' : plot_borrowings,
        'stock_health' : stock_health,
        'current_ratio' : current_ratio1,
        'asset_turnover' : asset_turnover1,
        'roa' : roa1,
        'roe' : roe1,
    }

    # Render the template with the context data
    return render(request, 'index.html', context)
'''
def index1(request):
    stock_name = None
    stock_last_quote = None

    if request.method == 'POST':
        # Get user input from the form
        stock_symbol = request.POST.get('stock_symbol')
        stock_symbol = stock_symbol.upper()
        stock_symbol = stock_symbol.replace(" ", "")
        stock_symbol = stock_symbol + '.NS'
        stock = yf.Ticker(stock_symbol)
        stock_name = stock_symbol  # Set stock_name to display the entered stock symbol
        stock_info = stock.history()
        stock_last_quote = round(stock_info['Close'].iloc[-1], 2)
        return stock_name

    # Render the template with the context data
    context = {
        'stock_name': stock_name,
        'stock_last_quote': stock_last_quote,
    }

    return render(request, 'trial.html', context)
'''
import yfinance as yf
from django.shortcuts import render
from .financial_metrics import FinancialMetricsCalculator, StockHealth, SalesVisualizer, StockHealthCalculator

def index1(request):
    stock_name = None
    stock_last_quote = None
    stock_metrics = None
    stock_health_score = None
    riskometer = None

    if request.method == 'POST':
        # Get user input from the form
        stock_symbol = request.POST.get('stock_symbol')
        stock_symbol = stock_symbol.upper()
        stock_symbol = stock_symbol.replace(" ", "")
        stock_symbol = stock_symbol + '.NS'
        stock = yf.Ticker(stock_symbol)

        # Get stock name and last quote
        stock_name = stock_symbol
        stock_info = stock.history(period='1d')
        stock_last_quote = round(stock_info['Close'].iloc[-1], 2)


        # Create financial metrics calculator
        financial_data = FinancialMetricsCalculator(stock.income_stmt, stock.balance_sheet, stock.cash_flow,stock.quarterly_income_stmt,stock.quarterly_balance_sheet,stock.quarterly_cashflow)

        # Calculate stock health score
        stock_health = StockHealthCalculator(financial_data)
        stock_health_score = stock_health.calculate_stock_health_score()

        # Visualize riskometer
        riskometer = stock_health.visualize_riskometer(stock_health_score)

    # Render the template with the context data
    context = {
        'stock_name': stock_name,
        'stock_last_quote': stock_last_quote,
        'stock_health_score': stock_health_score,
        'riskometer': riskometer,
    }

    return render(request, 'trial.html', context)


