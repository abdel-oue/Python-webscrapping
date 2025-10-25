import os,sys,re
from os import path
from bs4 import BeautifulSoup # beautifulsoup for web scraping

def extract(url :str) ->list[tuple[str,...]]: # we want to return a list 
    try :
        with open(url,'r') as htmlfile: # closes when block is finished
            content = htmlfile.read()

            soup = BeautifulSoup(content, 'lxml') # as string
            baby_names = soup.find_all('td')

            print(baby_names)
            
            
    except FileNotFoundError:
        print(f'{url} not found')
        return []
    except PermissionError:
        print(f'{url} permission denied')
        return []
    
    #(year, 1st male name, 1st female name)
    #check if url is dir
    # iter of dir to search for expected data
    results=[]
    return results

if __name__ == '__main__':
    extract('./data/baby1990.html')