
# Create your views here.
from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, StreamingHttpResponse
import json
from django.conf import settings
from pathlib import Path

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
    file_path = Path(settings.BASE_DIR) / "api" / "data.json"
    with open(file_path, "r", encoding="utf-8") as file:
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
        file_path = Path(settings.BASE_DIR) / "api" / "data.json"
        file_data = data.get('file_data')
        print(file_data)
        print(type(file_data))
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(file_data, file)
        return JsonResponse({"success": True,})


@csrf_exempt
def stream_bytes(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        filename = data.get("filename")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
    try:
        def generator():
            file_path = Path(settings.BASE_DIR) / "media" / "files" / f'{filename}'
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    yield chunk
        return StreamingHttpResponse(
            generator(),
            content_type="application/octet-stream"
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


