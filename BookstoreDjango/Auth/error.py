from django.http import JsonResponse

error_code = {
    401: "authorization fail.",
    511: "non exist user id {}",
    512: "exist user id {}",
    513: "non exist store id {}",
    514: "exist store id {}",
    515: "non exist book id {}",
    516: "exist book id {}",
    517: "stock level low, book id {}",
    518: "invalid order id {}",
    519: "not sufficient funds, order id {}",
    520: "",
    521: "",
    522: "",
    523: "",
    524: "",
    525: "",
    526: "",
    527: "",
    528: "",
}


def error_non_exist_user_id(user_id):
    return JsonResponse({"status": 511, "message": error_code[511].format(user_id)}, status=511)

def error_exist_user_id(user_id):
    return JsonResponse({"status": 512, "message": error_code[512].format(user_id)}, status=512)

def error_non_exist_store_id(store_id):
    return JsonResponse({"status": 513, "message": error_code[513].format(store_id)}, status=513)

def error_exist_store_id(store_id):
    return JsonResponse({"status": 514, "message": error_code[514].format(store_id)}, status=514)

def error_non_exist_book_id(book_id):
    return JsonResponse({"status": 515, "message": error_code[515].format(book_id)}, status=515)

def error_exist_book_id(book_id):
    return JsonResponse({"status": 516, "message": error_code[516].format(book_id)}, status=516)

def error_stock_level_low(book_id):
    return JsonResponse({"status": 517, "message": error_code[517].format(book_id)}, status=517)

def error_invalid_order_id(order_id):
    return JsonResponse({"status": 518, "message": error_code[518].format(order_id)}, status=518)

def error_not_sufficient_funds(order_id):
    return JsonResponse({"status": 519, "message": error_code[518].format(order_id)}, status=519)

def error_authorization_fail():
    return JsonResponse({"status": 401, "message": error_code[401]}, status=401)

def error_and_message(code, message):
    return JsonResponse({"status": code, "message": message}, status=code)