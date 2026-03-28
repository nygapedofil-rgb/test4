from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, StreamingHttpResponse
import json

User = get_user_model()
@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)
    d = get_object_or_404(User, username=username)

    with open('api/data.json', "r", encoding="utf-8") as file:
        try:
            datas = json.load(file)
            print('działa')
            # Parsowanie JSON → Python dict/list
        except Exception as e:
            print('błąd')
            print(e)
    if user is None:
        return JsonResponse({"error": "invalid credentials"}, status=401)
    else:
        print(datas)
        return JsonResponse({"success": True,'data': datas})

@csrf_exempt
def api_update_file(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)
    d = get_object_or_404(User, username=username)

    if user is None:
        return JsonResponse({"error": "invalid credentials"}, status=401)
    else:
       # return JsonResponse({"success": True,'data': })
        file_data = data.get('file_data')
        print(file_data)
        print(type(file_data))
        with open('api/data.json', "w", encoding="utf-8") as file:
            json.dump(file_data, file)
        return JsonResponse({"success": True,})

@csrf_exempt
def stream_bytes(request):
    def generator():
        with open("media/files/client.exe", "rb") as f:
            while chunk := f.read(8192):
                yield chunk

    return StreamingHttpResponse(
        generator(),
        content_type="application/octet-stream"
    )