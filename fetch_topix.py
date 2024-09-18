import requests
from lxml import html
import json
from datetime import datetime

url = "https://quote.jpx.co.jp/jpx/template/quote.cgi?F=tmp/real_index&QCODE=151"
response = requests.get(url)
tree = html.fromstring(response.content)
rows = tree.xpath("//div[@class='component-normal-table']/table/tr")
header_texts = [td.text for td in rows[0].xpath(".//th")]
[td0, td1, td2, td3, td4, td5] = header_texts
if ["取引日", "始値", "高値", "安値", "前日比"] != [td0, td1, td2, td3, td5] or td4 not in ["終値", "現在値"]:
    raise Exception(f"""Table header is not as expected: {header_texts}""")
[td0, td1, td2, td3, td4, td5] = [td.text_content().strip()
                                  for td in rows[1].xpath(".//td")]
json_data = {
    "取引日": td0,  # "2024/09/13のように、ゼロ埋めされた日付"
    "始値": td1,
    "高値": td2,
    "安値": td3,
    "終値": td4,
    "前日比": td5,
    "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

print(json_data)

with open("topix.json", "w", encoding="utf-8") as json_file:
    json_file.write(json.dumps(json_data, ensure_ascii=False, indent=4))
