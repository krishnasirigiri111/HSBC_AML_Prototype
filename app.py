from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Load suspicious transactions
    suspicious = pd.read_csv('suspicious_transactions.csv')
    
    # Prepare data for Chart.js
    chart_data = {
        'labels': suspicious['transaction_id'].astype(str).tolist(),
        'amounts': suspicious['amount'].tolist()
    }
    
    return render_template('dashboard.html', 
                         table=suspicious.to_html(classes='table table-striped', index=False),
                         chart_data=json.dumps(chart_data))

if __name__ == '__main__':
    app.run(debug=True)