" Item Database"

import sqlite3
import os

class itemDatabase():
	""" Number of Columns: col_names """
	def __init__(self):
		self.name="itemDatabase"

		if os.path.isfile(self.name+".db"):
			self.itemDatabase = sqlite3.connect('itemDatabase.db' ,check_same_thread = False)
			self.cursor = self.itemDatabase.execute('select * from items')
			self.col_names = [self.cursor.description[i][0] for i in range(1, len(self.cursor.description))]
			return

		self.itemDatabase= sqlite3.connect('itemDatabase.db' ,check_same_thread = False )
		self.cursor = self.itemDatabase.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS items (itemName TEXT PRIMARY KEY, itemCategory TEXT, itemPrice TEXT, \
			itemStock INT, itemDescription TEXT, postalCodeBarangay TEXT, itemIndex INT)")
		self.itemDatabase.commit()

	def add_item(self, name, category, price, stock, description, postalCodeBarangay):
		try:
			self.cursor.execute("SELECT itemIndex from items")
			temp_index = self.cursor.fetchall()
			num_index=len(temp_index)
			query = "INSERT INTO items (itemName, itemCategory, itemPrice, itemStock, itemDescription, postalCodeBarangay, itemIndex) VALUES(?,?,?,?,?,?,?)"
			data = (name, category, price, stock, description, postalCodeBarangay, num_index)
			self.cursor.execute(query, data)
			self.itemDatabase.commit()
			return True
		except:
			return False

	def edit_data(self,itemName,target_data,value):
		try:
			query = "UPDATE items SET "
			query += target_data
			query += "=? WHERE itemName =? "
			data=(value, itemName)
			self.cursor.execute(query, data)
			self.itemDatabase.commit()
		except:
			pass

	def delete_row(self,item):
		try:
			self.cursor.execute("DELETE FROM items WHERE itemName=?", (item,))
			self.itemDatabase.commit()
		except:
			pass

	def getAll_items(self):
		query = "SELECT itemName"
		for i in self.col_names:
			query += ", "+ i
		query += "  FROM items"
		self.cursor.execute(query)
		temp_log = self.cursor.fetchall()
		self.all_log=[]
		temp=[]
		for entry in temp_log:
			for detail in entry:
				temp.append(detail)
			self.all_log.append(temp)
			temp=[]
		return self.all_log

	def search_item(self, inquiry, column):
		try:
			self.getAll_items()
			self.search_result=[]
			for i_list in self.all_log:
				if inquiry.lower() in i_list[column].lower():
					self.search_result.append(i_list)
			return self.search_result
		except:
			pass

	def search_item_user(self, username):
		try:
			self.getAll_items()
			user_result = []
			for i_list in self.all_log:
				userExtracted = i_list[0].split(',')
				print(userExtracted)
				if username == userExtracted[0]:
					user_result.append(i_list)
			return user_result
		except:
			pass
