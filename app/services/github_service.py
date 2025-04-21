import requests
from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

TOKEN_URL = "https://github.com/login/oauth/access_token"
EMAIL_URL = "https://api.github.com/user/emails"
USER_URL = "https://api.github.com/user"

def get_github_access_token(code: str) -> str:
    headers = {"Accept": "application/json"}
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data, timeout=5, verify=False)
    if response.status_code != 200:
        raise Exception("Failed to retrieve GitHub access token")
    return response.json().get("access_token")

def get_github_primary_email(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(EMAIL_URL, headers=headers, timeout=5, verify=False)
    if response.status_code != 200:
        raise Exception("Failed to retrieve GitHub emails")
    emails = response.json()
    print("emails", emails)
    for email_entry in emails:
        if email_entry.get("primary") and email_entry.get("verified"):
            return email_entry.get("email")
    raise Exception("No verified primary email found in GitHub account")

def get_github_username(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    print("headers", headers)
    print("USER_URL", USER_URL)
    response = requests.get(USER_URL, headers=headers, timeout=60 , verify=False)
    if response.status_code != 200:
        raise Exception("Failed to retrieve GitHub user details")
    return response.json().get("login")
