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


@bind_user_id.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    user_id = None
    id_result = get_user_id_by_qr(str(message))
    logger.debug(f'USERID获取结果:{id_result}')
    if id_result['errorID'] == 0:
        user_id = id_result['userID']
    elif id_result['errorID'] == 1:
        await bind_user_id.send("ReaderSetupFail")
        return
    elif id_result['errorID'] == 2:
        await bind_user_id.send("二维码可能已过期，请刷新重试")
        return
    elif id_result['errorID'] == 3:
        await bind_user_id.send("ReaderIncompatible")
        return
    elif id_result['errorID'] == 4:
        await bind_user_id.send("DBResolveFail")
        return
    elif id_result['errorID'] == 5:
        await bind_user_id.send("DBAccessTimeout")
        return
    elif id_result['errorID'] == 6:
        await bind_user_id.send("DBAccessFail")
        return
    elif id_result['errorID'] == 7:
        await bind_user_id.send("AimeIdInvalid")
        return
    elif id_result['errorID'] == 8:
        await bind_user_id.send("NoBoardInfo")
        return
    elif id_result['errorID'] == 9:
        await bind_user_id.send("LockBanSystemUser")
        return
    elif id_result['errorID'] == 10:
        await bind_user_id.send("LockBanSystem")
        return
    elif id_result['errorID'] == 11:
        await bind_user_id.send("LockBanUser")
        return
    elif id_result['errorID'] == 12:
        await bind_user_id.send("LockBan")
        return
    elif id_result['errorID'] == 13:
        await bind_user_id.send("LockSystem")
        return
    elif id_result['errorID'] == 14:
        await bind_user_id.send("LockUser")
        return
    else:
        await bind_user_id.send("查询ID失败")
        return
    if save_user_id(user_qq, user_id) == 1:
        await bind_user_id.send("绑定成功")
    elif save_user_id(user_qq, user_id) == -1:
        await bind_user_id.send("请先联系机修解绑账号")
    elif save_user_id(user_qq, user_id) == -2:
        await bind_user_id.send("绑定错误，请联系机修。")
    else:
        await bind_user_id.send("绑定错误，请联系机修。")


@seeme.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    user_id = None
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
    else:
        await seeme.send("请先绑定账号")
    if user_id != -1:
        data = get_preview(user_id)
        if data['is_success']:
            await seeme.send(
                f"玩家昵称：\t{data['data']['userName']}\n"
                f"玩家Rating：\t{data['data']['playerRating']}\n"
                f"总觉醒数：\t{data['data']['totalAwake']}\n"
                f"头像：\t{data['data']['iconName']}\n"
                f"最近登录系统号：\t{data['data']['lastRomVersion']}\n"
                f"最近登录版本号：\t{data['data']['lastDataVersion']}\n"
                f"上次登陆时间：\t{data['data']['lastLoginDate']}\n"
                f"上次游玩时间：\t{data['data']['lastPlayDate']}\n"
                f"是否登入：\t{data['data']['isLogin']}\n"
                f"banState：\t{data['data']['banState']}\n"
            )
        else:
            await seeme.send("获取失败，请联系机修。")


@maihelp.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    await maihelp.send(
        "maimai插件帮助\n"
        "绑定账号 - 发送二维码解析出来的内容\n"
        "查询账号 - 发送'seeme'\n"
        "发2/3/5/6倍券 - 发送'发券2/3/5/6'\n"
        "查询账户内剩余功能票 - 发送'ticket'\n"
        "登入账号 - 发送login\n"
        "登出账号 - 发送logout(仅限通过本机器人登入的账号)"
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
            await ticket.send("参数错误")
            raise ValueError("匹配的不是有效的数字")
    else:
        await ticket.send("请输入参数")
        return
    if is_userid_exist(user_qq):
        # 判断是否存在userid
        user_id = get_userid(user_qq)
    else:
        await ticket.send("请先绑定账号")
        return

    if ticket_id == 2:
        result = send_ticket(user_id, 2)
        if result["is_success"]:
            await ticket.send("发送成功")
        else:
            await ticket.send(f"发送失败,{result['msg_body']}")
            return
    elif ticket_id == 3:
        result = send_ticket(user_id, 3)
        if result["is_success"]:
            await ticket.send("发送成功")
        else:
            await ticket.send(f"发送失败,{result['msg_body']}")
            return
    elif ticket_id == 5:
        result = send_ticket(user_id, 5)
        if result["is_success"]:
            await ticket.send("发送成功")
        else:
            await ticket.send(f"发送失败,{result['msg_body']}")
            return
    elif ticket_id == 6:
        result = send_ticket(user_id, 6)
        if result["is_success"]:
            await ticket.send("发送成功")
        else:
            await ticket.send(f"发送失败,{result['msg_body']}")
            return
    else:
        await ticket.send("无效参数请重新输入")
        return


@g_login.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
        result = login(user_id)
        if result["data"]:
            if result["data"]["returnCode"] == 1:
                await g_login.send("登入成功")
            else:
                await g_login.send(f"登入失败,{result['msg_body']}")
        else:
            await g_login.send(f"登入失败,{result['msg_body']}")
    else:
        await g_login.send("请先绑定账号")


@g_logout.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
        result = logout(user_id, 114514)
        if result["data"]:
            if result["data"]["returnCode"] == 1:
                await g_logout.send("登出成功")
            else:
                await g_logout.send(f"登出失败,{result['msg_body']}")
        else:
            await g_logout.send(f"登出失败,{result['msg_body']}")
    else:
        await g_logout.send("请先绑定账号")


@tickets.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    user_qq = event.get_user_id()
    if is_userid_exist(user_qq):
        user_id = get_userid(user_qq)
        result = query_ticket(user_id)
        if len(result["data"]["userChargeList"]) != 5:
            await tickets.send("请先在本版本游戏登陆一次")
        else:
            await tickets.send(
                f"您有：\n"
                f"2倍券：{result['data']['userChargeList'][0]['stock']}张\n"
                f"3倍券：{result['data']['userChargeList'][1]['stock']}张\n"
                f"5倍券：{result['data']['userChargeList'][2]['stock']}张\n"
                f"6倍券：{result['data']['userChargeList'][3]['stock']}张\n"
                f"联合券：{result['data']['userChargeList'][4]['stock']}张\n"
            )
    else:
        await tickets.send("请先绑定账号")
