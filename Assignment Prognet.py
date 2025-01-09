import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from webexteamssdk import WebexTeamsAPI

# Constants
API_KEY = "XZTnRZVAs2fC8Q9ODTkEhwXVA3puh4w8"  # Replace with your Calendarific API key
BASE_URL = "https://calendarific.com/api/v2/holidays"

# Webex Configuration
WEBEX_ACCESS_TOKEN = "<Your Webex Access Token>"  # Replace with your Webex access token
WEBEX_ROOM_ID = "<Your RoomID>"  # Replace with your Webex room ID

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


def fetch_holidays(country, year):
    """
    Fetch public holidays for a specific country and year using Calendarific API.
    """
    try:
        params = {
            "api_key": API_KEY,
            "country": country,
            "year": year
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["meta"]["code"] == 200:
            return data["response"]["holidays"]
        else:
            messagebox.showerror("Error", f"Error fetching holidays: {data['meta']['error_detail']}")
            return []
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error connecting to the API: {e}")
        return []


def filter_holidays(holidays, month=None, holiday_type=None, state=None):
    """
    Filter the holiday list based on user-selected criteria.
    """
    filtered = holidays
    if month and month != "Select All":
        filtered = [holiday for holiday in filtered if holiday["date"]["datetime"]["month"] == int(month)]
    if holiday_type and holiday_type != "Select All":
        filtered = [holiday for holiday in filtered if holiday_type in holiday["type"]]
    if state and state != "Select All":
        filtered = [
            holiday
            for holiday in filtered
            if "states" in holiday and isinstance(holiday["states"], list) and any(
                isinstance(s, dict) and "name" in s and s["name"] == state for s in holiday["states"]
            )
        ]
    return filtered


def send_to_webex(message):
    """
    Send a message to a Webex room.
    """
    try:
        api = WebexTeamsAPI(access_token=WEBEX_ACCESS_TOKEN)
        api.messages.create(roomId=WEBEX_ROOM_ID, markdown=message)
        messagebox.showinfo("Success", "Filtered results sent to Webex room!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send message to Webex: {e}")


def display_holidays(country, year):
    """
    Fetch and display holidays in a tabular format using Treeview, with filtering options.
    """
    holidays = fetch_holidays(country, year)

    # Filter out equinox and solstice holidays
    holidays = [holiday for holiday in holidays if not any(keyword in holiday["name"].lower() for keyword in ["equinox", "solstice"])]

    if not holidays:
        messagebox.showinfo("No Holidays", f"No holidays found for {country} in {year}.")
        return

    # Create a new window to display the holidays
    holidays_window = tk.Toplevel()
    holidays_window.title(f"Holidays in {country} ({year})")
    holidays_window.geometry("900x500")

    # Dropdown for filtering
    tk.Label(holidays_window, text="Filter by:").pack(pady=5)
    filter_frame = tk.Frame(holidays_window)
    filter_frame.pack()

    # Month filter
    tk.Label(filter_frame, text="Month:").grid(row=0, column=0, padx=5, pady=5)
    month_var = tk.StringVar()
    month_dropdown = ttk.Combobox(filter_frame, textvariable=month_var, values=["Select All"] + [str(i) for i in range(1, 13)], state="readonly")
    month_dropdown.grid(row=0, column=1)

    # Type filter
    tk.Label(filter_frame, text="Holiday Type:").grid(row=0, column=2, padx=5, pady=5)
    type_var = tk.StringVar()
    type_dropdown = ttk.Combobox(filter_frame, textvariable=type_var, state="readonly")
    type_dropdown.grid(row=0, column=3)

    # Populate holiday types dynamically
    all_types = set()
    for holiday in holidays:
        all_types.update(holiday["type"])
    type_dropdown["values"] = ["Select All"] + list(all_types)

    # State filter
    tk.Label(filter_frame, text="State:").grid(row=0, column=4, padx=5, pady=5)
    state_var = tk.StringVar()
    state_dropdown = ttk.Combobox(filter_frame, textvariable=state_var, state="readonly")
    state_dropdown.grid(row=0, column=5)

    # Populate states dynamically
    all_states = set()
    for holiday in holidays:
        if "states" in holiday:
            for state in holiday["states"]:
                if "name" in state:
                    all_states.add(state["name"])
    state_dropdown["values"] = ["Select All"] + list(all_states)

    # Treeview for displaying holidays
    tree = ttk.Treeview(holidays_window, columns=("Name", "Date", "Type", "States"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    # Define column headings
    tree.heading("Name", text="Holiday Name")
    tree.heading("Date", text="Date")
    tree.heading("Type", text="Type")
    tree.heading("States", text="States")

    # Set column widths
    tree.column("Name", width=300, anchor="w")
    tree.column("Date", width=100, anchor="center")
    tree.column("Type", width=200, anchor="w")
    tree.column("States", width=200, anchor="w")

    def update_tree():
        """
        Update the tree with filtered holidays and send results to Webex.
        """
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)

        # Apply filters
        month = month_var.get() if month_var.get() != "Select All" else None
        holiday_type = type_var.get() if type_var.get() != "Select All" else None
        state = state_var.get() if state_var.get() != "Select All" else None
        filtered_holidays = filter_holidays(holidays, month, holiday_type, state)

        # Prepare message for Webex
        webex_message = f"**Filtered Holidays**\n\n"
        if filtered_holidays:
            for holiday in filtered_holidays:
                name = holiday["name"]
                date = holiday["date"]["iso"]
                holiday_type = ", ".join(holiday["type"])
                
                # Handle the "states" field more safely
                if "states" in holiday and isinstance(holiday["states"], list):
                    states = ", ".join([state["name"] for state in holiday["states"] if isinstance(state, dict) and "name" in state]) or "All States"
                else:
                    states = "All States"

                # Add to Webex message
                webex_message += f"- **{name}** on *{date}* ({holiday_type}) in *{states}*\n"

                # Insert into the Treeview
                tree.insert("", tk.END, values=(name, date, holiday_type, states))
        else:
            webex_message += "No holidays found matching the filters."

        # Send filtered holidays to Webex
        send_to_webex(webex_message)

    # Filter button
    filter_button = tk.Button(filter_frame, text="Apply Filters", command=update_tree, bg="blue", fg="white")
    filter_button.grid(row=0, column=6, padx=10)

    # Initial population of the tree
    update_tree()


def main():
    """
    Main function to create the GUI for Public Holiday Finder.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Public Holiday Finder")
    root.geometry("400x300")

    # Title Label
    tk.Label(root, text="Public Holiday Finder", font=("Arial", 16, "bold")).pack(pady=10)

    # Country selection
    tk.Label(root, text="Select a Country:").pack(pady=5)
    country_var = tk.StringVar()
    country_dropdown = ttk.Combobox(root, textvariable=country_var, values=list(COUNTRIES.keys()), state="readonly")
    country_dropdown.pack(pady=5)
    country_dropdown.set("Malaysia")  # Default selection

    # Year selection
    tk.Label(root, text="Select a Year:").pack(pady=5)
    year_var = tk.IntVar()
    current_year = 2024
    year_dropdown = ttk.Combobox(
        root,
        textvariable=year_var,
        values=list(range(current_year - 30, current_year + 11)),
        state="readonly"
    )
    year_dropdown.pack(pady=5)
    year_dropdown.set(current_year)  # Default selection

    # Submit button
    def on_submit():
        selected_country = country_var.get()
        selected_year = year_var.get()
        if not selected_country or not selected_year:
            messagebox.showerror("Input Error", "Please select both a country and a year.")
            return
        country_code = COUNTRIES[selected_country]
        display_holidays(country_code, selected_year)

    submit_button = tk.Button(root, text="Find Holidays", command=on_submit, bg="blue", fg="white")
    submit_button.pack(pady=20)

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    main()
