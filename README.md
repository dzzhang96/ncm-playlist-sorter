# ncm-playlist-sorter · [![Build Status](https://travis-ci.com/yuetsin/ncm-playlist-sorter.svg?branch=master)](https://travis-ci.com/yuetsin/ncm-playlist-sorter)

![GitHub](https://img.shields.io/github/license/yuetsin/ncm-playlist-sorter.svg)
![Python version](https://img.shields.io/badge/python-3.x-blue.svg)

谢谢[yuetsin](https://github.com/yuetsin)的代码！增加可以将歌单按专辑名称/艺术家名称（按首字母，非长度）排序。

以下是原readme：

把「网易云音乐」歌单依显示长度排序。

> 大概像这样

> ![](https://raw.githubusercontent.com/yuxiqian/ncm-playlist-sorter/master/img/anim01.gif)

# 依赖

```bash
pip[3] install -r requirements.txt
```

# 用法

* 前往 [网易云音乐 Web 版](https://music.163.com)，打开你需要排序的歌单

* 获取歌单链接（ID），如图
  ![](https://raw.githubusercontent.com/yuxiqian/ncm-playlist-sorter/master/img/img02.png)

* 运行
  
  ```bash
  python[3] src/sorter.py
  ```

![](https://raw.githubusercontent.com/yuxiqian/ncm-playlist-sorter/master/img/img03.png)

* 瞩目：需要输入网易云音乐**账号和密码**，或者提供 Cookie 凭据。

# 致谢

* [ncmbot](https://github.com/xiyouMc/ncmbot), The ISC License

* [pycryptodome](https://github.com/Legrandin/pycryptodome), The BSD 2-Clause license

* [Pillow](https://github.com/python-pillow/Pillow), The Open Source PIL Software License

* [MusicBoxApi](https://github.com/wzpan/MusicBoxApi), The MIT License

* [NetEaseMusicApi](https://github.com/littlecodersh/NetEaseMusicApi), The MIT License

* [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi), The MIT License

# （叹气）

大概只有自己用得到
