import urllib.request
import json
import requests

def comm(user, passw):
    #Sends information to the server
    #url = "http://127.0.0.1:8000/api/verify/"
    url = "https://sleepy-hamlet-6170.herokuapp.com/api/verify/"
    json_dict = { 'username': user, 'password': passw }
    json_data = json.dumps(json_dict)
    post_data = json_data.encode('utf-8')
    headers = {}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, post_data, headers)
    #print(req)
    #r = requests.post(url, post_data)
    #text_file = open("Output.html", "w")
    #text_file.write(r.text)
    #text_file.close()
    res = urllib.request.urlopen(req)
    permiss = res.read().decode('utf-8')
    if permiss == "true":
        return True
    return False

def comm_reports(user, passw):
    #url = "http://127.0.0.1:8000/api/reports/"
    url = "https://sleepy-hamlet-6170.herokuapp.com/api/reports/"
    json_dict = { 'username': user, 'password': passw }
    json_data = json.dumps(json_dict)
    post_data = json_data.encode('utf-8')
    headers = {}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, post_data, headers)
    res = urllib.request.urlopen(req)
    res2 = res.read().decode('utf-8')
    permiss = json.loads(res2)
    return permiss;

def comm_dl(id_num):
   # url = "http://127.0.0.1:8000/api/files/"
    url = "https://sleepy-hamlet-6170.herokuapp.com/api/files/"
    json_dict = {'id': id_num}
    json_data = json.dumps(json_dict)
    post_data = json_data.encode('utf-8')
    headers = {}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, post_data, headers)
    res = urllib.request.urlopen(req)
    res2 = res.read().decode('utf-8')
    my_list = json.loads(res2)
    return my_list

def comm_get(id_num):
    '''url = "http://127.0.0.1:8000/api/reports/"
    json_dict = {'id_num': id_num}
    json_data = json.dumps(json_dict)
    post_data = json_data.encode('utf-8')
    headers = {}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, post_data, headers)
    res = urllib.request.urlopen(req)
    res2 = res.read().decode('utf-8')'''
    my_list = []
    my_list.append("text.txt")
    my_list.append("text2.txt")
    return my_list
