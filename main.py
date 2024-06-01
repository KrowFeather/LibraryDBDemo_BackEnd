from flask import Flask, jsonify
from flask_cors import CORS
from pymysql import *

app = Flask(__name__)
CORS(app)
conn = None
cursor = None
try:
    conn = connect(host='localhost', port=3306, user='root', password='123456', database='db_work')
    cursor = conn.cursor()
except Exception as e:
    print(e)


@app.route('/Logincheck/<usern>&&<passw>')
def logincheck(usern, passw):
    print("logincheck:", usern, passw)
    try:
        sql = f"SELECT * FROM user_password WHERE userid = \"{usern}\" AND password = \"{passw}\";"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        if len(result) > 0:
            return "Yes"
        else:
            return "No"
    except Exception as e:
        print(e)
        return "No"


@app.route('/regcheck/<usern>&&<passw>&&<qtype>&&<answer>')
def regcheck(usern, passw, qtype, answer):
    print("regcheck:", usern, passw, qtype, answer)
    try:
        sql = f"insert user_password values(\"{usern}\",\"{passw}\",\"{qtype}\",\"{answer}\")"
        cursor.execute(sql)
        return "Yes"
    except Exception as e:
        return "No"


@app.route('/regcheckNoques/<usern>&&<passw>')
def regcheckNoques(usern, passw):
    print("regcheck:", usern, passw)
    try:
        sql = f"insert user_password(userid,password) values(\"{usern}\",\"{passw}\")"
        cursor.execute(sql)
        return "Yes"
    except Exception as e:
        print(e)
        return "No"


@app.route('/getAllBookInfo')
def getAllBookInfo():
    try:
        sql = f"select * from bookinf"
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            print(item)
            res.append(
                {"bookid": item[0], "bookname": item[1], "booktype": item[2], "bookauthor": item[3], "total": item[4],
                 "borrowed": item[5]})
        return jsonify(res)
    except Exception as e:
        return 'failed'


@app.route('/addNewBook/<bookid>&&<bookname>&&<booktype>&&<bookauthor>&&<total>')
def addNewBook(bookid, bookname, booktype, bookauthor, total):
    print("addNewBook:", bookid, bookname, booktype, bookauthor, total)
    try:
        sql = f"insert bookinf values(\"{bookid}\",\"{bookname}\",\"{booktype}\",\"{bookauthor}\",\"{total}\",\"0\")"
        cursor.execute(sql)
        print(cursor.fetchall())
        return "success"
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/delBooks/<bookid>')
def delBooks(bookid):
    print('delbook:' + bookid)
    try:
        sql = f"delete from bookinf where bookid = \"{bookid}\" "
        cursor.execute(sql)
        return "success"
    except Exception as e:
        return 'failed'


@app.route('/alterBookInfo/<bookid>&&<bookname>&&<booktype>&&<bookauthor>&&<total>')
def alterBookInfo(bookid, bookname, booktype, bookauthor, total):
    print('alterBookInfo:', bookid, bookname, booktype, bookauthor, total)
    try:
        sql = f"update bookinf set bookname = \"{bookname}\",booktype = \"{booktype}\",bookauthor = \"{bookauthor}\",total = \"{total}\" where bookid = \"{bookid}\" "
        cursor.execute(sql)
        return "success"
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/getAllBorrowInfo')
def getAllBorrowInfo():
    try:
        sql = "select no,userid,bookid,DATE_FORMAT(borrowtime, '%Y-%m-%d'),DATE_FORMAT(returntime, '%Y-%m-%d') from borrow where returntime is null"
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            print(item)
            res.append(
                {"no": item[0], "userid": item[1], "bookid": item[2], "borrowtime": item[3], "returntime": item[4]})
        print(res)
        return jsonify(res)
    except Exception as e:
        return 'failed'


@app.route('/addNewBorrow/<userid>&&<bookid>&&<borrowtime>')
def addNewBorrow(userid, bookid, borrowtime):
    print("addNewBorrow:", userid, bookid, borrowtime)
    try:
        sql = f"insert into borrow (userid,bookid,borrowtime) values(\"{userid}\",\"{bookid}\",\"{borrowtime}\")"
        cursor.execute(sql)
        sql = f"update bookinf set borrowed=borrowed+1 where bookid = \"{bookid}\""
        cursor.execute(sql)
        print(cursor.fetchall())
        return "success"
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/delBorrow/<no>')
def delBorrow(no):
    print('delborrow:' + no)
    try:
        sql = f"delete from borrow where no = \"{no}\" "
        cursor.execute(sql)
        return "success"
    except Exception as e:
        return 'failed'


@app.route('/returnBorrow/<no>&&<returntime>')
def returnBorrow(no, returntime):
    print('returnBorrow:', no, returntime)
    try:
        sql = f"update borrow set returntime= \"{returntime}\" where no = \"{no}\" "
        cursor.execute(sql)
        sql = f"update bookinf set borrowed=borrowed-1 where bookid in (select bookid from borrow where no = \"{no}\")"
        cursor.execute(sql)
        return "success"
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/getAllBorrowInfoFiltered/<userid>&&<bookid>&&<borrowtime>')
def getAllBorrowInfoFiltered(userid, bookid, borrowtime):
    print('getAllBorrowInfoFiltered:', userid, bookid, borrowtime)
    try:
        sql = f"select no,userid,bookid,DATE_FORMAT(borrowtime, '%Y-%m-%d'),DATE_FORMAT(returntime, '%Y-%m-%d') from borrow where returntime is null and userid = \"{userid}\" and bookid = \"{bookid}\" and borrowtime = \"{borrowtime}\""
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            print(item)
            res.append(
                {"no": item[0], "userid": item[1], "bookid": item[2], "borrowtime": item[3], "returntime": item[4]})
        print(res)
        return jsonify(res)
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/getBorrowRankByDay')
def getBorrowRankByDay():
    print('here')
    try:
        sql = "select  DATE_FORMAT(borrowtime, '%Y-%m-%d'),count(*) from borrow group by borrowtime"
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            res.append({"borrowtime": item[0], "cnt": item[1]})
        print(res)
        return jsonify(res)
    except Exception as e:
        return 'failed'


