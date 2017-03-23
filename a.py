# -*- coding:utf-8 -*-
import uuid

import web
import json
import time
import datetime
from pymongo import *
from bson.objectid import ObjectId
DB = MongoClient()["aaa"]

urls = (
    '/test/(.*?)', 'Test',
    "/department", "Department",
    "/department/(.*?)", "Department",
    "/disease", "Disease",
    "/disease/(.*?)", "Disease",
    "/user", "User",
    "/user/(.*?)", "User",
    "/case", "Case",
    "/case/(.*?)", "Case",
    "/case/(.*?)/(.*?)", "Case",
    "/login", "Login",
    "/logout", "Logout",
    "/test_img", "TestImg"
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'time': datetime.datetime.now()})


def success(data):
    print("200")
    return json.dumps(
        {
            "status": 200,
            "data": data,
        },
        ensure_ascii=False,
        indent=2
    )


def fail(message):
    print("400")
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

    def isLogined(self):
        return True
        #token = web.ctx.env.get('HTTP_AUTHORIZATION')
        #return token is not None and DB["sessionid"].find_one({"sessionid": token})

    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Request-Headers", "*")
        web.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        web.header("Access-Control-Allow-Headers", "Origin,X-Requested-With,Content-Type Accept,Content-Type,Access-Control-Allow-Headers, token")
        if not self.isLogined():
            return fail("请登录")
        query = {}
        distinct = None
        for item in web.input():
            if item == "id":
                if web.input()[item] == "":
                    distinct = "id"
                else:
                    try:
                        query["_id"] = ObjectId(web.input()["id"])
                    except:
                        return fail("报错！！")
            else:
                if web.input()[item] == "":
                    distinct = item
                else:
                    query[item] = str(web.input()[item])
        return self.list(query, distinct)

    def POST(self, operation, param2 = None):
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Request-Headers", "*")
        web.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        web.header("Access-Control-Allow-Headers", "Origin,X-Requested-With,Content-Type Accept,Content-Type,Access-Control-Allow-Headers, token")
        if not self.isLogined():
            return fail("请登录")
        #nanshou = web.ctx.env.get("HTTP_ACCEPT")
        request = dict(web.input())
        if operation == "add":
            return self.add(request)
        elif operation == "delete":
            return self.delete(request)
        elif operation == "update":
            return self.update(request)


    def OPTIONS(self, value = None, value2 = None):
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Request-Headers", "*")
        web.header("Access-Control-Allow-Headers", "Origin, X-Requested-With,Content-Type Accept,Access-Control-Allow-Headers, token")
        web.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")

    def list(self, key=None, Distinct=None):
        if Distinct is None:
            List = []
            for item in self.client.find(key):
                data = dict(item)
                data["id"] = str(data["_id"])
                del(data["_id"])
                List.append(data)
            return success(List)
        else:
            return success(self.client.find(key).distinct(Distinct))

    def add(self, request, default={}, image=[]):
        dict = default
        _id = request.get("id")
        if self.client.find_one({"_id": ObjectId(_id)}) is not None:
            return fail(_id + " already exists")

        for key in self.keys:
            value = request.get(key)
            dict[key] = value
        return success(json.dumps({"id": str(self.client.insert_one(dict).inserted_id)}))

    def update(self, request):
        _id = request.get("id")

        if self.client.find_one({"_id": ObjectId(_id)}) is None:
            return fail(_id + " not found")

        D = {}
        for key in self.keys:
            value = request.get("new_" + key)
            D[key] = value
        return success(self.client.update({"_id": ObjectId(_id)}, {"$set": D}))

    def delete(self, request):
        value = request.get(self.majorKey)
        if self.client.find_one({self.majorKey: value}) is None:
            return fail("value not found")
        else:
            return success(self.client.delete_one({self.majorKey: value}))

# class Test():
#
#     def GET(self):
#         return web.ctx.env.get
#
#     def POST(self, operation):
#         return "POST"


class Department(BaseClass):
    def __init__(self):
        self.client = DB["department"]
        self.className = "Department"
        self.keys = ["department", "function", "manager"]

