# -*- coding: UTF-8 -*-
from song import Song
from PIL import Image, ImageDraw2, ImageFont
from MusicBoxApi import api as NetEaseApi
from ncmbot.ncmbot import *

import json
import os


buf_image = Image.new('RGB', (1024, 60), color='white')
buf_obj = ImageDraw2.Draw(buf_image)

netease = NetEaseApi.NetEase()
playlist = []
padding = 9
safe_ratio = 1.4

font_name = input(
    "请输入用于判定的字体名称：Windows 建议 MSYH 或 Arial，macOS 建议 PingFang 或 Songti >>>")
if len(font_name) == 0:
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


id = input("请输入歌单 ID 或 URL >>>").replace(
    "https://music.163.com/#/playlist?id=", "").replace("https://music.163.com/#/my/m/music/playlist?id=", "")

datalist = netease.playlist_detail(id)

for song in datalist:
    new_song = Song()
    # print(song)
    # input()
    new_song.name = song["name"]
    new_song.album = song["album"]["name"]
    artists = []
    for artist in song["artists"]:
        artists.append(artist["name"])
    new_song.artist = '/'.join(artists)
    new_song.name_size = get_pixel_width(new_song.name)
    playlist.append(new_song)

playlist.sort(key=lambda x: x.name_size)

max_width = 0
results = []

for item in playlist:
    print("Text = %s, size = %d" % (item.name, item.name_size))
    results.append(item.name)
    results.append("%s - %s\n" % (item.artist, item.album))
    if item.name_size > max_width:
        max_width = item.name_size

input("歌曲数目: %d。按回车来登录网易云账号并进行同步。" % len(playlist))

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

login_name = input("输入手机号码来登录 >>>")
login_password = input("输入密码 >>>")

# if '@' in login_name:
#     bot, resp = login(login_password, email=login_name)
# else:
bot, resp = login(login_password, phone=login_name)


print(json.dumps(dict(resp.headers)))
print(resp.content.decode())

login_resp = json.loads(json.dumps(dict(resp.headers)))['Set-Cookie']


user_token = login_resp.split('__csrf=')[1].split(';')[0]

# user_token = 'fakefakefake'

input("token = %s" % user_token)


# print(personal_fm().content.decode())
# input()

playlist_name = input("请输入要创建的新歌单名 >>>")

bot = NCloudBot()
bot.method = 'CREATE_LIST'
bot.params = {"csrf_token": user_token}
bot.data = {"name": str(playlist_name), "csrf_token": ""}
bot.send()
print(bot.response.content.decode())

print(resp)
