from flask import Flask, request, jsonify, send_from_directory
import csv
import os

app = Flask(__name__)

# Path to the CSV file where data will be stored
CSV_FILE = 'data.csv'

# Check if the CSV file exists, if not, create it with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Phone Number'])  # Add headers


@app.route('/download')
def download_file():
    # Ensure the file exists before attempting to send it
    if os.path.exists(CSV_FILE):
        return send_from_directory(
            directory=os.getcwd(),  # Current working directory
            path=CSV_FILE,           # The CSV file to be downloaded
            as_attachment=True,      # Forces download instead of opening in the browser
            download_name='data.csv', # The name the file will have when downloaded
            mimetype='text/csv'       # MIME type for CSV files
        )
    else:
        return "File not found", 404
    
@app.route('/submit', methods=['POST'])
def submit_data():
    # Get JSON data from the request
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')

    # Validate data
    if not name or not phone:
        return jsonify({'error': 'Name and Phone are required'}), 400

    # Open the CSV file and append the new row
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, phone])

    return jsonify({'message': 'Data saved successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
