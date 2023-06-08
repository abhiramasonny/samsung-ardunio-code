from flask import Flask
import csv

app = Flask(__name__)

@app.route('/')
def index():
    with open('index.html', 'r') as file:
        html = file.read()
    data = read_csv_data()
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Heart System Dashboard</title>
        <style>
            h1 {{
            text-align: center;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                text-align: center;
            }}
            
            th, td {{
                padding: 8px;
                border: 1px solid #ddd;
            }}
            
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Heart System Dashboard</h1>
        
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>BPM</th>
                </tr>
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
    </body>
    </html>
    """.format(generate_table_rows(data))

    return html

def read_csv_data():
    data = []
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def generate_table_rows(data):
    rows = ""
    for row in data:
        table_row = """
        <tr>
            <td>{}</td>
            <td>{}</td>
        </tr>
        """.format(row['Timestamp'], row['BPM'])
        rows += table_row
    return rows

if __name__ == '__main__':
    app.run()
