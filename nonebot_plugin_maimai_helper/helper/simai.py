import hashlib
import random
import re

import time
import nonebot
from datetime import datetime, timedelta
from nonebot.log import logger

import requests

from util.net.HTTPRequest import HTTPRequest
from data import ticket_define, region_map
from util.utils import find_chara_levels, find_chara_awakening
from manager.game_data import GameDataManager

chara_manager = GameDataManager("chara")
title_manager = GameDataManager("title")
frame_manager = GameDataManager("frame")
plate_manager = GameDataManager("plate")
partner_manager = GameDataManager("partner")
icon_manager = GameDataManager("icon")


config = nonebot.get_driver().config
dateTime_constant = getattr(config, 'dateTime_constant', 114514)
region_id = getattr(config, 'region_id')
placeId = getattr(config, 'place_id')
clientId = getattr(config, 'client_id')
chimeSalt = getattr(config, 'chime_salt')
chimeHost = getattr(config, 'chime_host')
aimeHost = getattr(config, 'aime_host')


def get_user_music_details(uid: int):
    req = HTTPRequest(uid)
    data = req.Request("GetUserMusicApiMaimaiChn", {"userId": uid, "nextIndex": 0, "maxCount": 2147483647})
    return [detail for music in data["userMusicList"] for detail in music["userMusicDetailList"]]


def get_preview(uid):
    result = {"is_success": False, "is_error": False, "user_id": uid, "data": {}, "msg_body": "",
              "is_in_whitelist": False}
    login_dict = {
        "userId": uid,
        "accessCode": "",
        "regionId": region_id,
        "placeId": placeId,
        "clientId": clientId,
        "dateTime": dateTime_constant,
        "isContinue": False,
        "genericFlag": 0
    }
    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户数据")
    preview = request.Request("GetUserPreviewApiMaimaiChn", login_dict)
    preview["iconName"] = icon_manager.get_resource(preview["iconId"])
    result["data"] = preview
    result["is_success"] = True
    result["is_error"] = False
    result["msg_body"] = "成功"
    return result


def get_preview_detailed(uid):
    result = {"is_success": False, "is_error": False, "user_id": uid, "data": {}, "msg_body": "",
              "is_in_whitelist": False}
    login_dict = {
        "userId": uid,
        "accessCode": "",
        "regionId": region_id,
        "placeId": placeId,
        "clientId": clientId,
        "dateTime": dateTime_constant,
        "isContinue": False,
        "genericFlag": 0,
        "nextIndex": 0,
        "maxCount": 20
    }
    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户数据")
    preview = request.Request("GetUserPreviewApiMaimaiChn", login_dict)
    if not preview["isLogin"]:
        logger.debug("开始登入用户账号")
        login = request.Request("UserLoginApiMaimaiChn", login_dict)
        if login["returnCode"] != 1:
            result["is_got_qr_code"] = False
            result["msg_body"] = "请在微信“舞萌 | 中二”服务号上点击一次“玩家二维码”按钮后再试一遍"
            logger.error("登入失败，请在微信“舞萌 | 中二”服务号上点击一次“玩家二维码”按钮后再试一遍")
            return result
    else:
        logger.success("登入成功")
        result["is_already_login"] = True
    logger.debug("开始获取用户详细信息")
    user_data = request.Request("GetUserDataApiMaimaiChn", login_dict)
    logger.debug("开始获取用户旅行伙伴信息")
    character_list = request.Request("GetUserCharacterApiMaimaiChn", login_dict)["userCharacterList"]

    player_info = user_data["userData"]
    player_info["charaLevel"] = find_chara_levels(character_list, user_data["userData"]["charaSlot"])
    player_info["charaAwakening"] = find_chara_awakening(character_list, user_data["userData"]["charaSlot"])
    player_info["charaName"] = [chara_manager.get_resource(title_id) for title_id in user_data["userData"]["charaSlot"]]
    player_info["frameName"] = frame_manager.get_resource(user_data["userData"]["frameId"])
    player_info["plateName"] = plate_manager.get_resource(user_data["userData"]["plateId"])
    player_info["iconName"] = icon_manager.get_resource(user_data["userData"]["iconId"])
    player_info["partnerName"] = partner_manager.get_resource(user_data["userData"]["partnerId"])
    player_info["titleName"] = title_manager.get_resource(user_data["userData"]["titleId"])["title"]
    player_info["titleRare"] = title_manager.get_resource(user_data["userData"]["titleId"])["rareType"]
    player_info["banState"] = user_data["banState"]
    player_info["loginState"] = preview["isLogin"]

    result["data"] = player_info

    if not preview["isLogin"]:
        logger.debug("开始登出用户账号")
        request.Request("UserLogoutApiMaimaiChn", login_dict)

    return result


