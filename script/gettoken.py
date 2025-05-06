import json
import os
import time

import jwt
from dotenv import load_dotenv
from jwt.algorithms import RSAAlgorithm

load_dotenv(".env", verbose=True)

with open("private_key.json", "r") as f:
    privateKey = json.load(f)

kid = os.getenv("KID")
channel_id = os.getenv("CHANNEL_ID")
headers = {"alg": "RS256", "typ": "JWT", "kid": kid}
payload = {
    "iss": channel_id,
    "sub": channel_id,
    "aud": "https://api.line.me/",
    "exp": int(time.time()) + (60 * 30),  # 30分の有効期限
    "token_exp": 60 * 60 * 24 * 30,  # 30分の有効期限
}

key = RSAAlgorithm.from_jwk(privateKey)
JWT = jwt.encode(payload, key, algorithm="RS256", headers=headers, json_encoder=None)
print(JWT)
