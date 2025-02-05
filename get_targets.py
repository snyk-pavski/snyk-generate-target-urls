import json
import requests
import argparse
import time
from datetime import datetime


# Define API version, URL base and Delay
API_VERSION = "2024-08-22"

API_BASE_URL = "https://api.snyk.io"
WEB_BASE_URL = "https://app.snyk.io"
RATE_LIMIT_DELAY = 0.2

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--group", required=True, help="Group ID")
parser.add_argument("--token", required=True, help="API token")
args = parser.parse_args()

def get_organizations(group_id, api_key):
    url = f"{API_BASE_URL}/rest/groups/{group_id}/orgs?version={API_VERSION}&limit=100"
    headers = {"accept": "application/vnd.api+json", "authorization": f"{api_key}"}
    organizations = []

    while url:
        start_time = time.time()
        response = requests.get(url, headers=headers)
        end_time = time.time()

        response.raise_for_status()  # Raise error for non-2xx status codes

        data = response.json()
        organizations.extend(data["data"])

        reponse_code = response.status_code
        
        # Print request details
        print(f"Response Code: {reponse_code} - Request URL: {url}")


        # Do not upset the API Overlords 
        time.sleep(RATE_LIMIT_DELAY)

        # Check for next page link
        links = data.get("links", {})
        url = links.get("next")

        # Add "https://api.snyk.io" if missing from next URL
        if url and not url.startswith("https://"):
            url = f"{API_BASE_URL}{url}"
        


    return organizations


def get_targets(org_id, api_key):
    url = f"{API_BASE_URL}/rest/orgs/{org_id}/targets?version={API_VERSION}&limit=100"
    headers = {"accept": "application/vnd.api+json", "authorization": f"{api_key}"}
    targets = []

    while url:
        start_time = time.time()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        end_time = time.time()

        data = response.json()
        targets.extend(data["data"])

        reponse_code = response.status_code

        # Print request details
        print(f"Response Code: {reponse_code} - Request URL: {url}")

        # Do not upset the API Overlords 
        time.sleep(RATE_LIMIT_DELAY)

        # Check for next page link
        links = data.get("links", {})
        url = links.get("next")

        # Add "https://api.snyk.io" if missing from next URL
        if url and not url.startswith("https://"):
            url = f"{API_BASE_URL}{url}"


    return targets


def extract_target_data(targets, org_name):
    target_data = []
    for target in targets:
        target_info = {
            "org_name": org_name,
            "org_id": target["relationships"]["organization"]["data"]["id"],
            "org_slug": org["attributes"]["slug"],
            "target_name": target["attributes"]["display_name"],
        }
        target_data.append(target_info)
    return target_data


if __name__ == "__main__":
    group_id = args.group
    api_key = args.token

    organizations = get_organizations(group_id, api_key)
    target_data = []

    for org in organizations:
        org_name = org["attributes"]["name"]
        targets = get_targets(org["id"], api_key)
        org_target_data = extract_target_data(targets, org_name)
        target_data.extend(org_target_data)


    for entry in target_data:
        output_file = f"./{org_name}.json"
        org_name = entry['org_name']
        org_slug = entry['org_slug']
        target_name = entry['target_name']
        target_search_url = f"{WEB_BASE_URL}/org/{org_slug}/projects?groupBy=targets&before&after&searchQuery={target_name}"
        entry.update({"target_search_url": target_search_url})
        
        with open(output_file, 'a+') as f: 
          json.dump(entry, f, indent=2) 
          f.write('\n') 

