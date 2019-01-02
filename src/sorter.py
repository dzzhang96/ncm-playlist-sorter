# -*- coding: UTF-8 -*-
from song import Song
from PIL import Image, ImageDraw2, ImageFont
from MusicBoxApi import api as NetEaseApi


buf_image = Image.new('RGB', (1024, 60), color='white')
buf_obj = ImageDraw2.Draw(buf_image)

netease = NetEaseApi.NetEase()
playlist = []
padding = 9
safe_ratio = 1.4

font_name = input(
    "请输入用于判定的字体名称：Windows 建议 MSYH 或 Arial，macOS 建议 PingFang 或 Songti >>> ")
if len(font_name) == 0:
    font_name = "PingFang"
font = ImageDraw2.Font('black', font_name, 60)


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
    new_song.name = song["name"]
    artists = []
    for artist in song["artists"]:
        artists.append(artist["name"])
    new_song.artist = '/'.join(artists)
    new_song.name_size = get_pixel_width(new_song.name)
    playlist.append(new_song)

playlist.sort(key=lambda x: x.name_size)

max_width = 0
result = ""

for item in playlist:
    print("Text = %s, size = %d" % (item.name, item.name_size))
    result += "%s - %s\n" % (item.name, item.artist)
    if item.name_size > max_width:
        max_width = item.name_size

result_image = Image.new(
    'RGB', (int(max_width * safe_ratio), len(playlist) * (60 + padding)), color="white")
result_draw = ImageDraw2.Draw(result_image)

input("歌曲数目: %d。按回车生成图片。" % len(playlist))

result_draw.text((padding, padding), result, font=font)
result_image.show()

file_name = input("输入文件名来保存 PNG 文件 >>>")
result_image.save("%s.png" % file_name)
