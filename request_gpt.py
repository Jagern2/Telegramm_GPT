import requests
import json

def get_answer(promt):
    url = "https://chatgptfree.ai/wp-admin/admin-ajax.php"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }
    data = {
        "_wpnonce": "394cdc5c04",
        "post_id": 6,
        "url": "https://chatgptfree.ai",
        "action": "wpaicg_chat_shortcode_message",
        "message": promt,
        "bot_id": 0,
        "chatbot_identity": "shortcode",
        "wpaicg_chat_client_id": "00Cj7dT0SU",
        "wpaicg_chat_history": [{"text":""}],
        "chat_id": 67363
    }
  
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
  
    if response.status_code == 200:
        full_message = []
        for line in response.iter_lines():
            if line.startswith(b'data:'):
                json_line = line[5:]
                if json_line == b'[DONE]':
                    break
                try:
                    message = json.loads(json_line)
                    if 'choices' in message and message['choices'][0]['delta'].get('content'):
                        full_message.append(message['choices'][0]['delta']['content'])
                except json.JSONDecodeError:
                    continue
        return ''.join(full_message)
    else:
        return "Error " + str(response.status_code)