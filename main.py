import json
import tqdm
import requests

ACCESS_TOKEN = "MTYzZDA2ZmNmZTU2YmYwM2JhYzVjYWM3OTkxMGYwZmZlZmEwNjg2NGU1MWQ5YmQyZTViOWRjYTBkMDI1Mzc4MA"
SEMESTER = 361

def get_two_grade_course(session: requests.Session):
    path = './'
    url = f"https://catalog.ustc.edu.cn/api/teach/lesson/list-for-teach/{SEMESTER}?access_token={ACCESS_TOKEN}"
    response = session.get(url)
    data = json.loads(response.text)
    #print(data)

    url = f"https://catalog.ustc.edu.cn/api/teach/lesson/infos?access_token={ACCESS_TOKEN}"
    for course in tqdm.tqdm(data):
        payload = f'{"{"}"codes":["{course["code"]}"],"semester":{SEMESTER}{"}"}'
        response = session.post(url, data=payload)
        json_text = json.loads(response.text)
        if (json_text[0]["grading"] == "二分制" or json_text[0]["examType"] == "机考" or json_text[0]["examType"] == "大作业（论文、报告、项目或作品等）"):
            print(json_text[0]["name"]["cn"], json_text[0]["grading"], json_text[0]["examType"])
            with open(path + '2024SU_pf.txt', 'a', encoding='utf-8') as fp:
                fp.write(json_text[0]["name"]["cn"] + " " + json_text[0]["grading"] + " " + json_text[0]["examType"] + "\n")

if __name__ == '__main__':
    session = requests.Session()
    session = get_two_grade_course(session)
