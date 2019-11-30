from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 20191028
from . import login_manager, db

# 20191108
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
# 20191112
from flask_login import AnonymousUserMixin

# 20191122
from datetime import datetime


class Equip(object):
	equipid = ""
	equipname = ""
	spec = ""
	usingcount = 0
	rdate = dict()

	def __init__(self, equipid,equipname):
		self.equipid=equipid
		self.equipname=equipname


class Progress(object):
	taskid:0
	userid = ""
	equipid = ""
	rdate = dict()
	estimated_end_time = "0000-00-00 00:00"
	estimated_price = -1
	confirmed = False
	paid = False
	complete = False

	def __init__(self, equipid, rdate,id):
		self.equipid = equipid
		self.rdate = rdate
		self.id = id

		# 클래스 생성시 equip id rdate입력하면 taskid업데이트 및 초기화 진행
		col_progress = db.get_collection('progress')
		try:
			self.totcount = col_progress.find_one(sort=[("taskid", -1)])['taskid']
		except:
			self.totcount = 0
		col_progress.insert_one({'taskid' : self.totcount + 1, 'user_id':
			id, 'equip_id': equipid, 'rdate': rdate, 'estimated_end_time': '0000 - 00 - 00 00:00:00', 'estimated_price':-1, 'confirmed':False, 'paid':False, 'complete':False})

	def generate_token(self, expiration=False):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.equipid}).decode('utf-8')
	def confirm(self):
		pass  # input data by admin and change confirm status mail to user

	def complete(self):
		pass  # 예상 작업시간 중간중간에 도달하면 mail to user and Admin

	def to_dict(self):
		dict_user = {
				'taskid'       : self.totcount+1,
				'userid'     : self.userid,
				'equipid'        : self.equipid,
			### 20191112
				'rdate'      : self.rdate,
			'estimated_end_time'  :self.estimated_end_time,
			####
				'estimated_price': self.estimated_price,
				'confirmed'    : self.confirmed,
			### 20191122
				'paid' : self.paid,
				'complete'    : self.complete
		}
		return dict_user

	def from_dict(self, data):
		if data is not None:
			self.taskid = data['taskid']
			self.userid = data['userid']
			self.equipid = data['equipid']
			### 20191112
			self.rdate = data['rdate']
			###
			self.estimated_end_time = data['estimated_end_time']
			self.estimated_price = data['estimated_price']
			### 20191122
			self.confirmed = data['confirmed']
			self.paid = data['paid']
			self.complete=data['complete']
			
class User(UserMixin, object):
	id = ""
	username = "cbchoi"
	role = None  # 20191112
	password_hash = ""
	confirmed = False
	member_since = ""
	last_seen = ""
	membergrade = 0
	point = 0

	def __init__(self, email, username, password, stuid):
		self.id = email
		self.username = username
		self.password = password
		self.stuid = stuid

		###
		#20191112
		collection = db.get_collection('roles')
		if self.id == current_app.config['ADMIN']:
			self.role = Role('Administrator', 0xff)
		else:
			result = collection.find_one({'default':True})
			self.role = Role(result['name'], result['permission'], result['default'])
		###
		 
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	 
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@login_manager.user_loader
	def load_user(user_id):
		collection = db.get_collection('users')
		results = collection.find_one({'id':user_id})
		if results is not None:
			user = User(results['id'], "", "", "")  # 20191112
			user.from_dict(results)
			return user
		else:
			return None

	##### 20191108
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		collection = db.get_collection('users')
		results = collection.update_one({'id':self.id}, {'$set':{'confirmed':self.confirmed}})
		return True
    #####

	###
    # 20191112
	def can(self, permissions):
		return self.role is not None and (self.role.permission & permissions) == permissions
    
	def is_administrator(self):
		return self.can(Permission.ADMINISTATOR)
	###

	###
	# 20191122
	def ping(self):
		self.last_seen = datetime.utcnow()
		collection = db.get_collection('users')
		results = collection.update_one({'id':self.id}, {'$set':{'last_seen':self.last_seen}})

# 20191028
	def to_dict(self):
		dict_user = {
				'id'           : self.id,
				'username'     : self.username,
				'stuid'        : self.stuid,
			### 20191112
				'role_id'      : self.role.name,
			'role_permission'  :self.role.permission,
			####
				'password_hash': self.password_hash,
				'confirmed'    : self.confirmed,
			### 20191122
				'member_since' : self.member_since,
				'last_seen'    : self.last_seen
		}
		return dict_user

	def from_dict(self, data):
		if data is not None:
			self.id = data['id']
			self.username = data['username']
			self.stuid = data['stuid']
			### 20191112
			self.role = Role(data['role_id'], data['role_permission'])
			###
			self.password_hash = data['password_hash']
			self.confirmed = data['confirmed']
			### 20191122
			self.member_since = data.get('member_since')
			self.last_seen = data.get('last_seen')

###
# 20191112
class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False
    
	def is_administrator(self):
		return False

class Role(object):
	name = ""
	permission = 0
	default = False

	def __init__(self, name, permission, default=False):
		Role.name = name
		Role.permission = permission
		Role.default = default

	@staticmethod
	def insert_roles():
		roles = {
		'User': (Permission.FOLLOW |
				 Permission.COMMENT |
				 Permission.WRITE_ARTICLES, True),
		'Moderator': (Permission.FOLLOW |
					  Permission.COMMENT |
					  Permission.WRITE_ARTICLES|
					  Permission.MODERATE_COMMENTS, False),
		'Administrator': (0xff, False)
		}

		collection = db.get_collection('roles')
		for k, v in roles.items():
			result = collection.find_one({'name':k})
			role = Role(k, v[0], v[1])			
			
			if result is not None:
				result = collection.update_one({'name':k}, {'$set':role.to_dict()})
			else:
				collection.insert_one(role.to_dict())
				

	def to_dict(self):
		dict_role = {
			'name': self.name, 
			'permission': self.permission,
			'default': self.default
		}
		return dict_role

	def from_dict(self, data):
		if data is not None:
			self.name = data['name']
			self.permission = data['permission']
			self.default = data['default']
			

class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTATOR = 0x80
###