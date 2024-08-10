# webscraper
Web scraper that takes csv as input and updates it with more detailed information. Designed for internship.

join joins csvs, remove duplicates removes duplicate entries in csvs

scraper uses Selenium and requests to scrape data while scraper_requests uses only requests.

update_contact is a separate program written for the internship which fetches contacts from an Apollo database 
to automatically create contacts in Bitrix24.

update_emails is for updating a csv file by ensuring that if the "First Name" column is empty, 
it is replaced by the value stored in the "Email" column.
