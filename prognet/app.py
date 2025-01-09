from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from webexteamssdk import WebexTeamsAPI

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your secret key

# Constants
API_KEY = "XZTnRZVAs2fC8Q9ODTkEhwXVA3puh4w8"  # Replace with your Calendarific API key
BASE_URL = "https://calendarific.com/api/v2/holidays"
WEBEX_ACCESS_TOKEN = "MjQzOGVhMDctODk0Zi00YWZkLWE2N2ItMTBiZWU4YjE2OWIxNzkwYWJjYWItZDc3_P0A1_e77bdb70-5835-4193-b328-1a7e84839fa8"  # Replace with your Webex access token
WEBEX_ROOM_ID = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vN2JhZjkxYTAtMjIyNi0xMWVmLWIwMmQtNmZhYWY3NDQ4NzE5"  # Replace with your Webex room ID

# List of countries and their ISO codes
COUNTRIES = {
    "Malaysia": "MY",
    "United States": "US",
    "United Kingdom": "GB",
    "Canada": "CA",
    "Australia": "AU",
    "India": "IN",
    "Singapore": "SG",
    "Philippines": "PH",
    "Japan": "JP",
    "Germany": "DE"
}


def send_to_webex(message):
    """
    Send a message to a Webex room.
    """
    try:
        api = WebexTeamsAPI(access_token=WEBEX_ACCESS_TOKEN)
        api.messages.create(roomId=WEBEX_ROOM_ID, markdown=message)
    except Exception as e:
        print(f"Error sending message to Webex: {e}")


@app.route("/")
def index():
    """
    Render the homepage with country and year selection.
    """
    return render_template("index.html", countries=COUNTRIES, current_year=2024)


@app.route("/results", methods=["POST"])
def results():
    """
    Fetch and display public holidays for the selected country and year.
    """
    country = request.form.get("country")
    year = request.form.get("year")
    if not country or not year:
        flash("Please select both a country and a year.", "error")
        return redirect(url_for("index"))

    # Fetch holidays from the API
    params = {"api_key": API_KEY, "country": country, "year": year}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["meta"]["code"] == 200:
            holidays = data["response"]["holidays"]

            # Extract unique holiday types and states
            holiday_types = set()
            states = set()
            for holiday in holidays:
                holiday_types.update(holiday["type"])
                if "states" in holiday and holiday["states"]:
                    states.update(state["name"] for state in holiday["states"] if "name" in state)

            return render_template(
                "results.html",
                holidays=holidays,
                country=country,
                year=year,
                holiday_types=holiday_types,
                states=states,
            )
        else:
            flash("Error fetching holidays: " + data["meta"]["error_detail"], "error")
    except requests.exceptions.RequestException as e:
        flash(f"Error connecting to the API: {e}", "error")

    return redirect(url_for("index"))


@app.route("/filter", methods=["POST"])
def filter_results():
    """
    Filter the holiday results based on the user-selected criteria (month, type, state).
    """
    import ast  # For safely evaluating strings as data structures
    holidays = ast.literal_eval(request.form.get("holidays"))  # Convert string back to a list
    country = request.form.get("country")
    year = request.form.get("year")
    month = request.form.get("month")
    holiday_type = request.form.get("holiday_type")
    state = request.form.get("state")

    # Apply filters
    if month and month != "Select All":
        holidays = [holiday for holiday in holidays if holiday["date"]["datetime"]["month"] == int(month)]
    if holiday_type and holiday_type != "Select All":
        holidays = [holiday for holiday in holidays if holiday_type in holiday["type"]]
    if state and state != "Select All":
        holidays = [
            holiday
            for holiday in holidays
            if "states" in holiday and any(
                isinstance(s, dict) and s.get("name") == state for s in holiday["states"]
            )
        ]

    # Format filtered holidays for Webex
    webex_message = f"**Filtered Holidays in {country} ({year})**\n\n"
    if holidays:
        for holiday in holidays:
            holiday_name = holiday["name"]
            date = holiday["date"]["iso"]
            holiday_type = ", ".join(holiday["type"])
            if "states" in holiday and holiday["states"]:
                states = ", ".join(
                    [s["name"] for s in holiday["states"] if isinstance(s, dict) and "name" in s]
                )
            else:
                states = "All States"

            webex_message += f"- **{holiday_name}** on *{date}* ({holiday_type}) in *{states}*\n"
    else:
        webex_message += "No holidays found matching the filters."

    # Send filtered results to Webex
    send_to_webex(webex_message)

    # Render the filtered results in the same template
    return render_template(
        "results.html", holidays=holidays, country=country, year=year, holiday_types=[], states=[]
    )

if __name__ == "__main__":
    app.run(debug=True)
