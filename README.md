<div align="center">

  <a href="https://v2.nonebot.dev/">
    <img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot">
  </a>

# nonebot-plugin-maimai-helper

_✨ [Nonebot2](https://github.com/nonebot/nonebot2) 插件，用于maimaiDX的相关辅助性功能 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/noneplugin/nonebot-plugin-petpet" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/nonebot-2.0.0rc1+-red.svg" alt="NoneBot">
    <a href="https://pypi.org/project/nonebot-plugin-maimai-helper">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-maimai-helper?logo=python&logoColor=edb641" alt="pypi">
  </a>
</p>

</div>


### 安装

- 使用 pip

```
    pip install nonebot-plugin-maimai-helper
```

- 直接下载

```
    直接下载本项目至nonebot的插件目录内，并在配置文件中启用本插件
```


### 数据库

请建立如下配置数据库
#### 表1
```
    表名：id
```
```
    字段1：qq
    字段2：userid
```
#### 表2
```
    表名：diving
```
```
    字段1：qq
    字段2：token
```


### 配置项

> 以下配置项可在 `.env.*` 文件中设置，具体参考 [NoneBot 配置方式](https://v2.nonebot.dev/docs/tutorial/configuration#%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F)
> 以下配置缺一不可，必须全部正确配置，否则插件无法运行。

#### `SUPERUSERS`
 - 类型：`list`
 - 默认：`[]`
 - 说明：机修的QQ号，nonebot1请在.env进行配置,nonebot2请在bot.py内的init内进行配置

#### `ticket`
 - 类型：`bool`
 - 默认：`True`
 - 说明：是否开启发票功能。（true/false）

#### `aes_key`
 - 类型：`str`
 - 默认：`EQ:R@`
 - 说明：服务器请求的相关加密信息，请自行寻找

#### `aes_iv `
 - 类型：`str`
 - 默认：`;1ovXa`
 - 说明：服务器请求的相关加密信息，请自行寻找

#### `db_host `
 - 类型：`str`
 - 默认：`localhost`
 - 说明：存储用户信息的数据库地址

#### `db_user`
 - 类型：`str`
 - 默认：`root`
 - 说明：存储用户信息的数据库用户名

#### `db_pass`
 - 类型：`str`
 - 默认：`<PASSWORD>`
 - 说明：存储用户信息的数据库密码

#### `db_name`
 - 类型：`str`
 - 默认：`aime`
 - 说明：存储用户信息的数据库名

#### `datatime_constant`
 - 类型：`int`
 - 默认：`114514`
 - 说明：用于登入登出的时间戳

#### `region_id`
 - 类型：`int`
 - 默认：`114514`
 - 说明：服务器交互有关参数，请自行寻找

#### `place_id`
 - 类型：`int`
 - 默认：`115414`
 - 说明：服务器交互有关参数，请自行寻找

#### `client_id`
 - 类型：`int`
 - 默认：`ABCDEFG`
 - 说明：服务器交互有关参数，请自行寻找

#### `chime_salt`
 - 类型：`str`
 - 默认：`PArBXE`
 - 说明：服务器交互有关加密参数，请自行寻找

#### `chime_host`
 - 类型：`str`
 - 默认：`localhost`
 - 说明：游戏相关服务器地址，请自行寻找

#### `aime_host`
 - 类型：`str`
 - 默认：`http://localhost`
 - 说明：游戏相关服务器地址，请自行寻找

#### `obfuscate_param`
 - 类型：`str`
 - 默认：`12Aacc`
 - 说明：服务器交互有关加密参数，请自行寻找

#### `title_host`
 - 类型：`str`
 - 默认：`https://localhost`
 - 说明：游戏相关服务器地址，请自行寻找


### 使用

**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空: `.env.*` 文件中设置 `COMMAND_START=[""]`**

**请勿在凌晨3点至凌晨7点使用本插件！！！**

#### 绑定账号

前缀 + 玩家二维码解析内容，如： SGWCMAID123456

本命令将会绑定玩家游戏账号信息到数据库

暂时还没写撤回，请提醒玩家及时撤回二维码内容


#### 查询账号

前缀 + seeme

会发送玩家简略游戏信息


#### 功能券发送

前缀 + 发券2/3/5/6，如：发券6

会向玩家账号内发送对应倍数的功能券


#### 查询账户剩余功能票

前缀 + ticket

会发送玩家账户内目前剩余功能票


#### 登入账号

前缀 + login

将会使玩家账户处于登录状态


#### 登出账号

前缀 + logout

将会登出玩家账号（仅支持由本插件登入的账户）


#### 查询足迹

前缀 + 舞萌足迹

可以查看在哪些地区玩过舞萌


#### 绑定token

前缀 + bind + 水鱼token

即可绑定token至机器人


#### 更新b50

前缀 + gb

即可更新b50


#### 更新水鱼歌曲列表（针对机修）

前缀 + uplist

建议定期执行一次


### 特别感谢

- [Error063/maibox_opensource](https://github.com/Error063/maibox_opensource) 面向微信公众平台的舞萌bot的实现
- [monkeycathyd/mai2_revive_fix](https://github.com/monkeycathyd/mai2_revive_fix) Mai 批复活 | MaiMai 逃离小黑屋