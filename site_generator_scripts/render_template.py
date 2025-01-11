from jinja2 import Environment, FileSystemLoader
from PagesApi import *
from dotenv import load_dotenv
import os

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_SECRET")
DB_ID = os.getenv("MAIN_DB_ID")

#set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('../templates'))  

#load the template file
template = env.get_template('index.html')

#template for read more pages
template_read_more = env.get_template('readmore_page_template.html')

p_api = PagesApi(NOTION_TOKEN, DB_ID)
all_pages = p_api.get_all_pages_from_database()

#create necessary html files for 'read more' pages
for each_page in all_pages:
    #if page has content
    if each_page.content != None:
        #render template with data
        readme_page_data = {
            'content': each_page.content
        }
        readme_file_output = template_read_more.render(readme_page_data)

        #create new folder 
        dir_name = each_page.title.lower().replace(" ", "_")
        output_directory = f"../output/{dir_name}"
        os.mkdir(output_directory)

        #add page to folder
        with open(f'{output_directory}/{dir_name}.html', 'w') as f:
            f.write(readme_file_output)

        each_page.readmore_page_link = f"{dir_name}/{dir_name}.html"

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