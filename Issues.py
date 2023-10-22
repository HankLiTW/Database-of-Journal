import csv

# 存储所有链接
all_links = []

# 循环生成不同Vol和Issue的链接
for vol in range(29, 77):
    for issue in range(1, 3):
        link = f"https://www.sciencedirect.com/journal/journal-of-accounting-and-economics/vol/{vol}/issue/{issue}"
        all_links.append(link)

#for vol in range(78, 143):
    #link = f"https://www.sciencedirect.com/journal/games-and-economic-behavior/vol/{vol}/suppl/C"
    #all_links.append(link)

# 保存链接到CSV文件
with open("c.csv", mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Links"])  # 写入CSV文件的标题行
    for link in all_links:
        writer.writerow([link])

print("Links have been saved to test.csv")
