def send_ticket_new(uid, ticket_id):
    result = {"is_success": False, "is_already_had_ticket": False, "is_error": False, "user_id": uid, "data": {}, "msg_body": ""}
    login_dict = {
        "userId": uid,
        "accessCode": "",
        "regionId": region_id,
        "placeId": placeId,
        "clientId": clientId,
        "dateTime": dateTime_constant,
        "isContinue": False,
        "genericFlag": 0
    }

    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户信息")
    preview = request.Request("GetUserPreviewApiMaimaiChn", login_dict)
    user_rating = preview["playerRating"]
    logger.debug("开始获取用户游玩信息")
    resp = request.Request("GetUserRegionApiMaimaiChn", {"userId": uid})
    play_count = 0
    for i in resp["userRegionList"]:
        play_count += i["playCount"]

    logger.debug("开始获取用户功能票信息")
    charges = request.Request("GetUserChargeApiMaimaiChn", login_dict)
    had_ticket = False
    if charges["userChargeList"]:
        for charge in charges["userChargeList"]:
            if charge["stock"] > 0 and charge["chargeId"] == int(ticket_id):
                had_ticket = True
                result["is_already_had_ticket"] = True
                result["msg_body"] = "无法重复发放跑图票"
                break

    if not had_ticket:
        date_time = datetime.now()
        timestamp_str = date_time.strftime('%Y-%m-%d %H:%M:%S.0')
        expire_timestamp = (date_time + timedelta(days=90)).strftime('%Y-%m-%d 04:00:00')
        ticket_dict = {
            "userId": uid,
            "userChargelog": {
                "chargeId": ticket_id,
                "price": ticket_define[ticket_id]["cost"],
                "purchaseDate": timestamp_str,
                "playCount": play_count,
                "playerRating": user_rating,
                "placeId": placeId,
                "regionId": region_id,
                "clientId": clientId,
            },
            "userCharge": {
                "chargeId": ticket_id,
                "stock": 1,
                "purchaseDate": timestamp_str,
                "validDate": expire_timestamp
            }
        }

        try:
            logger.debug("开始充值功能票")
            result["data"] = request.Request("UpsertUserChargelogApiMaimaiChn", ticket_dict)
            result["is_success"] = True
            result["msg_body"] = "成功"
        except Exception as e:
            print(e.with_traceback(None))
            result["is_error"] = True
            result["msg_body"] = f"未知错误：{e.with_traceback(None)}"

    return result


