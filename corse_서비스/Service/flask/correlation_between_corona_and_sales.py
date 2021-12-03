#!/usr/bin/env python
# coding: utf-8

# # 확진자 수와 업종별 매출 상관관계 분석

# In[4]:



import pandas as pd
from pandas.core import groupby
import pymysql
import simplejson as json
from pandas import json_normalize
from dotenv import load_dotenv
import os
# ### 데이터프레임 호출 : 임의로 강남구 지정
# => 추후에 '강남구' 부분을 html에서 변수로 받아와야 함

# In[5]:
def correlation(quarter):
    '''
    quarter : 자치구 이름
    확진자수와 업종들의 매출 상관관계를 분석해 데이터프레임을 생성하는 함수
    '''
    db = pymysql.connect(host='172.17.0.1', port=3306, user='inti', passwd='year_dream_school_user!!!', db='year_dream', charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
            SELECT  sector, qua_rev, region, year_mon
            FROM sales
            WHERE region = \'{}\'
        """.format(quarter)
    cursor.execute(sql)
    result = cursor.fetchall()
    #result가 딕트타입
    row2 = {'result': [dict(row) for row in result]}
    data = json_normalize(row2['result']) #Results contain the required data
    sang = list(data['sector'].unique()) 

    kind = [] 
    for i in sang:
        condition = (data.sector == i)
        kind_df = pd.DataFrame(data[condition].groupby('year_mon').sum())        
        kind_df = pd.DataFrame(kind_df['qua_rev'])
        kind.append(kind_df)
    result1 = pd.concat(kind,axis=1) #가로로 데이터프레임 합치기
    result1.columns = sang #데이터프레임 컬럼명 수정
    market = result1

    

    
    sql2 = """
        SELECT *
        FROM patient
    """.format(quarter)
    cursor.execute(sql2)
    result = cursor.fetchall()
    row2 = {'result': [dict(row) for row in result]}
    df2 = json_normalize(row2['result'])
    corona = df2.transpose()
    corona.rename(columns=corona.iloc[0], inplace=True)
    corona = corona.drop(corona.index[0])
    corona = corona[quarter]

    compare_df = corona.to_frame(name='확진자수').join(market)  # 강남구의 1.확진자수 2.매출 데이터프레임 합치기

    corr = compare_df.corr()  # 피어슨 상관관계 구하기
    corr = corr.round(4)

    corr_df = pd.DataFrame(corr.iloc[0])  # 확진자수와 업종간의 상관관계만 추출 & Series를 데이터프레임으로 형변환
    corr_df.columns = ["확진자수"]

    
    oneself = corr_df[corr_df["확진자수"] == 1].index.values
    corr_df = corr_df.drop(oneself)
    return corr_df


def corr_positive(quarter):
    '''
    quarter : 자치구 이름
    양의 상관관계 : 확진자 수가 증가할 때 매출액도 증가한 업종 데이터프레임을 생성하는 함수
    '''
    corr = correlation(quarter)
    
    positive_corr = corr.loc[corr['확진자수'] > 0].sort_values(by='확진자수', ascending=False)
    positive_corr['순위'] = positive_corr.rank(ascending=False)
    positive_corr['순위'] = positive_corr['순위'].astype(int)  # float to int
    
    return positive_corr


def corr_negative(quarter):
    '''
    quarter : 자치구 이름
    음의 상관관계 : 확진자 수가 증가할 때 매출액이 감소한 업종 데이터프레임을 생성하는 함수
    '''
    corr = correlation(quarter)
    
    negative_corr = corr.loc[corr['확진자수'] < 0].sort_values(by='확진자수')
    negative_corr['순위'] = negative_corr.rank()
    negative_corr['순위'] = negative_corr['순위'].astype(int)
    
    return negative_corr


def corr_none(quarter):
    '''
    quarter : 자치구 이름
    확진자 수 증감과 아무런 관계가 없는, 영향을 받지 않은 업종 데이터프레임
    '''
    corr = correlation(quarter)
    
    none = corr.loc[corr['확진자수'] == 0]
    
    return none


def corr_all(quarter):
    return {'positive':corr_positive(quarter), 'negative':corr_negative(quarter), 'none':corr_none(quarter)}



def ranking_guide(quarter, comp):
    '''
    quarter : 자치구 이름
    comp : 업종명
    파라미터로 주어진 업종이 코로나 확진자 수 증가와 관련된 순위를 반환화는 함수
    '''
    corr = corr_all(quarter)
    
    if comp in corr['positive'].index:
        return f"{comp}은(는) 코로나 확진자 수가 증가할 때 매출이 많이 증가한 업종 {len(corr['positive'])}개 중 {corr['positive'].loc[comp, '순위']}위 입니다."
    elif comp in corr['negative'].index:
        return f"{comp}은(는) 코로나 확진자 수가 증가할 때 매출이 많이 감소한 업종 {len(corr['negative'])}개 중 {corr['negative'].loc[comp, '순위']}위 입니다."
    else:
        return f"{comp}은(는) 코로나 확진자 수 증가와 아무런 관련이 없는 것으로 나왔습니다."
