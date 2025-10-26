# 👶 Baby Name Popularity Scraper

A Python script to scrape popular baby names data from local HTML files using **BeautifulSoup** and load the structured data into a **MySQL** database.

---

## ✨ Key Features

* **HTML Parsing:** Extracts baby name rankings (Rank, Male Name, Female Name) and the year of popularity from HTML files located in the `./data` directory.
* **Database Integration:** Connects to a local MySQL database (`PythonScraping`).
* **Schema Management:** Automatically creates `male_names` and `female_names` tables upon first run.
* **Batch Processing:** Efficiently processes a list of files and performs bulk data insertion for optimal performance.
* **Robust Logging:** Detailed logging of connection status, extraction, and database transactions to **`app.log`**.

---

## ⚙️ Setup & Prerequisites

1.  **Dependencies:** Install the required Python libraries:
    ```bash
    pip install mysql-connector-python beautifulsoup4 lxml
    ```

2.  **MySQL Database:**
    * Ensure your MySQL server is running.
    * A database named **`PythonScraping`** must exist.
    * **Note:** The script attempts to connect as `user='root'` with `password=''` on `host='127.0.0.1:3306'`. Adjust the `get_connection()` function if your credentials differ.

3.  **Data Files:**
    * Place all source HTML files (e.g., `baby1990.html`, `baby2008.html`) into the **`data/`** subdirectory.

---

## 🚀 Getting Started

1.  Place the `web-scrapping.py` script and the `data/` folder in your project directory.
2.  Execute the script from your terminal:

    ```bash
    python web-scrapping.py
    ```

The script will read each HTML file, extract the names and the year, and commit the data to the corresponding `male_names` and `female_names` tables in your database.

---

## 💾 Database Structure

The `male_names` and `female_names` tables share the same schema:

| Column | Data Type | Description |
| :--- | :--- | :--- |
| **`id`** | INT (PK, AI) | Unique record identifier. |
| **`name`** | VARCHAR(50) | The popular baby name. |
| **`year`** | YEAR | The year the ranking applies to. |
| **`rank`** | INT | The popularity rank (1, 2, 3, etc.). |

---

## 🗺️ Project Files

| File/Directory | Description |
| :--- | :--- |
| `web-scrapping.py` | Main script containing all logic for connection, extraction, and insertion. |
| `data/` | Directory holding the source HTML files. |
| `app.log` | Detailed log file generated during execution. |
| `README.md` | This documentation file. |