def send_ticket(uid, ticket_id):
    result = {"is_success": False, "is_got_qr_code": True, "is_already_login": False, "is_already_had_ticket": False,
              "is_error": False, "user_id": uid, "data": {}, "msg_body": ""}
    login_dict = {
        "userId": uid,
        "accessCode": "",
        "regionId": region_id,
        "placeId": placeId,
        "clientId": clientId,
        "dateTime": dateTime_constant,
        "isContinue": False,
        "genericFlag": 0
    }

    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户信息")
    preview = request.Request("GetUserPreviewApiMaimaiChn", login_dict)
    if preview["isLogin"]:
        result["is_already_login"] = True
        result["msg_body"] = "当前用户已上机，请先下机然后再试一遍"
        return result
    else:
        logger.debug("开始登入用户账户")
        login = request.Request("UserLoginApiMaimaiChn", login_dict)
        if login["returnCode"] != 1:
            result["is_got_qr_code"] = False
            result["msg_body"] = "请在微信“舞萌 | 中二”服务号上点击一次“玩家二维码”按钮后再试一遍"
            return result
    user_data = request.Request("GetUserDataApiMaimaiChn", login_dict)
    charges = request.Request("GetUserChargeApiMaimaiChn", login_dict)

    had_ticket = False
    if charges["userChargeList"]:
        for charge in charges["userChargeList"]:
            if charge["stock"] > 0 and charge["chargeId"] == int(ticket_id):
                had_ticket = True
                result["is_already_had_ticket"] = True
                result["msg_body"] = "无法重复发放跑图票"
                break

    if not had_ticket:
        date_time = datetime.now()
        timestamp_str = date_time.strftime('%Y-%m-%d %H:%M:%S.0')
        expire_timestamp = (date_time + timedelta(days=90)).strftime('%Y-%m-%d 04:00:00')
        ticket_dict = {
            "userId": uid,
            "userChargelog": {
                "chargeId": ticket_id,
                "price": ticket_define[ticket_id]["cost"],
                "purchaseDate": timestamp_str,
                "playCount": int(user_data["userData"]["playCount"]),
                "playerRating": int(user_data["userData"]["playerRating"]),
                "placeId": placeId,
                "regionId": region_id,
                "clientId": clientId,
            },
            "userCharge": {
                "chargeId": ticket_id,
                "stock": 1,
                "purchaseDate": timestamp_str,
                "validDate": expire_timestamp
            }
        }

        try:
            logger.debug("开始充值功能票")
            result["data"] = request.Request("UpsertUserChargelogApiMaimaiChn", ticket_dict)
            result["is_success"] = True
            result["msg_body"] = "成功"
        except Exception as e:
            print(e.with_traceback(None))
            result["is_error"] = True
            result["msg_body"] = f"未知错误：{e.with_traceback(None)}"

    if not preview["isLogin"]:
        logger.debug("开始登出用户账户")
        request.Request("UserLogoutApiMaimaiChn", login_dict)

    return result


def logout(uid, timestamp=dateTime_constant):
    result = {"is_success": False, "is_error": False, "user_id": uid, "data":{}, "msg_body": ""}
    login_dict = {
        "userId": uid,
        "accessCode": "",
        "placeId": placeId,
        "regionId": region_id,
        "clientId": clientId,
        "dateTime": timestamp,
        "isContinue": False,
        "type": 5
    }
    try:
        request = HTTPRequest(uid=uid)
        logger.debug("开始登出用户账户")
        result["data"] = request.Request("UserLogoutApiMaimaiChn", login_dict)
        result["is_success"] = True
        result["msg_body"] = "成功"
    except Exception as e:
        e.with_traceback(None)
        result["data"] = None
        result["is_error"] = True
        result["msg_body"] = f"未知错误：{e.with_traceback(None)}"

    return result


def login(uid):
    result = {"is_success": False, "is_error": False, "user_id": uid, "data": {}, "msg_body": ""}
    login_dict = {
        "userId": uid,
        "accessCode": "",
        "regionId": region_id,
        "placeId": placeId,
        "clientId": clientId,
        "dateTime": dateTime_constant,
        "isContinue": False,
        "genericFlag": 0
    }

    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户信息")
    preview = request.Request("GetUserPreviewApiMaimaiChn", login_dict)
    if preview["isLogin"]:
        result["data"] = None
        result["is_already_login"] = True
        result["msg_body"] = "当前用户已上机，请先下机然后再试一遍"
        return result
    else:
        logger.debug("开始登入用户账户")
        login = request.Request("UserLoginApiMaimaiChn", login_dict)
        if login["returnCode"] != 1:
            result["data"] = login
            result["is_got_qr_code"] = False
            result["msg_body"] = "请在微信“舞萌 | 中二”服务号上点击一次“玩家二维码”按钮后再试一遍"
            return result
        else:
            result["data"] = login
            result["is_success"] = True
            result["msg_body"] = "成功"
            return result


