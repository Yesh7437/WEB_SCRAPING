import requests
from bs4 import BeautifulSoup
import time
import csv

# Initialize variables
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
num_pages = 20
csv_filename = 'product_data.csv'

# Create and open the CSV file in write mode
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through multiple pages
    for page in range(1, num_pages + 1):
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find product containers
        product_containers = soup.find_all("div", class_="s-result-item")
        
        # Extract information from each product container
        for container in product_containers:
            # Extract product URL with error handling
            product_url_element = container.find("a", class_="a-link-normal")
            if product_url_element:
                product_url = "https://www.amazon.in" + product_url_element.get("href")
            else:
                product_url = "N/A"
            
            # Extract product name with error handling
            product_name_element = container.find("span", class_="a-text-normal")
            if product_name_element:
                product_name = product_name_element.text
            else:
                product_name = "N/A"
            
            # Extract product price with error handling
            product_price_element = container.find("span", class_="a-offscreen")
            if product_price_element:
                product_price = product_price_element.text
            else:
                product_price = "N/A"
            
            # Extract product rating with error handling
            product_rating_element = container.find("span", class_="a-icon-alt")
            if product_rating_element:
                product_rating = product_rating_element.text
            else:
                product_rating = "N/A"
            
            # Extract number of reviews with error handling
            num_reviews_element = container.find("span", class_="a-size-base")
            if num_reviews_element:
                num_reviews = num_reviews_element.text
            else:
                num_reviews = "N/A"
            
            # Fetch additional information from the product URL
            if product_url != "N/A":
                product_page = requests.get(product_url)
                product_soup = BeautifulSoup(product_page.content, "html.parser")
                
                # Extract product description, ASIN, product description, and manufacturer
                product_description_element = product_soup.find("span", id="productTitle")
                asin_element = product_soup.find("span", {"data-asin": True})
                manufacturer_element = product_soup.find("a", {"href": "/b/ref=bl_dp_s_web_0?node=16618424031&field-brandtextbin=", "class": "a-link-normal"})
                product_description = product_description_element.text.strip() if product_description_element else "N/A"
                asin = asin_element['data-asin'] if asin_element else "N/A"
                manufacturer = manufacturer_element.text.strip() if manufacturer_element else "N/A"
                
                # Append the data to the CSV file
                writer.writerow({'Product URL': product_url, 'Product Name': product_name, 'Product Price': product_price,
                                 'Rating': product_rating, 'Number of Reviews': num_reviews,
                                 'Description': "N/A", 'ASIN': asin, 'Product Description': product_description,
                                 'Manufacturer': manufacturer})
            
            # Wait for a moment before making the next request (to be respectful of the server)
            time.sleep(2)
