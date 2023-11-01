## Introduction
這邊的程式是用來爬Sciences Direct出版的期刊，Science Direct我們會需要爬的期刊有：
Journal of Accounting and Economics
Journal of Development Economics 
Journal of Econometrics
Journal of Economics Theory
Journal of Financial Economics
Journal of International Economics 
Journal of Monetary Economics 
Journal of Urban Economics
Review of Economics Dynamics
你們會需要做的是，下載相對應電腦版本的程式，並且下載好python和packages，還有對應期刊的csv檔案，直接跑程式就可以了。
在跑的過程中，可能有個別期刊他的網站跟人家長得不一樣，所以跑不出來，你們可以先試著改看看。
改的過程中，用我寫的單個網頁爬蟲的function(data_driver 或者 data_scraper_redirect)，print出soup去網頁結構。
通常，會需要你們直接點進去網頁裡面，找到作者的affiliation，然後在結構中搜尋找到對應位置，接下來，如果看不懂，丟chatgpt叫他教你。
雖然只要網頁結構複雜一點他的程式會亂寫，但是他還是能教你看懂網頁結構，所以就造著他所解釋的網頁結構去寫程式，真的改不好跟我說我幫你們改。
不過對各位比較不好意思的是，因為趕時間，所以我沒有管程式的架構好不好維護，所以委屈各位看亂七八糟的code了，如果要改看不懂跟我說。
## Mac 
### package

Mac的爬蟲是使用傳統的request的方法，只是因為大部分網頁都有用cloudflare反爬蟲，所以我用了另一個方法去繞過cloudflare，也就是cloudscraper。
接下來，會