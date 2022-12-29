import requests


class GithubHandler:
    """ Handler for reading info and running actions on a Github Repo"""

    def __init__(self, repo: str, token: str):
        self.client = requests.Session()
        self.client.auth = (token, '')
        self.repo = f'https://api.github.com/repos/{repo}'
        print('Connecting to Repo:', self.repo)

    def iter_github_files(self, path: str = 'contents') -> dict:
        """Given a URL of an endpoint in a Github Repo and a path recursively generates the file items """
        if path.startswith('.'):
            return
        response = self.client.get(url := f'{self.repo}/{path}')
        assert response.status_code == 200, f'Error getting files from URL: {url} ({response.status_code})'

        for item in response.json():
            type_ = item['type']
            if type_ == 'file':
                print('File:', item["path"])
                yield item
            elif type_ == 'dir':
                print('Directory:', item["path"])
                # List the contents of the directory recursively
                for x in self.iter_github_files(item['path']):
                    yield x
            else:
                print(f'Unknown item type: {type_} ({item["path"]})')

    def read_file_url(self, item: str | dict) -> str:
        """Given a URL or Json Item for a Github file, reads the content """
        if isinstance(item, dict):
            item = item['download_url']
        print('Reading:', item)
        file_response = self.client.get(item)
        assert file_response.status_code == 200, f'Error Reading file in URL: {file_response.status_code}'
        return file_response.text

    def create_issue(self, title: str, body: str = 'Issue Body'):
        url = f'{self.repo}/issues'
        payload = {'title': title, 'body': body}
        response = self.client.post(url, json=payload)
        assert response.status_code == 201, f'Error creating issue "{title}": {response.status_code}'
        print(f'Issue created: "{title}"')
