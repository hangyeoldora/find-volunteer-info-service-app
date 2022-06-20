import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

def get_href(soup):
    print(soup)
    a_href = driver.find_element(By.CSS_SELECTOR, "#content > div.content_view > div.search_form > div > p#text").text
    numbers = re.sub(r'[^0-9]', '', a_href)
    result = int(numbers)

    return result

def set_chrome_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    options.add_argument("lang=ko_KR")
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver

def main():

    option_list = ['6110000','6260000','6270000','6280000','6290000','6300000',
                   '6310000','5690000','6410000','6420000','6430000','6440000',
                   '6450000','6460000','6470000','6480000','6500000']
    url = "https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do"

    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")


    driver = set_chrome_driver()

    driver.get(url)
    driver.implicitly_wait(2)

    Select(driver.find_element(By.CSS_SELECTOR, '#searchHopeArea1')).select_by_value('6270000')
    btn = driver.find_element(By.CLASS_NAME, "btn_orange")
    btn.click()
    time.sleep(3)
    a_href = driver.find_element(By.CSS_SELECTOR, "#content > div.content_view > div.search_form > div > p").text
    # numbers = re.sub(r'[^0-9]', '', a_href)
    pagingNum = a_href.split('/')[1]
    pagingNum2 = pagingNum.split(']')[0]
    result = int(pagingNum2)
    print(result)
    # list_href_num = get_href(driver.find_element(By.CSS_SELECTOR, '#content > div.content_view > div.board_bottom > div > div > div > a.btn_prev').get_attribute("href"))
    # print(list_href_num)
    list_href_num = result
    driver.implicitly_wait(2)
    print(list_href_num)
    temp_dict = {}
    key_id = 0
    save_num = 0

    for i in range(1, list_href_num, 1):
        try:
            save_num += 1
            btn = driver.find_element(By.XPATH, '//a[@href="' + "?pageIndex=" + str(i) + '"]')
            btn.click()
            time.sleep(3)
            li_wrap = driver.find_element(By.CLASS_NAME, "wrap2")
            li_list = li_wrap.find_elements(By.CSS_SELECTOR, "#content > div.content_view > div.board_list.board_list2.non_sub > ul > li")

            for li in li_list:
                key_id += 1
                vol_id = key_id
                vol_title = li.find_element(By.CSS_SELECTOR, "#content > div.content_view > div.board_list.board_list2.non_sub > ul > li > a > dl > dt").text
                vol_center = li.find_element(By.CSS_SELECTOR, "#content > div.content_view > div.board_list.board_list2.non_sub > ul > li > a > dl > dd > dl:nth-child(1) > dd").text
                # 모집기간
                # vol_date = li.find_element(By.CSS_SELECTOR, "#content > div.content_view > div.board_list.board_list2.non_sub > ul > li > a > dl > dd > dl:nth-child(2) > dd").text
                vol_term = li.find_element(By.CSS_SELECTOR, "#content > div.content_view > div.board_list.board_list2.non_sub > ul > li > a > dl > dd > dl:nth-child(3) > dd").text
                # temp_list.append([vol_title, vol_center, vol_date, vol_term])
                temp_dict[vol_id] = {'제목': vol_title, '모집기관' : vol_center,  '봉사기간' : vol_term}
            print("{}행이 저장되었습니다.".format(save_num))
        except:
            i -= 1
            btn = driver.find_element(By.CLASS_NAME, 'btn_next')
            btn.click()
            time.sleep(3)
        time.sleep(3)

    # json 파일로 저장
    with open('대구.json', 'w', encoding="UTF-8") as f:
        json.dump(temp_dict, f, indent=4, ensure_ascii=False)




if __name__ == "__main__" :
    main()
