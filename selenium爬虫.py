import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

OUTPUT_PATH = r"C:\Users\Leo\Desktop\Python_project\selenium\result"
log = open(OUTPUT_PATH + "log.txt", "a", encoding="utf-8")
START =484
if __name__ == '__main__':
    url_list = ["https://foodb.ca/foods/FOOD00" + str(i) for i in range(1, 1000)]
    for i in range(START,955):
        print(len(url_list))
        print(i + 1)
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches",
                                       ['enable-automation', 'enable-logging'])
        browser = webdriver.Chrome(chrome_options=option)

        log.write("Start!\n")
        log.write(f"正在爬取第{i + 1}个食物的数据\n")
        log.write(url_list[i])
        browser.get(url_list[i])
        if int(browser.current_url.split("FOOD00")[1]) != i + 1:
            log.write(f"想获取的为{i + 1}食物，但网页跳转到了{browser.current_url}\n")
            sys.exit(0)
        # 设置等待全部元素加载出来后再获取节点
        wait = WebDriverWait(browser, 100)
        # 表示页数的节点
        last = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//*[@id="DataTables_Table_0_paginate"]/ul/li[last()-1]'
                 )))[0].text
        if last == "Previous":
            log.write("没有数据，跳过\n")
            o = open(
                rf"{OUTPUT_PATH}\{str(i + 1)}_no_food.txt",
                'w',
                encoding="utf-8")  # 输出文件
            o.write("no")
        elif int(last) > 500 :
            print(last + "页数据太多，跳过")
            browser.quit()
            9***9*********************************+-++continue
        else:
            last = int(str(last).replace(" ", ""))
            log.write(f"共有{last}页")
            o = open(
                rf"{OUTPUT_PATH}\{str(i + 1)}_food.txt",
                'w',
                encoding="utf-8")  # 输出文件
            for page in range(1, last + 1):
                log.write(f"      正在处理第{page}页")
                trs = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody//tr')))   # 通过XPATH定位表格
                for every_element in trs:
                    o.write(str(every_element.text) + "\n")
                # 获取点击按钮
                Next_button = wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        '//*[@id="DataTables_Table_0_paginate"]/ul/li[last()]/a'
                    )))
                # 点击
                browser.execute_script("arguments[0].click();", Next_button)
                log.write(f"正进入第{i + 1}个食物的{page + 1}页,等待3秒\n")
                time.sleep(5)
        browser.quit()
