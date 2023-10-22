import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# 創建一個Chrome瀏覽器實例
driver = webdriver.Chrome()

with open('stealth.min.js', "r") as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})


# 打開指定的網址
url = "https://onlinelibrary.wiley.com/doi/epdf/10.1111/joie.12310"
driver.get(url)

# 使用無限循環來保持瀏覽器打開
while True:
    pass  # 在這裡添加您的自動化操作，或等待一段時間

# 不要忘記最終關閉瀏覽器






