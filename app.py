from flask import Flask, jsonify, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

try:
    spreadsheet = gc.open('test-sheet')
    worksheet = spreadsheet.worksheet('testsheet')
except gspread.exceptions.SpreadsheetNotFound as e:
    print(f"Error: {e}")
    raise

# endpoint to read data from Google Sheet
@app.route('/read', methods=['GET'])
def read_data():
    data = worksheet.get_all_values()
    return jsonify(data)

# endpoint to write data to Google Sheet
@app.route('/write', methods=['POST'])
def write_data():
    try:
        data_to_write = request.get_json()
        worksheet.append_rows([list(data_to_write.values())])
        return jsonify({'message': 'Data written successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
