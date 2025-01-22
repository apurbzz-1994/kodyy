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
            html_to_render += f"<br/>"
        else:
            html_to_render += "<p>"
            #going through each block in rich-text, as there can be multiple strings with different styles
            for each_part in p_rich_text:
                to_append = f"{each_part["plain_text"]}"
                styles = each_part['annotations']

                #checking to see if a href is associated with a text block
                if each_part['href'] != None:
                    to_append = f"<a href='{each_part['href']}' class='a-page'>{to_append}</a>"
                else:
                    if styles['bold']:
                        to_append = f"<b>{to_append}</b>"
                    if styles['italic']:
                        to_append = f"<i>{to_append}</i>"
                    if styles['strikethrough']:
                        to_append = f"<s>{to_append}</s>"
                    if styles['underline']:
                        to_append = f"<u>{to_append}</u>"

                html_to_render += to_append
            html_to_render += "</p>"
        return html_to_render

    
    def __download_image_from_notion(self, image_url, save_file_path):
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(save_file_path, "wb") as file:
                file.write(image_response.content)
        else:
            print("Image file save error")

    
    
    def __render_image_elements(self, notion_block, p_title):
        image_url = notion_block[notion_block['type']]['file']['url']
        filename_prefix = p_title.lower().replace(" ", "_")
        filename = f"{filename_prefix}_{notion_block['id']}"
        filepath = f"../output/{filename}.png"
        html_to_render = ""

        #use the requests library to download the image
        self.__download_image_from_notion(image_url, filepath)

        html_to_render += f"<img src = '{filename}.png' class='img-fluid custom-img'>"
        return html_to_render

    
    
    def __get_page_content_from_database(self, page_id, p_title):
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
                elif "image" in each_block['type']:
                    image_html = self.__render_image_elements(each_block, p_title)
                    page_content+= image_html
                else:
                    page_content += ""
             
        else:
            page_content = None

        return page_content

    
    def __create_objects_from_page_data(self, api_response):
        page_objects = []
        for each_page in api_response:
            p_category = each_page['properties']['category']['select']['name'].upper()
            p_title = each_page['properties']['title']['title'][0]['plain_text']
            p_description = each_page['properties']['description']['rich_text'][0]['plain_text']
            p_archieved = each_page['properties']['archieved']['checkbox']
            p_last_updated = each_page['last_edited_time']
            p_timeline = each_page['properties']['timeline']['number']

            p_id = each_page['id']
            p_content = self.__get_page_content_from_database(p_id, p_title)

            #accounting for cover images
            cover_image_file_data = each_page['properties']['cover_image']['files']
            cover_image = None

            if len(cover_image_file_data) != 0:
                # this means a cover image is available
                cover_image_link = cover_image_file_data[0]['file']['url']
                #setting path with imagefilename
                image_local_path = f"../output/{p_title.lower().replace(" ", "_")}_cover.png"
                #download image
                self.__download_image_from_notion(cover_image_link, image_local_path)
                cover_image = f"{p_title.lower().replace(" ", "_")}_cover.png"

            p_obj = Page(p_category, p_title, p_description, p_archieved, content=p_content, last_updated=p_last_updated, timeline=p_timeline, cover_image=cover_image)

            page_objects.append(p_obj)
        return page_objects
    
    
    
    def get_all_pages_from_database(self, archieved_filter = None, category_filter = None, sort_by_year = None):
        filter = {}
        sort = []

        #better refactored code            
        if archieved_filter is not None or category_filter is not None:
            if archieved_filter is not None:
                archieved_condition =  {
                'property': "archieved",
                'checkbox': {"equals": archieved_filter}
                }
            if category_filter is not None:
                #accounting for multiple categories
                categories = category_filter.split(',')

                if len(categories) == 1:
                    single_category = categories[0]
                    # if not operator is present 
                    if single_category[0] == "!":
                        categories_condition = {
                            "property": "category",
                            'select':  {"does_not_equal": single_category}
                        }
                    else:
                        categories_condition = {
                            "property": "category",
                            'select':  {"equals": single_category}
                        }
                else:
                    categories_condition = {
                        "or": []
                    }

                    for each_category in categories:
                        if each_category[0] == "!":
                            categories_condition["or"].append(
                                {   
                                    "property": "category",
                                    'select':  {"does_not_equal": each_category}
                                }
                            )
                        else:
                            categories_condition["or"].append(
                                {   
                                    "property": "category",
                                    'select':  {"equals": each_category}
                                }
                            )

            if archieved_filter is not None and category_filter is not None:
                filter['and'] = [archieved_condition, categories_condition]
            else:
                filter = archieved_condition if archieved_filter is not None else categories_condition
            
       


        #adding sorting by year
        if sort_by_year == True:
            sort.append({
                'property': 'timeline',
                'direction': 'descending'
            })

        all_pages = self.util.get_all_rows_from_database(self.query_pages_endpoint, self.__create_objects_from_page_data, filter, sort)

        return all_pages

      
           

       

