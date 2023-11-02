import requests
import gspread
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

# Calculating tomorrow's date by adding one day using timedelta and formatting it.
tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')

# Const values needed to be set for accessing google account & sheet.
spreadsheet_name = "ShiftShedule"
sheet_name = "full_shedule"
full_form = {"M": "Morning","A": "Afternoon","N": "Night","O": "Off"}

def telegram_notification(msg_data):
    print(msg_data)
    # Sending a Telegram Notification.
    TOKEN = "5681478504:AAFGKXctUmv9-9IKVmZyNKJtO05I5IXxDHE"
    chat_id = "1069103389"
    message = msg_data
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    # Sends the Notification & also prints the response.
    requests.get(url).json()

def g_data():
    # Replace 'YOUR_CREDENTIALS_FILE.json' with the path to your downloaded JSON credentials file.
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/var/jenkins_home/workspace/Shift_1/servicekey.json', scope)
    client = gspread.authorize(credentials)
    print(credentials)

    # Check if the Sheet is availble and save the data to a variable.
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        msg_data = "Spreadsheet Not Found"
        telegram_notification(msg_data)
        return
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        msg_data = "Spread is Found but Sheet is not available"
        telegram_notification(msg_data)
        return

    # Find the row index for Kiren (assuming the names are in the first column).
    engg_name = worksheet.col_values(1)
    engg_row_index = engg_name.index('Kiren Aananth|1007620')  + 1 # Adding 1 to convert to 1-indexed.
    print(engg_row_index)

    # Find the column index for shift (assuming the shift are in the first row).
    shift_date = worksheet.row_values(1)
    shift_column_index = shift_date.index(tomorrow_date) + 1 # Adding 1 to convert to 1-indexed.
    print(shift_column_index)

    # Get Kiren's shift in shift from the corresponding cell.
    engg_shift = worksheet.cell(engg_row_index, shift_column_index).value
    print(engg_shift)
    shift_fullform = full_form.get(engg_shift)
    msg_data = ("Shift is "+ shift_fullform)
    telegram_notification(msg_data)

g_data()
