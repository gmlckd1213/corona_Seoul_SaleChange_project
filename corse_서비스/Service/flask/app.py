from os import name
from posix import NGROUPS_MAX
from flask import Flask, redirect,jsonify, request, render_template, url_for
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text # db와 연결하기 위하여 사용
import simplejson as json # flask에서 jsonify 처리할때 deciaml 타입의 객체형태의 숫자를 직렬화 할때 문제가 생겨서 import함
from pandas import json_normalize # dict타입을 df로 바로 처리
from dotenv import load_dotenv # 서버의 설정을 .env 파일로 처리하여 코드 자체에 문제되는 내용이 안보이게 처리
import os
import correlation_between_corona_and_sales as c
import making_wordcloud_data as m

load_dotenv()

app = Flask(__name__)
ID = os.environ.get('DB_ID')
PASSWORD = os.environ.get('DB_PASSWORD')
ADDRESSS = os.environ.get('DB_ADDRESSS')
PORT = os.environ.get('DB_PORT')
DATABASE = os.environ.get('DB_DATABASE')

database = create_engine(f"mariadb+mariadbconnector://{ID}:{PASSWORD}@{ADDRESSS}:{PORT}/{DATABASE}")

app.database = database
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/get')
def make_read_exel():
    quarter=request.args.get('data')
    #quarter upjong dropdown

    params = {'region': quarter}
    row = app.database.execute(text("""
            SELECT sector
            FROM sales
            where region = :region
    """), params).fetchall()
    com_list = [i[0] for i in row]
    com_list = list(set(com_list))
    com_list.insert(0, '선택하세요')

    return render_template('quarter.html', quarter=quarter, com_list=com_list)


@app.route("/get_data", methods = ["POST"])
def get_data():
    # quarter로 지역 type으로 업종을 받아옴
    quarter = request.json["quarter"]
    type = request.json["type"]
    params = {'region': quarter, 'type': type}
    #sql문에서 위에 있는 params를 통하여 quarter와 type 정보를 들고온다.
    row1 = app.database.execute(text("""
            SELECT SUM(qua_rev), year_mon, SUM(store)
            FROM sales 
            WHERE region = :region and sector = :type
            Group by year_mon
    """), params).fetchall()        
    row1 = {'result': [dict(row) for row in row1]}
    df = json_normalize(row1['result']) #Results contain the required data
    #df를 원하는 구간 만큼 슬라이싱
    result2 = df.iloc[:,0]
    result2 = result2.tolist()
    result3 = df.iloc[:,2]
    result3 = result3.tolist()


    row2 = app.database.execute(text("""
            SELECT *
            FROM patient 
            WHERE region = :region
    """), params).fetchall()



    row2 = {'result': [dict(row) for row in row2]}
    df2 = json_normalize(row2['result']) #Results contain the required data
    
    result1 = df2.values
    result1 = list(*result1)
    result1 = result1[1:7]

    if str(type)=='선택하세요':
        return {'corona':result1, 'price':[1,1,1,1,1,1,1,1,1,1] , 'store':[0,0,0,0,0,0,0,0,0,0] }

    return {"corona": result1, "price": result2 , 'store': result3 }

@app.route('/get_data2', methods=['POST'])
def get_data2():
    quarter = request.json['quarter']
    type = request.json['type']
    day = request.json['day']
    params = {'region': quarter}
    row2 = app.database.execute(text("""
            SELECT *
            FROM patient 
            WHERE region = :region
    """), params).fetchall()


    row2 = {'result': [dict(row) for row in row2]}

    df2 = json_normalize(row2['result']) #Results contain the required data
    
    result1 = df2.values
    result1 = list(*result1)
    result1 = result1[1:7]


    if str(day) == '요일 선택' :
        return {'corona': result1, 'week' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    params = {'region': quarter, 'type': type, 'day': day}
    #sql문에서 위에 있는 params를 통하여 quarter와 type 정보를 들고온다.
    row1 = app.database.execute(text("""
            SELECT mon_sale , tue_sale, wen_sale, thur_sale, fri_sale, sat_sale, sun_sale
            FROM sales 
            WHERE region = :region and sector = :type
            Group by year_mon
    """), params).fetchall()      

    row1 = {'result': [dict(row) for row in row1]}
    df = json_normalize(row1['result']) #Results contain the required data
  
    df.columns = ["월요일","화요일", "수요일","금요일","목요일","토요일","일요일"]
    #df를 원하는 구간 만큼 슬라이싱

    result2 = df[day]
    result2 = result2.tolist()

    return {'corona': result1, 'week' : result2}




@app.route("/wordcloud", methods=['POST'])
def wordcloud():
    quarter = request.json['quarter']
    
    data = m.making_wordcloud_data(quarter)

    positive_data = data[0]
    negative_data = data[1]

    return {"positive":positive_data, "negative":negative_data}


@app.route("/ranking_guide", methods=['POST'])
def ranking():
    quarter = request.json['quarter']
    upjong = request.json['type']

    ranking_guide = c.ranking_guide(quarter, upjong)

    return jsonify({'ranking_guide': ranking_guide})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