def dump_user_all(uid):
    result = {"is_success": False, "is_got_qr_code": True, "is_error": False, "user_id": uid, "data": {},
              "msg_body": ""}

    available_attrs = ["UserData", "UserExtend", "UserOption", "UserCharacter", "UserMap", "UserLoginBonus",
                       "UserRating", "UserItem", "UserMusic", "UserCourse", "UserCharge"]
    data = {}

    login_dict = {
        "userId": uid,
        "accessCode": "",
        "regionId": region_id,
        "placeId": placeId,
        "clientId": clientId,
        "dateTime": dateTime_constant,
        "isContinue": False,
        "genericFlag": 0
    }

    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户信息")
    preview = request.Request("GetUserPreviewApiMaimaiChn", login_dict)
    if not preview["isLogin"]:
        logger.debug("开始登入用户")
        login = request.Request("UserLoginApiMaimaiChn", login_dict)
        if login["returnCode"] != 1:
            result["is_got_qr_code"] = False
            result["msg_body"] = "请在微信“舞萌 | 中二”服务号上点击一次“玩家二维码”按钮后再试一遍"
            return result
    else:
        result["is_already_login"] = True

    for ava_attr in available_attrs:
        for i in range(0, 1):
            try:
                api = f"Get{ava_attr}Api"
                final_attr = ava_attr[0].lower() + ava_attr[1:]

                query = {"userId": uid, "nextIndex": 10000000000 if final_attr == "userItem" else 0,
                         "maxCount": 2147483647}
                resp = request.Request(api, datas=query)
                if final_attr in resp:
                    match final_attr:
                        case "userActivity":
                            data["userActList"] = resp["userActivity"]["playList"] + resp["userActivity"]["musicList"]
                        case _:
                            data[final_attr] = resp[final_attr]
                else:
                    match final_attr:
                        case "userMusic":
                            data["userMusicDetailList"] = []
                            for music in resp["userMusicList"]:
                                data["userMusicDetailList"] += music["userMusicDetailList"]
                        case _:
                            data[final_attr + "List"] = resp[final_attr + "List"]
                break
            except Exception as e:
                continue

    if not preview["isLogin"]:
        logger.debug("开始登出账户")
        request.Request("UserLogoutApiMaimaiChn", login_dict)
    result["is_success"] = True
    result["msg_body"] = "成功"
    result["data"] = data
    return result


def query_ticket(uid):
    result = {"is_success": False, "is_error": False, "user_id": uid, "data": {}, "msg_body": ""}
    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户功能票信息")
    ticket = request.Request("GetUserChargeApiMaimaiChn", {"userId": uid})
    if not ticket["userChargeList"]:
        ticket["userChargeList"] = []
    result["data"] = ticket
    result["is_success"] = True
    result["is_error"] = False
    result["msg_body"] = "成功"
    return result


def get_user_region(uid):
    result = {"is_success": False, "is_error": False, "user_id": uid, "data": {}, "msg_body": ""}
    request = HTTPRequest(uid=uid)
    logger.debug("开始获取用户登入信息")
    resp = request.Request("GetUserRegionApiMaimaiChn", {"userId": uid})

    for i in range(len(resp["userRegionList"])):
        region_name = region_map[int(resp["userRegionList"][i]["regionId"]) - 1]
        resp["userRegionList"][i]["regionName"] = region_name

    result["data"] = resp
    result["is_success"] = True
    result["is_error"] = False
    result["msg_body"] = "成功"
    return result


def get_user_id_by_qr(qr_code):
    if not (qr_code.startswith("SGWCMAID") and len(qr_code) == 84 and bool(re.match(r'^[0-9A-F]+$', qr_code[20:]))):
        return {
            "userID": 0,
            "errorID": 99,
            "timestamp": datetime.now().strftime("%Y%m%d%H%M%S")[2:],
            "key": ""
        }
    return get_user_id(qr_code[20:])


def get_user_id(qr_code):
    GAME_ID = "MAID"
    AIME_SALT = chimeSalt
    AIME_HOST = aimeHost

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")[2:]
    chip_id = "A63E-01E{0:08}".format(random.randint(0, 99999999))
    key = hashlib.sha256(f"{chip_id}{timestamp}{AIME_SALT}".encode()).hexdigest().upper()
    # 别问我为什么用字符串拼接不用json.dumps()，要问去问SBGA
    data_json = f"{{\"chipID\":\"{chip_id}\",\"openGameID\":\"{GAME_ID}\",\"key\":\"{key}\",\"qrCode\":\"{qr_code}\",\"timestamp\":\"{timestamp}\"}}"

    logger.debug("开始获取用户USER_ID")
    resp = requests.post(f"{AIME_HOST}/wc_aime/api/get_data", data_json, headers={
        "User-Agent": "WC_AIME_LIB",
    })
    return resp.json()
