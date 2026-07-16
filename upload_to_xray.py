import os
import requests

# ⚠️ Configure these values!
CLIENT_ID = os.getenv("XRAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("XRAY_CLIENT_SECRET")
 # From Jira > Apps > Xray > API Keys
PROJECT_KEY = "SD" 

print("1. Authenticating with Xray Cloud...")
auth_url = "https://xray.cloud.getxray.app/api/v2/authenticate"
auth_resp = requests.post(
    auth_url, 
    json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
)

if auth_resp.status_code != 200:
    print(f"Authentication failed: {auth_resp.text}")
    exit(1)

token = auth_resp.text.replace('"', '') # Strip quotes off the token
print("Authentication successful!")

print("\n2. Uploading JUnit results file to Xray...")
# Endpoint for importing standard JUnit XML
#import_url = f"https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey={PROJECT_KEY}"
import_url = "https://xray.cloud.getxray.app/api/v2/import/execution/junit?testExecKey=SD-13" 
# Update headers to indicate we are sending raw XML
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "text/xml"  # <-- Crucial change!
}
with open("results/junit-report.xml", "r", encoding="utf-8") as f:
    xml_data = f.read()
    response = requests.post(import_url, headers=headers, data=xml_data) # <-- Sending raw XML

if response.status_code == 200:
    print("Success! Results imported.")
    print(f"Jira Response: {response.text}")
else:
    print(f"Upload failed: {response.status_code}")
    print(response.text)
