import requests
import time
import leancloud

def getCacheUserNameListLen():
    leancloud.init("", "")
    list = []
    query = leancloud.Query('UserData')
    query.equal_to('blockIndex', "")
    user_list = query.find()
    return len(user_list)
  
while True:
    URL = "http://127.0.0.1:5001/block_data"
    if (getCacheUserNameListLen()>0):
        r = requests.get(url = URL)
        print("Get")
    else:
        print("Wait")
    time.sleep(5)
