from jinja2 import Environment, FileSystemLoader
from PagesApi import *
from LinksApi import *
from dotenv import load_dotenv
import os
import argparse

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_SECRET")
DB_ID = os.getenv("MAIN_DB_ID")
LINK_DB_ID = os.getenv("LINK_DB_ID")


def render_readmore_page(each_page, template_read_more):
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


def procure_render_to_template(primary_page_template, rm_page_template, data_dict, arch_filter = None, cat_filter = None, sort = None):
    output = None
    #grabbing pages from the database
    p_api = PagesApi(NOTION_TOKEN, DB_ID)
    all_pages = p_api.get_all_pages_from_database(archieved_filter=arch_filter, category_filter=cat_filter, sort_by_year=sort)

    if len(all_pages) != 0:
        #create necessary html files for 'read more' page and render archived content
        for each_page in all_pages:
            #if page has content
            if each_page.content != None:
                render_readmore_page(each_page, rm_page_template)
        
        # Define the data to inject
        data_dict['homepage_cards'] = all_pages
        
        # Render the template with the data
        output = primary_page_template.render(data_dict)

    return output



def generate_templates():

    print("Grabbing content from Notion database and creating templates......")

    #set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader('../templates'))  

    #load the template file
    template = env.get_template('index.html')

    #template for read more pages
    template_read_more = env.get_template('readmore_page_template.html')

    #template for archieved page
    template_archieved = env.get_template('archieved_template.html')

    #grabbing links from the database
    l_api = LinksApi(NOTION_TOKEN, LINK_DB_ID)
    all_links = l_api.get_all_links_from_database()


    data_archieved_page = {
        'homepage_cards': None
    }

    #render archieved page
    output_archieved_page = procure_render_to_template(template_archieved, template_read_more, data_archieved_page, arch_filter=True, sort=True) 

     # Define the data to inject
    data_index_page = {
        'homepage_cards': None,
        'homepage_links': all_links,
        'archive_link': True

    }
    #if no archived pages are available (filtered output returns no result)
    if output_archieved_page == None:
        data_index_page['archive_link'] = False
    else:
        #create archived page
        with open('../output/archieved.html', 'w') as f:
            f.write(output_archieved_page)

    #render the template with the data
    output_index_page = procure_render_to_template(template, template_read_more, data_index_page, arch_filter=False, sort=True, cat_filter="!homepage-block")

    # Save or print the rendered HTML
    with open('../output/index.html', 'w') as f:
        f.write(output_index_page)


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

