# coding: cp949

import os
import sys
from csv import excel
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


def main(id, password, browser):
    if browser == 'ie':
        ie_driver = os.path.abspath('./browser/IEDriverServer_win64_2.45.0.exe')
        driver = webdriver.Ie(ie_driver)
    elif browser == 'chrome':
        chrome_driver = os.path.abspath('./browser/chromedriver.exe')
        # if sys.platform == 'darwin':
        #     chrome_driver = os.path.abspath('./browser/chromedriver_mac_32')
        # elif sys.platform.startswith('win'):
        #     chrome_driver = os.path.abspath('./browser/chromedriver_win_32.exe')
        # else:
        #     exit('not found chrome-driver for {}'.format(sys.platform))
        driver = webdriver.Chrome(chrome_driver)
    elif browser == 'phantomjs':
        if sys.platform.startswith('win'):
            phantomjs_path = os.path.join(os.environ['APPDATA'], 'npm', 'node_modules',
                         'phantomjs', 'lib', 'phantom', 'phantomjs.exe')
            driver = webdriver.PhantomJS(
                executable_path = phantomjs_path,
                service_args = ['--ignore-ssl-errors=true'])
        else:
            driver = webdriver.PhantomJS()
    else:
        exit('invalid browser : {}'.format(browser))

    #driver.maximize_window()
    driver.get('http://tvo.kr/xe/index.php?mid=member4&act=dispMemberLoginForm')

    driver.get_screenshot_as_file('screenshot.png')

    element = driver.find_element_by_id('uid')
    element.send_keys(id)

    element = driver.find_element_by_id('upw')
    element.send_keys(password)

    element.send_keys(Keys.RETURN)

    #print('�α��ε� ������, 3�� ���')
    sleep(3)

    f = open("./lsit.txt", 'w')
    for page in range(1, 31):

        url = 'http://tvo.kr/xe/index.php?mid=download1&page='+ str(page)
        #print(url)

        #print('�Ǻ�����Ʈ ���񽺷� �̵�.')
        driver.get(url)

        #print('�������ɶ����� ���')
        old_page = driver.find_element_by_tag_name('html')
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'boardList')))

        html = driver.page_source
        soup = BeautifulSoup(html)

        for row in soup.select('a[href*="document_srl"]'):
            try:
                buffer = str(row.text)
                f.write('�n'+ ' ' + buffer)
            except UnicodeEncodeError as e:
                print(str(e))

        sleep(2)

    # print('3�� �ڿ� �������� �ݽ��ϴ�.')
    # sleep(3)
    # driver.close()


def exit(message):
    print(message, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    # try:
    #     browser = sys.argv[1].lower()
    # except IndexError:
    #     exit('����> {} ������<ie/chrome>'.format(sys.argv[0]))
    #
    # id = input('TVO ���̵� : ')
    # if not id:
    #     exit('���̵� �Է����ּ���.')
    #
    # password = getpass('TVO ��й�ȣ : ')
    # if not password:
    #     exit('��ȣ�� �Է����ּ���.')

    # main(id, password, browser)
    main("sergei5", "ml31592517", "chrome")

