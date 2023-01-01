from pathlib import Path
import time
import requests


class GithubHandler:
    """ Handler for reading info and running actions on a Github Repo"""

    def __init__(self, repo: str, token: str):
        self.client = requests.Session()
        self.client.auth = (token, '')
        self.repo = f'https://api.github.com/repos/{repo}'
        print('Connecting to Repo:', self.repo)

    def iter_github_files(self, path: str = '') -> dict:
        """Generator for recursively getting all URLs to files in github repo """

        response = self.client.get(url := f'{self.repo}/contents/{path}')
        assert response.status_code == 200, f'Error getting files from URL: {url} ({response.status_code})'

        for item in response.json():
            type_ = item['type']
            if type_ == 'file':
                print('File:', item["path"])
                yield item
            elif type_ == 'dir':
                folder = item['path']
                if Path(folder).name.startswith('.'):
                    print('Skipping:', folder)
                    continue
                print('Directory:', folder)
                # List the contents of the directory recursively
                for x in self.iter_github_files(folder):
                    yield x
            else:
                print(f'Unknown item type: {type_} ({item["path"]})')

    def read_file_url(self, item: str | dict) -> str:
        """Given a URL or Json Item for a Github file, reads the content of the file """
        if isinstance(item, dict):
            item = item['download_url']
        print('Reading:', item)
        file_response = self.client.get(item)
        assert file_response.status_code == 200, f'Error Reading file in URL: {file_response.status_code}'
        return file_response.text

    def create_issue(self, title: str, body: str = 'Issue Body'):
        """Create a new Issue in Our Repo."""
        time.sleep(0.3) # to avoid being kicked from the system
        url = f'{self.repo}/issues'
        payload = {'title': title, 'body': body}
        response = self.client.post(url, json=payload)
        assert response.status_code == 201, f'Error creating issue "{title}": {response.status_code}\n' \
                                            f'URL: {url}\nPayload: {payload}\n' \
                                            f'{response.content}'
        print(f'Issue created: "{title}"')

    def set_issue_state(self, iss_num: int, status: str):
        """Set the status of an issue, given its number and desired new status
           Example: gh.set_issue_state(34, 'closed') 
        """
        url = f'{self.repo}/issues/{iss_num}'
        return self.client.patch(url, json={'state': status})
