from rewriting import *
from intent_recognition import *
from boolean_search_query import *
import json
import requests


status = 0
response = ""
records = {}
news = {}
if q != "" or status:
  tx = requests.get('https://api.swiftype.com/api/v1/public/engines/search.json',
                    headers={"Content-Type": "application/json"},

                    data=json.dumps({"engine_key": "tokenprovidedbyswiftype",
                                     "q": q,
                                     "per_page": 2,
                                     "page": 1,
                                     "sort_field": {"page": "timestamp"},
                                     "fetch_fields": {"page": ["title", "url",
                                                               "image", "timestamp", "author"]},
                                     "search_fields": {"page": ["title"]}}))
  records = json.loads(tx.text)
  news = records["records"]["page"]
  status = 0
  if 1 in responses:
    response = responses[1]
  else:
    response = "Ok!"

else:

  if 0 in responses:
    response = responses[0]
  else:
    response = "Ok!"
  status = 1

elements = []

for new in news:
  url = new['url']
  image = new['image']
  s_image = image.split('?')
  title = new['title']
  stamp = new['timestamp'].split("T")[0]

  item = {"title": title, "image_url": s_image[0] + "?w=780&h=600", "subtitle": stamp,
          "default_action": {"type": "web_url", "url": url}, "buttons": [{"type": "web_url",
                                                                          "url": url, "title": "View on Web"}, {"type": "element_share"}]}

  elements.append(item)

# Chatfuel-specific JSON
out = {"set_attributes": {"session": session_id}, "messages": [{"text": response},
                                                               {"attachment": {"type": "template", "payload": {"template_type": "generic",
                                                                                                               "image_aspect_ratio": "horizontal", "elements": elements}}}]}

# FlowXO-specific JSON
# out = {"attachment": {"type": "template", "payload": {"template_type": "generic",\
# "image_aspect_ratio": "horizontal", "elements": elements}}}

d = json.dumps({"q": q, "responses": responses, "status": status, "page": 1})

print("JSON for the Facebook Messenger Chatbot: " + json.dumps(out, indent=4, sort_keys=True))
