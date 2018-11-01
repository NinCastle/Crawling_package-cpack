import os
from konlpy.tag import Twitter
from collections import Counter

# 형태소 분리 카운트 함수
def kor_noun(text, ntags = 50): #2글자인 명사만 추출
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

def tokenaze(keyword):
    twitter = Twitter()
    text_dict = tokenaze_dict(keyword)
    output_dict = {}
    for i in list(text_dict.keys()):
        output_dict[i] = twitter.nouns(text_dict[i])
    return output_dict
     ############### 작성중
        
        
        
# 분리된 형태소 빈도수 카운트
def tokenaze_count(a, ntags = 50):
    all_news_dict = tokenaze_dict(a)

    news_keyword = {}
    for news_date in list(all_news_dict.keys()):
        news_keyword[news_date] = kor_noun(all_news_dict[news_date], ntags)
    return news_keyword