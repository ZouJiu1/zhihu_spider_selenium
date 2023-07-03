#################
###ZouJiu-202306
#################
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver import EdgeOptions
import os
from selenium.webdriver.common.by import By
import time
import pickle
import json
from selenium.webdriver.support.wait import WebDriverWait
import requests
from copy import deepcopy
import argparse
from datetime import datetime
# import pdfkit
# import pinyin
from selenium.webdriver.common import keys
import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import numpy as np
import shutil
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

abspath = os.path.abspath(__file__)
filename = abspath.split(os.sep)[-1]
abspath = abspath.replace(filename, "")

import sys
sys.path.append(abspath)
# wkhtmltopdf_path = os.path.join(abspath, r'wkhtmltopdf\bin\wkhtmltopdf.exe')
# sys.path.append(wkhtmltopdf_path)
from thinkdeal import *

def save_cookie(driverkkk, path):
    #https://stackoverflow.com/questions/45417335/python-use-cookie-to-login-with-selenium
    with open(path, 'wb') as filehandler:
        pickle.dump(driverkkk.get_cookies(), filehandler)

def load_cookie(driverkkk, path):
    #https://stackoverflow.com/questions/45417335/python-use-cookie-to-login-with-selenium
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driverkkk.add_cookie(cookie)

def edgeopen(driverpath, strategy = False):
    service=Service(executable_path=driverpath)
    edge_options = EdgeOptions()

    #https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec
    edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    edge_options.add_experimental_option('useAutomationExtension', False)
    edge_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    edge_options.add_argument("disable-blink-features=AutomationControlled")#就是这一行告诉chrome去掉了webdriver痕迹
    
    #https://stackoverflow.com/questions/56897041/how-to-save-opened-page-as-pdf-in-selenium-python
    # settings = {
    #     "recentDestinations": [{
    #             "id": "Save as PDF",
    #             "origin": "local",
    #             "account": "",
    #         }],
    #         "selectedDestinationId": "Save as PDF",
    #         "version": 2
    #     }
    # prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    # edge_options.add_experimental_option('prefs', prefs)
    # edge_options.add_argument('--kiosk-printing')

    # https://www.selenium.dev/documentation/webdriver/drivers/options/#pageloadstrategy  
    # https://stackoverflow.com/questions/44503576/selenium-python-how-to-stop-page-loading-when-certain-element-gets-loaded
    # edge_options.add_argument(page_load_strategy, 'normal')
    if strategy:
        edge_options.page_load_strategy = 'none'
    # cap = DesiredCapabilities.EDGE
    # cap['pageLoadStrategy'] = 'none'
    
    driver = webdriver.Edge(options=edge_options, service = service)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    return driver

def login(driver):
    driver.find_elements(By.CLASS_NAME, "SignFlow-tab")[1].click()
    # driver.find_elements(By.CLASS_NAME, "username-input")[0].send_keys("")
    # driver.find_elements(By.CLASS_NAME, "username-input")[1].send_keys("")
    # driver.find_element(By.CLASS_NAME, "SignFlow-submitButton").click()
    WebDriverWait(driver, timeout=60).until(lambda d:d.find_element(By.CLASS_NAME, "TopstoryTabs-link"))
    return driver

def crawl_article_links(driver:webdriver, username:str):
    #crawl articles links
    articles = r'https://www.zhihu.com/people/zoujiu1/posts'
    articles_one = r'https://www.zhihu.com/people/zoujiu1/posts?page='
    article_detail = r'https://zhuanlan.zhihu.com/p/'

    driver.get(articles.replace("zoujiu1", username))
    pages = driver.find_elements(By.CLASS_NAME, 'PaginationButton')[-2]
    assert isinstance(int(pages.text), int)
    maxpages = int(pages.text)
    
    all_article_detail = {}
    #how many pages of articles
    for p in range(1, maxpages + 1):
        driver.get(articles_one + str(p))
        items = driver.find_elements(By.CLASS_NAME, "ArticleItem")
        #crawl article one by one
        for a in range(len(items)):
            introduce = items[a].get_attribute("data-zop")
            itemId = json.loads(introduce)
            links = items[a].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            # id = itemId['itemId']
            title = str(itemId['title'])
            all_article_detail[str(title)] = links #article_detail + str(id)
        time.sleep(sleeptime)
    with open(os.path.join(articledir, 'article.txt'), 'w', encoding='utf-%d'%(6+2)) as obj:
        for key, val in all_article_detail.items():
            obj.write(val + " " + key + '\n')

def crawl_answers_links(driver:webdriver, username:str):
    #crawl answers links
    answer = r'https://www.zhihu.com/people/zoujiu1/answers'
    answer_one = r'https://www.zhihu.com/people/zoujiu1/answers?page='

    driver.get(answer.replace("zoujiu1", username))
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "Pagination"))
    pages = driver.find_elements(By.CLASS_NAME, 'PaginationButton')[-2]
    assert isinstance(int(pages.text), int)
    maxpages = int(pages.text)
    
    all_answer_detail = []
    #how many pages of answers
    for p in range(1, maxpages + 1):
        driver.get(answer_one + str(p))
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "Pagination"))
        items = driver.find_elements(By.CLASS_NAME, "AnswerItem")
        #crawl answer one by one
        for i in range(len(items)):
            introduce = items[i].get_attribute("data-zop")
            itemId = json.loads(introduce)
            id = itemId['itemId']
            title = str(itemId['title'])
            links = items[i].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            all_answer_detail.append([links, str(title)])
        time.sleep(sleeptime)
    with open(os.path.join(answerdir, 'answers.txt'), 'w', encoding='utf-8') as obj:
        for links, title in all_answer_detail:
            obj.write(links + " " + title + '\n')

