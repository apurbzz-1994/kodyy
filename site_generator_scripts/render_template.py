from jinja2 import Environment, FileSystemLoader
from PagesApi import *
from dotenv import load_dotenv
import os

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_SECRET")
DB_ID = os.getenv("MAIN_DB_ID")

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('../templates'))  # '.' means the current directory

# Load the template file
template = env.get_template('index.html')


p_api = PagesApi(NOTION_TOKEN, DB_ID)
all_pages = p_api.get_all_pages_from_database()

# Define the data to inject
data = {
    'homepage_cards': all_pages

}

# Render the template with the data
output = template.render(data)

# Save or print the rendered HTML
with open('../output/index.html', 'w') as f:
    f.write(output)

print("Done!")