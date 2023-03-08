# =-=-= End User OAuth Client for all spreadsheets
# gspread Python API for Google Sheets
import gspread

# Requires a 'credentials.json' file to be present in '%appdata%\gspread' (Roaming folder), otherwise it might throw a
# FileNotFoundError.
# IMPORTANT NOTE: The JSON file obtained from Google Cloud console's 'IAM and admin' > 'Service accounts' > 'Keys' >
# 'Add key' (and/or something with 'Manage service accounts' > [Something about 'MedSheet357']) will NOT work and will
# likely throw a 'ValueError: Client secrets must be for a web or installed app.'.
# The JSON required for gspread & Google Sheets integration can be found under 'APIs and services' > 'Credentials' >
# 'OAuth 2.0 Client IDs' > 'Actions' tab > {Download icon} ('Download OAuth client') > 'DOWNLOAD JSON'.
# 09/02/2023 - gspread updated the authentication method, now .service_account() is used instead of .oauth()
# Also I needed a service_account.json from the "Manage service accounts thingy" anyway.
gc = gspread.service_account()
