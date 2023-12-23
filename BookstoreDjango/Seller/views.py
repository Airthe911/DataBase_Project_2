from DataBase import models
import sqlite3 as sqlite
from Auth import error
import uuid
import logging
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def add_book(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        store_id = data.get("store_id")
        book_info = data.get("book_info")
        stock_level = data.get("stock_level")
        book_id = book_info["id"]
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_non_exist_user_id(user_id)
        if not models.User2Store.objects.filter(store_id=store_id).exists():
            return error.error_non_exist_store_id(store_id)
        if not models.Book.objects.filter(book_id=book_id).exists():
            return error.error_non_exist_book_id(book_id)
        if models.Store.objects.filter(book_id=book_id, store_id=store_id).exists():
            return JsonResponse({"status": 350, "message": "该商品在该店铺已存在"}, status=350)
        models.Store.objects.create(store_id=store_id, book_id=book_id, price=book_info["price"], stock_level=stock_level)
        return JsonResponse({"status": 200, "message": "ok"}, status=200)
    except BaseException as e:
        return JsonResponse({"status": 530, "message": "{}".format(str(e))}, status=530)
    
@csrf_exempt
def add_stock_level(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        store_id = data.get("store_id")
        book_id = data.get("book_id")
        add_stock_level = data.get("add_stock_level")
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_non_exist_user_id(user_id)
        if not models.User2Store.objects.filter(store_id=store_id).exists():
            return error.error_non_exist_store_id(store_id)
        if not models.Book.objects.filter(book_id=book_id).exists():
            return error.error_non_exist_book_id(book_id)
        if not models.Store.objects.filter(store_id=store_id, book_id=book_id).exists():
            return JsonResponse({"status": 322, "message": "新增库存中，store_id或book_id错误"}, status=322)
        store_info = models.Store.objects.filter(store_id=store_id, book_id=book_id).first()
        ori_stock_level = store_info.stock_level
        new_stock_level = ori_stock_level + add_stock_level
        models.Store.objects.filter(store_id=store_id, book_id=book_id).update(stock_level=new_stock_level)
        return JsonResponse({"status": 200, "message": "ok"}, status=200)
    except BaseException as e:
        return JsonResponse({"status": 530, "message": "{}".format(str(e))}, status=530)

@csrf_exempt
def create_store(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        store_id = data.get("store_id")
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_non_exist_user_id(user_id)
        if models.User2Store.objects.filter(store_id=store_id).exists():
            return error.error_exist_store_id(store_id)
        models.User2Store.objects.create(user_id=user_id, store_id=store_id)
        return JsonResponse({"status": 200, "message": "ok"}, status=200)
    except BaseException as e:
        return JsonResponse({"status": 530, "message": str(e)}, status=530)
        