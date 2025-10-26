# 🍼 Python Baby Names Web Scraper

this project scrapes baby name data from HTML files (like those “popular baby names by year” pages)  
and stores it inside a MySQL database.  
it extracts **rank**, **male name**, **female name**, and **year**, then saves them into two tables.

---

## 📂 Project Structure

```
Python webscrapping/
│
├── data/                 # folder with baby*.html files
├── web-scrapping.py      # main script (where the magic happens)
├── app.log               # log file generated during execution
├── .gitignore            # ignore logs, cache, etc.
└── README.md             # this file
```

---

## ⚙️ What It Does

1. **Scrape HTML**
   - reads baby name HTML files using `BeautifulSoup`
   - extracts `(rank, male_name, female_name)` from `<tr align="right">`
   - extracts year from `<h3 align="center">`

2. **Database Integration**
   - connects to MySQL database `PythonScraping`
   - auto-creates two tables:
     - `male_names(id, name, year, rank)`
     - `female_names(id, name, year, rank)`
   - inserts all scraped data per year

3. **Logging Everything**
   - saves logs in `app.log` (connection status, insertions, errors, etc.)

---

## 🧠 How to Run

### 1️⃣ Requirements
make sure you have:
- Python 3.10+
- MySQL server running locally
- installed dependencies:
  ```bash
  pip install beautifulsoup4 lxml mysql-connector-python
  ```

### 2️⃣ Database Setup
create database:
```sql
CREATE DATABASE PythonScraping;
```

### 3️⃣ Run the Script
make sure your HTML files are inside the `/data` folder, named like:
```
baby1990.html, baby1992.html, baby1994.html ...
```

then run:
```bash
python web-scrapping.py
```

you’ll see logs inside `app.log`, and data inside MySQL tables.

---

## 🧩 Example

**HTML sample (simplified):**
```html
<h3 align="center">Popularity in 2000</h3>
<tr align="right">
  <td>1</td><td>Michael</td><td>Emily</td>
</tr>
```

**Result in database:**

| id | name     | year | rank |
|----|----------|------|------|
| 1  | Michael  | 2000 | 1    |
| 1  | Emily    | 2000 | 1    |

---

## 🪛 Functions Breakdown

| Function | Description |
|-----------|-------------|
| `get_connection()` | connects to MySQL |
| `extract_babies(url)` | extracts `(rank, male, female)` list |
| `extract_popularity_year(url)` | grabs year from HTML |
| `extract_info(url)` | returns names + year as tuple |
| `creating_tables(con)` | creates `male_names`, `female_names` |
| `insert_name_to_db(con, rank, year, name, gender)` | insert single name |
| `insert_many_names_to_db(con, listofnames, year)` | insert all from file |

---

## 🧾 Logs Example

```
2025-10-25 18:54:10 - INFO - Connected to MySQL database successfully.
2025-10-25 18:54:12 - INFO - Inserted 1000 names for year 2000
```

---

## 💡 Notes

- put HTML files inside `/data/`
- logs overwrite each run (change `'w'` → `'a'` in logging config to append)
- if script crashes, check `app.log` for the reason

---

## 👨‍💻 Author
**Abdelaziz Ouedghiri** 