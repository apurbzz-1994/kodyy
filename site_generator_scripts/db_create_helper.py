from Utils import Utils
from dotenv import load_dotenv
import argparse
import os

load_dotenv()
notion_key = os.getenv("NOTION_SECRET")

def db_create(page_id, db_name, props):
    endpoint = "https://api.notion.com/v1/databases/"
    
    payload = {

    #denotes the parent page the database is housed in   
    "parent": {
        "type": "page_id",
        "page_id": page_id
    },

    #database title
     "title": [
        {
            "type": "text",
            "text": {
                "content": db_name,
            }
        }
    ],

    #database columns
    "properties": props,

    }

    headers = {
            "Authorization": "Bearer " + notion_key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    #send request here

    util = Utils(headers)

    result = util.send_post_request_to_notion(endpoint, payload)

    if result['object'] and result['object'] == 'error':
        print("Error creating database")
    else:
        print(f"Your {db_name} database has been created! \n URL: {result['url']}\n Database ID is the last 32 character code in the URL. Save this to your .env file")





def db_create_pages(args):
    props = {
        "title": {
            "title": {}
        },
        "category": {
           "select": {
                "options": []
            }
        },
        "description": {
            "rich_text": {}
        }, 
        "archieved": {
            "checkbox": {}
        }, 
        "timeline": {
            "number": {
                'format': "number"
            }
        },
         "cover_image": {
            "files": {}
        }
     }
    
    db_create(page_id=args.page_id, db_name="Site Pages", props=props)



def db_create_links(args):
    props = {
        "title": {
            "title": {}
        },
        "link": {
            "url": {}
        }, 
        "description": {
            "rich_text": {}
        },
        "tags": {
           "multi_select": {
                "options": []
            }
        }
     }
    
    db_create(page_id=args.page_id, db_name="Site Links", props=props)
    


def main():
    parser = argparse.ArgumentParser(description="This CLI allow you to create databases for your Static Site Generator")
    subparsers = parser.add_subparsers(help="Available subcommands")


    #create pages db
    create_parser = subparsers.add_parser("pages", help="Create a Site Pages database")
    create_parser.add_argument("page_id", help="The ID of the parent page, which is the 32 character code at the end of the page URL")
    create_parser.set_defaults(func=db_create_pages)

    #create links db
    create_parser = subparsers.add_parser("links", help="Create a Site Links database")
    create_parser.add_argument("page_id", help="The ID of the parent page, which is the 32 character code at the end of the page URL")
    create_parser.set_defaults(func=db_create_links)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()



if __name__ == '__main__':
    main()
