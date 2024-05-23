import mysql.connector

class DBConnector:
    def __init__(self):
            self.host="localhost"
            self.user="root"
            self.password=""
            self.database="wandering-wisdom-db"

            self.mydb = mysql.connector.connect(
                host= self.host,
                user= self.user,
                password= self.password,
                database= self.database
            )

            self.DBhandler = self.mydb.cursor()

    def insertUser(self, fname, lname, email, phoneNumber, passWord):
        sql = "INSERT INTO users (fname, lname, email, phone, password) VALUES (%s, %s, %s, %s, %s)"
        val = (fname, lname, email, phoneNumber, passWord)
        self.DBhandler.execute(sql,val)
        self.mydb.commit()
        
        # print(self.DBhandler.rowcount, "record inserted.")

    def selectUserPass(self, email):
        self.DBhandler.execute(f"select * from users where email='{email}'")
        data = self.DBhandler.fetchone()
        # print(data)
        return data