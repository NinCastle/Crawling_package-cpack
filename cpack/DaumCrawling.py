import time
import pandas as pd
import requests
import lxml.html
import os
# 다음 크롤링함수
def crawling(startdate, lastdate, *args):
    many_date = [i.strftime('%Y%m%d') for i in pd.date_range(startdate, lastdate)]
    for keyword in list(args):
        print(keyword)
        # 뉴스 url획득
        for date in many_date:
            try:
#                 print(date)
                date_add_url ='https://search.daum.net/search?nil_suggest=btn&w=news&DA=STC&cluster=y&q='+keyword+'&sd='+date+'000000&ed='+date+'235959&period=u'
#                 print(date_add_url)
                # 폴더 생성
                if not os.path.exists('./Daum_news'):
                    os.makedirs('./Daum_news')
#                 print(keyword)
                if not os.path.exists('./Daum_news/'+keyword):
#                     print(keyword)
                    os.makedirs('./Daum_news/'+keyword)
#                 for page in date_add_url:
#                     print('page : ', page)
                # Wait for 500 milliseconds
                time.sleep(1.500)

                res = requests.get(date_add_url)
                root = lxml.html.fromstring(res.text)
                
                urls = []
                for link in root.cssselect('a.f_nb'):
                    urls.append(link.attrib['href'])
#                 print(urls)
                if urls != []:
                    # 뉴스 크롤링
                    articles = []
                    for u in urls:
    #                     print('url : ', u)
                        if not u.startswith('http'):
                            continue
                        res = requests.get(u)
                        root = lxml.html.fromstring(res.text)
                        body = root.cssselect('.article_view').pop()
                        content = body.text_content().strip()  # 본문을 가져와 앞뒤 공백을 제거
                        articles.append(content)
    #                 print('url len : ',len(urls))
                    with open('./Daum_news/'+keyword+'/'+date+'.txt', 'w', encoding='utf-8') as f:
                        f.write(str(articles))
                        print(date, 'Crawing done')
                else:
                    print(date)
            except Exception as e:
                print(e)
                pass

#     f.close()