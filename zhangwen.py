import requests
import json
from web3 import Web3
from eth_account.messages import encode_defunct
import datetime
import uuid

def sign_message(private_key, message):
    # 创建Web3实例
    w3 = Web3()
    # 从私钥创建账户
    account = w3.eth.account.from_key(private_key)
    # 对消息进行签名
    message_encoded = encode_defunct(text=message)
    signed_message = w3.eth.account.sign_message(message_encoded, private_key=private_key)
    return signed_message.signature.hex()

def check_in(token):
    url = "https://testnet-api.sightai.io/marketing/v1/check-in"
    
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
        "Authorization": f"Bearer {token}",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "https://sightai.io",
        "Pragma": "no-cache",
        "Referer": "https://sightai.io/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    try:
        response = requests.post(url, headers=headers)
        print("\n签到状态码:", response.status_code)
        print("签到响应:", response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"签到错误: {e}")
        return None

def sign_in_with_wallet(private_key):
    url = "https://testnet-api.sightai.io/marketing/v1/auth/sign-in"
    
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://sightai.io",
        "Pragma": "no-cache",
        "Referer": "https://sightai.io/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    
    # 创建账户实例以获取地址
    account = Web3().eth.account.from_key(private_key)
    
    # 生成新的 nonce 和时间戳
    nonce = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    
    # 构造消息
    message = f"https://sightai.io wants you to sign in with your Ethereum account: {account.address}\n\n" \
             f"Make sure that you trust this site and are aware of the security implications of signing this message.\n\n" \
             f"URI: https://sightai.io\n" \
             f"Version: 1\n" \
             f"Chain ID: 17000\n" \
             f"Nonce: {nonce}\n" \
             f"Issued At: {timestamp}\n"
    
    # 获取签名
    signature = sign_message(private_key, message)
    
    payload = {
        "message": message,
        "signature": signature,
        "referralCode": "D3LND5"
    }

    try:
        print("发送请求到:", url)
        print("请求头:", json.dumps(headers, indent=2))
        print("请求体:", json.dumps(payload, indent=2))
        
        response = requests.post(url, headers=headers, json=payload)
        
        print("\n响应状态码:", response.status_code)
        print("响应头:", dict(response.headers))
        print("响应内容:", response.text)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

if __name__ == "__main__":
    # 使用你的私钥
    private_key = ""
    
    # 先登录获取token
    login_result = sign_in_with_wallet(private_key)
    if login_result and 'accessToken' in login_result:
        print("登录成功，获取到token")
        # 使用token进行签到
        check_in_result = check_in(login_result['accessToken'])
        if check_in_result:
            print("签到成功:", check_in_result)
    else:
        print("登录失败，无法进行签到")
