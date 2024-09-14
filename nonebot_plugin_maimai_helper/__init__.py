from nonebot import on_command, on_regex, on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import EventMessage

from helper.simai import *
from util.utils import save_user_id, get_userid, is_userid_exist

bind_user_id = on_startswith(('SGWCMAID'), ignorecase=False)
seeme = on_command('seeme', aliases={'看我', '审视党性'}, priority=20)
maihelp = on_command('maihelp', priority=20)
g_login = on_command('login', priority=20)
g_logout = on_command('logout', priority=20)
tickets = on_command('ticket',aliases={'查票'}, priority=20)
trick = on_command('舞萌足迹', priority=20)


@bind_user_id.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    user_id = None
    id_result = get_user_id_by_qr(str(message))
    logger.debug(f'USERID获取结果:{id_result}')
    errorResult = {
        1: "ReaderSetupFail", 2: "二维码可能已过期", 3: "ReaderIncompatible", 4: "DBResolveFail",
        5: "DBAccessTimeout", 6: "DBAccessFail", 7: "AimeIdInvalid", 8: "NoBoardInfo",
        9: "LockBanSystemUser", 10: "LockBanSystem", 11: "LockBanUser", 12: "LockBan",
        13: "LockSystem", 14: "LockUser"
    }
    if id_result['errorID'] == 0:
        user_id = id_result['userID']
    else:
        await bind_user_id.finish([MessageSegment.reply(event.message_id), MessageSegment.text(f"查询ID失败:{errorResult[id_result['errorID']]}")])
    if save_user_id(user_qq, user_id) == 1:
        await bind_user_id.finish([MessageSegment.reply(event.message_id), MessageSegment.text("绑定成功")])
    elif save_user_id(user_qq, user_id) == -1:
        await bind_user_id.finish([MessageSegment.reply(event.message_id), MessageSegment.text("请先联系机修解绑账号")])
    elif save_user_id(user_qq, user_id) == -2:
        await bind_user_id.finish([MessageSegment.reply(event.message_id), MessageSegment.text("绑定错误，请联系机修。")])
    else:
        await bind_user_id.finish([MessageSegment.reply(event.message_id), MessageSegment.text("绑定错误，请联系机修。")])


@seeme.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    user_id = None
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
    else:
        await seeme.send("请先绑定账号")
    if user_id != -1:
        data = get_preview_detailed(user_id)
        if data["is_got_qr_code"]:
            await seeme.send([MessageSegment.reply(event.message_id), MessageSegment.text(
                f"玩家昵称：\t{data['data']['userName']}\n"
                f"玩家Rating：\t{data['data']['playerRating']}\n"
                f"总觉醒数：\t{data['data']['totalAwake']}\n"
                f"头像：\t{data['data']['iconName']}\n"
                f"背景板：\t{data['data']['frameName']}\n"
                f"姓名框：\t{data['data']['plateName']}\n"
                f"称号：\t{data['data']['titleName']}\n"
                f"搭档：\t{data['data']['partnerName']}\n"
                f"最近登录系统号：\t{data['data']['lastRomVersion']}\n"
                f"最近登录版本号：\t{data['data']['lastDataVersion']}\n"
                f"上次登陆时间：\t{data['data']['lastLoginDate']}\n"
                f"最后游玩时间：\t{data['data']['lastPlayDate']}\n"
                f"玩家注册时间：\t{data['data']['firstPlayDate']}\n"
                f"游玩次数：\t{data['data']['playCount']}\n"
                f"当前游玩区域：\t{data['data']['lastSelectCourse']}\n"
                f"旅行伙伴名称：\t{data['data']['charaName']}\n"
                f"旅行伙伴等级：\t{data['data']['charaLevel']}\n"
                f"旅行伙伴觉醒数：\t{data['data']['charaAwakening']}\n"
                f"banState：\t{data['data']['banState']}\n"
            )
                              ])
        else:
            data1 = get_preview(user_id)
            if data1['is_success']:
                await seeme.send([MessageSegment.reply(event.message_id), MessageSegment.text(
                    f"玩家昵称：\t{data1['data']['userName']}\n"
                    f"玩家Rating：\t{data1['data']['playerRating']}\n"
                    f"总觉醒数：\t{data1['data']['totalAwake']}\n"
                    f"头像：\t{data1['data']['iconName']}\n"
                    f"最近登录系统号：\t{data1['data']['lastRomVersion']}\n"
                    f"最近登录版本号：\t{data1['data']['lastDataVersion']}\n"
                    f"上次登陆时间：\t{data1['data']['lastLoginDate']}\n"
                    f"上次游玩时间：\t{data1['data']['lastPlayDate']}\n"
                    f"是否登入：\t{data1['data']['isLogin']}\n"
                    f"banState：\t{data1['data']['banState']}\n"
                    f"在公众号获取二维码后可以查看更多信息哟~"
                )])
            else:
                await seeme.send([MessageSegment.reply(event.message_id), MessageSegment.text("获取失败，请联系机修。")])


