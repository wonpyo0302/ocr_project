import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

import warnings
warnings.simplefilter("ignore")

df = pd.read_csv('../../df_file.csv',encoding="utf-8") # CSV 불러오기
df = df.replace({r'\r':'', r'\n':''}, regex=True) # 문장정렬

df['Label'] = df['Label'].replace([0,1,2,3,4],['Politics','Sport','Technology','Entertainment','Business']) # 데이터셋 라벨링 값 기재
df['Text'] = df['Text'].str.replace('횂짙','$') # 특수문자 치환

# papago 번역기를 돌린 후 chatGPT에서 제공하는 요약본 추출
# 1. 브라우저 열기
result = {}
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
url = "https://papago.naver.com/?sk=en&tk=ko"
driver.get(url)
time.sleep(2)

# 2. 데이터프레임의 TEXT 번역
for idx , data in df.iterrows():
    if idx < 11:
        driver.find_element_by_id('txtSource').clear()
        driver.find_element_by_id('txtSource').send_keys(data.Text)
        time.sleep(3)

        wait = WebDriverWait(driver,timeout=10)
        wait.until(expected_conditions.presence_of_element_located(By.CSS_SELECTOR,"#targetEditArea > p"))

        contents = driver.find_element_by_id('txtTarget').text
        result[contents] = data.Text

        print('{}번째 문장 번역 : {}'.format(idx+1,contents))
print("번역 종료")

driver.close()
driver.quit()


