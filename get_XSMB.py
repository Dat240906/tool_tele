import threading
import requests
from bs4 import  BeautifulSoup
import telebot
from datetime import datetime
from time import sleep

XSMB = {} # 5
XSMB_temp = {} # 2
users = {}
def handel_by_day(box_ketqua):
    time = box_ketqua.find('h2')
    time_split = time.text.split()
    print(time_split)
    if "DÒ" in time_split and "VÉ" in time_split and "XSMB" in time_split:
        return 
    title = "Xổ Số Miền Bắc"
    day_month = [time_split[i] for i in range(len(time_split)) if "/" in time_split[i]][0]
    thu = ''
    for i in range(len(time_split)):
        if "(" in time_split[i]:
            thu += f"{time_split[i][1:]} "           
        if ")" in time_split[i]:
            thu += time_split[i][:len(time_split[i])-1]
    giai = box_ketqua.find_all('tr')
    list_prize_original = []
    

       

    for item in giai:
        prize = item.find_all('td', attrs={'title': False})
        if prize:
            list_prize_original.append(prize[0].text)

    DB = list_prize_original[0]
    G1 = list_prize_original[1]

    G2_result = list_prize_original[2].split()
    G2 = (G2_result[0],G2_result[1] )

    G3_result = list_prize_original[3].split()
    G3 = (G3_result[0], G3_result[1],G3_result[2][:5], G3_result[2][5:], G3_result[3], G3_result[4]  )

    G4_result = list_prize_original[5].split()
    G4 = (G4_result[0], G4_result[1], G4_result[2], G4_result[3])

    G5_result = list_prize_original[6].split()
    G5 = (G5_result[0], G5_result[1], G5_result[2][:4], G5_result[2][4:], G5_result[3], G5_result[4])

    G6_result = list_prize_original[8].split()
    G6 = (G6_result[0], G6_result[1], G6_result[2])

    G7_result = list_prize_original[9].split()
    G7 = (G7_result[0], G7_result[1], G7_result[2], G7_result[3])

    XSMB[day_month] = {
        "DB":DB, 
        "G1":G1,
        "G2":G2,
        "G3":G3,
        "G4":G4,
        "G5":G5,
        "G6":G6,
        "G7":G7,
    }  

def tong_duyet(day_month):
    data = XSMB[day_month]
    DB = data['DB'][len(data['DB'])-2:]
    G1 = data['G1'][len(data['G1'])-2:]
    G2_list = data['G2']
    for i in range(len(G2_list)):
        G2_list[i] = G2_list[i][len(G2_list[i])-2:]
    G3_list = data['G3']
    for i in range(len(G3_list)):
        G3_list[i] = G3_list[i][len(G3_list[i])-2:]
    G4_list = data['G4']
    for i in range(len(G4_list)):
        G4_list[i] = G4_list[i][len(G4_list[i])-2:]
    G5_list = data['G5']
    for i in range(len(G5_list)):
        G5_list[i] = G5_list[i][len(G5_list[i])-2:]
    G6_list = data['G6']
    for i in range(len(G6_list)):
        G6_list[i] = G6_list[i][len(G6_list[i])-2:]
    G7_list = data['G7']
    for i in range(len(G7_list)):
        G7_list[i] = G7_list[i][len(G7_list[i])-2:]
    
    users_temp = users.copy()
    for chat_id, users_ in users_temp.items():
        for id_user, info in users_.items():
            number_ = info[1]
            for i in range(len(number_)):
                if number_[i] == DB:
                    number_[i] = "Đặc Biệt"
                elif number_[i] == G1:
                    number_[i] = "Giải Nhất"
                elif number_[i] in G2_list:
                    number_[i] = "Giải Nhì"
                elif number_[i] in G3_list:
                    number_[i] = "Giải Ba"
                elif number_[i] in G4_list:
                    number_[i] = "Giải Tư"
                elif number_[i] in G5_list:
                    number_[i] = "Giải Năm"
                elif number_[i] in G6_list:
                    number_[i] = "Giải Sáu"
                elif number_[i] in G7_list:
                    number_[i] = "Giải Bảy"
            users[chat_id][id_user][1] = number_




def get_ketqua():
    url = "https://xskt.com.vn/xsmb"


    response = requests.get(url)
    suop = BeautifulSoup(response.content, "html.parser")

    box_ketqua = suop.find_all('div', class_="box-ketqua")
    print(box_ketqua)
    for item in box_ketqua:
        if item:
            handel_by_day(item)
    print(XSMB)

get_ketqua()