import json
import requests
from bs4 import BeautifulSoup
import pandas

with open("config.json", "r", encoding="utf-8") as file:
    config_data = json.load(file)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cookie": config_data["Cookie"],
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
}

excel_path = "submission_data.xlsx"
used_data = []
first_line_id = ""

try:
    data_frame = pandas.read_excel(excel_path, dtype=str)
    for index, row in data_frame.iterrows():
        selected = [row["id"], row["name"], row["class"], row["problem"], row["time"]]
        used_data.append(selected)
        if index == 0:
            first_line_id = row["id"]
except FileNotFoundError:
    print(f"文件 {excel_path} 未找到。")

data = []
for i in range(1, 9999):
    url = config_data["url"] + "&result=AC&page=" + str(i)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    if len(soup.find_all("tr")) == 1:
        break
    st = True
    for tr in soup.find_all("tr"):
        if st:
            st = False
            continue
        temp = []
        for td in tr.find_all("td"):
            if td.a:
                temp.append(td.a.text.strip())
            else:
                temp.append(td.text.strip())
        if temp[0] == first_line_id:
            break
        ls = [temp[0], temp[1], temp[2], temp[3], temp[9]]
        data.append(ls)
        print(ls)
    else:
        continue
    break
data.extend(used_data)

data_frame = pandas.DataFrame(data)
header = ["id", "name", "class", "problem", "time"]
data_frame.to_excel(excel_path, index=False, header=header)
print(f"数据已保存到Excel文件:{excel_path}")
