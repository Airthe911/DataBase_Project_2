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
def new_order(request):
    order_id = ""
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        store_id = data.get("store_id")
        books = data.get("books")
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_non_exist_user_id(user_id)

        if not models.Store.objects.filter(store_id=store_id).exists():
            return error.error_non_exist_store_id(store_id)

        uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
        order_id = uid

        for book in books:
            book_id = book["id"]
            count = book["count"]
            if not models.Store.objects.filter(store_id=store_id, book_id=book_id).exists():
                return error.error_non_exist_book_id(book_id)

            book = models.Store.objects.get(store_id=store_id, book_id=book_id)
            stock_level = book.stock_level
            price = book.price

            if stock_level < count:
                return error.error_stock_level_low(book_id)

            models.Store.objects.filter(store_id=store_id, book_id=book_id).update(stock_level=stock_level - count)

            models.OrderInfo.objects.create(
                order_id=order_id,
                user_id=user_id,
                store_id=store_id,
                book_id=book_id,
                price=price,
                number=count,
                state=0,
                order_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                payment_time=None,
                delivery_time=None,
                receipt_time=None
            )

    except sqlite.Error as e:
        logging.info("528, {}".format(str(e)))
        return JsonResponse({"status": 528, "message": str(e)}, status=528)

    except BaseException as e:
        print(e)
        logging.info("530, {}".format(str(e)))
        return JsonResponse({"status": 530, "message": str(e)}, status=530)

    return JsonResponse({"status": 200, "message": "Order placed successfully", "order_id": order_id}, status=200)

@csrf_exempt
def payment(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        password = data.get("password")
        order_id = data.get("order_id")
        if not models.OrderInfo.objects.filter(order_id=order_id).exists():
            return error.error_invalid_order_id(order_id)
        order_info = models.OrderInfo.objects.filter(order_id=order_id).first()
        buyer_id = order_info.user_id
        store_id = order_info.store_id
        state_code = order_info.state
        if buyer_id != user_id:
            return error.error_authorization_fail()
        # 新功能需要，付款前先验证订单状态
        if state_code != 0:
            return JsonResponse({"status": 312, "message": "只有未付款的订单才能执行该操作"}, status=312)
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_authorization_fail()
        buyer_info = models.User.objects.filter(user_id=user_id).first()
        if buyer_info.password != password:
            return error.error_authorization_fail()
        balance = buyer_info.balance
        if not models.User2Store.objects.filter(store_id=store_id).exists():
            return error.error_non_exist_store_id(store_id)
        store_info = models.User2Store.objects.filter(store_id=store_id).first()
        seller_id = store_info.user_id
        if not models.User.objects.filter(user_id=seller_id).exists():
            return error.error_non_exist_user_id(seller_id)
        seller_balance = models.User.objects.filter(user_id=seller_id).first().balance
        if not models.OrderInfo.objects.filter(order_id=order_id).exists():
            return JsonResponse({"status": 303, "message": "查询order_info表出错"}, status=303)
        total_price = 0
        order_infoes = models.OrderInfo.objects.filter(order_id=order_id)
        for order_info in order_infoes:
            total_price = total_price + order_info.price * order_info.number
        if balance < total_price:
            return error.error_not_sufficient_funds(order_id)
        models.User.objects.filter(user_id=user_id).update(balance=balance - total_price)
        models.User.objects.filter(user_id=seller_id).update(balance=seller_balance + total_price)
        models.OrderInfo.objects.filter(order_id=order_id).update(state=1, payment_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return JsonResponse({"status": 200, "message": "ok"}, status=200)
    except sqlite.Error as e:
        return JsonResponse({"status": 528, "message": str(e)}, status=528)
    except BaseException as e:
        return JsonResponse({"status": 530, "message": str(e)}, status=530)

@csrf_exempt
def add_funds(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        password = data.get("password")
        add_value = data.get("add_value")
        if not models.User.objects.filter(user_id=user_id).exists():
            return error.error_authorization_fail()
        user = models.User.objects.filter(user_id=user_id).first()
        saved_password = user.password
        balance = user.balance
        if saved_password != password:
            return error.error_authorization_fail()
        models.User.objects.filter(user_id=user_id).update(balance=balance + add_value)
        return JsonResponse({"status": 200, "message": "ok"}, status=200)
    except sqlite.Error as e:
        return JsonResponse({"status": 528, "message": str(e)}, status=528)
    except BaseException as e:
        return JsonResponse({"status": 530, "message": str(e)}, status=530)
    

