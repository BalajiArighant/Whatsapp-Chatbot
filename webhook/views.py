import json
import os
import requests
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RequestSerializer
from .models import User
import logging

# Create your views here.
logger = logging.getLogger(__name__)
class Webhook(APIView):
    DOMAIN = "graph.facebook.com"
    VERSION = "v21.0"
    FROM_PHONE = "480826048452289"
    # FROM_PHONE = "122103045758696568"
    # FROM_PHONE = "529751833548015"
    ENDPOINT = "messages"
    URL = f"https://{DOMAIN}/{VERSION}/{FROM_PHONE}/{ENDPOINT}"

    def get(self, request, *args, **kwargs):
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")

        if mode == "subscribe" and token == os.getenv("VERIFY_TOKEN"):
            logger.info(f"Webhook verified by {request.META.get('REMOTE_ADDR')} with query params {request.query_params}")
            return Response(int(challenge))
        else:
            logger.error(f"Invalid token from {request.META.get('REMOTE_ADDR')} with query params {request.query_params}")
            raise PermissionDenied("Invalid token")

    def post(self, request, *args, **kwargs):
        kovil = [
            {
                "id": "Kovil-1",
                "title": "Illayathangudi Kovil",
                "description": "Illayathangudi"
            },
            {
                "id": "Kovil-2",
                "title": "Mathur Kovil",
                "description": "Mathur"
            },{
                "id": "Kovil-3",
                "title": "Vairavan Kovil",
                "description": "Vairavan"
            },{
                "id": "Kovil-4",
                "title": "Iraniyur Kovil",
                "description": "Iraniyur"
            },{
                "id": "Kovil-5",
                "title": "Nemam Kovil",
                "description": "Nemam"
            },{
                "id": "Kovil-6",
                "title": "Illupakudi Kovil",
                "description": "Illupakudi"
            },{
                "id": "Kovil-7",
                "title": "Sooraikudi Kovil",
                "description": "Sooraikudi"
            },{
                "id": "Kovil-8",
                "title": "Velankudi Kovil",
                "description": "Velankudi"
            }
        ]
        booth_collection = [
            {
                "id": "Booth-1",
                "title": "R.V. Thaneermalai",
                "description": "Sri Valli Medical, Mahalingapuram, Nungambakkam. 9444062246"
            },
            {
                "id": "Booth-2",
                "title": "U. Muthulakshmi",
                "description": "US Chettinad Idly, Valasaravakkam. 9841696151"
            },
            {
                "id": "Booth-3",
                "title": "S. Naggapan",
                "description": "Nagappa Pharmacy, Adyar, Chennai-20. 9884140162"
            },
            {
                "id": "Booth-4",
                "title": "SSS Muthukumar",
                "description": "Madipakkam, Chennai. 9962597888"
            },
            {
                "id": "Booth-5",
                "title": "K. Seetharaman",
                "description": "Vishagan Foods Pvt Ltd, Iyyapanthangal. 9176455955"
            },
            {
                "id": "Booth-6",
                "title": "S.A. Valliappan",
                "description": "RameshClicks, Kovur. 9677182010"
            },
            {
                "id": "Booth-7",
                "title": "S. Naggapan",
                "description": "Nagappa Pharmacy, Pallikaranai, Chennai-129. 9884140162"
            },
            {
                "id": "Booth-8",
                "title": "Jayanthi Manickam",
                "description": "Indhira Bavan, 12/6 Mastan ali garden, S V Lingam Road, Vadapalani. 9952901952"
            },
            {
                "id": "Booth-9",
                "title": "Dot Alagappan",
                "description": "Dot School of Design, Ambattur. 9444090221"
            }
        ]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv("ACCESS_TOKEN")}"
        }
        data = request.data
        serialized_data = RequestSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        # print(serialized_data.data)

        phone_number = serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
        user, created = User.objects.get_or_create(phone_number=phone_number)

        if created:
            file = open("webhook/reply_to_message.json", "r")
            template = json.loads(file.read())
            
            template["context"]["message_id"] = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
            template["to"] = serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            template["text"]["body"] = "Hello, Please enter your name to get started"

            file.close()

            response = requests.post(self.URL, headers=headers, json=template, verify=False)
            print(self.URL)
            print(f"Bearer {os.getenv("ACCESS_TOKEN")}")
            print(response.status_code)
            print(response.text)
            return Response(template)

        
        if not user.user_name:
            file = open("webhook/reply_to_message_list.json", "r")
            template = json.loads(file.read())

            user.user_name = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            user.save()
            template["to"] = serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            template["interactive"]["body"]["text"] = "Please choose your kovil place"
            template["interactive"]["action"]["button"] = "Choose kovil"
            template["interactive"]["action"]["sections"][0]["title"] = "Kovil"
            template["interactive"]["action"]["sections"][0]["rows"] = kovil

            file.close()

            response = requests.post(self.URL, headers=headers, json=template)
            print(response.status_code)
            print(response.text)
            return Response(template)

        elif not user.kovil:
            file = open("webhook/reply_to_message.json", "r")
            template = json.loads(file.read())

            user.kovil = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            user.save()
            template["context"]["message_id"] = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
            template["to"] = serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            template["text"]["body"] = "Please enter your native place"
            
            file.close()

            response = requests.post(self.URL, headers=headers, json=template)
            print(response.status_code)
            print(response.text)
            return Response(template)
        
        elif not user.native_place:
            file = open("webhook/reply_to_message.json", "r")
            template = json.loads(file.read())

            user.native_place = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            user.save()
            template["context"]["message_id"] = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
            template["to"] = serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            template["text"]["body"] = "Please enter your current living area"

            file.close()

            response = requests.post(self.URL, headers=headers, json=template)
            print(response.status_code)
            print(response.text)
            return Response(template)
        
        elif not user.current_location:
            file = open("webhook/reply_to_message_list.json", "r")
            template = json.loads(file.read())
            
            user.current_location = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            user.save()
            template["to"] = serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            template["interactive"]["body"]["text"] = "Please choose your collection location"
            template["interactive"]["action"]["button"] = "Choose location"
            template["interactive"]["action"]["sections"][0]["title"] = "Collection Location"
            template["interactive"]["action"]["sections"][0]["rows"] = booth_collection

            file.close()

            response = requests.post(self.URL, headers=headers, json=template)
            print(response.status_code)
            print(response.text)
            return Response(template)
        
        elif not user.booth_collection:
            file = open("webhook/reply_to_message.json", "r")
            template = json.loads(file.read())

            user.booth_collection = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

            last_token = User.objects.order_by("-token_number").first()
            next_token = 1 if User.objects.count() == 1 else (last_token.token_number + 1)
            user.token_number = next_token
            user.save()

            template["context"]["message_id"] = serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
            template["to"] = serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            template["text"]["body"] = "Thank you for registering with us. Your token number is " + str(next_token)

            file.close()

            response = requests.post(self.URL, headers=headers, json=template)
            print(response.status_code)
            print(response.text)
            return Response(template)
        
        else:
            file = open("webhook/reply_to_message.json", "r")
            template = json.loads(file.read())

            template.pop("context")
            template["to"] = "919445089785"
            template["text"]["body"] = "There was an error in the registration procces of *" + user.user_name + "* with phone number *" + user.phone_number + "*"

            file.close()

            response = requests.post(self.URL, headers=headers, json=template)
            print(response.status_code)
            print(response.text)
            return Response(template)
        
        
        return Response({
            "status": "success",
            "from": serialized_data.data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"],
            "message": serialized_data.data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        })