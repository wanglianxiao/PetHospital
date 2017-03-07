# -*- coding:utf-8 -*-
import web
import json
from pymongo import *

DB = MongoClient("172.30.235.146",21017)["aaa"]

urls = (
    '/test', 'test',
    "/disease", "Disease",
    "/admin", "Admin",
    "/login", "login"
              "/case", "Case"
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
            "status": 400,
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

    def list(self, key=None):
        List = []
        for item in self.client.find(key):
            data = dict(item)
            data["_id"] = str(data["_id"])
            List.append(data)
        return success(List)

    def add(self, default={}):
        dict = default
        majorValue = web.input().get(self.majorKey)
        if self.client.find({self.majorKey: majorValue}) is None:
            return fail(majorValue + " already exist")
        if self.majorKey not in dict:
            dict[self.majorKey] = majorValue
        for key in self.keys:
            if key in dict:
                continue
            value = web.input().get(key)
            dict[key] = value
        self.client.insert_one(dict)
        return success("")

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
        self.className = "Admin"
        self.client = DB["user"]
        self.majorKey = "name"
        self.keys = ["password", "role"]

    def GET(self):
        return "GET"

    def POST(self):
        return "POST"


class Case:
    def __init__(self):
        self.client = DB["case"]
        self.className = "Case"
        self.majorKey = ""


class Disease(BaseClass):
    def __init__(self):
        self.client = DB["disease"]
        self.className = "Disease"
        self.majorKey = "disease"
        self.keys = ["type"]


class Admin(BaseClass):
    def __init__(self):
        self.className = "Admin"
        self.client = DB["user"]
        self.majorKey = "name"
        self.keys = ["password", "role"]

    def add(self):
        return BaseClass.add(self, {"role": "internal"})


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
