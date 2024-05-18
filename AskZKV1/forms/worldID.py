import requests
import os

WORLD_ID_API_URL = "https://developer.worldcoin.org/api/v2/verify/"
YOUR_SECRET_KEY = os.getenv("SECRET_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")
WORLD_ID_CREATE_URL = "https://developer.worldcoin.org/api/v2/create-action/"

def verify_world_id(payload, action: str) -> bool:
    payload['action'] = action   
    
    headers = {
        "Authorization": f"Bearer {YOUR_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(WORLD_ID_API_URL + APPLICATION_ID, json=payload, headers=headers)
    
    if response.status_code == 200:
        verification_result = response.json()
        return verification_result.get('success', False)
    else:
        print(f"Verification failed: {response.status_code} - {response.text}")
        return False
    
def create_world_id_action(form_id):
    payload = {
        "action": str(form_id) + '-submit',
        "name": "Submit_form_" + str(form_id),
        "description": "Vote for" + str(form_id) + " form.",
        "max_verifications": 1
    }
    
    headers = {
        "Authorization": f"Bearer {YOUR_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    info = requests.post(WORLD_ID_CREATE_URL + APPLICATION_ID, json=payload, headers=headers)
    print(info.text)

