import requests
import pandas as pd
import os

# Folder to save live NAV files
output_folder = "data/raw"

# Create folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# AMFI Scheme Codes
schemes = {
    "HDFC_Top100_Direct": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

print("=" * 60)
print("LIVE NAV FETCH STARTED")
print("=" * 60)

for scheme_name, scheme_code in schemes.items():

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"\nFetching {scheme_name} ({scheme_code})")

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        nav_data = pd.DataFrame(data["data"])

        file_name = f"{scheme_name}_live_nav.csv"

        file_path = os.path.join(output_folder, file_name)

        nav_data.to_csv(file_path, index=False)

        print("Saved:", file_name)
        print("Records:", len(nav_data))

    else:

        print("Failed to fetch", scheme_name)

print("\nLive NAV fetching completed.")