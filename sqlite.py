import sqlite3

class DataBase():
    def __init__(self):
        self.db_name = 'conf.db'
        self.table_name = 'param'
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.baseUrl = 'http://www.17989.com/'
        self.url = 'http://www.17989.com/xiaohua/1.htm'
        self.BodyPattern = '<pre>.*?</pre>'
        self.UrlPattern = '<a href=(\".*?\") class=\"next\">'
    def query_data(self):
        res = self.cur.execute('select * from ? where base=?', (self.db_name, self.baseUrl))
        print(res)
        return res
    def insert_data(self):
        self.cur.execute('INSERT INTO PARAM VALUES (?,?,?,?,?,?)', (1,baseUrl,url,BodyPattern,UrlPattern,trunkPattern))

if __name__ == '__main__':
    mydb = DataBase()
    mydb.query_data()
