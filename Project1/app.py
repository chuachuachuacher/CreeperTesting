from flask import Flask, render_template, jsonify, send_file
import pymysql
import base64
import io

app = Flask(__name__)

# 数据库配置
config = {
    'host': '192.168.150.20',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'Creepers',
    'charset': 'utf8mb4',
    'autocommit': True
}

# 数据库连接函数
def get_db_connection():
    return pymysql.connect(**config)

# 将二进制图片转换为 Base64
def convert_binary_to_base64(binary_data):
    return base64.b64encode(binary_data).decode('utf-8')

# 主页：展示经典电影列表
@app.route('/')
def classic_movies():
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id, name, simage FROM ClassicMovies")
            movies = cursor.fetchall()
            # 将二进制图片数据转换为 Base64
            for movie in movies:
                movie['simage'] = f"data:image/jpeg;base64,{convert_binary_to_base64(movie['simage'])}"
    finally:
        connection.close()
    return render_template('classic.html', movies=movies)

# 详情页：展示经典电影详细信息
@app.route('/details/<int:movie_id>')
def movie_details(movie_id):
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT info, ename, about, bimage
                FROM ClassicMoviesDetails
                WHERE id = %s
            """, (movie_id,))
            movie = cursor.fetchone()
            if movie:
                movie['bimage'] = f"data:image/jpeg;base64,{convert_binary_to_base64(movie['bimage'])}"
    finally:
        connection.close()
    return render_template('classicDetail.html', movie=movie)

# 热门电影主页：展示热门电影列表
@app.route('/hot')
def hot_movies():
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id, name, simage FROM HotMovies")
            movies = cursor.fetchall()
            # 将二进制图片数据转换为 Base64
            for movie in movies:
                movie['simage'] = f"data:image/jpeg;base64,{convert_binary_to_base64(movie['simage'])}"
    finally:
        connection.close()
    return render_template('hot.html', movies=movies)

# 热门电影详情页：展示热门电影详细信息
@app.route('/hotdetails/<int:movie_id>')
def hot_movie_details(movie_id):
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT info, ename, about, bimage, ticketUrl
                FROM HotMoviesDetails
                WHERE id = %s
            """, (movie_id,))
            movie = cursor.fetchone()
            if movie:
                movie['bimage'] = f"data:image/jpeg;base64,{convert_binary_to_base64(movie['bimage'])}"
    finally:
        connection.close()
    return render_template('hotDetail.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
