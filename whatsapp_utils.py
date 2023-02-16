from flask import make_response
from pprint import pprint
import requests
import os

PRINT_REQUESTS = False
import Enum

class NotificationType(Enum):
  MESSAGE_SERVER_RECIVED = 0,
  MESSAGE_SENT = 1,
  MESSAGE_DELIVERED = 2,
  MESSAGE_RECIEVED = 3,
  UNSUPPORTED = 4

def verify_webhook(request, verification_token):
  pprint(request.args)
  args = request.args
  response = make_response("", 403) 
  try:
    mode = args.get('hub.mode')
    token = args.get('hub.verify_token')
    challenge = args.get('hub.challenge')
    if mode == "subscribe" and token == verification_token:
      print("WEBHOOK_VERIFIED");
      response = make_response(challenge, 200)
  except Exception as e:
    print(e)
  return response

class whatsapp_webhook_notification:
  def __init__(self, phone_number_id, from_number, text, json, notification_type):
    self.phone_number_id = phone_number_id
    self.from_number = from_number
    self.text = text
    self.json = json
    self.notification_type = notification_type

def parse_notification_type(json):
  notification = json["entry"][0]["changes"][0]["value"]
  if "messages" not in notification:
    return NotificationType.UNSUPPORTED
  if 'statuses' not in notification:
    return NotificationType.MESSAGE_SERVER_RECIVED


def parse_webhook_notification(request):
  json = request.get_json()
  if PRINT_REQUESTS:
    pprint(json)
  notification_type = parse_notification_type(json)
  raw_message = json["entry"][0]["changes"][0]["value"]
  phone_number_id = raw_message["metadata"]["phone_number_id"]
  from_number = raw_message["messages"][0]["from"]
  text = None
  if "text" in raw_message["messages"][0]:
    text = raw_message["messages"][0]["text"]["body"]  
  webhook_notification = whatsapp_webhook_notification(phone_number_id, from_number, text, json, notification_type)
  return webhook_notification
  
def get_authorization_header():
  return { "Authorization": "Bearer {}".format(os.environ.get('WHATSAPP_TOKEN')) }
  
def send_message(phone_number_id, phone_number, token, text):
  url = "https://graph.facebook.com/v16.0/{}/messages?access_token={}".format(phone_number_id, token)
  print(url)
  data = {
          "messaging_product": "whatsapp",
          "to": phone_number,
          "text": { "body": text },
        }
  headers_dict = get_authorization_header().update({ "Content-Type": "application/json" })
  response = requests.post(url, headers=headers_dict, json=data)
  pprint(response.text)