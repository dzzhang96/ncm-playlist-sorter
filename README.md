# ncm-playlist-sorter · [![Build Status](https://travis-ci.com/yuxiqian/ncm-playlist-sorter.svg?branch=master)](https://travis-ci.com/yuxiqian/ncm-playlist-sorter)

![GitHub](https://img.shields.io/github/license/yuxiqian/ncm-playlist-sorter.svg)
![Python version](https://img.shields.io/badge/python-3.x-blue.svg)

把网易云的歌单按歌名长度精确排序。


> 大概像这样

> ![](https://raw.githubusercontent.com/yuxiqian/ncm-playlist-sorter/master/img/anim01.gif)

# 依赖
``` bash
pip[3] install -r requirements.txt
```

# 用法
* 前往 [网易云音乐 Web 版](https://music.163.com)，打开你需要排序的歌单

* 获取歌单链接（ID），如图
![](https://raw.githubusercontent.com/yuxiqian/ncm-playlist-sorter/master/img/img02.png)

* 运行
``` bash
python[3] src/sorter.py
```

![](https://raw.githubusercontent.com/yuxiqian/ncm-playlist-sorter/master/img/img03.png)

* 瞩目：需要输入网易云音乐**账号和密码**。

# 字形问题
网易云音乐各平台客户端界面显示字体不一，但大部分是[非等宽字体](https://zh.wikipedia.org/wiki/比例字体)。

因此如果简单按一个汉字 = 两个西文字母的计算方法并不能得到很好的结果。

不同的非等宽字体也可能会有细微的比例差别。

因此如果有需要，可以按照所需平台所使用的字体在第一步中自定义字体。

# 致谢

* [ncmbot](https://github.com/xiyouMc/ncmbot), The ISC License

* [pycryptodome](https://github.com/Legrandin/pycryptodome), The BSD 2-Clause license

* [Pillow](https://github.com/python-pillow/Pillow), The Open Source PIL Software License

* [MusicBoxApi](https://github.com/wzpan/MusicBoxApi), The MIT License

* [NetEaseMusicApi](https://github.com/littlecodersh/NetEaseMusicApi), The MIT License

* [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi), The MIT License


# （叹气）
大概只有自己用得到
