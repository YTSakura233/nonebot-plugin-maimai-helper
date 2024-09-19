import pymysql
import nonebot


from nonebot.log import logger


config = nonebot.get_driver().config
db_host = getattr(config, 'db_host')
db_user = getattr(config, 'db_user')
db_pass = getattr(config, 'db_pass')
db = getattr(config, 'db_name')


def is_hex_string(s):
    return all(c in {'e', '4', '1', '6', '7', 'c', '8', '2', '0', '5', 'b', 'd', 'a', 'f', '9', '3'} for c in s)


def find_chara_levels(all_chara_list, chara_slot_list):
    """
    根据角色槽列表，从所有角色列表中找出对应角色的等级。

    :param all_chara_list: 包含所有角色信息的列表，每个元素是一个字典，必须包含"characterId"和"level"键。
    :param chara_slot_list: 包含角色槽ID的列表，用于查找对应角色的等级。
    :return: 一个整数列表，表示对应角色槽的角色等级。如果某个角色槽没有对应的角色，则该位置的等级为0。
    """
    # 初始化角色等级列表，长度与chara_slot_list相同
    character_levels = [0] * len(chara_slot_list)
    # {"characterId":101,"point":0,"useCount":2147483647,"level":9999,"nextAwake":0,"nextAwakePercent":0,"awakening":6}
    # 创建一个角色ID到等级的映射，以提高查找效率
    chara_id_to_level = {}
    for chara in all_chara_list:
        chara_id = chara.get("characterId")
        level = chara.get("level")
        if chara_id is not None and level is not None:
            chara_id_to_level[chara_id] = int(level)

    # 使用映射更新角色槽的等级信息
    for i, chara_slot in enumerate(chara_slot_list):
        level = chara_id_to_level.get(chara_slot)
        if level is not None:
            character_levels[i] = level

    return character_levels


def find_chara_awakening(all_chara_list, chara_slot_list):
    """
    根据角色槽列表，从所有角色列表中找出对应角色的觉醒数。

    :param all_chara_list: 包含所有角色信息的列表，每个元素是一个字典，必须包含"characterId"和"level"键。
    :param chara_slot_list: 包含角色槽ID的列表，用于查找对应角色的等级。
    :return: 一个整数列表，表示对应角色槽的角色等级。如果某个角色槽没有对应的角色，则该位置的等级为0。
    """
    # 初始化角色等级列表，长度与chara_slot_list相同
    character_awakening = [0] * len(chara_slot_list)
    # {"characterId":101,"point":0,"useCount":2147483647,"level":9999,"nextAwake":0,"nextAwakePercent":0,"awakening":6}
    # 创建一个角色ID到等级的映射，以提高查找效率
    chara_id_to_level = {}
    for chara in all_chara_list:
        chara_id = chara.get("characterId")
        awakening = chara.get("awakening")
        if chara_id is not None and awakening is not None:
            chara_id_to_level[chara_id] = int(awakening)

    # 使用映射更新角色槽的等级信息
    for i, chara_slot in enumerate(chara_slot_list):
        awakening = chara_id_to_level.get(chara_slot)
        if awakening is not None:
            character_awakening[i] = awakening

    return character_awakening


def is_userid_exist(user_qq):
    """
    根据QQ号查询userid是否在数据库内

    :param user_qq: 用户QQ号
    """
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db, charset='utf8')
    try:
        with conn.cursor() as cursor:
            logger.debug(f"开始查询数据库是否有QQ号:{user_qq}对应USER_ID")
            sql = 'select * from id where qq = %s'
            result = cursor.execute(sql, (user_qq,))
            if result > 0:
                logger.success("查询成功")
                return True
            else:
                logger.success("查询无结果")
                return False
    except Exception as e:
        logger.error(f"USER_ID查询失败:{e}")
        return False
    finally:
        conn.close()


