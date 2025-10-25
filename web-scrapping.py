import os,sys,re
from os import path
from bs4 import BeautifulSoup # beautifulsoup for web scraping
from mysql import connector
import logging

# ------------------------- DATABASE CONNECTION -------------------------
def get_connection():
    """Returns a connection to the MySQL database."""
    try:
        con = connector.connect(
            user='root',
            password='',
            database='PythonScraping',
            host='127.0.0.1',
            port=3306
        )
        logging.info("Connected to MySQL database successfully.")
        return con
    except connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        sys.exit(1)

# ------------------------- EXTRACT BABIES FROM HTML -------------------------
def extract_babies(url: str) -> list[tuple[str, ...]]:
    """Extracts a list of tuples (rank, male_name, female_name) from HTML file."""
    logging.debug(f"Extracting baby names from file: {url}")
    with open(url, 'r') as htmlfile:
        all_names = []
        content = htmlfile.read()
        soup = BeautifulSoup(content, 'lxml')
        baby_names = soup.find_all('tr', align='right')
        for column in baby_names:
            cleaned_row = column.find_all('td')
            if len(cleaned_row) == 3:
                cell1, cell2, cell3 = cleaned_row
                rank = cell1.text
                male_name = cell2.text
                female_name = cell3.text
                all_names.append((rank, male_name, female_name))
        logging.debug(f"Extracted {len(all_names)} names from {url}")
        return all_names

# ------------------------- EXTRACT YEAR FROM HTML -------------------------
def extract_popularity_year(url: str) -> str:
    """Extracts the year of popularity from HTML file."""
    logging.debug(f"Extracting popularity year from file: {url}")
    with open(url, 'r') as htmlfile:
        content = htmlfile.read()
        soup = BeautifulSoup(content, 'lxml')
        popularity_years_info = soup.find_all('h3', align='center')
        popularity_string = popularity_years_info[0].text
        popularity_year = popularity_string.replace("Popularity in ", "")
        logging.debug(f"Year extracted: {popularity_year}")
        return popularity_year


# ------------------------- COMBINE EXTRACTION -------------------------
def extract_info(url: str) -> tuple[list[tuple[str, ...]], str]:
    """Returns tuple (list of names, year) from HTML file."""
    try:
        all_names = extract_babies(url)
        popularity_year = extract_popularity_year(url)
        return all_names, popularity_year
    except FileNotFoundError:
        logging.error(f"{url} not found")
        return [], ''
    except PermissionError:
        logging.error(f"{url} permission denied")
        return [], ''


# ------------------------- CREATE TABLES -------------------------
def creating_tables(con):
    """Creates male_names and female_names tables if they don't exist."""
    queries = [
        'CREATE TABLE IF NOT EXISTS male_names (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, year YEAR NOT NULL, rank INT NOT NULL);',
        'CREATE TABLE IF NOT EXISTS female_names (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, year YEAR NOT NULL, rank INT NOT NULL);'
    ]
    try:
        cursor = con.cursor()
        for query in queries:
            cursor.execute(query)
            logging.info(f"Executed query: {query}")
        con.commit()
    except connector.Error as e:
        logging.error(f"Error creating tables: {e}")
        return False

# ------------------------- INSERT ONE NAME -------------------------
def insert_name_to_db(con, rank: int, year: str, name: str, gender: str):
    """Insert a single name into the database."""
    try:
        if gender == 'female':
            query = 'INSERT INTO female_names(name, year, rank) VALUES(%s, %s, %s);'
        else:
            query = 'INSERT INTO male_names(name, year, rank) VALUES(%s, %s, %s);'
        cursor = con.cursor()
        cursor.execute(query, (name, year, rank))
        con.commit()
        logging.debug(f"Inserted {gender} name: {name}, rank: {rank}, year: {year}")
    except connector.Error as e:
        logging.error(f"Error inserting name {name}: {e}")
        return False


"""
This function inserts many name to the database PythonScraping
"""

# ------------------------- INSERT MANY NAMES -------------------------
def insert_many_names_to_db(con, listofnames: list, year: str):
    """Insert multiple names into the database."""
    try:
        query_male = 'INSERT INTO male_names(name, year, rank) VALUES(%s, %s, %s);'
        query_female = 'INSERT INTO female_names(name, year, rank) VALUES(%s, %s, %s);'
        cursor = con.cursor()
        for name in listofnames:
            rank = int(name[0])
            male_name = name[1]
            female_name = name[2]
            cursor.execute(query_male, (male_name, year, rank))
            cursor.execute(query_female, (female_name, year, rank))
            logging.debug(f"Inserted rank {rank}: male={male_name}, female={female_name}")
        con.commit()
        logging.info(f"Inserted {len(listofnames)} names for year {year}")
    except connector.Error as e:
        logging.error(f"Error inserting multiple names: {e}")
        return False
    
if __name__ == '__main__':
    con = get_connection()
    creating_tables(con)
    listoffiles = ["baby1990.html", "baby1992.html", "baby1994.html", "baby1996.html",
                   "baby1998.html", "baby2000.html", "baby2002.html", "baby2004.html",
                   "baby2006.html", "baby2008.html"]

    for file in listoffiles:
        path_file = "./data/" + file
        logging.info(f"Processing file: {path_file}")
        listofnames, year = extract_info(path_file)
        insert_many_names_to_db(con, listofnames, year)
    