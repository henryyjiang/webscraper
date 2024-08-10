import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_info(link, emails, phone_numbers):
    try:
        email_pattern = r'\bmailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

        response = requests.get(link, timeout=5)
        response.raise_for_status()

        all_tags = re.findall(r'<a.*?href=[\'"](.*?)[\'"].*?>', response.text)

        for tag in all_tags:
            if re.match(email_pattern, tag) and emails is not None:
                email_match = re.search(r'(?<=mailto:)[\w\.-]+@[\w\.-]+', tag)
                if email_match:
                    emails.append(email_match.group(0))
            elif tag.startswith("tel:"):
                tag = tag[len("tel:"):]
                if not any(char.isalpha() for char in tag) and phone_numbers is not None:
                    phone_numbers.append(tag)

        return emails, phone_numbers
    except:
        return emails, phone_numbers

if __name__ == '__main__':
    csv_file = 'company_data.csv'
    count = 50

    df = pd.read_csv(csv_file, sep=',')

    for index, row in df.iterrows():
        company_name = row['Company Name']
        print(company_name)
        country = df.at[index, 'Country']
        city = df.at[index, 'City']
        address = df.at[index, 'Address']
        emails = df.at[index, 'Emails']
        websites = df.at[index, 'Domain']
        phone_numbers = df.at[index, 'Phone']

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 5)

        # Open Google search
        driver.get('https://www.google.com')

        search_input = driver.find_element(By.NAME, 'q')
        search_input.send_keys(company_name)
        search_input.submit()

        try:
            wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'a')))
        except:
            pass

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        address_element = soup.find(attrs={'data-attrid': 'kc:/location/location:address'})
        headquarters_element = soup.find(attrs={'data-attrid': 'kc:/organization/organization:headquarters'})
        phone_element = soup.find(attrs={'data-attrid': 'kc:/collection/knowledge_panels/has_phone:phone'})
        service_element = soup.find(attrs={'data-attrid': 'kc:/organization/organization:customer service phone'})

        if address_element:
            pattern = r'^(.*), (\w+ \w+), (\w+)$'
            match = re.match(pattern, address_element.find(class_='LrzXr').get_text())

            """
            NOTE: THE FOLLOWING CODE DOES NOT WORK FOR COUNTRIES WITH PROVINCES.
            CODE NEEDS TO BE ADDED TO CHECK FOR THE NUMBER OF COMMAS,
            4 HAVING A STATE/PROVINCE AND 3 HAVING NONE
            """

            if match:
                if pd.isna(country) or country == '':
                    country = match.group(3)
                if pd.isna(city) or city == '':
                    city = match.group(2)
                if pd.isna(address) or address == '':
                    address = match.group(0)

        elif headquarters_element:
            pattern = r'^(.*), (.+)$'
            match = re.match(pattern, headquarters_element.find(class_='LrzXr').get_text())

            if match:
                city_str = match.group(1).strip().split(', ')
                country_str = match.group(2).strip().split(', ')

                if pd.isna(country) or country == '':
                    country = match.group(2)
                if pd.isna(city) or city == '':
                    if len(city_str) > 0:
                        city = city_str[0]
                if pd.isna(address) or address == '':
                    address = match.group(0)

        if (pd.isna(phone_numbers) or phone_numbers == []) and phone_element:
            phone_numbers = [phone_element.find(class_='LrzXr').get_text()]

        elif phone_numbers == '' and phone_element:
            phone_numbers = phone_element.find(class_='LrzXr').get_text()

        elif (pd.isna(phone_numbers) and phone_numbers == []) and service_element:
            phone_numbers = [service_element.find(class_='LrzXr').get_text()]

        elif phone_numbers == '' and service_element:
            phone_numbers = service_element.find(class_='LrzXr').get_text()

        all_tags = driver.find_elements(By.TAG_NAME, 'a')
        links = []
        for tag in all_tags:
            href = tag.get_attribute("href")
            if href and "google" not in href.lower():
                links.append(href)

        driver.quit()

        if pd.isna(emails) or emails == []:
            emails_list = []
        else:
            emails_list = None
        if pd.isna(phone_numbers) or phone_numbers == []:
            phone_list = []
        else:
            phone_list = None

        for link in links:
            emails_list, phone_list = find_info(link, emails_list, phone_list)

        if pd.isna(emails) or emails == []:
            emails = emails_list
        if pd.isna(websites) or websites == []:
            websites = links
        if pd.isna(phone_numbers) or phone_numbers == []:
            phone_numbers = phone_list

        if isinstance(emails, list):
            emails_str = ', '.join(emails)
        else:
            emails_str = emails
        if isinstance(websites, list):
            websites_str = ', '.join(websites)
        else:
            websites_str = websites
        if isinstance(phone_numbers, list):
            phone_numbers_str = ', '.join(phone_numbers)
        else:
            phone_numbers_str = phone_numbers

        df.at[index, 'Country'] = country
        df.at[index, 'City'] = city
        df.at[index, 'Address'] = address
        df.at[index, 'Emails'] = emails_str
        df.at[index, 'Domain'] = websites_str
        df.at[index, 'Phone'] = phone_numbers_str

        df.to_csv(csv_file, index=False)