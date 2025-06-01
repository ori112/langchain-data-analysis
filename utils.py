def get_data(sheet_name: str):
    import gspread
    from gspread_dataframe import get_as_dataframe
    from oauth2client.service_account import ServiceAccountCredentials

    # Load your sheet config
    sheet_url = "https://docs.google.com/spreadsheets/d/1oxKEu-3KPbuQaajXDQxgY2AM7wIn_lB3zxXbsA6vDFE"
    key_path = "secrets/google_sheets_keys.json"  # adjust path if needed

    # Define access scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Authenticate
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
    client = gspread.authorize(creds)

    # Open and read
    worksheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    df = get_as_dataframe(worksheet, evaluate_formulas=True).dropna(axis=1, how="all")

    print("Sheet loaded. Shape:", df.shape)
    return df