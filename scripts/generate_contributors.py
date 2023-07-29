import requests
import json
import sys

# Replace with your repository's details
username = 'OTFCG'
repo = 'Awesome-Game-Analysis'

try:
    # Call GitHub API for contributors
    response = requests.get(f'https://api.github.com/repos/{username}/{repo}/contributors')

    # If the request was successful
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        sys.exit(-1)

    contributors = json.loads(response.content)

    # Build the list of contributors as Markdown
    contributors_list = []
    for contributor in contributors:
        if contributor["login"] == 'github-actions[bot]':
            continue
        contributors_list.append(
            '<td>'
            f'<a href="https://github.com/{contributor["login"]}">'
            f'<img src="{contributor["avatar_url"]}" width="50px" />'
            f'<br />'
            f'<sub>{contributor["login"]}</sub>'
            f'</a>'
            '</td>'
        )

    # Read the existing README
    with open('README.md', 'r') as f:
        readme = f.read()

    # Add the contributors list to the README, replacing the old one
    start_marker = '<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->'
    end_marker = '<!-- ALL-CONTRIBUTORS-LIST:END -->'
    start_index = readme.find(start_marker)
    end_index = readme.find(end_marker)
    if start_index != -1 and end_index != -1:
        new_readme = (
            readme[:start_index] + 
            start_marker + 
            '\n\n<table><tr>\n' + 
            '\n'.join(' '.join(contributors_list[i:i+5]) for i in range(0, len(contributors_list), 5)) +
            '\n</tr></table>\n' + 
            readme[end_index:]
        )
        with open('README.md', 'w') as f:
            f.write(new_readme)
    else:
        print(f"Error: Couldn't find markers in the README file")
        sys.exit(-1)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(-1)

# If everything executed successfully
sys.exit(0)

