"""POC running a program that creates an Issue in our repo for each .py file.
Example Usage:
python main.py --user ${{ github.actor }} --repo ${{ github.repository }} --token ${{ secrets.GITHUB_TOKEN }}
"""
import argparse
import requests


def main():
    """POC running a program that creates Issues in another Repo"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user', required=True, help="Pass here: ${{ github.actor }} ")
    parser.add_argument('--repo', required=True, help="Pass here: ${{ github.repository}}")
    parser.add_argument('--token', required=True, help="Pass here: ${{ secrets.GITHUB_TOKEN }}")
    args = parser.parse_args()

    print(args.user, args.repo, args.token)
    args.repo = '/'.join(x for x in args.repo.split('/') if x != args.user)  # remove user from path
    # Set up the API client
    client = requests.Session()
    client.auth = (args.token, '')

    # List the contents of the repository
    print(url := f'https://api.github.com/repos/{args.user}/{args.repo}/contents')
    response = client.get(url)

    if response.status_code != 200:
        print(f'Error getting files: {response.status_code}')
        return

    # Loop through the list of files
    print(json_ := response.json())
    for item in json_:
        if item['name'].endswith('.py'):
            # Create an Issue for each .py file
            url = f'https://api.github.com/repos/{args.user}/{args.repo}/issues'
            payload = {
                'title': item['name'],
                'body': 'This is the body of the issue.'
            }
            response = client.post(url, json=payload)
            if response.status_code == 201:
                print(f'Issue created for {item["name"]}')
            else:
                print(f'Error creating issue for {item["name"]}: {response.status_code}')


if __name__ == '__main__':
    main()
