import gspread
import json

# --- Configuration ---
CREDENTIALS_FILE = 'credentials.json' 

# IMPORTANT: Change this to your exact Google Sheet name
SHEET_NAME = 'Gov Jobs Admin' 

OUTPUT_JSON_FILE = 'offline_database.json'

def export_sheet_to_json():
    print("Connecting to Google Sheets...")
    try:
        # Authenticate using the secret credentials
        gc = gspread.service_account(filename=CREDENTIALS_FILE)
        
        # Open the entire spreadsheet file
        spreadsheet = gc.open(SHEET_NAME)

        # Create an empty dictionary to hold all the data
        all_data = {}

        print(f"Fetching all tabs from '{SHEET_NAME}'...")
        
        # Get a list of every tab in the spreadsheet
        worksheets = spreadsheet.worksheets()

        # Loop through each tab one by one
        for ws in worksheets:
            print(f"  -> Scraping tab: {ws.title}")
            # Grab all rows from this specific tab
            records = ws.get_all_records()
            # Save it into our dictionary using the tab's name as the label
            all_data[ws.title] = records

        # Save the combined data to the JSON file
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        print(f"Success! Saved data from {len(worksheets)} tabs to {OUTPUT_JSON_FILE}.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # This tells GitHub the action failed if there is an error
        raise SystemExit(1) 

if __name__ == '__main__':
    export_sheet_to_json()