@maihelp.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    await maihelp.send(
        "maimai插件帮助\n"
        "绑定账号 - 发送二维码解析出来的内容 - SGWCMAID123456\n"
        "查询账号 - 发送'seeme'\n"
        "发2/3/5/6倍券 - 发送'发券2/3/5/6'\n"
        "查询账户内剩余功能票 - 发送'ticket'\n"
        "登入账号 - 发送login\n"
        "登出账号 - 发送logout(仅限通过本机器人登入的账号)\n"
        "游玩足迹 - 发送'舞萌足迹'\n"
    )


ticket = on_regex(r"发券(\d+)", priority=20)
@ticket.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    regex = r"发券(\d+)"
    user_qq = event.get_user_id()
    user_id = None
    ticket_id = None
    match = re.search(regex, str(event.get_message()))
    if match:
        try:
            ticket_id = int(match.group(1))
        except ValueError:
            await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("世嘉现在还不支持这种券哟~")])
            raise ValueError("匹配的不是有效的数字")
    else:
        await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("你想发什么券呢？")])
        return
    if is_userid_exist(user_qq):
        # 判断是否存在userid
        user_id = get_userid(user_qq)
    else:
        await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("先绑定账号叭~")])
        return

    if ticket_id == 2:
        result = send_ticket(user_id, 2)
        if result["is_success"]:
            await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("购买成功喽\(^o^)/~")])
        else:
            await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"购买失败了,{result['msg_body']}")])
            return
    elif ticket_id == 3:
        result = send_ticket(user_id, 3)
        if result["is_success"]:
            await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("购买成功喽\(^o^)/~")])
        else:
            await ticket.send(
                [MessageSegment.reply(event.message_id), MessageSegment.text(f"购买失败了,{result['msg_body']}")])
            return
    elif ticket_id == 5:
        result = send_ticket(user_id, 5)
        if result["is_success"]:
            await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("购买成功喽\(^o^)/~")])
        else:
            await ticket.send(
                [MessageSegment.reply(event.message_id), MessageSegment.text(f"购买失败了,{result['msg_body']}")])
            return
    elif ticket_id == 6:
        result = send_ticket(user_id, 6)
        if result["is_success"]:
            await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("购买成功喽\(^o^)/~")])
        else:
            await ticket.send(
                [MessageSegment.reply(event.message_id), MessageSegment.text(f"购买失败了,{result['msg_body']}")])
            return
    else:
        await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("你想发什么券呢？")])
        return


@g_login.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
        result = login(user_id)
        if result["data"]:
            if result["data"]["returnCode"] == 1:
                await g_login.send([MessageSegment.reply(event.message_id), MessageSegment.text("登入成功啦！")])
            else:
                await g_login.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"登入失败了,{result['msg_body']}")])
        else:
            await g_login.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"登入失败了,{result['msg_body']}")])
    else:
        await g_login.send([MessageSegment.reply(event.message_id), MessageSegment.text("先绑定账号叭")])


@g_logout.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
        result = logout(user_id, 114514)
        if result["data"]:
            if result["data"]["returnCode"] == 1:
                await g_logout.send([MessageSegment.reply(event.message_id), MessageSegment.text("登出成功啦")])
            else:
                await g_logout.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"登出失败了,{result['msg_body']}")])
        else:
            await g_logout.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"登出失败了,{result['msg_body']}")])
    else:
        await g_logout.send([MessageSegment.reply(event.message_id), MessageSegment.text("先绑定账号叭")])


@tickets.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
        result = query_ticket(user_id)
        if len(result["data"]["userChargeList"]) != 5:
            await tickets.send([MessageSegment.reply(event.message_id), MessageSegment.text("需要先在本版本游戏登陆一次哟")])
        else:
            await tickets.send([MessageSegment.reply(event.message_id), MessageSegment.text(
                f"您有：\n"
                f"2倍券：{result['data']['userChargeList'][0]['stock']}张\n"
                f"3倍券：{result['data']['userChargeList'][1]['stock']}张\n"
                f"5倍券：{result['data']['userChargeList'][2]['stock']}张\n"
                f"6倍券：{result['data']['userChargeList'][3]['stock']}张\n"
                f"联合券：{result['data']['userChargeList'][4]['stock']}张\n"
            )
                                ])
    else:
        await tickets.send([MessageSegment.reply(event.message_id), MessageSegment.text("先绑定账号叭")])


@trick.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
        USERID = True
    else:
        USERID = False
        await trick.send('请先绑定账号叭')
    if USERID:
        tricklist = [MessageSegment.reply(event.message_id),]
        data = get_user_region(user_id)['data']['userRegionList']
        for place in data:
            tricklist.append(
                MessageSegment.text(
                    f"您在{place['regionName']}游玩过{place['playCount']}次\n"
                    f"最初游玩时间为{place['created']}\n"
                )
            )
        await trick.send(tricklist)