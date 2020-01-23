# 参数
url="http://106.15.248.8:8081" # OJ地址
username="lalalaterraria" # 用户名，需使用管理员账户来免除密码输入
password="ajziyin" # 密码
contest_name="2019年华南理工大学软件学院“新生杯”正式赛" # 比赛名称
wait_time=1 # js动态加载响应时间
stored_path="data/data.json" # 存储路径
problem_ID_type=0 # 0 表示1001, 1002, 1003, 1004计数，1表示A, B, C, D计数

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

print("opening selenium...")
chrome_options=Options()

# chrome_options.add_argument('--user-agent=""')  # 设置请求头的User-Agent
chrome_options.add_argument('--window-size=1920x1080')  # 设置浏览器分辨率（窗口大小）
chrome_options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
# chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
# chrome_options.add_argument('--disable-javascript')  # 禁用javascript
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面
chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
chrome_options.add_argument('–disable-software-rasterizer')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--start-maximized')

driver=webdriver.Chrome(chrome_options=chrome_options)

# 筛选一个类的方法
# import re
# s=" ".join(dir(driver))
# print(s)
# print("\n".join(re.findall("find_element\S+", s)))

# 输出类的所有属性和值
# for each in xxx.__dir__():
#     attr_name=each
#     attr_value=xxx.__getattribute__(each)
#     print(attr_name,':',attr_value)

# 打印页面html,base64截图
# base64转图片网站:https://codebeautify.org/base64-to-image-converter
# print(BeautifulSoup(driver.page_source, 'html.parser').prettify())
# print(driver.get_screenshot_as_base64())

# 整体html，内部html，base64截图
# print(tmp.get_attribute('outerHTML'))
# print(tmp.get_attribute('innerHTML'))
# print(tmp.screenshot_as_base64)

#登录部分
print("opening url and login...")
driver.get(url)
driver.find_element_by_xpath("//div[@id='header']/ul/div[2]/button/span").click()
driver.find_element_by_xpath("//input[@type='text']").click()
driver.find_element_by_xpath("//input[@type='text']").clear()
driver.find_element_by_xpath("//input[@type='text']").send_keys(username)
driver.find_element_by_xpath("//div[2]/div/div/div[2]/div/div").click()
driver.find_element_by_xpath("//input[@type='password']").click()
driver.find_element_by_xpath("//input[@type='password']").clear()
driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
driver.find_element_by_xpath("(//button[@type='button'])[4]").click()

#进入比赛和submissions
print("entering the contest and find the label of submissions...")
driver.find_element_by_xpath("//div[@id='header']/ul/li[3]").click()
time.sleep(wait_time)
driver.find_element_by_link_text(contest_name).click()
time.sleep(wait_time)
driver.find_element_by_xpath("//div[@id='contest-menu']/div/div/ul/li[4]").click()
time.sleep(wait_time)

#逐页爬取信息
print("begining to select the information...")
def go(page_number,total_info):
    driver.find_element_by_xpath("//li[@title=\'" + str(page_number) + "\']").click()
    time.sleep(wait_time)
    html=driver.page_source
    soup=BeautifulSoup(html, 'html.parser')
    
    # 打印规范页面
    # print(soup.prettify())

    # 找到status主体
    soup=soup.tbody
    str_soup=str(soup)
    soup=BeautifulSoup(str_soup, 'html.parser')

    # 开始分析
    info=soup.find_all('span') # other information
    info2=soup.find_all('a') # Author

    ans=[]
    tag=['when', 'id', 'status', 'problem', 'time', 'Memory', 'Language', 'Author']
    
    cnt=0
    info_dict={}
    for i in info:
        info_dict[tag[cnt]]=i.contents[0]
        cnt+=1
        if(cnt==7):
            cnt=0
            if(info_dict["status"]=="Compile Error": continue # CE不计入
            ans.append(info_dict)
            info_dict={}

    cnt=0
    for i in info2:
        ans[cnt][tag[7]]=i.contents[0]
        cnt+=1

    total_info+=ans

    # 输出json
    # print(json.dumps(ans,indent=4))

total_info=[]
try:
    i=0
    while(1):
        i+=1
        go(i,total_info)
        print(str(i) + ("st" if i % 10 == 1 else "nd" if i % 10 == 2 else "th") + " page has been crawled")
except: 
    print("over, " + str(i-1) + " pages has been crawled, now is analysing and storing data...")

# 最后接口对接处理
# tag=['when', 'id', 'status', 'problem', 'time', 'Memory', 'Language', 'Author']
# aim_tag=[
#             "submitId", # 提交序号，数字
#             "username", # 队伍名
#             "alphabetId" # 题目ID
#             "subTime", # 提交时间
#             "resultId" # 判题结果ID
#             # /**
#             # * 判题结果ID
#             # * @type {int}
#             # * @value 0 Accepted
#             # * @value 1 Presentation Error
#             # * @value 2 Time Limit Exceeded
#             # * @value 3 Memory Limit Exceeded
#             # * @value 4 Wrong Answer
#             # * @value 5 Runtime Error
#             # * @value 6 Output Limit Exceeded
#             # * @value 7 Compile Error
#             # * @value 8 System Error
#             # * @value 9 Security Error
#             # * @value -1 Waiting
#             # */
#         ]

final_info={"total":len(total_info),"data":total_info}

def transform(total_info, final_info):
    lim=len(total_info)
    final_info["data"]=[{} for _ in range(0,lim)]
    for i in range(0,lim):

        final_info["data"][i]["submitId"]=i
        tmp=total_info[i]["Author"]
        final_info["data"][i]["username"]=tmp
        final_info["data"][i]["alphabetId"]=chr(int(total_info[i]["problem"])-1001+ord("A")) if problem_ID_type == 0 else total_info[i]["problem"]
        final_info["data"][i]["subTime"]=total_info[i]["when"]
        final_info["data"][i]["resultId"]=0 if total_info[i]["status"] == "Accepted" else 4 


transform(total_info, final_info)

out=open(stored_path, 'w')
out.write(json.dumps(final_info, indent=4))

print("data has been stored in " + stored_path)

# 最重要的部分，不加准备死机吧
driver.quit()