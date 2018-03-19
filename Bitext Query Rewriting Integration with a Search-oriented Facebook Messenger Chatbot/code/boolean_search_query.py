from rewriting import *
from intent_recognition import *


intent_to_object_type = {"NewsIntentWithFeaturesNegative": {"polarity": "negative"},
                         "NewsIntentWithFeaturesPositive": {"polarity": "positive"}
                         }
q = ""
responses = {}

for query in queries:

    resp, intent, slots = process(query, session_id)

    if intent:
        op = ""
        if intent_to_object_type[intent]["polarity"] == "negative":
            op = "NOT "
        try:
            tag = slots['feature']
        except KeyError:
            tag = ""

        if intent == "Default Fallback Intent":
            tag = query

        if tag:
            tag = tag.replace("_", " ")
            if q != "":
                q += " " + "AND" + " "

            q += op + "\"" + tag + "\""

        if intent == "ValueIntentPositive":
            q = ""

        features = 1
    else:
        responses[0] = resp
    first_iter = False

print("Query for Swiftype: " + q + "\n")
