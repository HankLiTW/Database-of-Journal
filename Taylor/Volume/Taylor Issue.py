import csv

# 存储所有链接
all_links = []
total_issue = 448
# 循环生成不同Vol和Issue的链接
for vol in range(95, 119):
    abbr = "uasa20"
    #year = 2023 - 41 + vol
    for issue in range(1,5):
        total_issue += 1
        link = f"https://www.tandfonline.com/toc/{abbr}/{vol}/{total_issue}?nav=tocList"
        all_links.append(link)
    if vol == 118:
        for issue in range(1, 4):
            total_issue += 1
            link = f"https://www.tandfonline.com/toc/{abbr}/{vol}/{total_issue}?nav=tocList"
            all_links.append(link)
all_links.append("https://www.tandfonline.com/action/showAxaArticles?journalCode=uasa20")


#for vol in range(78, 143):
    #link = f"https://www.sciencedirect.com/journal/games-and-economic-behavior/vol/{vol}/suppl/C"
    #all_links.append(link)

# 保存链接到CSV文件
with open("Journal of the American Statistical Association_url.csv", mode="w", newline='') as file:
    for link in all_links:
        writer = csv.writer(file)
        writer.writerow([link])
print("Links have been saved to test.csv")
