import datetime
import json
import hashlib
import os
from flask import Flask, jsonify
import leancloud

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_blockchain(proof=1, previous_hash='0', UID='0', index='1')

    def create_blockchain(self, proof, previous_hash, UID, index):
        #index_1 = os.path.splitext("./data/" + str(UID) + "/" + str(index) + ".json")[0]
        block = {
            #'index': int(index_1[-1:]) + 1,
            'index': int(index) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        last_block = self.chain[-1]
        return last_block

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):  # generate a hash of an entire block
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):  # check if the blockchain is valid
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            current_proof = block['proof']
            hash_operation = hashlib.sha256(
                str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


app = Flask(__name__)

blockchain = Blockchain()

# def cache_read():
#     url = "https://skyproton.org/save/cache.txt"
#     file = urllib.request.urlopen(url)
#     name = file.readlines()[0].decode("utf-8")
#     name = name.strip('\n')
#     return name

def getCacheUserNameList():
    leancloud.init("", "")
    list = []
    query = leancloud.Query('UserData')
    query.equal_to('blockIndex', "")
    query.descending('createdAt')
    user_list = query.find()
    for user in user_list:
        list.append(user.get('nameOnBlk'))
        user.save()
    # if len(user_list) > 0:
    return list


def updateUserNameIndex(inUserName, inIndex):
    leancloud.init("", "")
    query = leancloud.Query('UserData')
    query.equal_to('username', inUserName)
    flag = False
    if (query.count()>0):
        user_list = query.find()
        # for user in user_list:
        user = user_list[0]
        if (user.get('username') == inUserName and user.get('blockIndex') == ""):
            user.set('blockIndex',str(inIndex))
            user.save()
            flag = True
    return flag

def hasIndex(inUserName):
    leancloud.init("", "")
    query = leancloud.Query('UserData')
    query.equal_to('username', inUserName)
    flag = False
    if (query.count()>0):
        user_list = query.find()
        user = user_list[0]
        if (user.get('blockIndex') != ""):
            flag = True
    return flag

def getUserName(inRealName):
    leancloud.init("", "")
    outName = ''
    flag = False
    query = leancloud.Query('UserData')
    query.equal_to('nameOnBlk', str(inRealName))
    if (query.count()>0):
        user_list = query.find()
        for user in user_list:
            if (user.get('nameOnBlk') == inRealName):
                outName = user.get('username')
                flag = True
    if (flag):
        return outName
    else:
        return flag

def getCacheBusinessList():
    leancloud.init("", "")
    bList = list()
    query = leancloud.Query('UserData')
    query.equal_to('isAdded', "f")
    query.descending('createdAt')
    user_list = query.find()
    for user in user_list:
        inList = list()
        inList.append(user.get('UID'))
        inList.append(user.get('companyType'))
        inList.append(user.get('companyName'))
        inList.append(user.get('DegreeOrJob'))
        inList.append(user.get('ClassOrYear'))
        bList.append(inList)
        user.set("isAdded","t")
        user.save()
    return bList

@app.route('/block_data', methods=['GET'])
def block_data():
    inNameList = getCacheBusinessList()
    while (len(inNameList)>0):
        inName = inNameList.pop()
        UID = inName[0]
        inType = inName[1]
        inBName = inName[2]
        inData_1 = inName[3]
        inData_2 = inName[4]
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)

        path = "/var/www/html/blockchain/data/" + str(UID)
        subdata_file = os.listdir(path)
        if len(subdata_file) > 0:
            index = max(subdata_file)[0]
        else:
            index = 1

        block = blockchain.create_blockchain(proof, previous_hash, UID, index)
        response = {'type': inType,
                    'data': {
                        'Name_of_Work_or_Study': inBName,
                        'data_1': inData_1,
                        'data_2': inData_2,
                    },
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash']}
        
        # username = getUserName(inName)
        # if (not hasIndex(username)):
        #     updateUserNameIndex(username, block['index'])

        json_object = json.dumps(response, indent = 5)
    
        with open("./data/" + str(UID) + "/" + str(block['index']) + ".json", "w") as outfile:
            outfile.write(json_object)

        #return jsonify(response), 200
    return jsonify(response = {'data': None,
                    'index': None,
                    'timestamp': None,
                    'proof': None,
                    'previous_hash': None}), 200


app.run(host='0.0.0.0', port=5002)


