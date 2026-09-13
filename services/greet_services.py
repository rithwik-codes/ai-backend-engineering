def process_greet(data):
    if not data or "name" not in data:
        return ({"error":"name is required"}),400
    name = data["name"]
    age = data.get("age")
    if age is  None:
        return ({"message": f"Hello {name}!"}),200
    if not isinstance(age,int):
        return ({"error":"Age must be an integer"}),400
    if age<18:
        return ({"message": f"Hello {name}, you are a minor!"}),200
    if age<0:
        return ({"error":"age should be a  positive number"}),400
    
    return ({"message": f"Hello {name}, you are an adult!"}),200