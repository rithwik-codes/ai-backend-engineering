def success_response(data):
    return {"success":True,"data":data},200
def error_response(message):
    return {"success":False,"error":message},400