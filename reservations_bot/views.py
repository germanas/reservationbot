from registration.models import Registration
import json, requests, random, re
from pprint import pprint
import time
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
from reservations_bot.vars import *


def post_facebook_button(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % (page_access_token)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{
    "attachment":{
      "type":"template",
         "payload":{
            "template_type":"button",
            "text":"Need further assistance? Talk to a representative",
            "buttons":[
               {
                  "type":"phone_number",
                  "title":"Call Representative",
                  "payload":"+15105551234"
               },
                {
                    "type": "postback",
                    "title": "Start chatting",
                    "payload": "niga"
                }
            ]
         }
    }}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % (page_access_token)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class reservations_botview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.POST.get('hub.verify_token') == verify_token:
            return HttpResponse(self.request.POST.get('hub.challenge'))
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        tomorows_date = datetime.date.today() + datetime.timedelta(days=1)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    #laikas = message['message']['nlp']['entities']['laikas']
                    diena = message['message']['nlp']['entities']['diena']
                    tikrai_diena = diena[0]['confidence']
                    pprint(tikrai_diena)
                    #tikrai_laikas = laikas[0]['confidence']
                    #pprint(tikrai_laikas)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    if tikrai_diena >= 0.75:
                        if diena[0]['value'] == 'siandien' or diena[0]['value'] == 'siandiena':
                            post_facebook_message(message['sender']['id'], time.strftime("%Y-%m-%d"))
                            p = Registration(name='nigga', surname='penis', registration_date=time.strftime("%Y-%m-%d"), registration_time='12:00')
                            p.save()

                        elif diena[0]['value'] == 'rytoj':
                            post_facebook_message(message['sender']['id'], tomorows_date.strftime("%Y-%m-%d"))
                        else:
                            post_facebook_message(message['sender']['id'], 'neatpazistu')
                    #elif tikrai_laikas >= 0.95:
                        #post_facebook_message(message['sender']['id'], laikas[0]['value'])
                    else:
                        print ('nay')
                        post_facebook_message(message['sender']['id'], 'Tai ne diena')
        return HttpResponse()