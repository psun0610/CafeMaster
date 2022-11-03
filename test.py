from audioop import add
from selenium import webdriver
from selenium.webdriver.common.by import By
import string
import time
import os
import django
url_list = []
data_id = []
datas = []
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CafeMaster.settings")
django.setup()

from articles.models import Cafe
def naverMapCrawling(search):
    driver = webdriver.Chrome("./chromedriver.exe") #selenium 사용에 필요한 chromedriver.exe 파일 경로 지정

    driver.get(f"https://m.map.naver.com/search2/search.naver?query={search}") 
    driver.implicitly_wait(3) # 로딩이 끝날 때 까지 10초까지는 기다림

    # 개별 url 접속 안 했을 때 사용할 변수 (li태그)
    items = driver.find_elements(By.CSS_SELECTOR, '._item')
    cnt = 0
    print(items)
    for item in items:
        cnt += 1
        title = item.get_attribute('data-title')
        address = item.find_element(By.CSS_SELECTOR,'.item_address').text.replace('주소보기\n', '')
        longtitude = float(item.get_attribute('data-longitude'))
        latitude = float(item.get_attribute('data-latitude'))
        tel = item.get_attribute('data-tel')
        id = int(item.get_attribute('data-id'))

        # url 들어가기
        # 들어가서 뽑을 것: 사진, 주차, 영업시간, 특이사항
        aitem = item.find_elements(By.CSS_SELECTOR, '.item_info > .item_common > sp_map btn_spi2 naver-splugin')
        sub_url = aitem.get_attribute('data-url').text
        driver.get(sub_url)
        # content = driver.find_elements(By.CSS_SELECTOR, )

        
        for character in string.punctuation:
            title = title.replace(character, '') # 특수기호 제거(파이어베이스에 경로로 저장하기 위해서)
        #document.querySelector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview > div > em")
        #ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview > div > em
        datas.append({
            "id" : id,
            "title" : title,
            "addr" : address,
            "longtitude" : longtitude,
            "latitude" : latitude,
            "tel" : tel
            })
        data_id.append(id)
        #딱 30개만
        if cnt>29:
            break    
        #print(datas)
        return datas

def add_data():
    result = []

    # 자료 수집 함수 실행
    for data in datas:
        tmp = data
        # 만들어진 dic를 리스트에 저장
        result.append(tmp)

    # DB에 저장
    for item in result:
        # Store(
        # #id=(item["id"]),
        # category=item["cat"],
        # title=item["title"],
        # addr=item["addr"],
        # longtitude=item["longtitude"],
        # latitude=item["latitude"],
        # tel=item["tel"]).save(),
        Cafe(
        #id=(item["id"]),
        category=item["cat"],
        title=item["title"],
        addr=item["addr"],
        longtitude=item["longtitude"],
        latitude=item["latitude"],
        tel=item["tel"]).save()


    return result


# DB 저장 함수 강제 실행(임시로 실행)

search = input("검색어를 입력해주세요 >> ")
naverMapCrawling(search)
add_data()