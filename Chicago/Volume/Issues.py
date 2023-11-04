import csv

# 存储所有链接
all_links = []

# 循环生成不同Vol和Issue的链接
for vol in range(18, 42):
    abbr = "jole"
    year = 2023 - 41 + vol
    if vol == 41 or vol==31 or vol==33 or vol==35 or vol==36 or vol==40:
        for issue in range(1,5):
            link = f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/{issue}"
            all_links.append(link)
        all_links.append(f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/S1")
    elif vol == 20:
        for issue in range(1,5):
            link = f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/{issue}"
            all_links.append(link)
        all_links.append(f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/S2")
    elif vol == 34 or vol == 37 or vol == 39:
        for issue in range(1,5):
            link = f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/{issue}"
            all_links.append(link)
        all_links.append(f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/S1")
        all_links.append(f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/S2")
    else:
        for issue in range(1, 5):
            link = f"https://www.journals.uchicago.edu/toc/{abbr}/{year}/{vol}/{issue}"
            all_links.append(link)

#for vol in range(78, 143):
    #link = f"https://www.sciencedirect.com/journal/games-and-economic-behavior/vol/{vol}/suppl/C"
    #all_links.append(link)

# 保存链接到CSV文件
with open("Journal of Labor Economics_url.csv", mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL"])  # 写入CSV文件的标题行
    for link in all_links:
        writer.writerow([link])

print("Links have been saved to test.csv")
