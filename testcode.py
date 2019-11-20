import pymongo
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('Reserved')

col_user = db.get_collection('user')
col_equip = db.get_collection('equip')
col_progress = db.get_collection('progress')

col_user.delete_many({})
col_equip.delete_many({})
col_progress.delete_many({})

col_user.insert_many([{'id':"21300259@handong.edu",'stuid':21300259, 'name':"peterlyoo", 'membergrade':5,'point':10},
{'id':"21300704@handong.edu",'stuid':21300704, 'name':"jino", 'membergrade':5,'point':15},
{'id':"21400259@handong.edu",'stuid':21400259, 'name':"nosummer", 'membergrade':4,'point':20},
{'id':"21500259@handong.edu",'stuid':21500259, 'name':"unknown", 'membergrade':3, 'point':30}])
col_equip.insert_many([{'equipid':'e20190001', 'equipname':'printerxz', 'spec':'No', 'usingcount':1},
{'equipid':'e20190003', 'equipname':'printeryy', 'spec':'Yes', 'usingcount':3},
{'equipid':'e20190002', 'equipname':'printerCBC', 'spec':'No', 'usingcount':4},
{'equipid':'e20190005', 'equipname':'printerD', 'spec':'Yes', 'usingcount':5}])


current_user = {'id':"21300259@handong.edu",'stuid':21300259, 'name':"peterlyoo", 'membergrade':5,'point':10}

results = col_user.find()
[print(result) for result in results] 

results = col_equip.find()
[print(result) for result in results]


# initiate 3d printing task

# get total count of the tasks
tot_count = …

col_progress = db.get_collection(‘progress’)
col_progress.insert_one(
 {‘task_id’:tot_count+1, ‘user_id’:current_user[‘id’], ‘equip_id’: ‘-’, ‘rdate’:’’, ‘estimated_end_time’:’0000-00-00 00:00:00’, ‘estimated_price’:-1, ‘confirmed’:False, ‘paid’:False, ‘complete’:False})

# Flask-Mail로 관리자에게 메일 보냄
send_email(user.id, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
