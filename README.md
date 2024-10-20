# AI-Powered Sales Recommendation Dashboard

This project is an AI-powered dashboard for forecasting sales and providing dynamic sales recommendations based on weather conditions and product categories. It integrates OpenAI's GPT API and OpenWeatherMap to enhance the decision-making process.

---

## Features
- **AI-Powered Recommendations:** Uses OpenAI's GPT models to provide real-time recommendations.
- **Weather Integration:** Retrieves real-time weather data using OpenWeatherMap API.
- **Sales Forecasting:** Predicts future sales trends using machine learning models.
- **Visualizations:** Displays total sales and sales trends using Chart.js.
- **Interactive Dashboard:** Users can register their business and receive tailored recommendations.

---

## Prerequisites
- Python 3.8+
- OpenAI API Key ([Get it here](https://beta.openai.com/signup/))
- OpenWeatherMap API Key ([Get it here](https://openweathermap.org/api))
- PostgreSQL database with your sales data

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-sales-dashboard.git
   cd ai-sales-dashboard
## Create a Virtual Environment
''' bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
## Install Dependencies
pip install -r requirements.txt

## Set Environment Variables
set OPENAI_API_KEY=your-openai-api-key
set OPENWEATHER_API_KEY=your-openweathermap-api-key

## Configure PostgreSQL Database
engine = 'postgresql://username:password@localhost:5432/your_database'
Access the Dashboard
Open your browser and go to:
http://127.0.0.1:5000

## Register Your Business
Enter your business type and select a product category from the dropdown.
## View AI Recommendations
After registration, view real-time weather-based sales recommendations and predictions on the dashboard.