def crawl_think_links(driver:webdriver, username:str):
    #crawl think links
    think = r'https://www.zhihu.com/people/zoujiu1/pins'
    think_one = r'https://www.zhihu.com/people/zoujiu1/pins?page='

    driver.get(think.replace("zoujiu1", username))
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "Pagination"))
    pages = driver.find_elements(By.CLASS_NAME, 'PaginationButton')[-2]
    assert isinstance(int(pages.text), int)
    maxpages = int(pages.text)
    
    # all_think_detail = []
    #how many pages of think
    for p in range(1, maxpages + 1):
        driver.get(think_one + str(p))
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "Pagination"))
        items = driver.find_elements(By.CLASS_NAME, "PinItem")
        #crawl answer one by one
        for i in range(len(items)):
            RichContent = items[i].find_element(By.CLASS_NAME, 'RichContent-inner')
            clockitem = items[i].find_element(By.CLASS_NAME, 'ContentItem-time')
            try:
                WebDriverWait(items[i], timeout=10).until(lambda d: len(d.text) > 2)
            except:
                driver.get(think_one + str(p))
                WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "Pagination"))
                items = driver.find_elements(By.CLASS_NAME, "PinItem")
                RichContent = items[i].find_element(By.CLASS_NAME, 'RichContent-inner')
                clockitem = items[i].find_element(By.CLASS_NAME, 'ContentItem-time')
                WebDriverWait(items[i], timeout=10).until(lambda d: len(d.text) > 2)
            # clockspan = clockitem.find_element(By.TAG_NAME, 'span')
            clock = clockitem.text
            clock = clock[3 + 1:].replace(" ", "_").replace(":", "_")
            dirthink = os.path.join(thinkdir, clock)
            if os.path.exists(dirthink):
                continue
            os.makedirs(dirthink, exist_ok=True)
            try:
                RichContent.find_element(By.CLASS_NAME, 'Button').click()
                WebDriverWait(items[i], timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "RichContent-inner"))
                RichContent = items[i].find_element(By.CLASS_NAME, 'RichContent-inner')
            except:
                pass
            content = RichContent.find_element(By.CLASS_NAME, 'RichText')
            # time.sleep(sleeptime)
            links_col = content.find_elements(By.TAG_NAME, 'a')
            links = []
            for itext in links_col:
                links.append(itext.get_attribute("href"))
            text = content.text.strip()
            if len(text)!=0:
                with open(os.path.join(dirthink, clock+".txt"), 'w', encoding='utf-8') as obj:
                    obj.write(text.replace("<br>", '\n').replace("<br data-first-child=\"\">", '\n')+"\n")
                    for itext in links:
                        obj.write(itext + "\n")
                    # all_think_detail.append([text])
            try:
                items[i].find_elements(By.CLASS_NAME, 'Image-PreviewVague')[0].click()
            except:
                continue
            cnt = 0
            while True:
                WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "ImageGallery-Inner"))
                img = driver.find_element(By.CLASS_NAME, 'ImageGallery-Inner').find_element(By.TAG_NAME, 'img')
                imglink = img.get_attribute('data-original')
                try:
                    response = requests.get(imglink, timeout=30)
                except:
                    try:
                        response = requests.get(imglink, timeout=30)
                    except:
                        continue
                if response.status_code==200:
                    with open(os.path.join(dirthink, clock + "_" + str(cnt) + '.jpg'), 'wb') as obj:
                        obj.write(response.content)
                    cnt += 1
                    time.sleep(sleeptime)
                try:
                    disable = driver.find_element(By.CLASS_NAME, 'ImageGallery-arrow-right')
                    if 'disabled' in disable.get_attribute('class'):
                        driver.find_element(By.CLASS_NAME, 'ImageGallery-close').click()
                        break
                    else:
                        disable.click()
                except:
                    break
            time.sleep(sleeptime)
    dealthink(thinkdir)

