# -*- coding: UTF-8 -*-
from song import Song
from PIL import Image, ImageDraw2, ImageFont
from MusicBoxApi import api as NetEaseApi
from ncmbot.ncmbot import *

import os
import json
import getpass
import platform
from math import ceil
from time import sleep


def separator():
    try:
        print("-" * os.get_terminal_size().columns)
    except OSError:
        print("-" * 17)


# 请求歌单详细信息的尺寸大小
# 过大会导致请求失败
chunk_size = 100

buf_image = Image.new('RGB', (1024, 60), color='white')
buf_obj = ImageDraw2.Draw(buf_image)

netease = NetEaseApi.NetEase()

playlist = []
padding = 9
safe_ratio = 1.4

separator()
font_name = input(
    """请输入用于判定的字体名称：
    Windows 建议 msyh.ttc（默认）或 Arial。
    macOS 建议 PingFang（默认）或 Songti。
    Linux 建议思源体系列。
为了显示效果考虑，请尽量选择非等宽字体。
直接按 Enter 来选择默认值
>>> """)

if len(font_name) == 0:
    sysstr = platform.system()
    if sysstr == "Windows":
        font_name = "msyh.ttc"
    elif sysstr == "Darwin":
        font_name = "PingFang"
    else:
        font_name = "FreeSans"


try:
    font = ImageDraw2.Font('black', font_name, 60)
    font_small = ImageDraw2.Font('black', font_name, 30)
except:
    print('%s 不是可用的字体文件。' % font_name)
    exit(-1)


def get_pixel_width(string):
    if string == None:
        return 0
    # 画到 BUF_OBJ 上，获取其宽度像素值
    size_tuple = buf_obj.textsize(string, font)
    if len(size_tuple) == 2:
        return size_tuple[0]
    return 0


while True:
    separator()
    try:
        option = int(
            input("想要如何登录到网易云音乐？\n\t1 - 用账号和密码\n\t2 - 用 HTTP Cookie\n>>> "))
    except KeyboardInterrupt:
        exit(0)
    except:
        continue
    if option == 1:
        separator()
        login_name = input("输入手机号码…\n>>> ")
        # if len(login_name) != 11:
        #     print('%s 不是合法的手机号码。' % login_name)
        #     exit(-2)

        login_password = getpass.getpass("以及密码…\n>>> ")

        # if '@' in login_name:
        #     bot, resp = login(login_password, email=login_name)
        # else:
        bot, resp = login(login_password, phone=login_name)

        # print(json.dumps(dict(resp.headers)))
        # print(resp.content.decode())

        login_resp = json.loads(json.dumps(dict(resp.headers)))['Set-Cookie']

    elif option == 2:
        separator()
        cookie_content = input("输入 Cookie 内容…\n>>> \n")
        login_resp = cookie_content

    try:
        MUSIC_U = login_resp.split('MUSIC_U=')[1].split(';')[0]
        user_token = login_resp.split('__csrf=')[1].split(';')[0]

        bot = NCloudBot(MUSIC_U)
        break
    except KeyboardInterrupt:
        exit(0)
    except:
        print("发生问题。请再试一次。")

separator()


try:
    playlist_id = input("请输入歌单 ID 或 URL…\n>>> ").split('&userid=')[0]       \
        .replace("https://music.163.com/#/playlist?id=", "")                    \
        .replace("https://music.163.com/#/my/m/music/playlist?id=", "")         \
        .replace("https://music.163.com/playlist?id=", "")

    bot.method = 'PLAY_LIST_DETAIL'
    bot.params = {"csrf_token": user_token}
    bot.data = {"id": playlist_id, "limit": 10000, "csrf_token": user_token}
    bot.send()

    trackids = json.loads(bot.response.content.decode())[
        'playlist']['trackIds']

    c = []
    for song in trackids:
        c.append({'id': song['id']})

    datalist = []

    for i in range(ceil(len(c) / chunk_size)):
        part = c[i * chunk_size: min((i + 1) * chunk_size, len(c))]
        bot.data = {'c': json.dumps(
            part), 'ids': part, "csrf_token": user_token}
        bot.method = 'SONG_DETAIL'
        bot.send()

        datalist += json.loads(bot.response.content.decode())['songs']

        print('\r获取歌曲 %d 之 %d…' %
              (min((i + 1) * chunk_size, len(c)), len(c)), end='')

        sleep(1)

    print()
