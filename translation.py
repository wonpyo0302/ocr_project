import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import subprocess
import time
import clipboard as cb


import warnings
warnings.simplefilter("ignore")

originDf = pd.read_csv(r'E:\df_file.csv') # CSV 불러오기
df = originDf.replace({r'\r':'', r'\n':''}, regex=True) # 문장정렬

df['Label'] = df['Label'].replace([0,1,2,3,4],['Politics','Sport','Technology','Entertainment','Business']) # 데이터셋 라벨링 값 기재
df['Text'] = df['Text'].str.replace('횂짙','$') # 특수문자 치환

# papago 번역기를 돌린 후 chatGPT에서 제공하는 요약본 추출
# 1. 브라우저 열기
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
url_papago = "https://papago.naver.com/?sk=en&tk=ko"

option = Options()
option.add_experimental_option("debuggerAddress","127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
driver.maximize_window()
driver.get(url_papago)

# # 2. 데이터프레임의 TEXT 번역
translateContents = []
excelArr = []
errorIndex = []
savePath = "E:/2.Personal_Project/translate"
fileSuffix = ".xlsx"
fileNumber = 1
saveExcelStartIdx = 0
for index, data in enumerate(df['Text']):
    if index < len(df):
        try:
            print("-----------------------{}번째 번역을 시작----------------------".format(index))
            print("{}번째 문장 확인: {}".format(index,data[:20]))
            wait = WebDriverWait(driver,30)
            textBox = driver.find_element(By.CSS_SELECTOR,"#txtSource")
            textBox.clear()
            
            textBox.send_keys(data)
            time.sleep(5)
            
            wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#txtTarget > span")))
            contents = driver.find_element(By.ID,'txtTarget').text
            translateContents.append(contents)

            print("{}번째 번역 확인: {}".format(index,contents[:20]))
            print("-----------------------{}번째 번역이 완료----------------------".format(index))
            if index % 300 == 0 and index != 0:
                
                # 3. 번역문 및 문장의 주제를 dataFrame으로 변환
                result_data = pd.DataFrame({'translateContents':translateContents[saveExcelStartIdx:saveExcelStartIdx+299]})
                print("{} ~ {} 번째 인덱스 DF 변환 확인: {}".format(saveExcelStartIdx,saveExcelStartIdx+299,result_data))

                # # 4. 변환된 dataFrame을 xlsx 파일로 저장
                result_data.to_excel(savePath + str(fileNumber) + '.' + fileSuffix, index=False)
                fileNumber += 1
                saveExcelStartIdx += 300
            if index == 2224:
                result_data = pd.DataFrame({'translateContents':translateContents[2100:]})
        except Exception as e:
            print("{}번째 번역 중 에러발생".format(index))
            print("에러 원인 : {}".format(e))
            errorIndex.append(index)
            continue
print("모든 번역 종료")
driver.close()
driver.quit()



if len(errorIndex) > 0:
    for error in errorIndex:
        print("error인덱스 확인: {}".format(error))

