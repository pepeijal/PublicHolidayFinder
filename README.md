# Public Holiday Finder 🗓️

This is a **Flask-based web application** that allows users to **search for public holidays** in different countries using the **Calendarific API**. The app also provides filtering options and **sends holiday details to a Webex room**.

## Features  
✅ Search public holidays for different countries and years  
✅ Filter holidays by month, type, and state  
✅ View holiday details in a user-friendly table  
✅ Send filtered holiday results to a Webex Teams room  

---

## Installation & Setup  

### 1. Clone the Repository  
```bash
git clone https://github.com/yourusername/Public-Holiday-Finder.git
cd Public-Holiday-Finder
```

### 2. Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### 3. Set API Keys  
In `app.py`, replace the following values with your own:  

- **Calendarific API Key:**  
  ```python
  API_KEY = "your_calendarific_api_key"
  ```
- **Webex Access Token:**  
  ```python
  WEBEX_ACCESS_TOKEN = "your_webex_access_token"
  ```
- **Webex Room ID:**  
  ```python
  WEBEX_ROOM_ID = "your_webex_room_id"
  ```

### 4. Run the Application  
```bash
python app.py
```
Then, open **http://127.0.0.1:5000/** in your browser.

---

## Project Structure  

```
/Public-Holiday-Finder
│── /static
│   ├── styles.css          # CSS for styling
│── /templates
│   ├── index.html          # Homepage template
│   ├── results.html        # Results page (not uploaded)
│── app.py                  # Flask app with API integrations
│── requirements.txt        # Required Python packages
│── README.md               # Project documentation
```

---

## Usage  
1. **Select a country and year** from the dropdown.  
2. Click **Find Holidays** to fetch holiday data.  
3. **Filter results** based on month, type, or state.  
4. Click submit to view the filtered list and **send results to Webex**.

---

## Technologies Used  
- **Python (Flask)**
- **HTML & CSS**
- **Calendarific API** (for holiday data)
- **Webex Teams API** (for sending results)

---

## Future Improvements 🚀  
- Add a **better UI** with JavaScript interactivity  
- Allow users to **subscribe to holiday updates** via email  
- Implement **user authentication** for private Webex messages  

---

## License  
This project is open-source under the **MIT License**.  

Happy coding! 🎉 🚀

