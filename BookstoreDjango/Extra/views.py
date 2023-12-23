from DataBase import models
import sqlite3 as sqlite
from Auth import error
import uuid
import logging
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime


@csrf_exempt
def delivery(request):
    data = json.loads(request.body)
    order_id = data.get("order_id")
    store_id = data.get("store_id")
    store_owner_id = data.get("store_owner_id")
    password = data.get("password")
    # step1 验证登录信息是否正确
    if not models.User.objects.filter(user_id=store_owner_id, password=password).exists():
        return error.error_authorization_fail()
    # step2 验证店主关系是否成立
    if not models.User2Store.objects.filter(store_id=store_id, user_id=store_owner_id).exists():
        return JsonResponse({"status": 304, "message": "当前用户不是对应店铺的店主"}, status=304)
    # step3 验证当前店铺是否确实存在这笔订单
    if not models.OrderInfo.objects.filter(order_id=order_id, store_id=store_id).exists():
        return JsonResponse({"status": 305, "message": "当前店铺没有这笔订单"}, status=305)
    # step4 查询当前订单的详情信息
    order_info = models.OrderInfo.objects.filter(order_id=order_id, store_id=store_id).first()
    if order_info.state != 1:
        return JsonResponse({"status": 307, "message": "只有处于未发货状态才能进行发货"}, status=307)
    # step 5 发货
    models.OrderInfo.objects.filter(order_id=order_id, store_id=store_id).update(state=2, delivery_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return JsonResponse({"status": 200, "message": "ok"}, status=200)

@csrf_exempt
def receipt(request):
    data = json.loads(request.body)
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    password = data.get("password")
    # step1 验证登录信息是否正确
    if not models.User.objects.filter(user_id=user_id, password=password).exists():
        return error.error_authorization_fail()
    # step2 验证这个用户是否确实有这个订单
    if not models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id).exists():
        return JsonResponse({"status": 305, "message": "订单信息不匹配"}, status=305)
    # step3 收货
    if not models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id, state=2).exists():
        return JsonResponse({"status": 309, "message": "只有处于已发货、未收货的状态，才能进行本操作"}, status=309)
    models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id).update(state=3, receipt_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return JsonResponse({"status": 200, "message": "ok"}, status=200)

@csrf_exempt
def lookup(request):
    data = json.loads(request.body)
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    password = data.get("password")
    # step1 验证登录信息是否正确
    if not models.User.objects.filter(user_id=user_id, password=password).exists():
        return error.error_authorization_fail()
    # step2 验证这个用户是否确实有这个订单
    if_exists_flag = False
    # 先以用户身份查找
    if not models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id).exists():
        # 代码运行到此处，证明以用户身份查找失败，接下来以店主身份进行查询
        if models.User2Store.objects.filter(user_id=user_id).exists():
            relations = models.User2Store.objects.filter(user_id=user_id)
            for relation in relations:
                store_id = relation.store_id
                if models.OrderInfo.objects.filter(order_id=order_id, store_id=store_id).exists():
                    if_exists_flag = True
                    break
    else:
        if_exists_flag = True
    if not if_exists_flag:
        return JsonResponse({"status": 305, "message": "订单信息不匹配"}, status=305)
    # step3 查询订单结果并返回
    result = models.OrderInfo.objects.filter(order_id=order_id).values()[0]
    return JsonResponse({"status": 200, "message": str(result)}, status=200)

@csrf_exempt
def cancer(request):
    data = json.loads(request.body)
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    password = data.get("password")
    # step1 验证登录信息是否正确
    if not models.User.objects.filter(user_id=user_id, password=password).exists():
        return error.error_authorization_fail()
    # step2 验证这个用户是否确实有这个订单
    if not models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id).exists():
        return JsonResponse({"status": 305, "message": "订单信息不匹配"}, status=305)
    # step3 查询订单状态
    order_info = models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id).first()
    state = order_info.state
    back_book_id = order_info.book_id
    back_count = int(order_info.number)
    back_price = float(order_info.price)
    back_store_id = order_info.store_id
    back_user_id = order_info.user_id
    if back_user_id != user_id:
        return JsonResponse({"status": 305, "message": "订单信息不匹配"}, status=305)
    if state == 0:  # 订单尚未付款,只需返还数据
        models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id).delete()
        ori_stock_level = models.Store.objects.filter(store_id=back_store_id, book_id=back_book_id).first().stock_level
        models.Store.objects.filter(store_id=back_store_id, book_id=back_book_id).update(stock_level=ori_stock_level+back_count)
        return JsonResponse({"status": 200, "message": "ok"}, status=200)
    elif state == 1:  # 订单已付款，但尚未发货。此时需要退钱
        # 额外需要知道店主是谁
        if not models.User2Store.objects.filter(store_id=back_store_id).exists():
            return JsonResponse({"status": 319, "message": "店铺不存在"}, status=319)
        store_info = models.User2Store.objects.filter(store_id=back_store_id).first()
        store_owner_id = store_info.user_id
        # 查一下店主钱是否充足，如果店主钱不足，仍然无法完成取消订单
        if not models.User.objects.filter(user_id=store_owner_id).exists():
            return JsonResponse({"status": 320, "message": "店主不存在"}, status=320)
        seller_balance = models.User.objects.filter(user_id=store_owner_id).first().balance
        if seller_balance < back_count * back_price:
            return JsonResponse({"status": 321, "message": "店主余额不足"}, status=321)
        # 删除订单信息，书籍返还
        models.OrderInfo.objects.filter(order_id=order_id, user_id=user_id).delete()
        ori_stock_level = models.Store.objects.filter(store_id=back_store_id, book_id=back_book_id).first().stock_level
        models.Store.objects.filter(store_id=back_store_id, book_id=back_book_id).update(stock_level=ori_stock_level+back_count)
        # 退钱
        models.User.objects.filter(user_id=store_owner_id).update(balance=float(seller_balance) - back_count * back_price)
        user_balance = models.User.objects.filter(user_id=user_id).first().balance
        models.User.objects.filter(user_id=user_id).update(balance=float(user_balance) + back_count * back_price)
        return JsonResponse({"status": 200, "message": "ok"}, status=200)
    else:
        return JsonResponse({"status": 317, "message": "已发货或已收货的订单无法取消"}, status=317)



