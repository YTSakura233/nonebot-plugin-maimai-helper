from nonebot import on_command, on_regex, on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import EventMessage
from nonebot.permission import SUPERUSER

from helper.simai import *
from util.utils import *
from helper.diving_fish import *
from update_music_list import *

bind_user_id = on_startswith(('SGWCMAID'), ignorecase=False)
seeme = on_command('seeme', aliases={'看我', '审视党性'}, priority=20)
maihelp = on_command('maihelp', priority=20)
g_login = on_command('login', priority=20)
g_logout = on_command('logout', priority=20)
tickets = on_command('ticket',aliases={'查票'}, priority=20)
trick = on_command('舞萌足迹', priority=20)
token_bind = on_command("bind", priority=20)
gb = on_command("gb", priority=20)
up_list = on_command('uplist', priority=20, permission=SUPERUSER)


def check_time():
    current_hour = datetime.now().hour
    if 3 <= current_hour < 7:
        return False
    else:
        return True


@bind_user_id.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
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
    else:
        await bind_user_id.send([MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])

@seeme.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
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
    else:
        await bind_user_id.send([MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])

@maihelp.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    await maihelp.send(
        "maimai插件帮助 - Ver.1.2.2\n"
        "绑定账号 - 发送二维码解析出来的内容 - SGWCMAID123456\n"
        "查询账号 - 发送'seeme'\n"
        "发2/3/5/6倍券 - 发送'发券2/3/5/6'\n"
        "(发券7 可发送中二·舞萌联合2倍券)\n"
        "查询账户内剩余功能票 - 发送'ticket'\n"
        "登入账号 - 发送login\n"
        "登出账号 - 发送logout(仅限通过本机器人登入的账号)\n"
        "游玩足迹 - 发送'舞萌足迹'\n"
        "绑定查分器 - 发送'bind+查分器token'\n"
        "更新b50 - 发送'gb'\n"
        "更新水鱼乐曲列表 - 发送'uplist'(仅限机修)\n"
        "请勿在凌晨三点至凌晨七点内使用本Bot！！\n"
    )


ticket = on_regex(r"发券(\d+)", priority=20)
@ticket.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
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
        elif ticket_id == 7:
            result = send_ticket(user_id, 20020)
            if result["is_success"]:
                await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("购买成功喽\(^o^)/~")])
            else:
                await ticket.send(
                    [MessageSegment.reply(event.message_id), MessageSegment.text(f"购买失败了,{result['msg_body']}")])
        else:
            await ticket.send([MessageSegment.reply(event.message_id), MessageSegment.text("你想发什么券呢？")])
            return
    else:
        await bind_user_id.send([MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])

@g_login.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
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
    else:
        await bind_user_id.send([MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])


@g_logout.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
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
    else:
        await bind_user_id.send([MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])


@tickets.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
        user_qq = event.get_user_id()
        if is_userid_exist(user_qq):
            user_id = get_userid(user_qq)
            result = query_ticket(user_id)
            ticketlist = [MessageSegment.reply(event.message_id),]
            for ticket in result['data']['userChargeList']:
                if ticket['chargeId'] == 2:
                    ticketlist.append(MessageSegment.text(f"您有2倍券:{ticket['stock']}张\n"))
                elif ticket['chargeId'] == 3:
                    ticketlist.append(MessageSegment.text(f"您有3倍券:{ticket['stock']}张\n"))
                elif ticket['chargeId'] == 5:
                    ticketlist.append(MessageSegment.text(f"您有5倍券:{ticket['stock']}张\n"))
                elif ticket['chargeId'] == 6:
                    ticketlist.append(MessageSegment.text(f"您有6倍券:{ticket['stock']}张\n"))
                elif ticket['chargeId'] == 20020:
                    ticketlist.append(MessageSegment.text(f"您有联合券:{ticket['stock']}张\n"))
            await tickets.send(ticketlist)
        else:
            await tickets.send([MessageSegment.reply(event.message_id), MessageSegment.text("先绑定账号叭")])
    else:
        await bind_user_id.send([MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])


@trick.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
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
    else:
        await bind_user_id.send([MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])


@token_bind.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
        token = str(event.message)[4:].strip()
        user_qq = event.get_user_id()
        if token and len(token) == 128:
            if is_token_exist(user_qq):
                await token_bind.send([MessageSegment.reply(event.message_id), MessageSegment.text("请先联系机修解绑token")])
            else:
                if save_user_token(user_qq, token) == 1:
                    await token_bind.send([MessageSegment.reply(event.message_id), MessageSegment.text("绑定成功,请及时撤回token")])
                elif save_user_token(user_qq, token) == -1:
                    await token_bind.send(
                        [MessageSegment.reply(event.message_id), MessageSegment.text("请先联系机修解绑token")])
                elif save_user_token(user_qq, token) == -2:
                    await token_bind.send(
                        [MessageSegment.reply(event.message_id), MessageSegment.text("绑定错误，请联系机修。")])
        else:
            await token_bind.send("请正确输入token")
    else:
        await bind_user_id.send(
            [MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])


@gb.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    if check_time():
        user_qq = event.get_user_id()
        if not is_token_exist(user_qq):
            await gb.send([MessageSegment.reply(event.message_id), MessageSegment.text("请先绑定token")])
        else:
            if not is_userid_exist(user_qq):
                await gb.send([MessageSegment.reply(event.message_id), MessageSegment.text("请先绑定账号")])
            else:
                await gb.send([MessageSegment.reply(event.message_id), MessageSegment.text("正在更新b50，请耐心等待，不要重复发送")])
                token = get_token(user_qq)
                user_id = get_userid(user_qq)
                old_data = dump_user_all(user_id)
                if not old_data['is_success']:
                    await gb.finish([MessageSegment.reply(event.message_id), MessageSegment.text(f"更新失败，{old_data['msg_body']}")])
                else:
                    old_data = old_data['data']['userMusicDetailList']
                try:
                    print(-1)
                    new_data, n = change_data(old_data)
                    print(0)
                    result = send_user_data(new_data, token)
                    print(1)
                    if result['status'] == 200:
                        await gb.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"更新成功，发送{n}首歌曲")])
                    else:
                        await gb.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"更新失败了，请联系机修查看错误信息，{result['msg']}")])
                except Exception as e:
                    await gb.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"更新失败，请联系机修查看错误信息，{e}")])
    else:
        await bind_user_id.send(
            [MessageSegment.reply(event.message_id), MessageSegment.text("现在为服务器维护时间，本功能暂停使用")])


@up_list.handle()
async def _(event: GroupMessageEvent, message: Message = EventMessage()):
    try:
        update_music_list()
        await up_list.send([MessageSegment.reply(event.message_id), MessageSegment.text("更新成功")])
    except Exception as e:
        await up_list.send([MessageSegment.reply(event.message_id), MessageSegment.text(f"更新失败,{e}")])
