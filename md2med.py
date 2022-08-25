import requests
import json
import os
import sys
import argparse
from pprint import pprint as pp


def md2medium(file_to_publish, tag) -> None:
    headers = {
        'Authorization': f"Bearer {os.environ['md2med_TOKEN']}",
        'accept': 'application/json',
        'Content-type': 'application/json',
        'Accept-Charset': 'utf-8'
    }
    cert = os.environ["cacert"]
    url = f"https://api.medium.com/v1/users/{os.environ['md2med_USERID']}/posts"

    with open(file_to_publish, mode="rt", encoding="utf-8") as docFile:
        doc_body = docFile.read()

    doc_name = input("Enter doc name:")
    data = {
        "title": doc_name,
        "contentFormat": "markdown",
        "content": f"# {doc_name}\n" + doc_body,
        "tags": [f"{tag}"],
        "publishStatus": "public",
    }

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(data).encode("utf-8"), verify=cert)
        response.raise_for_status()
        print(response)
        pp(json.loads(response.content.decode()))

    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        print(response.content)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_publish")
    parser.add_argument("--tag")
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    md2medium(file_to_publish=args.file_to_publish, tag=args.tag)


if __name__ == "__main__":
    main()
