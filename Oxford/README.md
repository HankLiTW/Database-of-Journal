## Introduction
這邊的程式是用來爬Oxford Academic Journals出版的期刊，Oxford Academic Journals我們會需要爬的期刊有：

The Quarterly Journal of Economics

The Review of Economics Studies

Journal of the European Economic Association

The Review of Financial Studies

Review of Finance

你們會需要做的是，下載相對應電腦版本的程式，並且下載好python和packages，還有對應期刊的csv檔案，直接跑程式就可以了。
在跑的過程中，可能有個別期刊他的網站跟人家長得不一樣，所以跑不出來，你們可以先試著改看看。
改的過程中，用我寫的單個網頁爬蟲的function(data_driver 或者 data_scraper_redirect)，print出soup去網頁結構。
通常，會需要你們直接點進去網頁裡面，找到作者的affiliation，然後在結構中搜尋找到對應位置，接下來，如果看不懂，丟chatgpt叫他教你。
雖然只要網頁結構複雜一點他的程式會亂寫，但是他還是能教你看懂網頁結構，所以就照著他所解釋的網頁結構去寫程式，真的改不好跟我說我幫你們改。
不過對各位比較不好意思的是，因為趕時間，所以我沒有管程式的架構好不好維護，所以委屈各位看亂七八糟的code了，如果要改看不懂跟我說。
## Note
1. Oxford的Mac和Windows可以用一樣的方法。
2. 程式中 if __name__ == "__main__": 以下的程式碼為使用範例，請你們根據你們要爬的期刊去改期刊名稱。
3. 我已經設置了很多反偵測爬蟲的方法，但如果還是被抓到，出現403錯誤，或者webdriver打不開的話，請修改程式sleep的時間，設長一點，這樣可以防止被抓到。
## Packages
cloudscraper

pandas

random

time

BeautifulSoup


urllib.parse

json
## Install
打開你的terminal，輸入以下指令，有些電腦要在pip前加驚嘆號;有些電腦會不行安裝，不行的話搜尋一下怎麼解決安裝問題，真的搞不定跟我說。

pip install cloudscraper

pip install pandas

pip install beautifulsoup4

其他套件應該不用特別安裝你的電腦就已經有了。
## Mathod
爬蟲是使用傳統的request的方法，只是因為大部分網頁都有用cloudflare反爬蟲，所以我用了另一個方法去繞過cloudflare，也就是cloudscraper。
接下來，會使用beautifulsoup去解構網頁原始碼，得到網頁結構，我再去從網頁結構抓資訊下來。
因為每個publisher的網頁不一樣，所以都要重寫；有時候甚至同publisher但不同期刊的網頁也不一樣，但通常只需要小改，就麻煩各位如果遇到就自己改一下，不行跟我說。
最後，程式在根據affiliation去找出台灣機構發出的論文。

輸出會是一個期刊名_taiwan_scholar.csv的檔案，上傳那個檔案到 https://drive.google.com/drive/folders/1tKU229oOzh0zIwITzy5umGMXdW_0QvU_?usp=drive_link