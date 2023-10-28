from flask import Flask, request
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
    try:
        order_id = request.args.get('order-id')
        product_id = request.args.get('product-id')
        data_to_append = [[order_id, product_id]]
        worksheet.append_rows(data_to_append)
        return 'success'
    
    except ValueError as e:
        return f'Error: {str(e)}', 400

    except KeyError as e:
        return f'Missing parameter: {str(e)}', 400

    except Exception as e:
        return f'Error: {str(e)}', 500


if __name__ == '__main__':
    app.run(debug=False)