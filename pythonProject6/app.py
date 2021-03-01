from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/reviews', methods=['GET'])
def listing():

    songs = list(db.music.find({}, {'_id': False}))

    return jsonify({'all_song':songs})

## API 역할을 하는 부분
@app.route('/reviews', methods=['POST'])
def saving():

    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    singer_receive = request.form['singer_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    song = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']


    doc = {
        'singer':singer_receive,
        'song':song,
        'url':url_receive,
        'comment':comment_receive,
        'image':image

    }

    db.music.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)