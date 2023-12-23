from Auth import error
import logging
from DataBase import models
import jwt
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")

def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded

def __check_token(user_id, db_token, token) -> bool:
    token_lifetime = 3000
    try:
        if db_token != token:
            return False
        jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
        ts = jwt_text["timestamp"]
        if ts is not None:
            now = time.time()
            if token_lifetime > now - ts >= 0:
                return True
    except jwt.exceptions.InvalidSignatureError as e:
        logging.error(str(e))
        return False

def check_password(user_id: str, password: str) -> bool:
    if models.User.objects.filter(user_id=user_id).exists():
        user = models.User.objects.get(user_id=user_id)
        if user.password == password:
            return 200, "ok"
        else:
            return 401, "authorization fail."
    else:
        return 401, "authorization fail."

def check_token(user_id: str, token: str):
    if models.User.objects.filter(user_id=user_id).exists():
        user = models.User.objects.get(user_id=user_id)
        db_token = user.token
        if not __check_token(user_id, db_token, token):
            return 401, "authorization fail."
        return 200, "ok"
    else:
        return 401, "authorization fail."

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            password = data.get("password")
            terminal = data.get("terminal")
            token = ""

            code, message = check_password(user_id, password)
            if code != 200:
                return JsonResponse({"status": code, "message": message})

            token = jwt_encode(user_id, terminal)
            if not models.User.objects.filter(user_id=user_id).exists():
                return error.error_authorization_fail()
            else:
                models.User.objects.filter(user_id=user_id).update(token=token, terminal=terminal)
                return JsonResponse({"status": 200, "message": "ok", "token": token})

        except BaseException as e:
            return JsonResponse({"status": 530, "message": str(e)})

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            password = data.get("password")
            terminal = "terminal_{}".format(str(time.time()).replace(".", "_"))
            token = jwt_encode(user_id, terminal)
            if models.User.objects.filter(user_id=user_id).exists():
                return JsonResponse({"status": 931, "message": "该账号已被注册"})
            models.User.objects.create(user_id=user_id, password=password, balance=0, token=token, terminal=terminal)
        except Exception as e:
            return JsonResponse({"status": 901, "message": str(e)})
        return JsonResponse({"status": 200, "message": "ok"})

@csrf_exempt
def logout(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        token = data.get("token")
        code, message = check_token(user_id, token)
        if code != 200:
            return JsonResponse({"status": code, "message": message})
        terminal = "terminal_{}".format(str(time.time()).replace(".", "_"))
        dummy_token = jwt_encode(user_id, terminal)
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_authorization_fail()
        else:
            models.User.objects.filter(user_id=user_id).update(token=dummy_token, terminal=terminal)
    except BaseException as e:
        return JsonResponse({"status": 530, "message": str(e)})

    return JsonResponse({"status": 200, "message": "Logged out successfully"})

@csrf_exempt
def unregister(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        password = data.get("password")
        code, message = check_password(user_id, password)
        if code != 200:
            return JsonResponse({"status": code, "message": message})
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_authorization_fail()
        else:
            models.User.objects.filter(user_id=user_id).delete()
    except BaseException as e:
        return JsonResponse({"status": 530, "message": str(e)})

    return JsonResponse({"status": 200, "message": "Unregistered successfully"})

@csrf_exempt
def change_password(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        code, message = check_password(user_id, old_password)
        if code != 200:
            return JsonResponse({"status": code, "message": message})

        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_authorization_fail()

        else:
            terminal = "terminal_{}".format(str(time.time()).replace(".", "_"))
            token = jwt_encode(user_id, terminal)
            models.User.objects.filter(user_id=user_id).update(password=new_password, token=token, terminal=terminal)
            return JsonResponse({"status": 200, "message": "Password changed successfully"})

    except BaseException as e:
        return JsonResponse({"status": 530, "message": str(e)})