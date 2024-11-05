# The purpose of this script is to perform a simple task of extracting the list of drinks and their prices from the Oda website
# I used a google chrome extention called "Check My links" to scan and export all the links to the products in the Drinks Catalogue
# NB: I have never scrapped a site before today, so I searched for help on sites like Stackoverflow for help on how to approach it.


import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd  

# List to store the product data
oda_drinkscatalogue = []

# This function extracts the product data from the product URL
def extract_product_data(url):
    # Send a GET request to the product page
    response = requests.get(url)
    response.raise_for_status() 

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all script tags containing in the product data
    script_tags = soup.find_all('script', type='application/ld+json')

  #loop through the script_tags
    for script in script_tags:
        try:
            # Load the JSON content
            data = json.loads(script.string)

            # Checking if the JSON contains product information
            if data.get('@type') == 'Product':
                product_name = data.get('name')
                product_description = data.get('description', 'N/A')
                product_price = data.get('offers', {}).get('price', 'N/A')
                product_currency = data.get('offers', {}).get('priceCurrency', 'N/A')

                # Append the extracted data to the oda_drinkscatalogue list
                oda_drinkscatalogue.append({
                    "Product Name": product_name,
                    "Description": product_description,
                    "Price": f"{product_price} {product_currency}"
                })

                # Print the extracted data in terminal to verify if it is working correctly 
                print(f"Product Name: {product_name}")
                print(f"Description: {product_description}")
                print(f"Price: {product_price} {product_currency}")
                print("-" * 20)

        except json.JSONDecodeError:
            continue

    print(f"Product data not found for URL: {url}")
    return False 

