from selenium import webdriver
from bs4 import BeautifulSoup, Tag
import csv

num_pages = 887
page = 0
filename = 'data.csv'
headers = ["Nama", "No telepon"]

with open(filename, 'w') as f:
  write = csv.writer(f)
  write.writerow(headers)

base_url = 'https://idn.bizdirlib.com'

while page <= 887:
  if page == 0:
    catalogue_url = base_url + '/da/taxonomy/term/9'
  else:
    catalogue_url = base_url + '/da/taxonomy/term/9?page=' + str(page)
  
  driver = webdriver.Chrome('chromedriver.exe')
  driver.get(catalogue_url)
  content = driver.page_source
  soup = BeautifulSoup(content, 'html.parser')
  company_list = soup.ol

  if company_list is not None:
    for c in company_list.children:
      if type(c) == Tag and c is not None:
        for child in c.children:
          company_data = []
          if type(child) == Tag and child is not None:
            company_url = child.a['href']
            driver.get(base_url + company_url)
            company_content = driver.page_source
            company_soup = BeautifulSoup(company_content, 'html.parser')
            
            try:
              company_name_soup = company_soup.find('strong', string='Firmaets navn').next_sibling.next_sibling
              if company_name_soup is not None:
                company_name = company_name_soup.text
            except AttributeError:
              try:
                company_name_soup = company_soup.find_all(attrs={"itemprop": "name"})
                company_name = company_name_soup[2].text
              except IndexError:
                company_name = 'Undefined'
            
            try:
              company_telephone_soup = company_soup.find(attrs={"itemprop": "telephone"})
              if company_telephone_soup is not None:
                company_telephone = company_telephone_soup.text
            except AttributeError:
                company_telephone = 'Undefined'
            
            company_data.append(company_name)
            company_data.append(company_telephone)

            with open(filename, 'a+', newline='') as f:
              write = csv.writer(f)
              write.writerow(company_data)
            print(company_data)

  page = page + 1
