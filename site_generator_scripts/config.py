'''
Setting this to true will render the 'last updated' date for read more pages. 
If this is a new page, the 'last updated' time is the same as 'created' time
This option can be useful for rendering blog-like templates
'''
show_last_updated_date = False


'''
Category names assigned to this variable (separated by commas) will act as content blocks for the homepage. This means the 
content within the pages will be directly rendered.
Note: You'll have to introduce variables of the same name as the corresponding categories in your homepage template
Second Note: Each of these will have to be unique, meaning only one entry can have each category
'''
homepage_blocks_to_load = "homepage_block"


'''
Category names assigned to this variable will be filtered out and displayed in the main-page
'''
category_filters = "Experience,Project"

'''
Sort homepage tiles based on year (latest first)
'''
sort_by_year = True