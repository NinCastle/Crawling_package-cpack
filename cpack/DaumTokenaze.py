import os
from konlpy.tag import Twitter
from collections import Counter

# 형태소 분리 카운트 함수
def kor_noun(text, ntags = 50):
    twitter = Twitter()
    nouns = twitter.nouns(text)
    count = Counter(nouns)
    return_llst = []
    for n, c in count.most_common(ntags):
        temp ={'tag':n, 'count':c}
        return_llst.append(temp)
    return return_llst

# 폴더 확인 함수
def look_dir():
    for (path, dir_, files) in os.walk('./Daum_news/'):
        if dir_ != []:
            return dir_

# 경로 확인 함수
def path_win(keyword):
    mid_list_pack = []
    for (path, dir_, files) in os.walk('./Daum_news/'+keyword):
        for filename in files:
            ext = os.path.splitext(filename)
            if ext != '.ipynb':
                # \\ 윈도우 경로
                mid_list_pack.append(str(path)+'\\'+str(filename))
    return mid_list_pack

# 형태소 분리
def tokenaze_dict(a):
    all_news_dict = {}
    for i in path_win(a):
        all_news_dict[i[-12:-4]] = ""
        
    for i in path_win(a):
        text_a = ""
        with open(i, 'r', encoding='utf-8') as text:
            text_a = text.read()
        all_news_dict[i[-12:-4]] += text_a
    return all_news_dict

# 명사만 분리
def tokenaze(keyword):
    twitter = Twitter()
    text_dict = tokenaze_dict(keyword)
    output_dict = {}
    for i in list(text_dict.keys()):
        print(i)
        output_dict[i] = twitter.nouns(text_dict[i])
    return output_dict               
        
# 분리된 형태소 빈도수 카운트
def tokenaze_count(a, ntags = 50):
    all_news_dict = tokenaze_dict(a)

    news_keyword = {}
    for news_date in list(all_news_dict.keys()):
        news_keyword[news_date] = kor_noun(all_news_dict[news_date], ntags)
    return news_keyword

# 감성점수 생성 함수
def sensitivity_score(text_dict):  
    import pandas as pd
    
    sentiment_dict_df=pd.read_csv('./cpack/polarity3.csv', encoding='cp949', index_col=0)
    score_dict = {}
    token_dict = sentiment_dict_df.T.to_dict()
    for words in list(token_dict):
    #     print(words)
    #     print(words.split(';'))
        for pos in words.split(';'):
            if pos.split('/')[-1] == 'NNG':
    #             print(pos.split('/')[0])
    #             print(words)
    #             print(token_dict_list[words])
                if token_dict[words]['max.value'] == 'NEG':
                    score_dict[pos.split('/')[0]] = - token_dict[words]['NEG']
                if token_dict[words]['max.value'] == 'POS':
                    score_dict[pos.split('/')[0]] = token_dict[words]['POS']
        if words.split('/')[-1] == 'NNG':
            if token_dict[words]['max.value'] == 'NEG':
                score_dict[words.split('/')[0]] = - token_dict[words]['NEG']
            if token_dict[words]['max.value'] == 'POS':
                score_dict[words.split('/')[0]] = token_dict[words]['POS']
    day_point = {}
    for first in list(text_dict.keys()):
        day_point[first] = 0
    # day_point
    for word_to_point in list(text_dict.keys()):
        for noun_word in text_dict[word_to_point]:
    #         print(score_dict[noun_word])
            try:
                day_point[word_to_point] = day_point[word_to_point] + score_dict[noun_word]
    #             print('점수가 있는 단어 : ', noun_word, score_dict[noun_word])
            except Exception as e:
    #             print('점수가 없는 단어 : ', e)
                pass
    return day_point