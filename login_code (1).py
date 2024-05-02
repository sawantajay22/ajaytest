import requests
import websocket
import json

market_url = "https://developers.symphonyfintech.in/apimarketdata/auth/login"

headers = {
    "Content-Type": "application/json"
} 

def market_login(secret_key, app_key, market_url):
    market_token = None
    userid = None
    socket = None

    try:
        # Market login
        payload = {
            "secretKey": secret_key,
            "appKey": app_key,
            "source": "WebAPI"
        }
        response = requests.post(market_url, json=payload)
        data = response.json()
        if data['type'] == 'success':
            token = data['result']['token']
            userid = data['result']['userID']
            socket = websocket.create_connection("wss://developers.symphonyfintech.in/apimarketdata/socket.io/?EIO=3&transport=websocket")
            auth_data = {"userID": userid, "token": market_token}
            socket.send(json.dumps(auth_data))
            print("WebSocket connected")
        return socket,token,userid
    except Exception as e:
        print("Error:", e)
        return None, None, None

    return socket, market_token, userid
    
def getdata(socket,token,userid,app_key,secret_key):
    if socket:
        headers = {
            "Authentication": f"Bearer {token}",
            "Content-Type": "application/json"
        } 
        payload = {
            "secretKey": secret_key,
            "appKey": app_key,
            "source": "WebAPI"
        }
        url = "https://developers.symphonyfintech.in/marketdata/instruments/quotes"
        response = requests.post(url,headers=headers,json=payload)
        data = response.json()
        print(data)
#def Connect(token,userid):
    

app_key="9ae69e2cf30f2a02571972"
secret_key="Bbbg837$@Z"
socket,token,userid = market_login(secret_key,app_key,market_url)
#Connect(token, userid)
getdata(socket,token,userid,app_key,secret_key)