@app.route('/getMostPopularBooks')
def getMostPopularBooks():
    print('here')
    try:
        sql = "select bookid,count(*) from borrow group by bookid order by count(*) desc"
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            res.append({"bookid": item[0], "cnt": item[1]})
        print(res)
        return jsonify(res)
    except Exception as e:
        return 'failed'


@app.route('/getMostWelcomeUser')
def getMostWelcomeUser():
    print('here')
    try:
        sql = "select userid,count(*) from borrow group by userid order by count(*) desc"
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            res.append({"userid": item[0], "cnt": item[1]})
        print(res)
        return jsonify(res)
    except Exception as e:
        return 'failed'


@app.route('/createNewBorrow/<bookid>&&<userid>&&<date>')
def createNewBorrow(bookid, userid, date):
    print('createNewBorrow', bookid, userid, date)
    try:
        sql = f"insert into borrow(userid,bookid,borrowtime) values(\"{userid}\",\"{bookid}\",\"{date}\")"
        cursor.execute(sql)
        sql = f"update bookinf set borrowed = borrowed+1 where bookid =\"{bookid}\""
        cursor.execute(sql)
        return "success"
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/getAllUserBorrow/<userid>')
def getAllUserBorrow(userid):
    try:
        sql = f"select no,bookname,bookauthor,DATE_FORMAT(borrowtime, '%Y-%m-%d'),DATE_FORMAT(returntime, '%Y-%m-%d') from borrow,bookinf where userid=\"{userid}\" and borrow.bookid=bookinf.bookid order by borrowtime"
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            print(item)
            res.append(
                {"no": item[0], "bookname": item[1], "bookauthor": item[2], "borrowtime": item[3],
                 "returntime": item[4]})
        print(res)
        return jsonify(res)
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/changePassword/<oldP>&&<newP>&&<userid>')
def changePassword(oldP, newP, userid):
    print('changePassword', oldP, newP, userid)
    try:
        sql = f"select password from user_password where userid=\"{userid}\""
        cursor.execute(sql)
        rr = cursor.fetchall()
        res = ''
        for item in rr:
            res = item[0]
        print(res)
        if (oldP != res):
            return 'wrong'
        else:
            sql = f"update user_password set password= \"{newP}\" where userid=\"{userid}\""
            cursor.execute(sql)
        return 'success'
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/delAccount/<password>&&<userid>')
def delAccount(password, userid):
    print('changePassword', password, userid)
    try:
        sql = f"select password from user_password where userid=\"{userid}\""
        cursor.execute(sql)
        rr = cursor.fetchall()
        res = ''
        for item in rr:
            res = item[0]
        print(res)
        if (password != res):
            return 'wrong'
        else:
            sql = f"delete from user_password where userid=\"{userid}\""
            cursor.execute(sql)
        return 'success'
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/getAllBookCanBorrow')
def getAllBookCanBorrow():
    try:
        sql = f"select bookid,bookname,booktype,bookauthor,(total-borrowed) as rem from bookinf where total-borrowed>0"
        cursor.execute(sql)
        res = []
        rr = cursor.fetchall()
        for item in rr:
            print(item)
            res.append(
                {"bookid": item[0], "bookname": item[1], "booktype": item[2], "bookauthor": item[3], "rem": item[4]})
        return jsonify(res)
    except Exception as e:
        return 'failed'


@app.route('/changeSeQtoDefault/<userid>')
def changeSeQtoDefault(userid):
    try:
        sql = f"update user_password set question=null and answer=null where userid=\"{userid}\""
        cursor.execute(sql)
        return "success"
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/changeSeQ/<userid>&&<question>&&<answer>')
def changeSeQ(userid, question, answer):
    print('changeSeQ:', userid, question, answer)
    try:
        sql = f"update user_password set question=\"{question}\" and answer=\"{answer}\" where userid=\"{userid}\""
        cursor.execute(sql)
        return "success"
    except Exception as e:
        print(e)
        return 'failed'


@app.route('/getSeQ/<usern>')
def getSeQ(usern):
    print("getSeQ", usern)
    try:
        sql = f"SELECT question FROM user_password WHERE userid = \"{usern}\""
        cursor.execute(sql)
        rr = cursor.fetchall()
        res = ''
        for item in rr:
            res = item[0]
        print(res)
        if res is None:
            return "NULL"
        return res
    except Exception as e:
        print(e)
        return "No"


@app.route('/confirmSeQ/<usern>&&<answer>')
def confirmSeQ(usern, answer):
    print("confirmSeQ", usern, answer)
    try:
        sql = f"SELECT answer FROM user_password WHERE userid = \"{usern}\""
        cursor.execute(sql)
        rr = cursor.fetchall()
        res = ''
        for item in rr:
            res = item[0]
        print(res)
        if answer == res:
            sql = f"SELECT password FROM user_password WHERE userid = \"{usern}\""
            cursor.execute(sql)
            rr = cursor.fetchall()
            res = ''
            for item in rr:
                res = item[0]
            print(res)
            return res
        else:
            return "failed"
    except Exception as e:
        print(e)
        return "No"


if __name__ == '__main__':
    app.run()
