import json
import random
from re import sub
import time
import os

import traceback
from yiban import YiBan
import util

if __name__ == '__main__':
    try:
        account = "youraccount"
        password = "yourpassword"
        #if(len(account)==0 or len(password)==0):
        #    print("账号")
        #    account = input()
        #    print("密码")
        #    password = input()

        yb = YiBan(account, password) # FIXME:账号密码
        yb.login()
        yb.getHome()
        print("登录成功 %s \n"%yb.name)
        yb.auth()
        uncompleted_list = yb.getUncompletedList()["data"]
        #获取上次提交的结果
        yesterdayResult = yb.getJsonByInitiateId(yb.getTaskDetail(yb.getCompletedList()["data"][0]["TaskId"])["data"]["InitiateId"])
        formData = yesterdayResult["data"]["Initiate"]["FormDataJson"]
        extendData = yesterdayResult["data"]["Initiate"]["ExtendDataJson"]

        print("未完成的任务:"+str(yb.getUncompletedList())+"\n")
        print("已完成的任务:",yesterdayResult,"\n")

        uncompleted_list = list(filter(lambda x: "体温检测" in x["Title"], uncompleted_list))  # FIXME: 长理的打卡任务标题均含有"体温检测"字样 此举是防止其他表单干扰 （可能会变）
        if len(uncompleted_list) == 0:
            print("没找到今天长理体温上报的任务，可能是你已经上报，如果不是请手动上报。")
        else:
            uncompleted_list_sort = util.desc_sort(uncompleted_list, "StartTime")  # 按开始时间排序
            new_task = uncompleted_list_sort[0]  # 只取一个最新的

            # 更新extendData
            print("更新前的exdata",extendData,"\n")
            extendData["TaskId"] = new_task["TaskId"]
            extendData["content"][0]["value"] = new_task["Title"]

            print("找到未上报的任务:", new_task,"\n")
            print("更新后的exdata",extendData,"\n")

            # 更新formData
            print("更新前的formdata",formData,"\n")
            formData[0]['value'] = time.strftime('%Y-%m-%d %H:%M',time.localtime())
            formDataJson = {each['id']: each['value'] for each in formData}
            print("更新后的formdata",formDataJson,"\n")

            task_detail = yb.getTaskDetail(new_task["TaskId"])["data"]
            print("今日任务:"+str(task_detail),"\n")

            #以下两行行为测试代码 一般情况下可注释 查看提交的具体表单内容
            #formRes = yb.getform(task_detail["WFId"])
            #print("formRes"+str(formRes))

            submit_result = yb.clockIn(task_detail["WFId"],formDataJson,extendData)
            #print(str(submit_result))
            if submit_result["code"] == 0:
                #share_url = yb.getShareUrl(submit_result["data"])["data"]["uri"]
                print("已完成一次体温上报[%s]" % task_detail["Title"])
                #print("访问此网址查看详情:%s" % share_url)
            else:
                print("[%s]遇到了一些错误:%s" % (task_detail["Title"], submit_result["msg"]))
    except Exception as e:
        print("出错啦")
        print(str(e))
    #os.system("pause")