import time
import requests
import urllib
import json
import os
import random

#Configuration
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

#請求連接Sougou圖片搜尋網頁，擷取圖片url，並下載圖片
def GetSougouImag(search_item,path):

    # 設定m起始值為1，方便圖片數量記數
    m=1

    # 定義空list，儲存圖片id
    imgs_ids = []

    for num in range(0, 3500, 48):
        url = 'https://pic.sogou.com/pics?query=' + search_item + '&mode=1&start={}&reqType=ajax&tn=0&reqFrom=detail'.format(num)
        print('正在連接：'+ url)

        try:
            # 發送get請求
            f = requests.get(url=url, headers={'Accept-Encoding': ''}) #f = requests.get(url,headers=headers)
            print('get請求狀態：', f.status_code) #印出HTTP狀態碼

            #解析請求url之json檔
            js = json.loads(f.text) #將json字串轉換為dict
            js_items = js['items']

            #擷取圖片url與id
            for j in range(len(js_items)):
                img_id=(js_items[j]['mf_id'])
                img_url=(js_items[j]['thumbUrl'])
                print('** '+str(m) + '_' + search_item + '_' +img_id +'.jpg **'+' Downloading...')
                print(img_url)

                # 保存圖片id到imgs_ids(list)，避免重複下載圖片
                if img_id != None and not img_id in imgs_ids:
                    imgs_ids.append(img_id)
                    print("儲存此照片id：" + img_id)
                    try:
                        filename = str(m) + '_' + search_item + '_' + img_id + '.jpg'
                        urllib.request.urlretrieve(img_url, os.path.join(path, filename)) #將URL的檔案儲存到本地端
                        time.sleep(float(random.randint(100, 200)) / 200)
                        m += 1
                    except Exception as e:
                        pass
                        print(e)

                else:
                    print("！！！此照片id已重複！！！")

        except Exception as g:
            pass
            print(g)

    #每抓取48張圖片休息2.5~3.5秒
    time.sleep(1+ float(random.randint(300, 500))/200)

def main():

    #計算爬蟲程式執行時間(起點)
    start = time.time()

    # 輸入搜尋標題，定義圖片儲存路徑，若無此路徑，創建該資料夾
    #search = ['臥推器材', '臥推架', '舉重床','臥推健身器材', '大飛鳥 健身器材', '大飛鳥 器材', '大飛鳥 龍門架', '大飛鳥訓練器', '小飛鳥 健身器材', '小飛鳥 器材', '小飛鳥 龍門架', '小飛鳥訓練器', '包膠啞鈴', '浸塑啞鈴', '啞鈴 器材', '塑膠啞鈴', '電鍍啞鈴', '坐姿下拉 器械', '背肌訓練器', '背肌訓練機', '高位下拉器', '高拉背訓練器', '高拉背訓練機', '划船機', '倒蹬机']
    search = ['健身房']

    for i in search:
        local_path = r'C:\Users\88691\PycharmProjects\20200905_pic\sougou_pic_request\{}'.format(i)
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        print(local_path)
        GetSougouImag(i, local_path)
        time.sleep(5 + float(random.randint(400, 700)) / 200)

    #計算爬蟲程式執行時間(終點)
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print(f'一共花費了{hour}小時{minu}分鐘{sec}秒')

if __name__ == '__main__':
    main()
    print('Download complete!')
