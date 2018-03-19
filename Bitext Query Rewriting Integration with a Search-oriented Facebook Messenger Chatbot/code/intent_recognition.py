import json
import apiai
import boto3
from rewriting import *

CLIENT_ACCESS_TOKEN = "tokenprovidedbydialogflow"
_ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
queries = rewrite_message(user_message)


def process_dialogflow(query, session_id):
    request = _ai.text_request()
    request.session_id = session_id
    request.query = query

    response = json.loads(request.getresponse().read().decode('utf-8'))
    status = response['status']['code']

    if status == 200:
        reply = response['result']['fulfillment']['speech']
        intent = response['result']['metadata']['intentName']
        slots = response['result']['parameters']
    else:
        reply = ""
        intent = ""
        slots = {}

    return (reply, intent, slots)


def process_lex(query, session_id):
    client = boto3.client('lex-runtime', region_name='us-east-1')
    response = client.post_text(botName='TechCrunch', botAlias='BETA', userId=session_id, inputText=query)
    status = response['ResponseMetadata']['HTTPStatusCode']
    if status == 200:
        reply = response['message']
        intent = response['intentName']
        slots = response['slots']
    else:
        reply = ""
        intent = ""
        slots = {}

    return (reply, intent, slots)


for query in queries:
    print("Dialogflow response: " + str(process_dialogflow(query, session_id)) + "\n")

for query in queries:
    print("Lex response: " + str(process_lex(query, session_id)) + "\n")
