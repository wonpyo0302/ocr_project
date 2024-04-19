import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import subprocess
import time
import clipboard as cb


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
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
url_gpt = "https://chat.openai.com/"
url_papago = "https://papago.naver.com/?sk=en&tk=ko"

option = Options()
option.add_experimental_option("debuggerAddress","127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
driver.maximize_window()
driver.get(url_gpt)
main_window = driver.current_window_handle # 현재 창의 윈도우 핸들 저장
driver.execute_script("window.open('{}');".format(url_papago))
time.sleep(1)

# # 2. 데이터프레임의 TEXT 번역
num = 0
for data in df['Text']:
    num+=1
    for handle in driver.window_handles: # 파파고로 driver 포커스 전환
        if handle != main_window:
            driver.switch_to.window(handle)
            break
    if num < 2:
        driver.find_element(By.ID,'txtSource').clear()
        driver.find_element(By.ID,'txtSource').send_keys(data)
        time.sleep(7)

        wait = WebDriverWait(driver,30)
        wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#txtTarget > span")))
        contents = driver.find_element(By.ID,'txtTarget').text
        translateContents.append(contents)
        cb.copy(contents+'\n 위 문장의 주제가 뭐야? 주제는 쌍따옴표로 감싸서 말해줘') # 클립보드에 gpt로 넘길 문장 저장
        time.sleep(2)
        driver.switch_to.window(main_window)
        driver.find_element(By.ID,'prompt-textarea').clear()
        driver.find_element(By.ID,'prompt-textarea').send_keys(cb.paste())
        Keys.ENTER
        getTitle = driver.find_element(By.CLASS_NAME, 'markdown prose w-full break-words dark:prose-invert light').text
        print("반환된 주제는 : '{}'입니다.".format(getTitle))
print("번역 종료")

driver.close()
driver.quit()

# 3. 원문,번역문,원문분류를 dataFrame으로 변환
# result_data = DataFrame({'translateContents':translateContents})
# print(result_data)

# # 4. 변환된 dataFrame을 csv 파일로 저장
# df['translateText'] = result_data["translateContents"]
# print(df)
# savePath = ""
# df.to_excel('E:/2.Personal_Project/test2.xlsx',index=False)

