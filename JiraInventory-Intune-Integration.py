# The purpose of this script is to automate the retrieval of device information from our Intune MDM enviroment and create or update the data retrived in a kanban 
# format in Jira for asset tracking. This helps me extract only the information I need about the devices we manage in the Nordics exclduing "India" and visualize it in Kanban tile 
# that is easily managable and visualized

# This script has been modified and some info changed for security reasons and I purposed it solely for this case study. The original script is being run in Azure Runbook.


# Importing the modules needed to run the script
import requests
import base64
import json

# Refresh access Graph token function
def refresh_access_token():
    client_id = "c784a0ed-70dd-42e6-b315-427fe7fabab6"
    client_secret = "LzO8Q~b7HUh6VNwpjwx6vjiAwcyOHGw3fyW4RcV4"
    tenant_id = "cb6228a1-8648-4033-bced-c3b97aac6223"
    token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }
    
    response = requests.post(token_endpoint, data=body)
    response_data = response.json()
    
    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        raise Exception("Failed to refresh access token")

# Jira API Token and email used for authentication
api_token = 'ATBTT-vwsJe2Q0CwY13sAb4pgt3kyqXr9NteaqgVVH0sZXnTC1QwBYx0zGeNrlmuvDZpexCqax5PU5bfz030c7rkx3bFX63uzrr__XHsM9oUxM=04B0FD9F'
email = 'bplangji@catalystone.com'

# Encoding credentials for Base64 auth
auth_string = f'{email}:{api_token}'
base64_auth_info = base64.b64encode(auth_string.encode('ascii')).decode('ascii')

# Jira API endpoint and headers
jira_api_endpoint = "https://catalystone.atlassian.net/rest/api/3/issue/"
jira_headers = {
    "Authorization": f"Basic {base64_auth_info}",
    "Content-Type": "application/json"
}

# Access token obtained from authentication
access_token = refresh_access_token()

# Intune API endpoint URL for retrieving device information
intune_api_url = "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Send GET request to Intune API endpoint
response = requests.get(intune_api_url, headers=headers)
response_data = response.json()

# Check if the response contains data
if 'value' in response_data:
    devices = response_data['value']
    
    for device in devices:
        # Skip devices with names starting with "INDIA" 
        if device.get('deviceName', '').startswith("INDIA"):
            continue
        
        # Build the Jira issue object with the data points/fields needed
        issue_data = {
            "fields": {
                "project": {"key": "NAI"},
                "issuetype": {"name": "Asset"},
                "summary": f"{device.get('userDisplayName')} - {device.get('model')}",
                "customfield_10268": device.get('serialNumber'),
                "customfield_10267": device.get('model'),
                "customfield_10270": device.get('operatingSystem'),
                "customfield_10265": device.get('userDisplayName'),
                "customfield_10269": device.get('deviceCategory'),
                "customfield_10266": device.get('deviceName'),
                "customfield_10273": device.get('complianceState'),
                "customfield_10274": device.get('isEncrypted'),
                "customfield_10278": device.get('enrolledDateTime')
            }
        }

        # Convert issue data to JSON format
        json_data = json.dumps(issue_data)

        # Send data to Jira API to create the issue
        jira_response = requests.post(jira_api_endpoint, headers=jira_headers, data=json_data)

        if jira_response.status_code == 201:
            jira_issue = jira_response.json()
            issue_key = jira_issue.get('key')
            
            # If issue is created, update with additional information
            update_data = {
                "fields": {
                    "project": {"key": "NAI"},
                    "issuetype": {"name": "Asset"},
                    "summary": f"{device.get('userDisplayName')} - {device.get('model')}",
                    "customfield_10268": device.get('serialNumber'),
                    "customfield_10267": device.get('model'),
                    "customfield_10270": device.get('operatingSystem'),
                    "customfield_10265": device.get('userDisplayName'),
                    "customfield_10269": device.get('deviceCategory'),
                    "customfield_10266": device.get('deviceName'),
                    "customfield_10273": device.get('complianceState'),
                    "customfield_10274": device.get('isEncrypted'),
                    "customfield_10278": device.get('enrolledDateTime')
                }
            }

            # Convert update data to JSON format
            update_json_data = json.dumps(update_data)

            # Construct the URI for updating the issue
            update_uri = f"{jira_api_endpoint}{issue_key}"

            # Send the update request
            update_response = requests.put(update_uri, headers=jira_headers, data=update_json_data)

            if update_response.status_code == 204:
                print(f"Issue {issue_key} updated successfully.")
            else:
                print(f"Failed to update issue {issue_key}.")
        else:
            print("Failed to create issue.")
else:
    print("No device information found.")
