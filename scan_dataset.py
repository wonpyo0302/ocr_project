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

originDf = pd.read_csv('../../df_file_copy.csv',encoding="utf-8") # CSV 불러오기
df = originDf.replace({r'\r':'', r'\n':''}, regex=True) # 문장정렬

df['Label'] = df['Label'].replace([0,1,2,3,4],['Politics','Sport','Technology','Entertainment','Business']) # 데이터셋 라벨링 값 기재
df['Text'] = df['Text'].str.replace('횂짙','$') # 특수문자 치환

# papago 번역기를 돌린 후 chatGPT에서 제공하는 요약본 추출
# 1. 브라우저 열기
originContents = []
translateContents = []
contentsType = []
# service = Service(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome()
url = "https://papago.naver.com/?sk=en&tk=ko"
driver.get(url)
time.sleep(2)

# 2. 데이터프레임의 TEXT 번역
for idx , data in df.iterrows():
    if idx < 3:
        driver.find_element(By.ID,'txtSource').clear()
        driver.find_element(By.ID,'txtSource').send_keys(data.Text)
        time.sleep(7)

        wait = WebDriverWait(driver,30)
        wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#txtTarget > span")))

        contents = driver.find_element(By.ID,'txtTarget').text
        originContents.append(data.Text)
        translateContents.append(contents)
        contentsType.append(data.Label)
        print('\n{}번째 문장 번역 : {}'.format(idx+1,contents))
print("번역 종료")

driver.close()
driver.quit()


# 3. 원문,번역문,원문분류를 dataFrame으로 변환
from pandas import Series, DataFrame
result_data = {'translateContents':translateContents,
            'contentsType':contentsType}
result_data = DataFrame(result_data)
print("dataFrame 결과 \n",result_data)

# 4. 변환된 dataFrame을 csv 파일로 저장
originDf['translateText'] = result_data["translateContents"]
originDf['translateLabel'] = result_data["contentsType"]
print(originDf)
originDf.to_csv("../../df_file_copy.csv",na_rep='Unknown',encoding='utf-8',mode='a')

