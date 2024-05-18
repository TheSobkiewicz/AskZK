import requests
import os

WORLD_ID_API_URL = "https://developer.worldcoin.org/api/v2/verify/"
YOUR_SECRET_KEY = os.getenv("SECRET_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")

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

