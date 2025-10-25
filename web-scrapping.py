import os,sys,re
from os import path
from bs4 import BeautifulSoup # beautifulsoup for web scraping
from mysql import connector

def extract_babies(url :str) ->list[tuple[str,...]]: # we want to return a list of tuple (rank , male name, female name)
    with open(url,'r') as htmlfile:
        all_names = []
        content = htmlfile.read()
        soup = BeautifulSoup(content, 'lxml') # as string
        baby_names = soup.find_all('tr', align='right')
        for column in baby_names:
            cleaned_row = column.find_all('td')
            if len(cleaned_row) == 3:
                cell1, cell2, cell3 = cleaned_row
                rank = cell1.text
                male_name = cell2.text
                female_name = cell3.text
                all_names.append((rank,male_name,female_name))
        return all_names

def extract_popularity_year(url :str) -> str:
    with open(url,'r') as htmlfile:
        content = htmlfile.read()
        soup = BeautifulSoup(content, 'lxml') # as string
        popularity_years_info = soup.find_all('h3', align='center')
        popularity_string = popularity_years_info[0].text
        popularity_year = popularity_string.replace("Popularity in ","")
        return popularity_year


def extract_info(url: str) -> tuple[list[tuple[str, ...]], str]:
    try:
        all_names = extract_babies(url)
        popularity_year = extract_popularity_year(url)
        return all_names, popularity_year
    except FileNotFoundError:
        print(f'{url} not found')
        return [], ''
    except PermissionError:
        print(f'{url} permission denied')
        return [], ''

def get_connection():
    return connector.connect(
        user='root',
        password='',
        database='PythonScraping',
        host='127.0.0.1',
        port=3306
    )

def creating_tables():
    querys=['CREATE TABLE male_names (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(50) NOT NULL,year YEAR NOT NULL,rank INT NOT NULL);'
            ,'CREATE TABLE female_names (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(50) NOT NULL,year YEAR NOT NULL,rank INT NOT NULL);']
    try:
        con = get_connection()
        cursor = con.cursor()
        for query in querys:
            cursor.execute(query)
        con.commit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    #extract_popularity_year('./data/baby1990.html')
    creating_tables()