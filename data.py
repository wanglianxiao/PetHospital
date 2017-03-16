# -*- coding:utf-8 -*-
from pymongo import *
import re
import base64
import random
import os
client = MongoClient()["aaa"]


def department():
    client["department"].drop()
    dict = [
        {"department": "科室", "function": "功能", "manager": "主要责任人"},
        {"department": "前台", "function": "包括接待挂号、导医咨询、病历档案发出与回收、收费等。", "manager": "前台"},
        {"department": "档案室", "function": "包括病例档案的合理保存与数据统计等。", "manager": "前台"},
        {"department": "诊室", "function": "包括诊室的布局介绍；对宠物进行临床基本检查（视、听、触、嗅等）、疾病诊断；与宠物主人交流并根据情况开具处方。",
         "manager": "执业兽医师"},
        {"department": "免疫室", "function": "包括为健康宠物接种疫苗的流程，对常见并发症的处理流程，对常见免疫相关问题的解答等。", "manager": "助理、执业兽医师"},
        {"department": "化验室",
         "function": "包括对送检样本的预处理，对相应样本进行血常规、血液生化、电解质、血气、血凝指标、激素指标、尿常规、微生物学检查、药敏、皮肤刮片、粪便检查、传染病检查等检查操作流程。",
         "manager": "助理、执业兽医师"},
        {"department": "影像室",
         "function": "包括X线检查、B超检查以及CT、MRI检查。如X线检查：X光机的结构功能介绍、全身各部位的摆位、拍摄条件的选择、拍摄流程、洗片的操作流程。B超检查：扫查探头的选择、全身各个部位扫查的摆位、腹部扫查流程。",
         "manager": "助理、执业兽医师"},
        {"department": "专科检查室",
         "function": "包括对眼科、骨科、神经科、心脏科等专科疾病的检查，如眼科（检眼镜检查、眼压检查、裂隙灯检查、眼底检查、泪液分泌量检查等）、心脏科检查（心脏听诊、心电图检查等）、神经学检查（步态检查、各种反射检查等）等。",
         "manager": "执业兽医师"},
        {"department": "处置室", "function": "包括口服投药、换药、清洗耳道、挤肛门腺、修剪指甲、鼻饲管放置、灌肠、安乐死等基本处置操作流程。",
         "manager": "助理、执业兽医师"},
        {"department": "药房", "function": "包括对各种药物的存放要求、处方的审核流程、药物的发放流程、常见药物的使用说明等。", "manager": "助理执业兽医师"},
        {"department": "注射室", "function": "包括静脉注射、皮下注射、肌肉注射、局部封闭注射的操作流程，常见问题的处理方法，输液泵、加热垫的使用方法，注射室的消毒流程。",
         "manager": "助理、执业兽医师"},
        {"department": "手术准备室",
         "function": "包括术前对宠物进行麻前给药、注射麻醉、吸入麻醉的流程，保定、剃毛、消毒的流程，常见手术器械的介绍，手术器械包的准备、灭菌流程，手术人员的消毒、穿戴手术衣流程等。",
         "manager": "助理、执业兽医师"},
        {"department": "手术室", "function": "包括手术室的布局介绍，手术室消毒流程，手术无菌要求，常规手术、特殊手等的操作规范。", "manager": "执业兽医师"},
        {"department": "住院部", "function": "包括对需要住院的病例进行护理分级，不同护理级别的要求，住院部的工作流程，住院部的消毒流程等。",
         "manager": "住院执业兽医师或助理执业兽医师"},
        {"department": "病理剖检室", "function": "包括对病死动物剖解的流程，病理剖检室的消毒流程，病历剖检过程的人员要求，病理剖检过程中的人道关怀。",
         "manager": "执业兽医师"}
    ]
    client["department"].insert_many(dict)

def disease():
    client["disease"].drop()
    dict = [
        {"type": "传染病", "list": ["犬瘟热", "犬细小病毒", "犬传染性肝炎", "犬冠状病毒", "猫泛白细胞减少症", "猫病毒性病气管炎", "皮肤真菌感染"]},
        {"type": "寄生虫病", "list": ["蛔虫病", "钩虫病", "绦虫病", "球虫病", "疥螨虫病", "蚤病"]},
        {"type": "内科",
         "list": ["口炎", "肠炎", "肠便秘", "胰腺炎", "肝炎", "腹膜炎", "肛门腺炎", "感冒", "鼻炎", "气管支气管炎", "肺炎", "心力衰竭", "尿道感染", "尿结石",
                  "膀胱炎", "肾炎", "佝偻病", "有机磷中毒", "糖尿病", "耳血肿", "中耳炎", "眼睑内翻", "结膜炎", "角膜炎"]},
        {"type": "外产科疾病",
         "list": ["外伤", "外科感染", "骨折", "关节脱位", "湿疹", "皮炎", "脓皮病", "脱毛症", "趾间囊肿", "疝", "阴道炎", "阴道脱出", "子宫蓄脓", "难产",
                  "乳房炎"]},
        {"type": "常用手术", "list": ["绝育", "剖腹产", "瞬膜腺增生物切除", "眼球摘除", "立耳术", "断尾术"]},
        {"type": "免疫", "list": ["犬", "猫免疫程序"]},
    ]
    for item in dict:
        for disease in item["list"]:
            client["disease"].insert_one({"type": item["type"], "disease": disease})
    client["disease"].ensure_index({"type": 1})

def wanglianxiao():
    openfile = open("D:/2.txt", "r")
    input = openfile.readline()
    input = re.subn(r"<img ng-src=\"data:image\/(png|gif|jpeg);base64,", '', input)[0]
    input = re.subn(r"\">", '', input)[0]
    imgdata = base64.b64decode(input)
    file = open('D:/1.jpg', 'wb')
    file.write(imgdata)
    file.close()

# def test():
#     st = "abc12abc12bc"
#     result, number = re.subn("\d", "hehe", st)
#     print(result)


# def test():
#     # edge = [
#     #     (0, 1, 0.5),
#     #     (1, 2, 0.5),
#     #     (2, 3, 0.5),
#     #     (0, 4, 0.9),
#     #     (4, 5, 0.9),
#     #     (5, 2, 0.9),
#     #     (0, 6, 0.9),
#     #     (6, 7, 0.9),
#     #     (7, 2, 0.9)
#     # ]
#     # print max(max(edge, key= lambda x: x[0])[0] + 1, max(edge, key= lambda x: x[1])[1]), edge.__len__()
#     # for e in edge:
#     #     print e[0] + 1, e[1] + 1, e[2], "0"
#     #     print e[1] + 1, e[0] + 1, "0", e[2]
#     n = 500
#     a = []
#     output = file("1.txt", "w")
#     for i in range(n):
#         for j in range(i + 1, n):
#             if random.uniform(0, 1) > 1 - 10.0 / n:
#                 a.append((i + 1, j + 1, random.uniform(0, 1), random.uniform(0, 1)))
#     output.write("%d %d\n" % (n, a.__len__()))
#     for x in a:
#         output.write("%d %d %f %f\n" % (x[0], x[1], x[2], x[3]))
#         output.write("%d %d %f %f\n" % (x[1], x[0], x[3], x[2]))
#
# test()
# #disease()
department()
disease()
