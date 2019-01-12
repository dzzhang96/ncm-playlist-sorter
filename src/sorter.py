# -*- coding: UTF-8 -*-
from song import Song
from PIL import Image, ImageDraw2, ImageFont
from MusicBoxApi import api as NetEaseApi
from ncmbot.ncmbot import *

import os
import json
import platform


def separator():
    print("-" * os.get_terminal_size().columns)


buf_image = Image.new('RGB', (1024, 60), color='white')
buf_obj = ImageDraw2.Draw(buf_image)

netease = NetEaseApi.NetEase()
playlist = []
padding = 9
safe_ratio = 1.4

separator()
font_name = input(
    "请输入用于判定的字体名称：\nWindows 建议 msyh.ttc（默认）或 Arial，macOS 建议 PingFang（默认）或 Songti\n为了显示效果考虑，请尽量选择非等宽字体\n按回车选择默认值 >>>")
if len(font_name) == 0:
    sysstr = platform.system()
    if sysstr == "Windows":
        font_name = "msyh.ttc"
    else:
        font_name = "PingFang"

font = ImageDraw2.Font('black', font_name, 60)
font_small = ImageDraw2.Font('black', font_name, 30)


def get_pixel_width(string):
    if string == None:
        return 0
    # 画到 BUF_OBJ 上，获取其宽度像素值
    size_tuple = buf_obj.textsize(string, font)
    if len(size_tuple) == 2:
        return size_tuple[0]
    return 0


separator()
id = input("请输入歌单 ID 或 URL >>>").replace(
    "https://music.163.com/#/playlist?id=", "").replace("https://music.163.com/#/my/m/music/playlist?id=", "")

datalist = netease.playlist_detail(id)

for song in datalist:
    new_song = Song()
    # print(song)
    # input()
    new_song.name = song["name"]
    new_song.album = song["album"]["name"]
    new_song.id = song["id"]
    artists = []
    for artist in song["artists"]:
        artists.append(artist["name"])
    new_song.artist = '/'.join(artists)
    new_song.name_size = get_pixel_width(new_song.name)
    playlist.append(new_song)

playlist.sort(key=lambda x: x.name_size)

track_ids = []


for item in playlist:
    print("歌曲名称 = %s, 相对长度 = %d" % (item.name, item.name_size))
    # results.append(item.name)
    # results.append("%s - %s\n" % (item.artist, item.album))
    # if item.name_size > max_width:
    #     max_width = item.name_size

separator()
controller = input("歌曲数目: %d。按回车来登录网易云账号并进行同步。输入 I/i 来倒序排列歌曲。" % len(playlist))

if controller != 'I' and controller != 'i':
    playlist.reverse()


for p in playlist:
    track_ids.append(str(p.id))

trackIdString = '[' + ', '.join(track_ids) + ']'

# result_image = Image.new(
#    'RGB', (1080, len(playlist) * (130)), color = "white")
# result_draw = ImageDraw2.Draw(result_image)

# frame_width = 1080

# for i in range(0, len(playlist)):
#    result_draw.text((padding * 5, padding + 130 * i),
#                     results[2 * i], font=font)
#    result_draw.text((padding * 5, padding + 130 * i + 80),
#                     results[2 * i + 1], font=font_small)

#    result_draw.line((padding * 5, padding + 130 * i + 120),
#                     (frame_width, padding + 130 * i + 120), 'gray')


# result_image.show()

# file_name = input("输入文件名来保存 PNG 文件 >>>")
# result_image.save("%s.png" % file_name)

separator()
login_name = input("输入手机号码来登录 >>>")
login_password = input("输入密码 >>>")

# if '@' in login_name:
#     bot, resp = login(login_password, email=login_name)
# else:
bot, resp = login(login_password, phone=login_name)


# print(json.dumps(dict(resp.headers)))
# print(resp.content.decode())

login_resp = json.loads(json.dumps(dict(resp.headers)))['Set-Cookie']
MUSIC_U = login_resp.split('MUSIC_U=')[1].split(';')[0]


user_token = login_resp.split('__csrf=')[1].split(';')[0]

# user_token = 'fakefakefake'

# input("token = %s" % user_token)

# print(personal_fm().content.decode())
# input()

separator()
playlist_name = input("请输入要创建的新歌单名 >>>")

# input(MUSIC_U)
bot = NCloudBot(MUSIC_U)
bot.method = 'CREATE_LIST'
bot.params = {"csrf_token": user_token}
bot.data = {"name": str(playlist_name), "csrf_token": user_token}
bot.send()

result = json.loads(bot.response.content.decode())

separator()
if result['code'] != 200:
    print("创建歌单失败。")
    exit(1)

new_playlist_id = result['id']

final_result = add_song(str(new_playlist_id), trackIdString, MUSIC_U)

final_response = json.loads(final_result.content.decode())['code']

# print(resp)

if final_response == 200:
    print("成功！")
    exit(0)
else:
    print("哪里不太对的样子")
    exit(-1)
