python
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the dataset (Ensure the dataset is in the same directory as the script)
data = pd.read_excel('ADX_Market_Bulletin_30th_April_2026.xlsx')

@app.route('/')
def index():
    # Extract unique sectors and companies for filtering
    sectors = data['Sector'].unique()
    companies = data['Company'].unique()
    return render_template('index.html', sectors=sectors, companies=companies)

@app.route('/filter', methods=['POST'])
def filter_data():
    selected_sector = request.form.get('sector')
    selected_company = request.form.get('company')

    # Filter data based on user selection
    filtered_data = data
    if selected_sector:
        filtered_data = filtered_data[filtered_data['Sector'] == selected_sector]
    if selected_company:
        filtered_data = filtered_data[filtered_data['Company'] == selected_company]

    # Generate Visualization
    plt.figure(figsize=(10, 5))
    plt.bar(filtered_data['Company'], filtered_data['Market Capitalization'])
    plt.xlabel('Company')
    plt.ylabel('Market Capitalization')
    plt.title(f'Market Capitalization for {selected_sector} Sector')
    plt.savefig('static/market_cap_chart.png')
    plt.close()

    return render_template('results.html', image='static/market_cap_chart.png')

if __name__ == '__main__':
    app.run(debug=True)
