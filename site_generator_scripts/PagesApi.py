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

    def __render_heading_elements(self, notion_block):
        #grabbing the number associated with the heading
        heading_type = notion_block["type"].split("_")[1]
        heading_content = notion_block[notion_block["type"]]["rich_text"][0]['plain_text']

        html_to_render = f"<h{heading_type}>{heading_content}</h{heading_type}>"

        return html_to_render
    

    def __render_paragraph_elements(self, notion_block):
        html_to_render = ""
        p_rich_text = notion_block[notion_block['type']]['rich_text']
        #check to see if there is an empty paragraph
        if len(p_rich_text) == 0:
            html_to_render += f"<p> </p>"
        else:
            html_to_render += "<p>"
            #going through each block in rich-text, as there can be multiple strings with different styles
            #NOTE: Need to consider annotation styles and links later as well
            for each_part in p_rich_text:
                to_append = f"{each_part["plain_text"]}"
                html_to_render += to_append
            html_to_render += "</p>"
        return html_to_render

    
    
    def __get_page_content_from_database(self, page_id):
        page_content = ""
        endpoint = f"https://api.notion.com/v1/blocks/{page_id}/children"


        content_result = self.util.send_get_request_to_notion(endpoint)['results']

        #if page has content
        if len(content_result) != 0:
            for each_block in content_result:
                #handling headings 
                if "heading_" in each_block['type']:
                    header_html = self.__render_heading_elements(each_block)
                    page_content += header_html
                #handling paragraphs
                elif "paragraph" in each_block['type']:
                    paragraph_html = self.__render_paragraph_elements(each_block)
                    page_content += paragraph_html
                else:
                    page_content += ""
             
        else:
            page_content = None

        return page_content


    
    
    def __create_objects_from_page_data(self, api_response):
        page_objects = []
        for each_page in api_response:
            p_category = each_page['properties']['category']['select']['name'].upper()
            p_title = each_page['properties']['title']['title'][0]['text']['content']
            p_description = each_page['properties']['description']['rich_text'][0]['text']['content']
            p_archieved = each_page['properties']['archieved']['checkbox']
            p_last_updated = each_page['last_edited_time']
            p_timeline = each_page['properties']['timeline']['number']

            p_id = each_page['id']
            p_content = self.__get_page_content_from_database(p_id)

            p_obj = Page(p_category, p_title, p_description, p_archieved, content=p_content, last_updated=p_last_updated, timeline=p_timeline)

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

