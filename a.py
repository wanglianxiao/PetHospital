# -*- coding:utf-8 -*-
import web
import json
from pymongo import *

DB = MongoClient("172.30.235.146", 27017)["aaa"]

urls = (
    '/test', 'test',
    "/disease", "Disease",
    "/admin", "Admin",
    "/login", "login"
)

def success(data):
    return json.dumps(
        {
            "status": 200,
            "data": data
        },
        ensure_ascii=False,
        indent=2
    )

def fail(message):
    return json.dumps(
        {
            "status": 200,
            "message": message
        },
        ensure_ascii=False,
        indent=2
    )

class BaseClass:
    def __init__(self):
        self.className = "BaseClass"
        self.client = None
        self.majorKey = None
        self.keys = None

    def GET(self):
        return self.className

    def POST(self):
        operation = web.input().get("operation")
        if operation == "list":
            key = web.input().get("key")
            return self.list(key)
        elif operation == "add":
            return self.add()
        elif operation == "delete":
            return self.delete()
        elif operation == "update":
            return self.update()

    def list(self, key = None):
        List = []
        for item in self.client.find(key):
            data = dict(item)
            data["_id"] = str(data["_id"])
            List.append(data)
        return success(List)

    def add(self):
        dict = {}
        majorValue = web.input().get(self.majorKey)
        if self.client.find(majorValue):
            return fail(majorValue + " already exist")
        for key in self.keys:
            value = web.input().get(key)
            dict[key] = value
        return self.client.insert_one(dict)

    def update(self):
        majorValue = web.input().get(self.majorKey)
        newMajorValue = web.input().get("new_" + self.majorKey)

        if self.client.find_one({self.majorKey: majorValue}) is None:
            return fail(majorValue + " not found")
        if majorValue == newMajorValue and self.client.find_one({self.majorKey: newMajorValue}) is not None:
            return fail(majorValue + " already exist")

        dict = {self.majorKey: newMajorValue}
        for key in self.keys:
            value = web.input().get("new_" + key)
            dict[key] = value
        return success(self.client.update({self.majorKey: majorValue}, {"$set": dict}))

    def delete(self):
        value = web.input().get(self.majorKey)
        if self.client.find_one({self.majorKey: value}) is None:
            return fail("value not found")
        else:
            return success(self.client.delete_one({self.majorKey: value}))

class test(BaseClass):
    def __init__(self):
        self.Class = "test"

class case:
    def GET(self):
        return "case"

    def POST(self):
        client = DB["case"]
        operation = web.input().get("operation")
        if operation == "list":
            list = []
            for item in client.find():
                list.append(item["name"])
            return success(list)
        elif operation == "add":
            Class = web.input().get("class")
            name = web.input().get("name")
            return success(client["disease"].insert_one({"class": Class, "name": name}))
        elif operation == "delete":
            name = web.input().get("name")
            return success(client["disease"].delete_one({"name": name}))
        elif operation == "update":
            name = web.input().get("name")
            newClass = web.input().get("new_class")
            newName = web.input().get("new_name")
            if newClass is None:
                return client["disease"].update({'name': name}, {"$set": {"name": newName}})
            elif newName is None:
                return client["disease"].update({'name': name}, {"$set": {"class": newClass}})
            else:
                return client["disease"].update({'name': name}, {"$set": {"name": newName, "class": newClass}})

class Disease(BaseClass):
    def GET(self):
        return "disease"

    def POST(self):
        client = DB["disease"]
        operation = web.input().get("operation")
        if operation == "list_disease":
            type = web.input().get("type")
            List = []
            for item in client.find({"type": type}):
                list.append(item["disease"])
            return success(List)
        elif operation == "list_type":
            S = set()
            for item in client.find():
                S.add(item["type"])
            List = list(S)
            return success(List)
        elif operation == "add":
            type = web.input().get("type")
            disease = web.input().get("disease")
            return success(client.insert_one({"type": type, "disease": disease}))
        elif operation == "delete":
            disease = web.input().get("disease")
            return success(client.delete_one({"disease": disease}))
        elif operation == "update":
            disease = web.input().get("disease")
            newtype = web.input().get("new_type")
            newdisease = web.input().get("new_disease")

            if client.find_one({"disease": disease}) is None:
                return fail("disease not found")
            if disease != newdisease and client.find_one({"disease": newdisease}) is not None:
                return fail("disease already exist")
            dict = {}
            if newtype is not None:
                dict["type"] = newtype
            if newdisease is not None:
                dict["disease"] = newdisease
            return success(client.update({'disease': disease}, {"$set": dict}))

class Admin(BaseClass):
    def __init__(self):
        self.className = "Admin"
        self.client = DB["user"]
        self.majorKey = "name"
        self.keys = ["password", "role"]

class login:
    def GET(self):
        return "login"

    def POST(self):
        username = web.input().get("username")
        password = web.input().get("password")
        user = DB["user"].find_one({"name": username})
        response = {}
        if user is None:
            return fail("用户名不存在")
        elif password == user["password"]:
            data = dict(user)
            data["_id"] = str(data["_id"])
            return success(data)
        else:
            return fail("密码错误")

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
