<div align="center">

![Bilibili Badge](https://github.com/luyanci/luyanci/raw/main/bilibili/user.svg)![level](https://github.com/luyanci/luyanci/raw/main/bilibili/level.svg)![Live room](https://github.com/luyanci/luyanci/raw/main/bilibili/liveroom.svg)
![video view](https://github.com/luyanci/luyanci/raw/main/bilibili/views.svg)![Followers](https://github.com/luyanci/luyanci/raw/main/bilibili/follower.svg)![Following](https://github.com/luyanci/luyanci/raw/main/bilibili/following.svg)

# bili-badge-py
 b站小勋章

</div>

## 开发原因

主要是因为我的profile之前使用的是[lonelyion/bilibili-stats-badges](https://github.com/lonelyion/bilibili-stats-badges)的公共api，而且只能展示关注数和粉丝数，最近发现公共api的域名已经过期了，现在无法展示，而且我希望能展示更多的功能，于是这个项目便诞生了
## 使用
### 准备工作

1. 根据文档获取`SESSDATA`和 `bili_jct` 的值并复制(https://nemo2011.github.io/bilibili-api/#/get-credential)

1. 在B站个人空间的链接中找到 UID (https://space.bilibili.com/282873551)

## 开发

```bash
pip install -r requirements.txt
```

## 感谢

- [lonelyion/bilibili-stats-badges](https://github.com/lonelyion/bilibili-stats-badges) 灵感及参考项目
- [bilibili-api](https://github.com/Nemo2011/bilibili-api) 提供了方便的B站api调用
- [google/pybadges](https://github.com/google/pybadges) 提供生成badge的方法

## 相关项目

- [bili-gist-py](https://github.com/luyanci/bili-gist-py) Pinned Gist信息卡