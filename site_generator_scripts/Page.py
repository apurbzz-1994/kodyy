class Page:
    def __init__(self, category, title, description, archieved, content = None, last_updated = None, timeline = None):
        self.category = category
        self.title = title
        self.description = description
        self.archieved = archieved
        self.content = content
        self.last_updated = last_updated
        self.timeline = timeline
