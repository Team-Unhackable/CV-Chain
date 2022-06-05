import requests
import time
import leancloud
import json
import os

def getCacheBusinessListLen():
    leancloud.init("", "")
    bList = []
    query = leancloud.Query('UserData')
    query.equal_to('isAdded', "f")
    user_list = query.find()
    return len(user_list)
  
while True:
    URL = "http://127.0.0.1:5002/block_data"
    if (getCacheBusinessListLen()>0):
        r = requests.get(url = URL)
        print("Get")
        
        path = "/var/www/html/blockchain/data"
        list = os.listdir(path)
        number_files = len(list)

        for i in range(2, number_files+1):
            path = "/var/www/html/blockchain/data/" + str(i)
            subdata_file = os.listdir(path)
            if len(subdata_file) > 0:
                index = int(max(subdata_file)[0]) - 1
                num = {'num': index}
                json_object = json.dumps(num, indent = 1)
                with open("./count/" + str(i) + ".json", "w") as outfile:
                    outfile.write(json_object)
        
    else:
        print("Wait")
    time.sleep(5)
