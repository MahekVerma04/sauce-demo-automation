import os
import requests

# ⚠️ Configure these values!
CLIENT_ID = os.getenv("XRAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("XRAY_CLIENT_SECRET")
 # From Jira > Apps > Xray > API Keys
PROJECT_KEY = "DEM" 

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
import_url = f"https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey={PROJECT_KEY}"

# ✅ FIX: Make the path absolute so the GitHub Runner always finds it
base_dir = os.path.dirname(os.path.abspath(__file__))
report_path = os.path.join(base_dir, "results", "junit-report.xml")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "text/xml"
}

# Add a quick check to see if the file actually exists before reading it
if not os.path.exists(report_path):
    print(f"❌ Error: Cannot find the report file at: {report_path}")
    print("Make sure your pytest step generated the XML file successfully.")
    exit(1)

with open(report_path, "r", encoding="utf-8") as f:
    xml_data = f.read()
    response = requests.post(import_url, headers=headers, data=xml_data)

if response.status_code == 200:
    print("🚀 Success! Results imported.")
    print(f"Jira Response: {response.text}")
else:
    print(f"❌ Upload failed with status code: {response.status_code}")
    print(response.text)
