from flask import Flask, request, render_template, redirect, url_for, jsonify
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Initialize the users list
users = []
engine = 'postgresql://postgres:Kgau123%40M@localhost:5432/data'

# Load and prepare the Fashion Retail Sales data
try:
    query = "SELECT * FROM data_dynamo;"
    sales_data = pd.read_sql(query, engine)
    sales_data['Date Purchase'] = pd.to_datetime(sales_data['Date Purchase'], errors='coerce')

    # Clean and group the data
    sales_data_clean = sales_data[['Date Purchase', 'Item Purchased', 'Purchase Amount (USD)']]
    sales_data_grouped = sales_data_clean.groupby(['Date Purchase', 'Item Purchased']).sum().reset_index()

    # Pivot to get product-category-by-date sales matrix
    sales_data_pivot = sales_data_grouped.pivot(
        index='Date Purchase', columns='Item Purchased', values='Purchase Amount (USD)'
    ).fillna(0)
except Exception as e:
    print(f"Error loading or processing the sales data: {e}")
    sales_data_pivot = pd.DataFrame()

API_KEY = '7f33ea49a3a50210cccd681d651abb46'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def safe_float(value):
    """Convert a value to float, or return 0.0 if conversion fails."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def get_items():
    return list(sales_data_pivot.columns) if not sales_data_pivot.empty else []

def get_weather(city='Seattle'):
    """Fetch real-time weather data for a given city."""
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'temperature': data['main'].get('temp', 0.0),
            'precipitation': data.get('rain', {}).get('1h', 0.0),
            'wind_speed': data['wind'].get('speed', 0.0)
        }
    except requests.RequestException as e:
        print(f"Failed to retrieve weather data: {e}")
        return {'temperature': 0.0, 'precipitation': 0.0, 'wind_speed': 0.0}

def train_model(product_column):
    """Train a model for a specific product category."""
    if product_column not in sales_data_pivot.columns:
        raise ValueError(f"Invalid product category: {product_column}")

    X = sales_data_pivot[['Handbag', 'Tunic', 'Tank Top']]
    y = sales_data_pivot[product_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

@app.route('/', methods=['GET', 'POST'])
def register():
    """Register a business with a product category using a dropdown."""
    product_categories = get_items()

    if request.method == 'POST':
        business_type = request.form.get('business_type')
        product_category = request.form.get('product_category', 'Unknown')

        if product_category not in product_categories:
            return f"Invalid product category. Available categories: {', '.join(product_categories)}", 400

        users.append({'business_type': business_type, 'product_category': product_category})
        return redirect(url_for('dashboard'))

    return render_template('register.html', categories=product_categories)

@app.route('/dashboard')
def dashboard():
    """Display the forecasted sales, weather, and recommendations."""
    if not users:
        return redirect(url_for('register'))

    user = users[-1]
    weather_forecast = get_weather(city='Seattle')

    temperature = safe_float(weather_forecast.get('temperature'))
    precipitation = safe_float(weather_forecast.get('precipitation'))
    wind_speed = safe_float(weather_forecast.get('wind_speed'))

    try:
        model = train_model(user['product_category'])
    except ValueError as e:
        return str(e), 400

    prediction = model.predict([[temperature, precipitation, wind_speed]])[0]
    recommendation = recommend_action(temperature, precipitation, user['product_category'])

    # Calculate total sales by product category
    total_sales = sales_data_pivot.sum().to_dict()

    # Calculate sales trends over time (convert Timestamp to string)
    sales_trends = {date.strftime('%Y-%m-%d'): amount for date, amount in sales_data_pivot.sum(axis=1).items()}

    return render_template(
        'dash.html',user=user,
        prediction=prediction,
        recommendation=recommendation,
        weather_forecast=weather_forecast,
        total_sales=total_sales,
        sales_trends=sales_trends
    )

def recommend_action(temperature, precipitation, product):
    """Provide recommendations based on product category and weather."""
    if product == 'Handbag' and temperature < 5:
        return "Promote winter-themed handbags."
    elif product == 'Tunic' and precipitation > 20:
        return "Offer waterproof tunics with discounts."
    elif product == 'Tank Top' and temperature > 30:
        return "Promote summer sales on tank tops."
    else:
        return "Maintain regular stock levels."

if __name__ == '__main__':
    app.run(debug=True)
