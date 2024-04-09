import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from pandas import DataFrame

import warnings
warnings.simplefilter("ignore")

originDf = pd.read_csv('../../df_file.csv') # CSV 불러오기
df = originDf.replace({r'\r':'', r'\n':''}, regex=True) # 문장정렬

df['Label'] = df['Label'].replace([0,1,2,3,4],['Politics','Sport','Technology','Entertainment','Business']) # 데이터셋 라벨링 값 기재
df['Text'] = df['Text'].str.replace('횂짙','$') # 특수문자 치환
df = df.head(2)

# papago 번역기를 돌린 후 chatGPT에서 제공하는 요약본 추출
# 1. 브라우저 열기
translateContents = []

# service = Service(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome()
url = "https://papago.naver.com/?sk=en&tk=ko"
driver.get(url)
time.sleep(2)

# # 2. 데이터프레임의 TEXT 번역
num = 0
for data in df['Text']:
    num+=1
    driver.find_element(By.ID,'txtSource').clear()
    driver.find_element(By.ID,'txtSource').send_keys(data)
    time.sleep(7)

    wait = WebDriverWait(driver,30)
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#txtTarget > span")))

    contents = driver.find_element(By.ID,'txtTarget').text
    translateContents.append(contents)
    # print('\n{}번째 문장 번역 : {}'.format(num,contents))
print("번역 종료")

driver.close()
driver.quit()

# 3. 원문,번역문,원문분류를 dataFrame으로 변환
result_data = DataFrame({'translateContents':translateContents})
print(result_data)

# # 4. 변환된 dataFrame을 csv 파일로 저장
df['translateText'] = result_data["translateContents"]
print(df)
# savePath = ""
df.to_excel('E:/2.Personal_Project/test2.xlsx',index=False)

