import pandas as pd

# 读取合并后的CSV文件
merged_file_path = "Economic_Theory_Experimental_Economics_International_Review_of_Economi_Journal_of_Economic_Growth_Journal_of_Risk_and_Uncertainty_data.csv"
data = pd.read_csv(merged_file_path)

# 创建一个条件以判断"Authors"列是否包含数据（除了"N/A"）
has_valid_authors_data = (data["Authors"] != "N/A") & data["Authors"].notna()

# 仅保留包含有效作者数据的行
data_with_valid_authors = data[has_valid_authors_data]

# 使用.loc明确指定操作位置，将"Year"列的日期格式从 "YYYY/MM" 改为 "YYYY"
data_with_valid_authors.loc[:, "Year"] = data_with_valid_authors["Year"].str.replace(r'\/.*', '', regex=True)

# 筛选出"Year"列中大于等于2000年的数据
filtered_data = data_with_valid_authors[data_with_valid_authors["Year"].astype(int) >= 2000]

# 保存筛选后的数据为新的CSV文件
filtered_file_path = "Economic_Theory_Experimental_Economics_International_Review_of_Economi_Journal_of_Economic_Growth_Journal_of_Risk_and_Uncertainty_data_2000.csv"
filtered_data.to_csv(filtered_file_path, index=False)

print(f"已删除2000年以前的数据，并保存为 {filtered_file_path}")

# 读取筛选后的CSV文件
filtered_file_path = "Economic_Theory_Experimental_Economics_International_Review_of_Economi_Journal_of_Economic_Growth_Journal_of_Risk_and_Uncertainty_data_2000.csv"
data = pd.read_csv(filtered_file_path)

# 计算每个期刊每年的发表总篇数
journal_year_counts = data.groupby(["Journal", "Year"])["Paper Title"].count().reset_index()
journal_year_counts.rename(columns={"Paper Title": "Total Papers"}, inplace=True)

# 保存计数结果为新的CSV文件
result_file_path = "Economic_Theory_Experimental_Economics_International_Review_of_Economi_Journal_of_Economic_Growth_Journal_of_Risk_and_Uncertainty_data_Year_Counts.csv"
journal_year_counts.to_csv(result_file_path, index=False)

print(f"已计算每个期刊每年的发表总篇数，并保存为 {result_file_path}")


# 读取规范化后的CSV文件
normalized_year_file_path = "Economic_Theory_Experimental_Economics_International_Review_of_Economi_Journal_of_Economic_Growth_Journal_of_Risk_and_Uncertainty_data_2000.csv"
data_normalized_year = pd.read_csv(normalized_year_file_path)

# 列出台湾排名前四十大学的名称、"Academia Sinica"和"Jinan University"
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
]

# 创建一个条件以判断"Institutions"列是否包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"
has_taiwan_institutions = data_normalized_year["Institutions"].str.contains("|".join(taiwan_universities), case=False, na=False)

# 筛选包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"的行
data_taiwan = data_normalized_year[has_taiwan_institutions]

# 保存包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"的行为一个新的CSV文件
file_taiwan = "Economic_Theory_Experimental_Economics_International_Review_of_Economi_Journal_of_Economic_Growth_Journal_of_Risk_and_Uncertainty_data_taiwan.csv"
data_taiwan.to_csv(file_taiwan, index=False)

print(f"已提取包含台湾排名前四十大学、Academia Sinica 和 Jinan University 的数据并保存为 {file_taiwan}")
