import pandas as pd
def correct_url(journal_name):
    df = pd.read_csv(f"{journal_name}_api.csv")
    for url in df["URL"]:
        corrected_url = url.replace("//doi", "/doi")
        df.loc[df["URL"] == url, "URL"] = corrected_url
    df.to_csv(f"{journal_name}_api.csv", index=False)

journal_list = ["Journal of Labor Economics","Journal of Political Economy","The Journal of Law and Economics"]
for journal in journal_list:
    correct_url(journal)
