from selenium import webdriver
import time
import urllib
import os
from selenium.webdriver.chrome.options import Options
import requests

# 輸入搜尋標題，組成欲爬取頁面的url
search = input("請輸入搜尋標題：")
url = 'https://pic.sogou.com/pics?query={}'.format(search)

# 定義圖片儲存路徑，若無此路徑，創建該資料夾
local_path = r'C:\Users\88691\PycharmProjects\20200905_pic\sougou_pic_selenium\{}'.format(search)
if not os.path.exists(local_path):
    os.mkdir(local_path)

# 定義啟動無頭模式參數
chrome_options = Options()
chrome_options.add_argument('--headless')

# 啟動chrome瀏覽器，並打開爬取頁面
chromeDriver = r'C:\Users\88691\PycharmProjects\20200905_pic\chromedriver'  # chromedriver檔案放的位置
driver = webdriver.Chrome(chromeDriver,options=chrome_options)
driver.get(url)

# 紀錄已下載的圖片url，避免重覆下載
img_url_dic = {}

# 模擬視窗滾動，以瀏覽更多圖片
pos = 0
m = 0  # 圖片編號
xpath = '//div/ul/li//a/img' # 定義目標元素的xpath
start = time.time()
for i in range(80):
    pos += i * 500  # 每次往下滾動視窗500單位
    js = "document.documentElement.scrollTop=%d" % pos
    driver.execute_script(js)
    time.sleep(1)

    for element in driver.find_elements_by_xpath(xpath):
        try:
            img_url = element.get_attribute('src') #抓取圖片url

            # 保存圖片到指定路徑
            if img_url != None and not img_url in img_url_dic:
                img_url_dic[img_url] = ''
                m += 1
                ext = img_url.split('/')[-1]
                filename = str(m) + '_' + search + '_' + ext + '.jpg'

                print(filename)
                print(img_url)
                urllib.request.urlretrieve(img_url, os.path.join(local_path, filename)) # 保存圖片

        except OSError:
            print('發生OSError!')
            print(pos)
            break;

print('Download complete!')
end = time.time()
spend = end - start
hour = spend // 3600
minu = (spend - 3600 * hour) // 60
sec = spend - 3600 * hour - 60 * minu
print(f'一共花費了{hour}小時{minu}分鐘{sec}秒')

driver.close()


# js_final = json.dumps(img_url_dic)
# 将数据存储到json文件中
# with open('data_json.json', 'a+', encoding='utf-8') as f:
#     json.dump(data_list, f, ensure_ascii=False, indent=4)
# print('json文件写入完成')
# # 将数据存入csv文件中
# # 表头
# csv_title = data_list[0].keys()
# with open('data_csv.csv', 'w', encoding='utf-8', newline='') as f:
#     writer = csv.writer(f)
#     # 写入表头
#     writer.writerow(csv_title)
#     # 批量写入表头
#     for row in data_list:
#         writer.writerow(row.values())
# print('csv文件写入完成')