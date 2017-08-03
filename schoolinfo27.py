# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:40:56 2017
@author: 1310615
"""

import sys
import os
import argparse
import pandas as pd
import logging
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.support.ui import Select
#from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import StaleElementReferenceException
#from selenium.common.exceptions import ElementNotVisibleException


def getParentPaid(args):

    reload(sys)
    sys.setdefaultencoding('utf-8')

    driver = None
    schoolDf = None
    schoolDfempty = None
    acctPblcDf = None
    acctPrvtDf = None
    pathFile = '.\\'
    pathWebDriver = '.\\webdriver\\'
    pathResult = '.\\result\\'
    pathLog = '.\\log\\'

    if not os.path.exists(pathResult):
        os.makedirs(pathResult)
    if not os.path.exists(pathLog):
        os.makedirs(pathLog)

    logging.basicConfig(filename = pathLog + 'schoolinfo27.log'
                      , level = logging.DEBUG
                      , format = '%(asctime)s %(message)s'
                      , datefmt = '%Y/%m/%d %I:%M:%S %p')
    logger = logging.getLogger("crumbs")
    logger.setLevel(logging.INFO)

    logger.info('ParentPaid Start !!')
    grade = { 'e':u'초등학교'
            , 'm':u'중학교'
            , 'h':u'고등학교'
            , 'u':u'대학교'
            , 'g':u'대학원'
            , 's':u'특수학교'
            , 'o':u'기타' }

    gList = list(grade.keys())

    if args.grade == 'a':
        gList = gList
    else:
        del gList
        gList= list(args.grade)

    logger.info(u'웹드라이버 선택(팬텀은 화면표시 없음)')
    if args.browser == 'c':
        driver = webdriver.Chrome(pathWebDriver + "chromedriver")
    elif args.browser == 'p':
        driver = webdriver.PhantomJS(pathWebDriver + "phantomjs-2.1.1-windows\\bin\\phantomjs")
    elif args.browser == 'i':
        driver = webdriver.Ie(pathWebDriver + "IEDriverServer_win32_2.45.0")
    else:
        driver = webdriver.Chrome(pathWebDriver + "chromedriver")

    logger.info(u'학교등급 선택')
    for g in gList:
        schoolDf = schoolDfempty

        print(grade.get(g) + u"처리")

        logger.info(grade.get(g) + u'학교목록 읽어오기')
        if g == 'e':
            schoolDf = pd.read_excel(pathFile  + u"2-2) 초등학교 현황.xlsx")
            schoolDf.columns = schoolDf.iloc[2,0:]
            schoolDf = schoolDf.drop([0,1,2],axis=0)
        elif g == 'm':
            schoolDf = pd.read_excel(pathFile  + u"2-3) 중학교 현황.xlsx")
            schoolDf.columns = schoolDf.iloc[2,0:]
            schoolDf = schoolDf.drop([0,1,2],axis=0)
        elif g == 'h':
            schoolDf = pd.read_excel(pathFile  + u"2-4) 고등학교 현황.xlsx")
            schoolDf.columns = schoolDf.iloc[2,0:]
            schoolDf = schoolDf.drop([0,1,2],axis=0)
        elif g == 'u':
            schoolDf = pd.read_excel(pathFile  + u"1-1) 대학 현황.xlsx")
            schoolDf.columns = schoolDf.iloc[4,0:]
            schoolDf.rename(columns={u"학교명(국문)":u"학교명"}, inplace = True)
            schoolDf = schoolDf.drop([0,1,2,3,4],axis=0)
        elif g == 'g':
            schoolDf = pd.read_excel(pathFile  + u"1-2) 대학원 현황.xlsx")
            schoolDf.columns = schoolDf.iloc[4,0:]
            schoolDf.rename(columns={u"학교명(국문)":u"학교명"}, inplace = True)
            schoolDf = schoolDf.drop([0,1,2,3,4],axis=0)
        elif g == 's':
            schoolDf = pd.read_excel(pathFile  + u"2-5) 특수학교 및 기타학교 현황.xlsx", sheetname =u"특수학교")
            schoolDf.columns = schoolDf.iloc[2,0:]
            schoolDf = schoolDf.drop([0,1,2],axis=0)
        elif g == 'o':
            schoolDf = pd.read_excel(pathFile  + u"2-5) 특수학교 및 기타학교 현황.xlsx", sheetname =u"기타학교")
            schoolDf.columns = schoolDf.iloc[3,0:]
            schoolDf = schoolDf.drop([0,1,2,3],axis=0)
        else:
            pass

        logger.info(u'변수 초기화')
        schooltype = 'thead'

        # 국공립학교 계정
        acctPblcDf = DataFrame(columns=(u'학교명','구분', u'공시년월',u'학부모부담수입',u'등록금'
                                       ,u'학교운영지원비', u'수익자부담수입',u'급식비'
                                       ,u'방과후학교활동비', u'현장체험학습비',u'청소년단체활동비'
                                       ,u'졸업앨범대금', u'교과서대금',u'기숙사비',u'기타수익자부담수입'
                                       ,u'누리과정비',u'교복구입비',u'운동부운영비')
                             , index = None)

        # 사립학교 계정
        acctPrvtDf = DataFrame(columns=(u'학교명',u'구분', u'공시년월',u'학부모부담수입' ,u'등록금'
                                       ,u'입학금' ,u'수업료' ,u'학교운영지원비' ,u'수익자부담수입'
                                       ,u'급식비' ,u'방과후학교활동비' ,u'현장체험학습비'
                                       ,u'청소년단체활동비' ,u'졸업앨범대금' ,u'교과서대금'
                                       ,u'기숙사비' ,u'기타수익자부담수입' ,u'누리과정비'
                                       ,u'교복구입비',u'운동부운영비')
                             , index = None)

        # City Loop BEGIN
        for city in schoolDf[u'시도'].drop_duplicates():
            print(city + u'처리')
            countPblc = 1
            countPrvt = 1

            # School Loop BEGIN
            for idx, row in schoolDf.loc[(schoolDf[u'시도'] == city)].iterrows():
            # for idx, row in schoolDf.loc[(schoolDf[u'시도'] == city)].iloc[:3].iterrows():
                try:
                    logger.info(u'웹 호출')
                    driver.implicitly_wait(3)
                    driver.get('http://www.schoolinfo.go.kr')

                    sname = row[u'학교명'].strip()
                    url = 'http://' + row[u'홈페이지'].strip().replace('http://','').rstrip('/')
                    city = row[u'시도'].strip()

                    print(sname + " " + url)

                    logger.info(sname + ': Loop Start')

                    driver.find_element_by_id("SEARCH_KEYWORD").send_keys("")
                    driver.find_element_by_id("SEARCH_KEYWORD").send_keys(sname)
                    driver.find_element_by_xpath(u"//button[@title='검색하기']").click()

                    logger.info(sname + ': btnMore')
                    while 1:
                        try:
                            driver.find_element_by_id("btnMore")
                        except Exception as e:
                            logger.exception(sname + ": btnMore" + e.msg)
                            break

                        driver.find_element_by_id("btnMore").click()

                    logger.info(sname + u'학교검색결과 색인')
                    driver.find_element_by_xpath("//a[@href='"+url+"']/parent::span/parent::li/parent::ul/parent::article/h1[@class='School_Name']/a").click()

                    logger.info(sname + u'국공사립 구분확인')
                    establish = driver.find_element_by_xpath("//ul[@class='School_Data']/li[2]").text[5:]

                    logger.info(sname + u'상세정보 클릭')
                    driver.find_element_by_link_text(u'상세정보').click()

                    logger.info(sname + u'예결산서 클릭')
                    if establish in (u'국립',u'공립'):
                        schooltype = 'thead'
                        colNo01 = '22'
                        colNo02 = '23'
                        colNo03 = '24'
                        colNo04 = '25'
                        colNo05 = '26'
                        colNo06 = '27'
                        colNo07 = '28'
                        colNo08 = '29'
                        colNo09 = '30'
                        colNo10 = '31'
                        colNo11 = '32'
                        colNo12 = '33'
                        colNo13 = '34'
                        colNo14 = '35'
                        colNo15 = '36'
                        driver.find_element_by_link_text(u'학교회계 예·결산서').click()

                    elif establish == u'사립':
                        schooltype = 'tbody'
                        colNo01 = '23'
                        colNo02 = '24'
                        colNo03 = '25'
                        colNo04 = '26'
                        colNo05 = '27'
                        colNo06 = '28'
                        colNo07 = '29'
                        colNo08 = '30'
                        colNo09 = '31'
                        colNo10 = '32'
                        colNo11 = '33'
                        colNo12 = '34'
                        colNo13 = '35'
                        colNo14 = '36'
                        colNo15 = '37'
                        colNo16 = '38'
                        colNo17 = '39'
                        driver.find_element_by_link_text(u'사립학교 교비회계 예·결산서').click()

                    else:
                        pass

                    logger.info(sname + u'iframe 해제')
                    driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))

                    logger.info(sname + u'자세히보기 클릭')
                    driver.find_element_by_id("btnDetail").click()

                    logger.info(sname + u'공시년월 목록 선택')
                    select = Select(driver.find_element_by_id('select_trans_dt'))

                    for index in range(len(select.options)):

                        select = Select(driver.find_element_by_id('select_trans_dt'))
                        select.select_by_index(index)
                        openYYmm = driver.find_element_by_xpath("//select[@id='select_trans_dt']/option[@selected='']").text

                        logger.info(sname + u'공시년월별 자세히 보기 Loop : ' )

                        existDetail = driver.find_element_by_xpath("//div[@id='btnDetail']/a")

                        if existDetail.is_displayed():
                            existDetail.click()

                        cell = []
                        print(sname + " " + openYYmm)
                        cell.append(sname)
                        cell.append(establish)
                        cell.append(openYYmm)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo01 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo02 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo03 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo04 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo05 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo06 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo07 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo08 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo09 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo10 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo11 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo12 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo13 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo14 +"]/td").text)
                        cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo15 +"]/td").text)
                        if establish == u'사립':
                            cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo16 +"]/td").text)
                            cell.append(driver.find_element_by_xpath("//table[@class='TableType1']/"+schooltype+"/tr["+ colNo17 +"]/td").text)

                        if establish in (u'국립',u'공립'):
                            acctPblcDf.loc[countPblc] = cell
                            countPblc += 1
                        elif establish == u'사립':
                            acctPrvtDf.loc[countPrvt] = cell
                            countPrvt += 1

                except Exception as e:
                    logger.exception(sname + ' ' + str(e))
                    pass
                # School Loop END

            logger.info(sname + u': 파일 저장(' + grade.get(g) +u')')
            acctPblcDf.to_excel(pathResult + city + grade.get(g) + u'공립' + u'.xlsx',  header=True, index=True)
            acctPrvtDf.to_excel(pathResult + city + grade.get(g) + u'사립' + u'.xlsx',  header=True, index=True)
            acctPblcDf.drop(acctPblcDf.index, inplace=True)
            acctPrvtDf.drop(acctPrvtDf.index, inplace=True)
            # City Loop END

        # Grade Loop END

    driver.close()
    driver.quit()
    # getParentPaid END

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u'description: 학교알리미 Web Crawler'
                                   , formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-b', '--browser', choices=['i', 'c', 'p'], default='c'
                      , help=u'''사용할 인터넷 브라우저 선택(p는 백그라운드실행)\ni = IE, c = Chrome, p = PhantomJS''')
    parser.add_argument('-g', '--grade', choices=['e', 'm', 'h', 'u', 'g', 's', 'o','a'], default='a'
                      , help=u'''학교등급 선택\n  e = 초등학교\n, m = 중학교\n, h = 고등학교\n, u = 대학교\n, g = 대학원\n, s = 특수학교\n, o = 기타학교\n, a = 전학급''')
    args, unparsed = parser.parse_known_args()
    getParentPaid(args)
