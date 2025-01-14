import requests
class Utils:

    def __init__(self, headers):
        self.headers = headers

    
    def send_get_request_to_notion(self, endpoint_url):
        requested_response = None
        try:
            response = requests.get(endpoint_url, headers=self.headers)
            requested_response = response.json()
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
        finally:
            return requested_response
        
    
    def send_post_request_to_notion(self, endpoint_url, json_payload, success_message = None):
        requested_response = None
        try:
            response = requests.post(endpoint_url, json=json_payload, headers=self.headers)
            requested_response = response.json()
            if success_message!= None:
                print(success_message)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
        finally:
            return requested_response
        
    
    def get_all_rows_from_database(self, query_db_enpoint, obj_create_func, filter = None):
        results = None
        payload = {
            'page_size': 100
        }

        #adding filters, if available 
        if filter != None:
            if filter:
                payload["filter"] = filter


        pages_data = self.send_post_request_to_notion(query_db_enpoint, payload)

        if pages_data['object'] != 'error':
            all_pages = pages_data['results']

            while pages_data['has_more'] and pages_data['next_cursor'] != 'null':
                next_payload = {
                    'page_size': 100,
                    'start_cursor': pages_data['next_cursor']
                }
                next_pages_data = self.send_post_request_to_notion(query_db_enpoint, next_payload)
                all_pages.extend(next_pages_data['results'])
            
            #creating page objects
            all_page_objs = obj_create_func(all_pages)

            results = all_page_objs
        
        return results

        

