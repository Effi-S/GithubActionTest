"""POC running a program that creates an Issue in our repo for each .py file.
Example Usage:
python main.py  --repo ${{ github.repository }} --token ${{ secrets.GITHUB_TOKEN }}
"""
import git_utils


def main():
    """POC running a program that creates Issues in another Repo"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, help="Pass here: ${{ github.repository}}")
    parser.add_argument('--token', required=True, help="Pass here: ${{ secrets.GITHUB_TOKEN }}")
    args = parser.parse_args()

    # Set up the API client
    github_handler = git_utils.GithubHandler(args.repo, args.token)

    # Loop through the files of the repository
    for file_item in github_handler.iter_github_files():
        if file_item['name'].endswith('.py'):
            # Read the python file
            text = github_handler.read_file_url(file_item)
            # Create the Issue body
            dummy_body = ''.join(text.splitlines()[-1:])  # Just the last line of the file, for POC
            # Create an Issue
            github_handler.create_issue(title=file_item['name'], body=dummy_body)


if __name__ == '__main__':
    main()
