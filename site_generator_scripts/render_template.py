from jinja2 import Environment, FileSystemLoader
from PagesApi import *
from dotenv import load_dotenv
import os
import argparse

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_SECRET")
DB_ID = os.getenv("MAIN_DB_ID")


def generate_templates():

    print("Grabbing content from Notion database and creating templates......")

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

            # check to see if there are images associated with the page in the folder
            # if yes, then move them all into the folder
            for each in os.listdir("../output"):
                if each.endswith('.png') and dir_name in each:
                    if "_cover" not in each:
                        os.replace(f'../output/{each}', f'{output_directory}/{each}')


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

    print("Templates created! Please check your output folder")


def clear_output_folder(d_path):
    for each_item in os.listdir(d_path):
        current_dir = f"{d_path}/{each_item}"
        if os.path.isdir(current_dir):
            clear_output_folder(current_dir)
        elif each_item != "style.css" and each_item != "favicon.ico":
            #remove data
            print(f"Removed: {current_dir}")
            os.remove(current_dir)
    #deal with remaining folders
    for each_dir in os.listdir(d_path):
        current = f"{d_path}/{each_dir}"
        if os.path.isdir(current):
            os.rmdir(current)


        

def main():
    parser = argparse.ArgumentParser(description="This CLI allow you to generate a static website with data coming from Notion database")
    subparsers = parser.add_subparsers(help="Available subcommands", dest="command", required=True)

    #render subcommand
    render_parser = subparsers.add_parser("render", help="Render website from templates")
    
    #clear subcommand
    clear_parser = subparsers.add_parser("clear_output_folder", help="Clears the output folder in case templates have to be regenerated")
   
    args = parser.parse_args()
    
    if args.command == "render":
        generate_templates()
    elif args.command == "clear_output_folder":
        clear_output_folder("../output")

if __name__ == '__main__':
    main()

