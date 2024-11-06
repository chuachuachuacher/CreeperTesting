from flask import Flask, render_template, request, redirect, url_for
import pymysql
from CreeperBaseClass import CreeperBase, operateDb, tableName
from main import LinksNet

app = Flask(__name__)

def connect_db():
    return pymysql.connect(
        host="192.168.1.129",
        user="root",
        password="root",
        charset="utf8",
        database="py_creeper0",
        port=3306
    )

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    url = request.form.get('url')
    if url:
        Turl = LinksNet(url)
        tdata = Turl.getData()
        if tdata:
            operateDb(tdata, tableName(url))
        return redirect(url_for('result', table_name=tableName(url)))
    return redirect(url_for('start'))

@app.route('/result')
def result():
    table_name = request.args.get('table_name')
    if not table_name:
        return "——————————————出错了，没有这个表名lol"
    
    connection = connect_db()
    cursor = connection.cursor()
    sql = f"SELECT id, info, link FROM {table_name};"
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()
    
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)