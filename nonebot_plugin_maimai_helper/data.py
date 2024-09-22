import os
from datetime import datetime
from manager.usage_count import NetworkCount


root_path = os.path.dirname(__file__)
network_count = NetworkCount()


start_time = datetime.now()

# constants
ticket_define = {
    2:{
        "id": 2,
        "cost": 1
    },
    3:{
        "id": 3,
        "cost": 2
    },
    4:{
        "id": 4,
        "cost": 3
    },
    5:{
        "id": 5,
        "cost": 4
    },
    6:{
        "id": 6,
        "cost": 5
    },
    20020:{
        "id": 20020,
        "cost": 3
    }
}
region_map = (
    "北京市",
    "重庆市",
    "上海市",
    "天津市",
    "安徽省",
    "福建省",
    "甘肃省",
    "广东省",
    "贵州省",
    "海南省",
    "河北省",
    "黑龙江省",
    "河南省",
    "湖北省",
    "湖南省",
    "江苏省",
    "江西省",
    "吉林省",
    "辽宁省",
    "青海省",
    "陕西省",
    "山东省",
    "山西省",
    "四川省",
    "台湾省",
    "云南省",
    "浙江省",
    "广西壮族自治区",
    "内蒙古自治区",
    "宁夏回族自治区",
    "新疆维吾尔自治区",
    "西藏自治区"
)

mai_genres = [
    {
        "id": 101,
        "title": "流行&动漫",
        "genre": "POPSアニメ"
    },
    {
        "id": 102,
        "title": "niconico＆VOCALOID™",
        "genre": "niconicoボーカロイド"
    },
    {
        "id": 103,
        "title": "东方Project",
        "genre": "東方Project"
    },
    {
        "id": 104,
        "title": "其他游戏",
        "genre": "ゲームバラエティ"
    },
    {
        "id": 105,
        "title": "舞萌",
        "genre": "maimai"
    },
    {
        "id": 106,
        "title": "音击/中二节奏",
        "genre": "オンゲキCHUNITHM"
    },
    {
        "id": 107,
        "title": "宴会場",
        "genre": "宴会場"
    }
]
mai_versions = [
    {
        "id": 0,
        "title": "maimai",
        "version": 10000
    },
    {
        "id": 1,
        "title": "maimai PLUS",
        "version": 11000
    },
    {
        "id": 2,
        "title": "GreeN",
        "version": 12000
    },
    {
        "id": 3,
        "title": "GreeN PLUS",
        "version": 13000
    },
    {
        "id": 4,
        "title": "ORANGE",
        "version": 14000
    },
    {
        "id": 5,
        "title": "ORANGE PLUS",
        "version": 15000
    },
    {
        "id": 6,
        "title": "PiNK",
        "version": 16000
    },
    {
        "id": 7,
        "title": "PiNK PLUS",
        "version": 17000
    },
    {
        "id": 8,
        "title": "MURASAKi",
        "version": 18000
    },
    {
        "id": 9,
        "title": "MURASAKi PLUS",
        "version": 18500
    },
    {
        "id": 10,
        "title": "MiLK",
        "version": 19000
    },
    {
        "id": 11,
        "title": "MiLK PLUS",
        "version": 19500
    },
    {
        "id": 12,
        "title": "FiNALE",
        "version": 19900
    },
    {
        "id": 13,
        "title": "舞萌DX",
        "version": 20000
    },
    {
        "id": 15,
        "title": "舞萌DX 2021",
        "version": 21000
    },
    {
        "id": 17,
        "title": "舞萌DX 2022",
        "version": 22000
    },
    {
        "id": 19,
        "title": "舞萌DX 2023",
        "version": 23000
    },
    {
        "id": 21,
        "title": "舞萌DX 2024",
        "version": 24000
    }
]

