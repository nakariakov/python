# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os
os.getcwd()

kndDf = pd.read_excel(".\\school\\list\\2. 유초중등교육기관 주소록\\2-1) 유치원 현황.xlsx")

kndDf.shape
kndDf.columns
kndDf = kndDf.drop(0,axis=0)
kndDf = kndDf.drop(1,axis=0)
kndDf.columns = kndDf.ix[2,0:]
kndDf = kndDf.drop(2,axis=0)


from selenium import webdriver

driver = webdriver.Chrome("C:\\app\\webdriver\\chromedriver")
driver.implicitly_wait(3)
driver.get('http://www.schoolinfo.go.kr')
driver.find_element_by_id("SEARCH_KEYWORD").send_keys("봉담고등학교 학교회계 예·결산서")
driver.find_element_by_xpath("//button[@title='검색하기']").click()
driver.find_element_by_xpath(".//input[@id='ExcelData'][@name='ExcelData'][@type='hidden']").text()