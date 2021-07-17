
import sqlite3

class userDatabase():
	def __init__(self):
		self.name="userDatabase"
		self.userDatabase= sqlite3.connect('userDatabase.db',check_same_thread = False)
		self.cursor = self.userDatabase.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS users (accountName TEXT PRIMARY KEY, password TEXT, isBuyer BOOL, \
			userInformation TEXT, userIndex INT)")
		self.userDatabase.commit()

	def add_user(self, new_name, new_password, isBuyer, userInformation):
		try:
			self.cursor.execute("SELECT userIndex from users")
			temp_index=self.cursor.fetchall()
			new_userIndex = len(temp_index)
			self.name = str(new_name)
			self.password= str(new_password)
			self.cursor.execute("INSERT OR IGNORE INTO users(accountName, password, isBuyer, userInformation, userIndex)\
			VALUES(:accountName,:password,:isBuyer,:userInformation,:userIndex)",{'accountName':self.name,'password':self.password,'isBuyer':isBuyer,\
				'userInformation':userInformation,'userIndex':new_userIndex})
			self.userDatabase.commit()
		except:
			pass

	def login(self,name,password):
		self.cursor.execute("SELECT * FROM users")
		all_login = self.cursor.fetchall()
		for i in range(len(all_login)):
			if(all_login[i][0] == name and all_login[i][1] == password):
				return all_login[i]
		return None