except KeyboardInterrupt:
    exit(0)
except:
    print('请求 %s 失败。请检查歌单 ID 及网络连接。' % playlist_id)
    exit(-2)

# print(datalist)
# input()
separator()

try:
    sort_by = input("""想要依照哪个字段进行排序？
\tn - 依照歌曲名称（Name）进行排序（默认）
\ta - 依照专辑名称（Album）进行排序
\tr - 依照艺术家（aRtist）进行排序
>>> """).lower()[0]
except:
    sort_by = 'n'


for song in datalist:

    new_song = Song()
    # print(song)
    # input()

    try:
        new_song.id = song["id"]
        new_song.name = song["name"]
        new_song.album = song["al"]["name"]
        artists = []
        if type(song["ar"]) == list:
            for artist in song["ar"]:
                artists.append(artist["name"])
            new_song.artist = ' / '.join(artists)
        elif type(song["ar"] == str):
            new_song.artist = song["ar"]
        else:
            new_song.artist = ''

        if sort_by == 'a':
            playlist.sort(key=lambda x: x.album)
        elif sort_by == 'r':
            playlist.sort(key=lambda x: x.artist)
        else:
            new_song.name_size = get_pixel_width(new_song.name)
            playlist.sort(key=lambda x: x.name_size)
        playlist.append(new_song)
    except:
        print("在解析 ID「%s」的歌曲时发生错误。已将其抛弃。" %
              str(new_song.id) if new_song.id else '不明')

#playlist.sort(key=lambda x: x.name_size)

track_ids = []


# for item in playlist:
#     print("歌曲名称 = %s, 相对长度 = %d" % (item.name, item.name_size))
# results.append(item.name)
# results.append("%s - %s\n" % (item.artist, item.album))
# if item.name_size > max_width:
#     max_width = item.name_size

separator()
controller = input(
    "处理了 %d 首歌。\n按回车来创建新歌单。或者，在此之前输入 i 来从长到短地排列歌曲。\n>>> " % len(playlist))

if controller != 'I' and controller != 'i':
    playlist.reverse()


separator()
playlist_name = input("请输入要创建的新歌单名…\n>>> ")

# input(MUSIC_U)
bot.method = 'CREATE_LIST'
bot.params = {"csrf_token": user_token}
bot.data = {"name": str(playlist_name), "csrf_token": user_token}
bot.send()

result = json.loads(bot.response.content.decode())

separator()
if result['code'] != 200:
    print("创建歌单失败。")
    exit(-4)

new_playlist_id = result['id']
sleep(0.5)
# separator()
# print(result)

# separator()


for p in playlist:
    # print(repr(p.id))
    track_ids.append(p.id)

for i in range(ceil(len(track_ids) / chunk_size)):
    song_chunk = track_ids[i *
                           chunk_size: min((i + 1) * chunk_size, len(track_ids))]

    bot.method = 'ADD_SONG'
    bot.params = {"csrf_token": user_token}
    bot.data = {"op": "add", "pid": new_playlist_id,
                "trackIds": '[' + ','.join([str(v) for v in song_chunk]) + ']', "csrf_token": user_token}

    # print(bot.data)
    bot.send()

    final_response = json.loads(bot.response.content.decode())
    if final_response['code'] != 200:
        print("\n往歌单中添加歌曲失败…")
        print(final_response)
        exit(-5)
    else:
        print('\r添加歌曲 %d 之 %d…' %
              (min((i + 1) * chunk_size, len(c)), len(c)), end='')
        sleep(1)

# print(final_result.content.decode())

print()
separator()


# print(resp)


print("成功！\n现在应该可以在\n https://music.163.com/#/playlist?id=%s \n访问新歌单了。" %
      new_playlist_id)
