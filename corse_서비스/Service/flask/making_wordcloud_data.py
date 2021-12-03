#!/usr/bin/env python
# coding: utf-8

# # javascript에서 워드클라우드 생성 시 필요한 데이터 형식 만들기 : [{x:key, value:value}, ..., {x:key, value:value}] 

# In[6]:


import correlation_between_corona_and_sales as c
import json


# In[7]:


def making_wordcloud_data(quarter):
    '''
    javascrip에서 워드클라우드 생성 시 필요한 데이터 형식 만들기
    [양의 상관관계 데이터, 음의 상관관계 데이터]를 리스트로 반환
    '''
    corr_pos = c.corr_positive(quarter)
    wordcloud_positive_data_list = []
    corr_neg = c.corr_negative(quarter)
    corr_neg = abs(corr_neg)
    wordcloud_negative_data_list = []
    
    for i in corr_pos.index:
        wordcloud_positive_data_list.append({"x":i, "value":corr_pos.loc[i]['확진자수']})
    for i in corr_neg.index:
        wordcloud_negative_data_list.append({"x":i, "value":corr_neg.loc[i]['확진자수']})
    
    return [wordcloud_positive_data_list, wordcloud_negative_data_list]


# In[ ]:

def making_positive_json(quarter):
    '''
    양의 상관관계 데이터프레임을 json 형식으로 반환
    '''
    corr = c.corr_positive(quarter)
    corr_dict = corr.transpose().to_dict('records')[0]
    corr_js = json.dumps(corr_dict, ensure_ascii=False)
    return corr_js

def making_negative_json(quarter):
    '''
    음의 상관관계 데이터프레임을 json 형식으로 반환
    '''
    corr = c.corr_negative(quarter)
    corr_dict = corr.transpose().to_dict('records')[0]
    corr_js = json.dumps(corr_dict, ensure_ascii=False)
    return corr_js


