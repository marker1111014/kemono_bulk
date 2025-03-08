import os
import time
import requests  # 用來下載檔案
import undetected_chromedriver as uc  # 自動下載 ChromeDriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote  # 用來解碼 URL 轉換的字元
from tqdm import tqdm  # 進度條模組

# 取得當前執行檔的目錄
current_directory = os.getcwd()  # 改用 os.getcwd() 確保獲取當前目錄

# 啟動無頭模式的 Chrome
options = uc.ChromeOptions()
options.add_argument("--headless")  # 如果想看到視窗，請移除這行
driver = uc.Chrome(options=options)

# 目標網址
url = input("請輸入K站某一頁的連結：")
driver.get(url)

# 等待頁面載入
time.sleep(5)

# 抓取所有 class 為 "post__attachment-link" 的 <a> 標籤
attachment_links = driver.find_elements(By.CSS_SELECTOR, "a.post__attachment-link")

# 下載檔案
if attachment_links:
    for idx, element in enumerate(attachment_links, start=1):
        file_url = element.get_attribute("href")  # 取得檔案下載連結
        file_name = unquote(file_url.split("?f=")[-1])  # **解碼檔案名稱**

        print(f"\n正在下載：{file_name} ...")

        # 先取得檔案大小
        response = requests.get(file_url, stream=True)
        total_size = int(response.headers.get("content-length", 0))  # 檔案大小（位元組）

        if response.status_code == 200:
            file_path = os.path.join(current_directory, file_name)  # 儲存在當前目錄
            with open(file_path, "wb") as file, tqdm(
                total=total_size, unit="B", unit_scale=True, unit_divisor=1024, desc=file_name
            ) as progress_bar:
                for chunk in response.iter_content(1024):  # 下載 1 KB（1024 B）一次
                    file.write(chunk)
                    progress_bar.update(len(chunk))  # 更新進度條

            print(f"✅ 下載完成：{file_name}")
        else:
            print(f"❌ 無法下載 {file_name}，狀態碼：{response.status_code}")

else:
    print("找不到任何 'post__attachment-link' 的下載連結。")

# 關閉瀏覽器
driver.quit()
