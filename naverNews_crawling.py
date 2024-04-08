from bs4 import BeautifulSoup
import requests
import re
import time
import os
import sys
import urllib.request
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# WebDriver 설정
options = webdriver.ChromeOptions() # 크롬브라우저의 옵션을 설정하기위한 객체 생성
options.add_experimental_option("excludeSwitches",["enable=automation"]) # 자동화를 감지하는 설정 제거
options.add_experimental_option("useAutomationExtenstion",False) # 자동화 확장 프로그램 비활성화
driver = webdriver.Chrome(ChromeDriverManager().install()) # webDriver 객체생성
driver.implicitly_wait(3) # 최대 3초간 대기


# Naver Api 정보 입력
client_id = "Qf7xOGk5H9OIsXs2hQBa"
client_secret = "wAAMxk09YY"