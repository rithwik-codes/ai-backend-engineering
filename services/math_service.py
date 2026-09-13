def add_numbers(data):
    if not data or "a" not in data or"b"not in data:
        return ({"success":False,
                 "error":"Both 'a' and 'b' are required"
                 }),400
    a =data["a"]
    b = data["b"]

    if not isinstance(a,int) or not isinstance(b,int):
        return ({"success":False,
                 "error":"Both 'a' and 'b' must be integers"}),400
    result = a+b
    return ({"success": True,
             "data": {"result":result}
             }),200