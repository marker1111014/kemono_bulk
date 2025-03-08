import time
import webbrowser  # 內建模組，用來自動打開瀏覽器
import undetected_chromedriver as uc  # 讓程式自動下載 ChromeDriver
from selenium.webdriver.common.by import By

# 啟動無頭模式的 Chrome（內建下載對應版本的 ChromeDriver）
options = uc.ChromeOptions()
options.add_argument("--headless")  # 如果想看視窗，請移除這行
driver = uc.Chrome(options=options)  # 不用手動設定 driver 路徑

# 目標網址
url = input("請輸入K站某一頁的網址：")
driver.get(url)

# 等待頁面載入
time.sleep(5)

# 抓取所有 class 為 "post__attachment-link" 的 <a> 標籤
attachment_links = driver.find_elements(By.CSS_SELECTOR, "a.post__attachment-link")

# 顯示抓取到的連結並打開它們
if attachment_links:
    for idx, element in enumerate(attachment_links, start=1):
        link = element.get_attribute("href")
        print(f"第 {idx} 個連結：{link}")

        # 自動打開連結
        webbrowser.open(link)
else:
    print("找不到任何 'post__attachment-link' 的連結。")

# 關閉瀏覽器
driver.quit()
