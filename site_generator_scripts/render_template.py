from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('../templates'))  # '.' means the current directory

# Load the template file
template = env.get_template('index.html')

#class for data
class Page:
    def __init__(self, category, title, description):
        self.category = category
        self.title = title
        self.description = description

class Links:
    def __init__(self, title, link, description, tags):
        self.title = title
        self.link = link
        self.description = description
        self.tags = tags

# Define the data to inject
data = {
    'homepage_cards': [Page('EXPERIENCE', 'Space Martian', "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    Page('PROJECT', 'Flux Capacitor', "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum")],

    'link_cards': [Links('Awesome Project 1', '#', "Eget etiam mauris quis aptent mauris. Viverra at primis fusce magna ullamcorper elit. Nunc metus tristique per habitant bibendum magna tortor curabitur. Platea netus taciti nec enim et magnis vitae pharetra. Scelerisque montes maecenas ullamcorper habitasse in auctor orci condimentum. Nisi aliquet aliquam justo neque ullamcorper nisi. Sociosqu nisi blandit venenatis accumsan ad mi. Amet feugiat egestas consequat lectus aptent nisl. Sit molestie nisl urna facilisi consequat est blandit interdum euismod. Senectus ultrices hendrerit magnis aliquam feugiat quam tempus consectetur tristique.", ['python', 'CLI', 'automation', 'notion']), 
                   Links('Awesome Project 2', '#', "Mollis cras nisl conubia metus dictum aliquet. Posuere habitant litora nam tristique orci dictum vitae fermentum. Nostra quis tellus taciti porta non pharetra gravida scelerisque fringilla. Iaculis malesuada sollicitudin magnis nisl; primis suspendisse ultrices. Volutpat suscipit phasellus laoreet per venenatis urna quam accumsan. Risus elementum posuere cursus velit cras.", ['python', 'visualisation'])
                ]

}

# Render the template with the data
output = template.render(data)

# Save or print the rendered HTML
with open('../output/index.html', 'w') as f:
    f.write(output)

print("Done!")