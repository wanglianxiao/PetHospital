# -*- coding:utf-8 -*-
import web
import json
import uuid
import datetime
from pymongo import *

DB = MongoClient()["aaa"]

urls = (
    '/test/(.*)', 'Test',
    "/disease/(.*)", "Disease",
    "/user/(.*)", "User",
    "/login", "Login",
    "/case/(.*)", "Case"
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'time':datetime.datetime.now()})


def success(data):
    return json.dumps(
        {
            "status": 200,
            "data": data,
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

    def IsLogined(self):
        token = web.ctx.env.get('HTTP_AUTHORIZATION')
        if token is None:
            return False
        elif DB["sessionid"].find_one({"sessionid": token}):
            return True
        else:
            return False

    def GET(self, uri):
        if self.IsLogined():
            wtf = uri.encode("UTF-8")
            query = {}
            for st in wtf.split("&"):
                if "=" in st:
                    s = st.split("=")
                    query[s[0]] = s[1]
            return self.list(query)

    def POST(self, operation):
        if self.IsLogined():
            if operation == "add":
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
        if self.client.find_one({self.majorKey: majorValue}) is not None:
            return fail(majorValue + " already exists")
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


class Test(BaseClass):
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
        self.majorKey = "name"
        self.keys = ["disease_name", "received", "result", "treatment"]

class Disease(BaseClass):
    def __init__(self):
        self.client = DB["disease"]
        self.className = "Disease"
        self.majorKey = "disease"
        self.keys = ["type"]


class User(BaseClass):
    def __init__(self):
        self.className = "Admin"
        self.client = DB["user"]
        self.majorKey = "name"
        self.keys = ["password", "role"]

    def add(self):
        return BaseClass.add(self, {"role": "internal"})

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
            session.user = user
            session.sessionid = str(uuid.uuid1())
            DB["sessionid"].insert({"sessionid": session.sessionid, "user": session.user})
            data["token"] = session.sessionid
            return success(data)
        else:
            return fail("密码错误")

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()





    # session.time = datetime.datetime.now()
    # data["session_time "] = str(session.time)
    # last_login = web.cookies().get('time')
    # last_login_data = str(time.asctime( time.localtime(time.time()) ))

    # if session._config["cookie_name"] is None:
    #     web.config.session_parameters['cookie_name'] = uuid.uuid1()
    #     data["session_id"] = str(web.config.session_parameters['cookie_name'])
    #     DB["sessionid"].insert({"sessionid": data["session_id"], "user": session.login })
    # else:
    #     sessionid = DB["sessionid"].find_one({"user": username})
    #     if session._config["cookie_name"] == DB["sessionid"].find_one({"user": username}):
    #         return success(data)
    #     else:
    #         return fail("session expired")