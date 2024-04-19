from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import subprocess
import time

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
time.sleep(2)
print("메인브라우저 핸들러:'{}', 파파고브라우저 핸들러 추가: '{}'".format(main_window,driver.window_handles))

# login_btn = driver.find_element(By.TAG_NAME,"button")
# login_btn.click()
