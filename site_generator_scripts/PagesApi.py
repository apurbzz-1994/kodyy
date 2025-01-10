from Utils import *
from Page import *

class PagesApi:
    def __init__(self, notion_key, db_id):
        self.notion_key = notion_key
        self.db_id = db_id
        self.pages = []
        self.headers = {
            "Authorization": "Bearer " + self.notion_key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.query_pages_endpoint = f"https://api.notion.com/v1/databases/{self.db_id}/query"
        self.util = Utils(self.headers)

    
    def __create_objects_from_page_data(self, api_response):
        page_objects = []
        for each_page in api_response:
            p_category = each_page['properties']['category']['select']['name'].upper()
            p_title = each_page['properties']['title']['title'][0]['text']['content']
            p_description = each_page['properties']['description']['rich_text'][0]['text']['content']
            p_archieved = each_page['properties']['archieved']['checkbox']
            p_last_updated = each_page['last_edited_time']
            p_timeline = each_page['properties']['timeline']['number']

            p_obj = Page(p_category, p_title, p_description, p_archieved, last_updated=p_last_updated, timeline=p_timeline)

            page_objects.append(p_obj)
        return page_objects
    
    
    
    
    def get_all_pages_from_database(self):
        results = None
        payload = {
            'page_size': 100
        }

        pages_data = self.util.send_post_request_to_notion(self.query_pages_endpoint, payload)

        if pages_data['object'] != 'error':
            all_pages = pages_data['results']

            while pages_data['has_more'] and pages_data['next_cursor'] != 'null':
                next_payload = {
                    'page_size': 100,
                    'start_cursor': pages_data['next_cursor']
                }
                next_pages_data = self.util.send_post_request_to_notion(self.query_pages_endpoint, next_payload)
                all_pages.extend(next_pages_data['results'])
            
            #creating page objects
            all_page_objs = self.__create_objects_from_page_data(all_pages)

            results = all_page_objs
        
        return results

