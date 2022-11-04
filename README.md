## 背景

个人观影爱好者，拥有比较强的分享欲。

群晖及 Apple TV用户，因此使用 Plex Server + Infuse 的方式流媒体观影。希望能够将自己最近的观影影片分享出去，因此想要借鉴海报墙的方式，搭建一个个人观影清单分享网站。

既然现有 Plex Server 的数据，可以根据 Plex 提供的 [API](https://www.plexopedia.com/) 收集影片相关信息并解析入库，再组织后编写新的 API 接口以供页面展示。因此，项目的架构是 Plex + Flask + React，其中 Flask 作为数据中台，解析 Plex 数据并对外提供 API，React 则负责海报墙的前端显示。

## 版本

### V 0.1.221104_beta

1. 完成对 Plex Library 中的影片（剧集）信息的解析入库；
2. 完成对 Plex 中影片（剧集）的海报及背景图片的缓存功能。
