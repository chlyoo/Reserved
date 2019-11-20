class User(object):
	id=""
	stuid=""
	#name=""
	rdate="2019-11-19"
	rstarttime="0800"
	rendtime="1000"
	pid=""
	membergrade=""
	point=""
	coworker=""
	progress=""

class Equip(object):
	#equipname=""
	equipid=""
	spec=""
	usingcount=""	



class UserManager(object):
	pass


class EquipManager(object):
	'''
장비 예약과 관련한 것? 
CRUD, 예약및취소, 
	'''
	equip_create
	equip_read
	equip_update
	equip_delete
	time_reserve	#장비예약취소가능 시간
	time_cancel



class History():
	pass	

class reservestat(object):
	
'''
장비신청상황
학생id, 장비 ID, 신청날짜, 장비사용날짜, 사용금액  
'''
	stat={}

	def addstat():
		pass