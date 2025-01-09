# Public Holiday Finder

## Overview
Public Holiday Finder is a Python-based GUI application that allows users to fetch and filter public holidays for various countries using the Calendarific API. The application also integrates with Webex to send filtered holiday results to a Webex room.

## Features
- Fetch public holidays for different countries and years using the Calendarific API.
- Filter holidays by month, type, and state.
- Display results in a user-friendly GUI using Tkinter.
- Send filtered holiday lists to a Webex room.

## Technologies Used
- Python
- Tkinter (GUI framework)
- Requests (HTTP requests)
- WebexTeamsSDK (Webex API integration)

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x
- Required Python libraries:
  ```bash
  pip install requests tkinter webexteamssdk
  ```
- A valid Calendarific API key
- A Webex access token and room ID

## Installation
1. Clone or download the project files.
2. Install the required dependencies using pip:
   ```bash
   pip install requests webexteamssdk
   ```
3. Replace the placeholders in the script with your own API credentials:
   - `API_KEY`: Your Calendarific API key.
   - `WEBEX_ACCESS_TOKEN`: Your Webex access token.
   - `WEBEX_ROOM_ID`: Your Webex room ID.

## Usage
1. Run the script:
   ```bash
   python public_holiday_finder.py
   ```
2. Select a country and year from the dropdown menus.
3. Click "Find Holidays" to fetch and display public holidays.
4. Apply optional filters by month, holiday type, or state.
5. Click "Apply Filters" to update the displayed results.
6. Filtered holidays will be sent to the Webex room automatically.

## File Structure
```
public_holiday_finder.py  # Main script file
README.md                  # Documentation
```

## Security Considerations
- **DO NOT** hardcode sensitive API keys or access tokens in public repositories.
- Consider using environment variables or a configuration file to store credentials securely.
- Use `.gitignore` to exclude sensitive files from version control.

## Troubleshooting
- **No holidays found:** Ensure the selected country and year have public holidays listed in the Calendarific API.
- **API connection error:** Check your internet connection and verify that the API key is valid.
- **Webex message not sent:** Ensure your Webex access token and room ID are correct and valid.

## Limitation
- **Only limited to 500 API requests**
- **Need to make sure your Webex Access token and RoomID is Correct and Valid**
- **Limited Country Support** : The project only includes a predefined set of countries (Malaysia, USA, UK, etc.), so users cannot search for holidays in countries not listed.
  
## License
This project is released under the MIT License. (i guess)