class Case(BaseClass):
    def __init__(self):
        self.client = DB["case"]
        self.className = "Case"
        #self.majorKey = "name"
        self.keys = ["name", "disease_name", "received", "result", "treatment", "image"]

    def list(self, key=None, Distinct=None):
        if Distinct is None:
            List = []
            for item in self.client.find(key):
                data = dict(item)
                data["id"] = str(data["_id"])
                del (data["_id"])
                data["treatment"].sort(key=lambda x:x["timestamp"],reverse=True)
                #sortedtreatment = sorted(data["treatment"].iteritems(), key=lambda d:d[1]["timestamp"])
                List.append(data)
            return success(List)
        else:
            return success(self.client.find(key).distinct(Distinct))

    def POST(self, treatment, operation = None):
        if operation is None:
            return BaseClass.POST(self, treatment, None)
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Request-Headers", "*")
        web.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        web.header("Access-Control-Allow-Headers",
                   "Origin,X-Requested-With,Content-Type Accept,Content-Type,Access-Control-Allow-Headers, token")
        if not self.isLogined():
            return fail("请登录")
        # nanshou = web.ctx.env.get("HTTP_ACCEPT")
        request = dict(web.input())
        if operation == "add":
            return self.treatment_add(request)
        return fail("WTF")

    def treatment_add(self, request):
        _id = request["id"]
        content = request["content"]
        collection = self.client.find_one({"_id": ObjectId(_id)})
        if collection:
            now = time.strftime('%Y/%m/%d',time.localtime(time.time()))
            contents = collection["treatment"]
            self.client.update_one(
                {
                    "_id": ObjectId(_id)
                },
                {
                    "$push": {
                        "treatment": {
                            "date": now,
                            "content": content,
                            "timestamp": time.time()
                        }
                    }
                })
            #L = []
            #for item in self.client.find_one({"_id": ObjectId(_id)})["treatment"]:
            #    L.insert(0, item)
            L = self.client.find_one({"_id": ObjectId(_id)})["treatment"]
            L.sort(key=lambda x:x["timestamp"],reverse=True)
            return success(L)#success(self.client.find_one({"_id": ObjectId(_id)})["treatment"])
        else:
            return fail(_id + " not exists")

class Disease(BaseClass):
    def __init__(self):
        self.client = DB["disease"]
        self.className = "Disease"
        self.keys = ["disease", "type", "introduction"]

class User(BaseClass):
    def __init__(self):
        self.className = "User"
        self.client = DB["user"]
        #self.majorKey = "name"
        self.keys = ["name", "password", "role"]

    def GET(self, operation = None):
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Request-Headers", "*")
        web.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        web.header("Access-Control-Allow-Headers", "Origin,X-Requested-With,Content-Type Accept,Content-Type,Access-Control-Allow-Headers, token")
        if operation is None:
            return BaseClass.GET(self)
        if operation == "profile":
            return self.profile()

    def profile(self):
        #sessionid = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'time': datetime.datetime.now()})
        sessionid = web.ctx.env.get("HTTP_TOKEN")
        user = self.client.find_one({"sessionid": sessionid})
        if user:
            data = dict(user)
            data["id"] = str(data["_id"])
            del (data["_id"])
            return success(data)
        else:
            return fail(sessionid + " not existed")

    def add(self, request):
        return BaseClass.add(self, request, {"role": "intern"})

class Login:
    def GET(self):
        return "login"

    def POST(self):
        username = web.input().get("name")
        password = web.input().get("password")
        user = DB["user"].find_one({"name": username})
        if user is None:
            return fail(username + " not existed")
        elif password == user["password"]:
            data = dict(user)
            data["_id"] = str(data["_id"])

            session.logged_in = True
            session.user = user
            session.sessionid = str(uuid.uuid1())

            DB["user"].update(session.user, {"$set": {"sessionid": session.sessionid}})
            data["sessionid"] = session.sessionid

            return success(data)
        else:
            return fail("密码错误")

class Logout:
    def GET(self):
        return "logout"

    def POST(self):
        token = web.ctx.env.get('HTTP_TOKEN')
        user = DB["user"].find_one({"sessionid": token})
        if user is None:
            return fail("你他喵的没登录啊")
        else:
            return success(DB["user"].update({"_id": user["_id"]}, {"$unset": {"sessionid": 1}}))


class TestImg:
    def GET(self):
        return

if __name__ == "__main__":
    app.run()