def crawl_article_detail(driver:webdriver):
    website_col = {}
    for i in os.listdir(articledir):
        try:
            kk = int(i)
            shutil.rmtree(os.path.join(articledir, i))
        except:
            pass
    with open(os.path.join(articledir, 'article.txt'), 'r', encoding='utf-8') as obj:
        for i in obj.readlines():
            i = i.strip()
            ind = i.index(" ")
            website = i[:ind]
            title   = i[ind+1:].replace(" ", "_").replace("\n", "")
            website_col[website] = title
    for website, title in website_col.items():
        nam = title.replace(":", "_").replace("?", ";"). \
                    replace("/","_").replace("\\","_").replace("\"", "_").\
                    replace("*","_").replace("|", "_").replace(" ", "_")
        temp_name = str(np.random.randint(999999999)) + str(np.random.randint(999999999))
        # nam_pinyin = pinyin.get(nam, format='numerical')
        # if '泰勒公式使用积分来推导' not in title:
        #     continue
        dircrea  = os.path.join(articledir, temp_name)
        fileexit = os.path.exists(os.path.join(articledir, nam, nam + ".pdf"))
        if fileexit:
            filesize = os.path.getsize(os.path.join(articledir, nam, nam + ".pdf"))
        direxit  = os.path.exists(os.path.join(articledir, nam))

        if direxit and not fileexit:
            os.remove(os.path.join(articledir, nam))
        if direxit and fileexit and filesize > 0:
            continue
        if direxit and fileexit and filesize == 0:
            os.remove(os.path.join(articledir, nam, nam + ".pdf"))
            os.remove(os.path.join(articledir, nam))
        os.makedirs(dircrea, exist_ok = True)
        original_window = driver.current_window_handle
        
        #get math formuladriver.find_element(By.ID, 'Popover15-toggle').click()
        driverkk = edgeopen(driverpath, strategy=True)
        pyautogui.press(["Enter", "Enter", "Enter"])
        driverkk.get(r"https://www.zhihu.com/signin")
        try:
            load_cookie(driverkk, cookie_path)
            driverkk.get(website)
        except:
            driverkk = login(driverkk)
            save_cookie(driverkk, cookie_path)
            
        #get math formula
        # pyautogui.press(["Enter", "Enter", 'enter'])
        # pyautogui.hotkey("ctrl", "l")
        # pyautogui.hotkey("ctrl", "l")
        # pyautogui.write(website, 0.01)
        # pyautogui.hotkey("ctrl", "l")
        # pyautogui.press(["enter", 'enter', 'enter'])
        # time.sleep(formula_time)
        try:
            WebDriverWait(driverkk, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "ztext-math"))
        except:
            pass
        driverkk.execute_script("window:stop();")
        richtext = driverkk.find_element(By.CLASS_NAME, "Post-RichText")
        # pyautogui.press(["esc", "esc", "esc", "esc", "esc", "esc"])
        # matherr = -1
        # try:
        #     richtext = driver.find_element(By.CLASS_NAME, "Post-RichText")
        #     MathJax_SVG = driver.find_elements(By.CLASS_NAME, "MathJax_SVG")
        #     if len(MathJax_SVG) > 0:
        #         matherr = 1
        #         raise ValueError("")
        # except:
        #     pyautogui.hotkey("ctrl", "l")
        #     pyautogui.hotkey("ctrl", "l")
        #     pyautogui.write(website, 0.01)
        #     pyautogui.press(["enter", 'enter', 'enter'])
        #     if matherr < 0:
        #         time.sleep(formula_time+0.2)
        #     else:
        #         time.sleep(max(formula_time - 0.1, 0.3))
        #     matherr = -1
        #     pyautogui.press(["esc", "esc", "esc", "esc", "esc", "esc"])
        #     try:
        #         richtext = driver.find_element(By.CLASS_NAME, "Post-RichText")
        #         MathJax_SVG = driver.find_elements(By.CLASS_NAME, "MathJax_SVG")
        #         if len(MathJax_SVG) > 0:
        #             matherr = 1
        #             raise ValueError("")
        #     except:
        #         pyautogui.hotkey("ctrl", "l")
        #         pyautogui.hotkey("ctrl", "l")
        #         pyautogui.write(website, 0.01)
        #         pyautogui.press(["enter", 'enter', 'enter'])
        #         if matherr < 0:
        #             time.sleep(formula_time+0.3)
        #         else:
        #             time.sleep(max(formula_time - 0.2, 0.3))
        #         pyautogui.press(["esc", "esc", "esc", "esc", "esc", "esc"])
        #         richtext = driver.find_element(By.CLASS_NAME, "Post-RichText")

        titletext = driverkk.find_element(By.CLASS_NAME, "Post-Title")
        textlink = []
        tabletd = richtext.find_elements(By.TAG_NAME, "td")
        pcontent = richtext.find_elements(By.TAG_NAME, "a")
        time.sleep(sleeptime)
        for i in range(len(tabletd)):
            textlink.append(tabletd[i].text)
        for i in range(len(pcontent)):
            linksite = pcontent[i].get_attribute("href")
            if linksite:
                linksite = linksite.replace("//link.zhihu.com/?target=https%3A", "").replace("//link.zhihu.com/?target=http%3A", "")
                textlink.append("["+pcontent[i].text+"]"+"("+linksite + ")\n")



        rt = richtext.text
        h1 = richtext.find_elements(By.TAG_NAME, "h1")
        for i in range(len(h1)):
            rt = rt.replace(h1[i].text.strip()+"\n", "# " + h1[i].text.strip() + "\n")
        h2 = richtext.find_elements(By.TAG_NAME, "h2")
        for i in range(len(h2)):
            rt = rt.replace(h2[i].text.strip()+"\n", "## " + h2[i].text.strip() + "\n")
        pcontent = richtext.find_elements(By.TAG_NAME, "p")
        imgcontent = richtext.find_elements(By.TAG_NAME, "figure")
        pcontent[0].find_elements(By.CLASS_NAME)
        pre = 0
        Pheight = []
        imgheight = []
        for i in range(len(pcontent)):
            Pheight.append(pcontent[i].rect['y'])
        for i in range(len(imgcontent)):
            imgheight.append(imgcontent[i].rect['y'])

        imgpre = 0
        first = ""
        tempstring = ""
        tails = ""
        number = 0
        temptxt = ''
        for i in range(len(pcontent)):
            imgtext = ''
            temptxt += pcontent[i].text
            while True:
                if imgpre >= len(imgheight):
                    break
                if i==0 and \
                    imgheight[imgpre] < Pheight[i]:
                    imgtext += '''<img src="%d.jpg" width="100%%"/>\n'''%number
                    imgpre += 1
                    number += 1
                elif i!=len(pcontent)-1 and \
                    imgheight[imgpre] > Pheight[i] and \
                    imgheight[imgpre] < Pheight[i+1]:
                    imgtext += '''<img src="%d.jpg" width="100%%"/>\n'''%number
                    imgpre += 1
                    number += 1
                elif i==len(pcontent)-1 and \
                    imgheight[imgpre] > Pheight[i]:
                    imgtext += '''<img src="%d.jpg" width="100%%"/>\n'''%number
                    imgpre += 1
                    number += 1
                else:
                    break
            if len(imgtext) > 0:
                ind = rt[pre:].find(temptxt)
                first = rt[:ind + pre + len(temptxt)]
                tails = rt[ind + pre + len(temptxt):]
                rt = first + imgtext + tails
                pre = len(first) + len(imgtext)
                temptxt = ''
        pre = 0
        for i in range(len(pcontent)):
            formula_span = pcontent[i].find_elements(By.CLASS_NAME, "math-holder")
            for j in range(len(formula_span)):
                ele = formula_span[j]
                # kk = ele.get_attribute('class')
                # if kk is not None and 'ztext-math' in kk:
                formulatxt = ele.text
                ind = rt[pre:].find(formulatxt)
                first = rt[:pre]
                tempstring = rt[pre:pre + ind + len(formulatxt)]
                tails = rt[ind + pre + len(formulatxt):]
                tempstring = tempstring.replace(ele.text, "$" + ele.text + "$")
                rt = first + tempstring + tails
                pre = len(first) + len(tempstring)
        
        

        rt = rt.replace("修改\n", "").replace("开启赞赏\n", "开启赞赏, ").replace("添加评论\n", "").replace("分享\n", "").\
            replace("收藏\n", "").replace("设置\n", "")
        tle = titletext.text

        if len(textlink) + len(rt) > 0:
            with open(os.path.join(dircrea, nam + "_formula_" + ".md"), 'w', encoding='utf-8') as obj:
                obj.write("# " + tle+"\n\n")
                if len(rt) > 0:
                    obj.write(rt + "\n\n\n")
                    
                for i in range(len(textlink)):
                    obj.write(textlink[i] + "\n\n")
        driverkk.quit()

        #get article text
        driver.switch_to.window(original_window)
        driver.get(website)
        pyautogui.press(["Enter", "Enter", "Enter"])
        # pyautogui.press("F5")
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "Post-Topics"))
            
        #https://stackoverflow.com/questions/61877719/how-to-get-current-scroll-height-in-selenium-python
        scrollHeight = driver.execute_script('''return document.documentElement.scrollHeight''')
        footer = driver.find_element(By.TAG_NAME, "html")
        scroll_origin = ScrollOrigin.from_element(footer, 0, -60)
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, -100000).perform()
        for i in range(18):
            ActionChains(driver).scroll_from_origin(scroll_origin, 0, scrollHeight//18).perform()
            time.sleep(0.8)
        pyautogui.press(["Enter", "Enter", "Enter"])
        #remove noneed element
        try:
            driver.execute_script('''document.getElementsByClassName("Post-Sub")[0].remove();''')
        except:
            pass
        try:
            driver.execute_script('''document.getElementsByClassName("ColumnPageHeader-Wrapper")[0].remove();''')
        except:
            pass
        try:
            driver.execute_script('''document.getElementsByClassName("RichContent-actions")[0].remove();''')
        except:
            pass

        richtext = driver.find_element(By.CLASS_NAME, "Post-RichText")
        # textlink = []
        # tabletd = richtext.find_elements(By.TAG_NAME, "td")
        # pcontent = richtext.find_elements(By.TAG_NAME, "a")
        time.sleep(sleeptime)
        # for i in range(len(tabletd)):
        #     textlink.append(tabletd[i].text)
        # for i in range(len(pcontent)):
        #     linksite = pcontent[i].get_attribute("href")
        #     if linksite:
        #         linksite = linksite.replace("//link.zhihu.com/?target=https%3A", "").replace("//link.zhihu.com/?target=http%3A", "")
        #         textlink.append(linksite + "\n" + pcontent[i].text)
        rt = richtext.text

        if len(textlink) + len(rt) > 0:
            with open(os.path.join(dircrea, nam + ".txt"), 'w', encoding='utf-8') as obj:
                if len(rt) > 0:
                    obj.write(rt + "\n\n\n")
                    
                for i in range(len(textlink)):
                    obj.write(textlink[i] + "\n\n")

        # article image saving
        imgchunk = richtext.find_elements(By.TAG_NAME, 'img')
        cnt = 0
        for i in range(len(imgchunk)):
            imglink = imgchunk[i].get_attribute("data-original")
            try:
                response = requests.get(imglink, timeout=30)
            except:
                try:
                    response = requests.get(imglink, timeout=30)
                except:
                    continue
            if response.status_code==200:
                with open(os.path.join(dircrea, str(cnt) + '.jpg'), 'wb') as obj:
                    obj.write(response.content)
                cnt += 1
                time.sleep(sleeptime)
            
        # article to pdf 
        fileexit = os.path.exists(os.path.join(dircrea, temp_name + ".pdf"))
        if fileexit:
            os.remove(os.path.join(dircrea, temp_name + ".pdf"))

        with pyautogui.hold("Ctrl"):
            pyautogui.press("P")

        time.sleep(2+addtime)
        pyautogui.press("Enter")
        time.sleep(2+addtime)
        pyautogui.write(str(temp_name + ".pdf"), interval=0.01)
        pyautogui.press(["Tab"]*6 + ["Enter"])
        pyautogui.write(dircrea, interval=0.01)
        pyautogui.press(["Enter"])
        time.sleep(2+addtime)
        pyautogui.press(["Enter", "Enter", "Enter", "Enter"])
        time.sleep(6+addtime)
        clocktxt = driver.find_element(By.CLASS_NAME, "Post-NormalMain").find_element(By.CLASS_NAME, "ContentItem-time")
        time.sleep(1+addtime)
        clock = clocktxt.text[3+1:].replace(" ", "_").replace(":", "_")
        with open(os.path.join(dircrea, clock+".txt"), 'w', encoding='utf-8') as obj:
            obj.write(clock)
        try:
            os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
        except:
            time.sleep(3+addtime)
            try:
                os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
            except:
                time.sleep(10+addtime)
                try:
                    os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
                except:
                    time.sleep(60+addtime)
                    os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
        os.rename(dircrea, os.path.join(articledir, nam))

        time.sleep(sleeptime)

        #https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
        #https://github.com/JazzCore/python-pdfkit
        # if article_to_jpg_pdf_markdown:
        #     config = pdfkit.configuration(wkhtmltopdf = wkhtmltopdf_path)
        #     pdfkit.from_url(website, os.path.join(dircrea, nam_pinyin+".pdf"), configuration = config)
            
        # time.sleep(600)

def crawl_answer_detail(driver:webdriver):
    website_col = {}
    for i in os.listdir(answerdir):
        try:
            kk = int(i)
            shutil.rmtree(os.path.join(answerdir, i))
        except:
            pass
    with open(os.path.join(answerdir, 'answers.txt'), 'r', encoding='utf-8') as obj:
        for i in obj.readlines():
            i = i.strip()
            ind = i.index(" ")
            website = i[:ind]
            title   = i[ind+1:].replace(" ", "_").replace("\n", "")
            website_col[website] = title
    for website, title in website_col.items():
        nam = title.replace(":", "_").replace("?", ";"). \
                    replace("/","_").replace("\\","_").replace("\"", "_").\
                    replace("*","_").replace("|", "_").replace(" ", "_")
        temp_name = str(np.random.randint(999999999)) + str(np.random.randint(999999999))
        # nam_pinyin = pinyin.get(nam, format='numerical')
        if '用矩阵的初等变化来' not in title:
            continue
        dircrea  = os.path.join(answerdir, temp_name)
        fileexit = os.path.exists(os.path.join(answerdir, nam, nam + ".pdf"))
        if fileexit:
            filesize = os.path.getsize(os.path.join(answerdir, nam, nam + ".pdf"))
        direxit  = os.path.exists(os.path.join(answerdir, nam))

        if direxit and not fileexit:
            os.remove(os.path.join(answerdir, nam))
        if direxit and fileexit and filesize > 0:
            continue
        if direxit and fileexit and filesize == 0:
            os.remove(os.path.join(answerdir, nam, nam + ".pdf"))
            
            os.remove(os.path.join(answerdir, nam))
        os.makedirs(dircrea, exist_ok = True)
        original_window = driver.current_window_handle
        
        #get math formula
        driverkk = edgeopen(driverpath, strategy=True)
        pyautogui.press(["Enter", "Enter", "Enter"])
        driverkk.get(r"https://www.zhihu.com/signin")
        pyautogui.press(["Enter", "Enter", "Enter"])
        try:
            load_cookie(driverkk, cookie_path)
            driverkk.get(website)
        except:
            driverkk = login(driverkk)
            save_cookie(driverkk, cookie_path)
        # pyautogui.press(["Enter", "Enter", 'enter'])
        # pyautogui.hotkey("ctrl", "l")
        # pyautogui.hotkey("ctrl", "l")
        # pyautogui.write(website, 0.01)
        # pyautogui.hotkey("ctrl", "l")
        # pyautogui.press(["enter", 'enter', 'enter'])
        # time.sleep(formula_time)
        # driver.find_element(By.CLASS_NAME, "ztext-math")
        try:
            WebDriverWait(driverkk, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "ztext-math"))
        except:
            pass
        driverkk.execute_script("window:stop();")
        # pyautogui.press(["esc", "esc", "esc", "esc", "esc", "esc"])
        Created = "not found"
        Modified = "not found"
        QuestionAnswer = driverkk.find_element(By.CLASS_NAME, "QuestionAnswer-content")
        richtext = QuestionAnswer.find_element(By.CLASS_NAME, "RichContent--unescapable")
        metatext = QuestionAnswer.find_elements(By.TAG_NAME, "meta")
        for i in range(len(metatext)):
            if metatext[i].get_attribute("itemprop")=="dateCreated":
                Created = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")
            if metatext[i].get_attribute("itemprop")=="dateModified":
                Modified = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")
        # matherr = -1
        # try:
            # QuestionAnswer = driverkk.find_element(By.CLASS_NAME, "QuestionAnswer-content")
            # richtext = QuestionAnswer.find_element(By.CLASS_NAME, "RichContent--unescapable")
            # metatext = QuestionAnswer.find_elements(By.TAG_NAME, "meta")
        #     MathJax_SVG = QuestionAnswer.find_elements(By.CLASS_NAME, "MathJax_SVG")
        #     if len(MathJax_SVG) > 0:
        #         matherr = 1
        #         raise ValueError("")
            # for i in range(len(metatext)):
            #     if metatext[i].get_attribute("itemprop")=="dateCreated":
            #         Created = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")
            #     if metatext[i].get_attribute("itemprop")=="dateModified":
            #         Modified = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")
        # except:
        #     pyautogui.hotkey("ctrl", "l")
        #     pyautogui.hotkey("ctrl", "l")
        #     pyautogui.write(website, 0.01)
        #     pyautogui.press(["enter", 'enter', 'enter'])
        #     if matherr < 0:
        #         time.sleep(formula_time+0.2)
        #     else:
        #         time.sleep(max(formula_time - 0.1, 0.3))
        #     matherr = -1
        #     pyautogui.press(["esc", "esc", "esc", "esc", "esc", "esc"])
        #     try:
        #         QuestionAnswer = driverkk.find_element(By.CLASS_NAME, "QuestionAnswer-content")
        #         richtext = QuestionAnswer.find_element(By.CLASS_NAME, "RichContent--unescapable")
        #         metatext = QuestionAnswer.find_elements(By.TAG_NAME, "meta")
        #         MathJax_SVG = QuestionAnswer.find_elements(By.CLASS_NAME, "MathJax_SVG")
        #         if len(MathJax_SVG) > 0:
        #             matherr = 1
        #             raise ValueError("")
        #         for i in range(len(metatext)):
        #             if metatext[i].get_attribute("itemprop")=="dateCreated":
        #                 Created = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")
        #             if metatext[i].get_attribute("itemprop")=="dateModified":
        #                 Modified = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")
        #     except:
        #         pyautogui.hotkey("ctrl", "l")
        #         pyautogui.hotkey("ctrl", "l")
        #         pyautogui.write(website, 0.01)
        #         pyautogui.press(["enter", 'enter', 'enter'])
        #         if matherr < 0:
        #             time.sleep(formula_time+0.3)
        #         else:
        #             time.sleep(max(formula_time - 0.2, 0.3))
        #         pyautogui.press(["esc", "esc", "esc", "esc", "esc", "esc"])
        #         QuestionAnswer = driverkk.find_element(By.CLASS_NAME, "QuestionAnswer-content")
        #         richtext = QuestionAnswer.find_element(By.CLASS_NAME, "RichContent--unescapable")
        #         metatext = QuestionAnswer.find_elements(By.TAG_NAME, "meta")
        #         for i in range(len(metatext)):
        #             if metatext[i].get_attribute("itemprop")=="dateCreated":
        #                 Created = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")
        #             if metatext[i].get_attribute("itemprop")=="dateModified":
        #                 Modified = metatext[i].get_attribute("content").replace(" ", "_").replace(":", "_").replace(".", "_")

        textlink = []
        tabletd = richtext.find_elements(By.TAG_NAME, "td")
        pcontent = richtext.find_elements(By.TAG_NAME, "a")
        time.sleep(sleeptime)
        for i in range(len(tabletd)):
            textlink.append(tabletd[i].text)
        for i in range(len(pcontent)):
            linksite = pcontent[i].get_attribute("href")
            if linksite:
                linksite = linksite.replace("//link.zhihu.com/?target=https%3A", "").replace("//link.zhihu.com/?target=http%3A", "")
                textlink.append("["+pcontent[i].text+"]"+"("+linksite + ")\n")



        rt = richtext.text
        h1 = richtext.find_elements(By.TAG_NAME, "h1")
        for i in range(len(h1)):
            rt = rt.replace(h1[i].text.strip()+"\n", "# " + h1[i].text.strip() + "\n")
        h2 = richtext.find_elements(By.TAG_NAME, "h2")
        for i in range(len(h2)):
            rt = rt.replace(h2[i].text.strip()+"\n", "## " + h2[i].text.strip() + "\n")
        pcontent = richtext.find_elements(By.TAG_NAME, "p")
        imgcontent = richtext.find_elements(By.TAG_NAME, "figure")
        pcontent[0].find_elements(By.CLASS_NAME)
        pre = 0
        Pheight = []
        imgheight = []
        for i in range(len(pcontent)):
            Pheight.append(pcontent[i].rect['y'])
        for i in range(len(imgcontent)):
            imgheight.append(imgcontent[i].rect['y'])

        imgpre = 0
        first = ""
        tempstring = ""
        tails = ""
        number = 0
        temptxt = ''
        for i in range(len(pcontent)):
            imgtext = ''
            temptxt += pcontent[i].text
            while True:
                if imgpre >= len(imgheight):
                    break
                if i==0 and \
                    imgheight[imgpre] < Pheight[i]:
                    imgtext += '''<img src="%d.jpg" width="100%%"/>\n'''%number
                    imgpre += 1
                    number += 1
                elif i!=len(pcontent)-1 and \
                    imgheight[imgpre] > Pheight[i] and \
                    imgheight[imgpre] < Pheight[i+1]:
                    imgtext += '''<img src="%d.jpg" width="100%%"/>\n'''%number
                    imgpre += 1
                    number += 1
                elif i==len(pcontent)-1 and \
                    imgheight[imgpre] > Pheight[i]:
                    imgtext += '''<img src="%d.jpg" width="100%%"/>\n'''%number
                    imgpre += 1
                    number += 1
                else:
                    break
            if len(imgtext) > 0:
                ind = rt[pre:].find(temptxt)
                first = rt[:ind + pre + len(temptxt)]
                tails = rt[ind + pre + len(temptxt):]
                rt = first + imgtext + tails
                pre = len(first) + len(imgtext)
                temptxt = ''
        pre = 0
        for i in range(len(pcontent)):
            formula_span = pcontent[i].find_elements(By.CLASS_NAME, "math-holder")
            for j in range(len(formula_span)):
                ele = formula_span[j]
                # kk = ele.get_attribute('class')
                # if kk is not None and 'ztext-math' in kk:
                formulatxt = ele.text
                ind = rt[pre:].find(formulatxt)
                first = rt[:pre]
                tempstring = rt[pre:pre + ind + len(formulatxt)]
                tails = rt[ind + pre + len(formulatxt):]
                tempstring = tempstring.replace(ele.text, "$" + ele.text + "$")
                rt = first + tempstring + tails
                pre = len(first) + len(tempstring)
        
        
        rt = rt.replace("修改\n", "").replace("开启赞赏\n", "开启赞赏, ").replace("添加评论\n", "").replace("分享\n", "").\
            replace("收藏\n", "").replace("设置\n", "")

        if len(textlink) + len(rt) > 0:
            with open(os.path.join(dircrea, nam + "_formula_" + ".md"), 'w', encoding='utf-8') as obj:
                obj.write("# " + title+"\n\n")
                obj.write("Created: " + Created + "\n")
                obj.write("Modified: " + Modified + "\n\n")
                if len(rt) > 0:
                    obj.write(rt + "\n\n\n")
                    
                for i in range(len(textlink)):
                    obj.write(textlink[i] + "\n\n")
        driverkk.quit()

        #get article text
        driver.switch_to.window(original_window)
        driver.get(website)
        pyautogui.press(["Enter", "Enter", "Enter"])
        # pyautogui.press("F5")
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "AnswerItem-editButtonText"))
        
        #https://stackoverflow.com/questions/61877719/how-to-get-current-scroll-height-in-selenium-python
        scrollHeight = driver.execute_script('''return document.getElementsByClassName("QuestionAnswer-content")[0].scrollHeight''')
        footer = driver.find_element(By.TAG_NAME, "html")
        scroll_origin = ScrollOrigin.from_element(footer, 0, 0)
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, -100000).perform()
        for i in range(18):
            ActionChains(driver).scroll_from_origin(scroll_origin, 0, scrollHeight//18).perform()
            time.sleep(0.8)
        pyautogui.press(["Enter", "Enter", "Enter"])
        #remove noneed element
        
        try: 
            driver.execute_script('''document.getElementsByClassName("MoreAnswers")[0].remove();''')
        except:
            pass
        try:
            driver.execute_script('''document.getElementsByClassName("ViewAll")[0].remove();''')
        except:
            pass
        try:
            driver.execute_script('''document.getElementsByClassName("ViewAll")[0].remove();''')
        except:
            pass
        try:
            driver.execute_script('''document.getElementsByClassName("AppHeader")[0].remove();''')
        except:
            pass
        try:
            driver.execute_script('''document.getElementsByClassName("Reward")[0].remove();''')
        except:
            pass
        try:
            driver.execute_script('''document.getElementsByClassName("Question-sideColumn")[0].remove();''')
        except:
            pass

        QuestionAnswer = driver.find_element(By.CLASS_NAME, "QuestionAnswer-content")
        richtext = QuestionAnswer.find_element(By.CLASS_NAME, "RichContent--unescapable")
        # textlink = []
        # tabletd = richtext.find_elements(By.TAG_NAME, "td")
        # pcontent = richtext.find_elements(By.TAG_NAME, "a")
        time.sleep(sleeptime)
        # for i in range(len(tabletd)):
        #     textlink.append(tabletd[i].text)
        # for i in range(len(pcontent)):
        #     linksite = pcontent[i].get_attribute("href")
        #     if linksite:
        #         linksite = linksite.replace("//link.zhihu.com/?target=https%3A", "").replace("//link.zhihu.com/?target=http%3A", "")
        #         textlink.append(linksite + "\n" + pcontent[i].text)
        rt = richtext.text

        if len(textlink) + len(rt) > 0:
            with open(os.path.join(dircrea, nam + ".txt"), 'w', encoding='utf-8') as obj:
                obj.write(title+"\n\n")
                obj.write("Created: " + Created + "\n")
                obj.write("Modified: " + Modified + "\n")
                if len(rt) > 0:
                    obj.write(rt + "\n\n\n")
                    
                for i in range(len(textlink)):
                    obj.write(textlink[i] + "\n\n")

        # article image saving
        imgchunk = richtext.find_elements(By.TAG_NAME, 'img')
        cnt = 0
        for i in range(len(imgchunk)):
            imglink = imgchunk[i].get_attribute("data-original")
            try:
                response = requests.get(imglink, timeout=30)
            except:
                try:
                    response = requests.get(imglink, timeout=30)
                except:
                    continue
            if response.status_code==200:
                with open(os.path.join(dircrea, str(cnt) + '.jpg'), 'wb') as obj:
                    obj.write(response.content)
                cnt += 1
                time.sleep(sleeptime)
            
        # article to pdf 
        fileexit = os.path.exists(os.path.join(dircrea, temp_name + ".pdf"))
        if fileexit:
            os.remove(os.path.join(dircrea, temp_name + ".pdf"))

        with pyautogui.hold("Ctrl"):
            pyautogui.press("P")
        
        time.sleep(2+addtime)
        pyautogui.press("Enter")
        time.sleep(2+addtime)
        pyautogui.write(str(temp_name + ".pdf"), interval=0.01)
        pyautogui.press(["Tab"]*6 + ["Enter"])
        pyautogui.write(dircrea, interval=0.01)
        pyautogui.press(["Enter"])
        time.sleep(2+addtime)
        pyautogui.press(["Enter", "Enter", "Enter", "Enter"])
        time.sleep(6+addtime)
        # clocktxt = driver.find_element(By.CLASS_NAME, "Post-NormalMain").find_element(By.CLASS_NAME, "ContentItem-time")
        time.sleep(1+addtime)
        clock = Created    #clocktxt.text[3+1:].replace(" ", "_").replace(":", "_")
        with open(os.path.join(dircrea, clock+".txt"), 'w', encoding='utf-8') as obj:
            obj.write(clock)
        try:
            os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
        except:
            time.sleep(3+addtime)
            try:
                os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
            except:
                time.sleep(10+addtime)
                try:
                    os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
                except:
                    time.sleep(60+addtime)
                    os.rename(os.path.join(dircrea, temp_name + ".pdf"), os.path.join(dircrea, nam + ".pdf"))
        os.rename(dircrea, os.path.join(answerdir, nam))
        time.sleep(sleeptime)
        #https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
        #https://github.com/JazzCore/python-pdfkit
        # if article_to_jpg_pdf_markdown:
        #     config = pdfkit.configuration(wkhtmltopdf = wkhtmltopdf_path)
        #     pdfkit.from_url(website, os.path.join(dircrea, nam_pinyin+".pdf"), configuration = config)
            
        time.sleep(600)

def zhihu(driverpath, cookie_path):
    website = r"https://www.zhihu.com/signin"
    
    #login and save cookies of zhihu
    driver = edgeopen(driverpath)
    driver.get(website)
    try:
        load_cookie(driver, cookie_path)
        driver.get(website)
    except:
        driver = login(driver)
        save_cookie(driver, cookie_path)
    pyautogui.press(["Enter"]*10)
    driver.find_element(By.ID, 'Popover15-toggle').click()
    driver.find_element(By.CLASS_NAME, 'Menu-item').click()
    url = driver.current_url
    username = url.split("/")[-1]

    # #crawl think links
    if crawl_think:
        crawl_think_links(driver, username)

    # #crawl articles links
    if crawl_article:
        if not os.path.exists(os.path.join(articledir, 'article.txt')):
            crawl_article_links(driver, username)
        else:
            if crawl_links_scratch:
                nowtime = datetime.fromtimestamp(time.time()).isoformat().replace(":", "_")
                os.rename(os.path.join(articledir, 'article.txt'), os.path.join(articledir, 'article_%s.txt'%nowtime))
                crawl_article_links(driver, username)
            else:
                pass
            crawl_article_detail(driver)
        
    # #crawl answers links
    if crawl_answer:
        if not os.path.exists(os.path.join(answerdir, 'answers.txt')):
            crawl_answers_links(driver, username)
        else:
            if crawl_links_scratch:
                nowtime = datetime.fromtimestamp(time.time()).isoformat().replace(":", "_")
                os.rename(os.path.join(answerdir, 'answers.txt'), os.path.join(answerdir, 'answers_%s.txt'%nowtime))
                crawl_answers_links(driver, username)
            else:
                pass
            crawl_answer_detail(driver)
    
    driver.quit()

if __name__ == "__main__":
    #version four.one_zero.zero
    driverpath = os.path.join(abspath, 'msedgedriver\msedgedriver.exe')
    savepath = deepcopy(abspath)
    cookiedir = os.path.join(savepath, 'cookie')
    thinkdir = os.path.join(savepath, 'think')
    answerdir = os.path.join(savepath, 'answer')
    articledir = os.path.join(savepath, 'article')
    os.makedirs(cookiedir, exist_ok=True)
    os.makedirs(thinkdir,  exist_ok=True)
    os.makedirs(answerdir,    exist_ok=True)
    os.makedirs(articledir,   exist_ok=True)
    cookie_path =os.path.join(cookiedir, 'cookie_zhihu.pkl')
    
    parser = argparse.ArgumentParser(description=r'crawler zhihu.com, 爬取知乎的想法, 回答, 文章, 包括数学公式')
    parser.add_argument('--sleep_time', type=float, default = 2, \
                        help=r'crawler sleep time during crawling, 爬取时的睡眠时间, 避免给知乎服务器带来太大压力, \
                        可以日间调试好，然后深夜运行爬取人少, 给其他小伙伴更好的用户体验, 避免知乎顺着网线过来找人, 默认: 2s')
    # parser.add_argument('--formula_time', type=float, default=0.6-0.2, \
    #                     help=r'crawler math formula sleep time,default:0.6-0.2, 爬取数学公式页面, 需要的sleep时间, 默认0.6-0.2')
    parser.add_argument('--computer_time_sleep', type=float, default=0, \
                        help=r'computer running sleep time 默认:0, 电脑运行速度的sleep时间, 默认:0')
    parser.add_argument('--think',   action="store_true", help=r'crawl think, 是否爬取知乎的想法, 已经爬取过的想法不会重复爬取, 所以可以多次爬取断了也没关系')
    parser.add_argument('--answer',  action="store_true", help=r'crawl answer, 是否爬取知乎的回答, 保存到pdf、markdown以及相关图片等，已经爬取过的不会重复爬取，\
                    断了再次爬取的话，可以配置到--links_scratch，事先保存好website')
    parser.add_argument('--article', action="store_true", help=r'crawl article, 是否爬取知乎的文章, 保存到pdf、markdown以及相关图片等，已经爬取过的不会重复爬取，\
                    断了再次爬取的话，可以配置到--links_scratch，事先保存好website')
    # parser.add_argument('--article_to_jpg_pdf_markdown', action="store_true", help=r'save article to pdf, 文章保存到pdf和markdown以及图片等')
    parser.add_argument('--links_scratch', action="store_true", \
                        help=r'crawl links scratch for answer or article, 是否使用已经保存好的website和title, 否则再次爬取website')
    args = parser.parse_args()
    sleeptime = args.sleep_time
    crawl_think = args.think
    crawl_answer = args.answer
    crawl_article = args.article
    crawl_links_scratch = args.links_scratch
    # article_to_jpg_pdf_markdown = args.article_to_jpg_pdf_markdown
    addtime = args.computer_time_sleep
    # formula_time = args.formula_time
    
    
    # crawl_think = True
    # crawl_article = True
    crawl_answer = True
    # crawl_links_scratch = True
    # python.exe c:/Users/10696/Desktop/access/zhihu/crawler.py --sleep_time 1 --think --links_scratch
    # python.exe c:/Users/10696/Desktop/access/zhihu/crawler.py --sleep_time 1 --article --links_scratch
    # python.exe c:/Users/10696/Desktop/access/zhihu/crawler.py --sleep_time 1 --answer --links_scratch
    # python.exe c:/Users/10696/Desktop/access/zhihu/crawler.py --sleep_time 1 --think --answer --article --links_scratch
    zhihu(driverpath, cookie_path)