import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import csv
import time
import random

Kabels = ["ВВГ"]
# url = "https://bystrokabel.ru/character/search?query=ввг&page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1026 Yowser/2.5 Safari/537.36",
    "Referer": "https://bystrokabel.ru/",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
}
def pagination(item):
    link = f"https://bystrokabel.ru/character/search?query={item}&page=1"
    res = requests.get(url= link, headers= headers)
    data = BeautifulSoup(res.text, "lxml")
    number_of_pages = (data.find("div").find_all(class_="non-selected-right"))[1].text

    return int(number_of_pages)


def get_data(item_,page):
    products_dict = []

    with open(f"aLessons\parsing_bystrocabel\data\{item_}.csv", "w",encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow((
            "Наименование",
            "Расчетная масса, кг/км",
            "Наружный диаметр, мм",
            "Минимальный барабан",
            "Макс. длина в бухте (≈50 кг), м"
            )
        )
    try:
        link =f"https://bystrokabel.ru/character/search?query={item_}&page={page}"
        res = requests.get(url= link, headers= headers)
        time.sleep((random.randint(1,3)))
        data = BeautifulSoup(res.content, "lxml")
        products = data.find("table", class_="result-table").find_all("tr")
        for item in products:
            if item.find_all(class_="char_name") == []:
                continue
            name = item.find(class_="char_name").text
            mass = item.find(class_="char_mass").text
            diam = item.find(class_="char_diam").text
            bar = item.find(class_="char_bar").find("span").text
            buhta = item.find(class_="char_buhta").text
            
            product = {
                "Name": name,
                "Massa": mass,
                "Diametr": diam,
                "Minimum drum": bar,
                "Max.Length": buhta,
            }
            products_dict.append(product)
            with open(f"aLessons\parsing_bystrocabel\data\{item_}.csv", "a" , encoding= "utf-8", newline='')as file:
                writer = csv.writer(file)
                writer.writerow (
                    (
                        name,
                        mass,
                        diam,
                        bar,
                        buhta
                    )
                )
            
        print(f"[INFO] {link} download")

        with open(f"aLessons\parsing_bystrocabel\data\{item_}.json", "w", encoding="utf-8") as file:
            json.dump(products_dict,file,indent=4, ensure_ascii=False)
        
        
    except Exception as ex:
        print(ex)
        print(f'[ERROR] {link}')       

if __name__ == "__main__":
    start = datetime.now()
    for item in Kabels:
        # for page in range(1,pagination(item)+1):
        for page in range(1,2):
            get_data(item,page)
    print(f'[COMPLETED]')
    end = datetime.now()
    total = end -start
    print(total)

    
        





