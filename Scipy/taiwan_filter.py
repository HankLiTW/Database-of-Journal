import pandas as pd


def taiwan_filter(journal_name):
    taiwan_universities = [
        "National Taiwan University",
        "National Tsing Hua University",
        "National Chiao Tung University",
        "National Cheng Kung University",
        "Taipei Medical University",
        "National Yang Ming University",
        "Chung Yuan Christian University",
        "National Central University",
        "National Sun Yat-sen University",
        "National Taiwan Normal University",
        "National Chung Cheng University",
        "National Taitung University",
        "National Chi Nan University",
        "Tunghai University",
        "National Chengchi University",
        "Soochow University",
        "Chang Gung University",
        "Providence University",
        "Feng Chia University",
        "Tamkang University",
        "I-Shou University",
        "National Taipei University of Technology",
        "Aletheia University",
        "St. John's University",
        "Nanhua University",
        "Chia Nan University of Pharmacy & Science",
        "Tung Fang Design University",
        "Asia University",
        "Ming Chuan University",
        "Kainan University",
        "Chien Hsin University of Science & Technology",
        "Southern Taiwan University of Science & Technology",
        "Takming University of Science & Technology",
        "National Taipei University",
        "Chinese Culture University",
        "National Dong Hwa University",
        "Shih Hsin University",
        "Yuan Ze University",
        "Tzu Chi University",
        "Hsuan Chuang University",
        "Tatung University",
        "National Taiwan Ocean University",
        "National Taipei University of Education",
        "National Ilan University",
        "Chaoyang University of Technology",
        "National Formosa University",
        "Da-Yeh University",
        "Chung Hua University",
        "Far East University",
        "Chung Jen University",
        "Shu-Te University",
        "Shih Chien University",
        "Ta Hwa University",
        "De Lin Institute of Technology",
        "Vanung University",
        "Tungnan University",
        "China Medical University",
        "Fu Jen Catholic University",
        "Chung Yuan Christian University",
        "Chihlee University of Technology",
        "Ming Chuan University",
        "University of Taipei",
        "Kainan University",
        "Tatung University",
        "Chang Gung University",
        "Tzu Chi University",
        "Nanhua University",
        "Tung Fang Design University",
        "Chien Hsin University of Science & Technology",
        "Chaoyang University of Technology",
        "Da-Yeh University",
        "Chung Hua University",
        "Far East University",
        "Chung Jen University",
        "Shu-Te University",
        "Shih Chien University",
        "Ta Hwa University",
        "De Lin Institute of Technology",
        "Vanung University",
        "Tungnan University",
        "China Medical University",
        "Fu Jen Catholic University",
        "Chung Yuan Christian University",
        "Chihlee University of Technology",
        "Ming Chuan University",
        "University of Taipei",
        "Kainan University",
        "Tatung University",
        "Chang Gung University",
        "Tzu Chi University",
        "Nanhua University",
        "Tung Fang Design University",
        "Chien Hsin University of Science & Technology",
        "Academia Sinica",
        "Taiwan"
        'taiwan'
        ".tw"
    ]

    journal = pd.read_csv(f"{journal_name}.csv")
    print("open success")
    # 创建一个条件以判断"Institutions"列是否包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"
    has_taiwan_institutions = journal["Affiliations"].str.contains("|".join(taiwan_universities), case=False, na=False)

    # 筛选包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"的行
    data_taiwan = journal[has_taiwan_institutions]

    # 保存包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"的行为一个新的CSV文件
    file_taiwan = f"{journal_name}_taiwan_scholar.csv"
    data_taiwan.to_csv(file_taiwan, index=False)

    print(f"已提取包含台湾排名前四十大学、Academia Sinica 和 Jinan University 的数据并保存为 {file_taiwan}")

if __name__ == "__main__":
    journal_list = ['Economics Journal', 'Econometrica' ,'Journal of Finance', 'Quantitative Economics','Theoretical Economics']
    for journal_name in journal_list:
        taiwan_filter(journal_name)
        # same as your code