# List of all the drinks URLs in the drink catalogue extracted using "Check my link" chrome extension 
urls = [
    "https://oda.com/no/products/64138-hard-seltzer-rod-jul-6-x-05l/",
    "https://oda.com/no/products/32752-schous-pilsner-10-x-033l/",
    "https://oda.com/no/products/36371-somersby-mango-lime-lite-6-x-050-l/",
    "https://oda.com/no/products/64275-grans-cola-x-uten-sukker-4-x-15l/",
    "https://oda.com/no/products/32092-hansa-borg-hansa-hard-seltzer-mango/",
    "https://oda.com/no/products/502-farris-naturell/",
    "https://oda.com/no/products/61792-ringnes-munkholm-radler-mango-passion-6x033l/",
    "https://oda.com/no/products/65858-grans-hard-seltzer-jordbaer-rabarbra/",
    "https://oda.com/no/products/1600-ringnes-pilsner-6-x-05l/",
    "https://oda.com/no/products/62016-grans-hard-seltzer-tropiske-frukter/",
    "https://oda.com/no/products/22024-grevens-cider-skogsbaer-uten-sukker-6-x-05l/",
    "https://oda.com/no/products/64257-alt-alt-sparkling-blanc-de-blancs-alkoholfri-vin/",
    "https://oda.com/no/products/32090-hansa-borg-hansa-hard-seltzer-grapefrukt/",
    "https://oda.com/no/products/12553-frydenlund-fatol-6-x-05l/",
    "https://oda.com/no/products/62594-solo-super-10-x-033l/",
    "https://oda.com/no/products/58154-villa-lett-boks-10-x-033l/",
    "https://oda.com/no/products/29119-carlsberg-alcohol-free-flaske-6-x-033l/",
    "https://oda.com/no/products/27870-grevens-cider-fruktsmak-uten-sukker-6-x-05l/",
    "https://oda.com/no/products/64772-coca-cola-coca-cola-zero-sugar-4-x-033l/",
    "https://oda.com/no/products/506-farris-bris-naturell/",
    "https://oda.com/no/products/30308-corona-extra-6-x-033l/",
    "https://oda.com/no/products/7996-farris-bris-sitron-sitrongress/",
    "https://oda.com/no/products/7999-farris-lime/",
    "https://oda.com/no/products/30420-peroni-nastro-azzurro-peroni-nastro-azzurro-6-x-03/",
    "https://oda.com/no/products/33776-ambijus-ambijus-clearly-confused-alkoholfri-cider/",
    "https://oda.com/no/products/29447-somersby-paere-6-x-05l/",
    "https://oda.com/no/products/64267-strauch-strauch-blanc-pur-riesling-alkoholfri/",
    "https://oda.com/no/products/27395-munkholm-fatol-6-x-033l/",
    "https://oda.com/no/products/20014-smirnoff-ice-4-x-025l/",
    "https://oda.com/no/products/40892-munkholm-radler-sitron-6-x-033l/",
    "https://oda.com/no/products/64773-fanta-fanta-orange-zero-sugar-4-x-033l/",
    "https://oda.com/no/products/22021-grevens-cider-paere-uten-tilsatt-sukker-6-x-05l/",
    "https://oda.com/no/products/64826-snasavann/",
    "https://oda.com/no/products/31788-isbiter/",
    "https://oda.com/no/products/58043-pepsi-max-10-x-033l/",
    "https://oda.com/no/products/6715-red-bull-energidrikk-sukkerfri-24x250ml/",
    "https://oda.com/no/products/29448-somersby-apple-lite-6-x-05l/",
    "https://oda.com/no/products/28821-battery-brett-24-x-033l/",
    "https://oda.com/no/products/62768-monster-monster-energy-6x05l/",
    "https://oda.com/no/products/28421-monster-monster-ultra-white/",
    "https://oda.com/no/products/12109-tine-original-appelsinjuice/",
    "https://oda.com/no/products/62767-monster-monster-mango-loco-6-x-05l/",
    "https://oda.com/no/products/29091-battery-fresh/",
    "https://oda.com/no/products/24281-froosh-smoothie-mango-appelsin-6-x-150ml/",
    "https://oda.com/no/products/25893-freia-oboy-mindre-sukker/",
    "https://oda.com/no/products/443-fun-light-bringebaer/",
    "https://oda.com/no/products/7249-freia-regia-sjokoladedrikk-10-stk/",
    "https://oda.com/no/products/463-oboy-oboy-original/",
    "https://oda.com/no/products/7522-lipton-lipton-forest-fruit-tea-pyramide-34g/",
    "https://oda.com/no/products/6706-lerum-husholdningssaft/",
    "https://oda.com/no/products/31335-tine-presset-eple-bringebaerjuice/",
    "https://oda.com/no/products/22849-snapple-kiwi-strawberry/",
    "https://oda.com/no/products/61793-lipton-iste-sitron/",
    "https://oda.com/no/products/28835-fever-tree-fever-tree-premium-tonic-mixer/",
    "https://oda.com/no/products/28334-tine-original-tropisk-juice/",
    "https://oda.com/no/products/24269-froosh-smoothie-mango-appelsin-12-x-250-ml/",
    "https://oda.com/no/products/940-freia-regia-kakao-original/",
    "https://oda.com/no/products/24282-froosh-smoothie-jordbaer-banan-guava-6-x-150ml/",
    "https://oda.com/no/products/28834-fever-tree-fever-tree-ginger-beer-mixer/",
    "https://oda.com/no/products/36826-fun-light-julebrus/",
    "https://oda.com/no/products/12100-tine-original-eplejuice/",
    "https://oda.com/no/products/469-frokostkaffe-filtermalt/",
    "https://oda.com/no/products/15711-capri-sonne-appelsin-10-stk/",
    "https://oda.com/no/products/27779-tine-premium-mango-og-eplejuice/",
    "https://oda.com/no/products/8948-freia-regia-sjokoladedrikk-boks/",
    "https://oda.com/no/products/5917-twinings-gronn-te-sitron-50-poser/",
    "https://oda.com/no/products/24272-froosh-smoothie-blabaer-bringebaer/",
    "https://oda.com/no/products/25170-nescafe-cafe-vanilla-8-stk/",
    "https://oda.com/no/products/8086-tine-iskaffe-caffe-gosto-brasileiro/",
    "https://oda.com/no/products/29308-twinings-earl-grey-100-poser/",
    "https://oda.com/no/products/26231-ice-coffee-8-stk/",
    "https://oda.com/no/products/15130-kjeldsberg-instantkaffe/",
    "https://oda.com/no/products/11005-twinings-spicy-indian-chai-20-poser/",
    "https://oda.com/no/products/25966-soda-water/",
    "https://oda.com/no/products/7735-twinings-earl-grey-50-poser/",
    "https://oda.com/no/products/22852-snapple-mango/",
    "https://oda.com/no/products/25361-tonic-zero/",
    "https://oda.com/no/products/32755-tine-iskaffe-caffe-mocha-uten-tilsatt-sukker/",
    "https://oda.com/no/products/24270-froosh-smoothie-ananas-banan-kokos/",
    "https://oda.com/no/products/24271-froosh-smoothie-jordbaer-banan-guava/",
    "https://oda.com/no/products/10091-schweppes-schweppes-tonic/",
    "https://oda.com/no/products/849-tine-orginal-eplejuice/",
    "https://oda.com/no/products/3385-friele-frokostkaffe-morkbrent-filtermalt/",
    "https://oda.com/no/products/7375-oboy-original-refill/",
    "https://oda.com/no/products/12124-tine-iskaffe-latte-uten-tilsatt-sukker/",
    "https://oda.com/no/products/29119-carlsberg-alcohol-free-flaske-6-x-033l/",
    "https://oda.com/no/products/470-friele-frokostkaffe-hele-bonner/",
    "https://oda.com/no/products/61794-lipton-iste-fersken/",
    "https://oda.com/no/products/26097-tine-iskaffe-cappuccino-uten-tilsatt-sukker/",
    "https://oda.com/no/products/53088-schweppes-pink-tonic/",
    "https://oda.com/no/products/20626-twinings-eple-kanel-rosin-te/",
]

# Looping through each product URL and extracting the product data
for url in urls:
    print(f"Processing Product URL: {url}")
    extract_product_data(url)
    time.sleep(1)

# Convert the oda_drinkscatalogue list into a DataFrame
df = pd.DataFrame(oda_drinkscatalogue)

# Print the DataFrame to the terminal to verify
print(df)

# Save the DataFrame to a CSV file
df.to_csv("oda_drinkscatalogue.csv", index=False)
