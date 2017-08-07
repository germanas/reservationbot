
import json, requests, random, re
from pprint import pprint

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAE7XGty0qABAPPy687CGMnwSDQsnppPvIvM7y5cklekVjYFgVAdh7CD62uRMDATpbQtGMKzTOWq6GalviMSaIgsTy3vanfFUHZCnxZBZAZAUHGr3as0W4Lg7lCoWxQB5dvAasMyqYkNiGrbe5nqxZCZAxWYoCwkq3PBCsZC5aaHAZDZD'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Create your views here.
class reservations_botview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.POST.get('hub.verify_token') == '19891010':
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
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                #pprint (message['message']['nlp']['entities'])
                if message['message'] == 'labas':
                    post_facebook_message(message['sender']['id'],  'ypi')
                else:
                    post_facebook_message(message['sender']['id'], 'you are bad')
        return HttpResponse()