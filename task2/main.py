from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from functools import wraps

def connection_or_input_errors(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{e}")
            return ["Please enter command correctly"]
    return inner

# create connection to DB
@connection_or_input_errors
def connection_to_db():
    uri = "mongodb+srv://newuser:newuserpassword@mycluster.4vebhys.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    work_db = client.NEW_TEST_DB.NEW_TEST_COLLECTION
    return work_db

def parse_input_input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print(f"Neither command entered, please enter one of: {args[1]}")
            return "nothing"                                                             #return some iterable to continue
        except KeyError:
            print(f"Command '{args[0]}' unsupported, please enter one of: {args[1]}")
            return "nothing"                                                             #return some iterable to continue   
        except Exception as e:
            print(f"{e}")                                                                   
            return "nothing"                                                             #return some iterable to continue
    return inner

@parse_input_input_error
def parse_input(user_input, cmd_dict):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    cmd_dict[cmd]                           #check if entered command correct (exists in commands list)
    return cmd, *args

# insert new doc
@connection_or_input_errors
def add_new(args, connect):
    name, age, features = args
    if connect.find_one({"name": name}):
        return f"Record {name} allrady exists" 
    else:
        connect.insert_one({
            "name": name,
            "age": age,
            "features": [features]
        })
        return f"{connect.find_one({"name": name})} -> added!"

# select doc by name
@connection_or_input_errors
def show_one(args, connect):
    name = args[0]
    if connect.find_one({"name": name}):
        return connect.find_one({"name": name}) 
    else: 
        return "No record with such name"

# select all docs
@connection_or_input_errors
def show_all(connect):
    if len(list(connect.find({}))) != 0:
        return connect.find({}) 
    else: 
        return ["Base is empty"]

# update doc - age by name
@connection_or_input_errors
def update_age(args, connect):
    name, age = args
    if connect.find_one({"name": name}):
        doc_old = connect.find_one({"name": name})
        connect.update_one({"name": name}, {"$set": {"age": age}})
        doc_new = connect.find_one({"name": name})
        return [doc_old, "updated to", doc_new]
    else:
        return ["No record with such name"]

# update doc - features by name
@connection_or_input_errors
def update_features(args, connect):
    name, features = args
    if connect.find_one({"name": name}):
        doc_old = connect.find_one({"name": name})
        connect.update_one({"name": name}, {"$addToSet": {"features": features}})
        doc_new = connect.find_one({"name": name})
        return [doc_old, "updated to", doc_new]
    else:
        return ["No record with such name"]

# delte doc by name
@connection_or_input_errors
def delete_one(args, connect):
    name = args[0]
    if connect.find_one({"name": name}):
        doc = connect.find_one({"name": name})
        connect.delete_one({"name": name})
        return f"{doc} -> deleted!"
    else:
        return "No record with such name"

# delte all docs
@connection_or_input_errors
def delete_all(connect):
    if len(list(connect.find({}))) != 0:
        all_docs = connect.find({})
        delted_list = [f"{el} -> deleted!" for el in all_docs]
        connect.delete_many({})
        return delted_list
    else:
        return ["Base is empty"]

def main():
    connect = connection_to_db()
    cmd_dict = {
                "close": "exit bot", "exit": "exit bot", "hello": "greeting - non functional command", 
                "add": "adding new record >>> add [name] [age] [features]",
                "show": "show info if exists >>> show [name]", "show_all": "show all records",
                "update_age": "update age >>> update [name] [new_age]", "update_features": "update features >>> update [name] [new_features]",
                "delete": "delete >>> delete [name]", "delete_all": "delete all"
                }   
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input, cmd_dict)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_new(args, connect))
        elif command == "show":
            print(show_one(args, connect))
        elif command == "show_all":
            for el in show_all(connect):
                print(el, end="\n")
        elif command == "update_age":
            for el in update_age(args, connect):
                print(el, end="\n")
        elif command == "update_features":
            for el in update_features(args, connect):
                print(el, end="\n")
        elif command == "delete":
            print(delete_one(args, connect))
        elif command == "delete_all":
            for el in delete_all(connect):
                print(el, end="\n")

if __name__ == "__main__":
    main()