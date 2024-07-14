from flask import Flask, jsonify, render_template
from tsa import TimeSeries
from weather import Weather
import assistant
import requests

app = Flask(__name__,template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tsa')
def tsa():
    return render_template('tsa.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/tsa_forecast', methods=['GET'])
def tsa_forecast():
    start_year = requests.args.get('start_year')
    end_year = requests.args.get('end_year')
    
    if not start_year or not end_year:
        return jsonify({"error": "Start year and end year are required"}), 400
    
    try:
        ts = TimeSeries('cardamom data.xlsx')
        forecast_data = ts.forecast(start_year, end_year)
        return forecast_data.to_json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather', methods=['GET'])
def get_weather():
    city=Weather().weather("Kochi")
    return city

@app.route('/assistant', methods=['GET'])
def assistant():
    assistant.run()

if __name__ == '__main__':
    app.run(debug=True)

