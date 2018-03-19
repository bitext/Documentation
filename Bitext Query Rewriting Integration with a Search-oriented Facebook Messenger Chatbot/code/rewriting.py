import json
import requests

API_URL = "https://svc02.api.bitext.com/rewriting/"
API_LANGUAGE = "eng"
API_MODE = "news"
API_KEY = "tokenprovidedbybitext"

user_message = "I want to read news about Tesla but not about Elon Musk"
session_id = "abcdef1234"


def rewrite_message(message_text):
    headers = {'Content-Type': 'application/json', 'Authorization': 'bearer ' + API_KEY}
    data = json.dumps({
        'language': API_LANGUAGE,
        'text': message_text,
        'simple': False,
        'mode': API_MODE
    })

    r = requests.post(API_URL, headers=headers, data=data)

    if r.status_code == 201:
        resultid = json.loads(r.text)['resultid']
        while True:
            r = requests.get(API_URL + resultid + '/', headers=headers)
            if r.status_code != 202:
                break
            print(r.status_code)
        if r.status_code == 200:
            rewriting = []
            for sentence in json.loads(r.text)['rewritinganalysis']:
                rewriting.append(sentence)
            return rewriting

    return []


rewritten_message = rewrite_message(user_message)

print("Original Text: " + "'" + user_message + "'" + "\n")
print("Rewritten Text: " + str(rewritten_message) + "\n")