def del_user_id(user_qq, user_id):
    """
    删除对应QQ的USERID

    :param user_qq: 用户QQ号
    :param user_id: 用户USER_ID
    """
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db, charset='utf8')
    try:
        with conn.cursor() as cursor:
            logger.debug(f"开始删除QQ:{user_qq}对应USERID:{user_id}")
            sql = 'delete from id where qq = %s'
            cursor.execute(sql, (user_id,))
            conn.commit()
            logger.success("删除失败")
            return True
    except Exception as e:
        logger.error(f"删除QQ:{user_qq}对应ID{user_id}失败:{e}")
        return False
    finally:
        conn.close()


def save_user_id(user_qq, user_id):
    """
    存入对应QQ号的USER_ID

    :param user_qq: 用户QQ号
    :param user_id: 用户USER_ID
    """
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db, charset='utf8')
    try:
        if not is_userid_exist(user_qq):
            with conn.cursor() as cursor:
                logger.debug(f"开始存入QQ:{user_qq}的USERID:{user_id}")
                sql = 'insert into id (qq, userid) values (%s, %s)' % (user_qq, user_id)
                cursor.execute(sql)
                conn.commit()
                logger.success("存入成功")
                return 1
        else:
            return -1
    except Exception as e:
        logger.error(f"插入/更新QQ:{user_qq}对应USERID:{user_id}失败:{e}")
        return -2
    finally:
        conn.close()


def get_userid(user_qq):
    """
    根据QQ号查询userid

    :param user_qq: 用户QQ号
    """
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db, charset='utf8')
    try:
        if is_userid_exist(user_qq):
            with conn.cursor() as cursor:
                logger.debug(f"开始获取QQ号:{user_qq}对应USER_ID")
                sql = 'select * from id where qq = %s' % (user_qq)
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    logger.success(f'获取QQ:{user_qq}对应USER_ID成功:{row[1]}')
                    return row[1]
        else:
            logger.error(f"QQ:{user_qq}不存在USER_ID")
            return -1
    except Exception as e:
        logger.error(f"QQ:{user_qq}对应USER_ID获取失败:{e}")
        return -1
    finally:
        conn.close()

def is_token_exist(user_qq):
    """
    根据QQ号查询token是否在数据库内

    :param user_qq: 用户QQ号
    """
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db, charset='utf8')
    try:
        with conn.cursor() as cursor:
            logger.debug(f"开始查询数据库是否有QQ号:{user_qq}对应TOKEN")
            sql = 'select * from diving where qq = %s'
            result = cursor.execute(sql, (user_qq,))
            if result > 0:
                logger.success("查询成功")
                return True
            else:
                logger.success("查询无结果")
                return False
    except Exception as e:
        logger.error(f"USER_ID查询失败:{e}")
        return False
    finally:
        conn.close()


def save_user_token(user_qq, token):
    """
    存入对应QQ号的USER_ID

    :param user_qq: 用户QQ号
    :param user_token: 用户USER_TOKEN
    """
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db, charset='utf8')
    try:
        if not is_token_exist(user_qq):
            with conn.cursor() as cursor:
                logger.debug(f"开始存入QQ:{user_qq}的TOKEN:{token}")
                sql = 'insert into diving (qq, token) values (%s, %s)' % (user_qq, f"'{token}'")
                print(sql)
                cursor.execute(sql)
                conn.commit()
                logger.success("存入成功")
                return 1
        else:
            return -1
    except Exception as e:
        logger.error(f"插入/更新QQ:{user_qq}对应USERID:{token}失败:{e}")
        return -2
    finally:
        conn.close()


def get_token(user_qq):
    """
    根据QQ号查询token

    :param user_qq: 用户QQ号
    """
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db, charset='utf8')
    try:
        if is_token_exist(user_qq):
            with conn.cursor() as cursor:
                logger.debug(f"开始获取QQ号:{user_qq}对应USER_ID")
                sql = 'select * from diving where qq = %s' % (user_qq)
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    logger.success(f'获取QQ:{user_qq}对应USER_ID成功:{row[1]}')
                    return row[1]
        else:
            logger.error(f"QQ:{user_qq}不存在USER_ID")
            return -1
    except Exception as e:
        logger.error(f"QQ:{user_qq}对应USER_ID获取失败:{e}")
        return -1
    finally:
        conn.close()