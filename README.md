<div align="center">
  <img src="assets/logo.svg" alt="logo">

  [_General API for GZHU developers_](https://docs.gzhuapi.xyz/)

  📖 _非官方广州大学开发者通用接口_

[![GZHU docs](https://img.shields.io/static/v1?label=GZHU_API&message=DOC&style=flat-square&logo=GitBook)](https://docs.gzhuapi.xyz/)
![flask](https://img.shields.io/static/v1?label=Python&message=Flask&color=blue&logo=Python)
![Redis](https://img.shields.io/static/v1?label=Redis&message=CLI&logo=redis)
[![Join on Slack](https://img.shields.io/badge/%20Issues-push-black?logo=GitHub&style=social&logoColor=lightgrey)](https://github.com/favorhau/GZHU_API/issues)

🖐🏻小项目正在抓紧时间筹备当中...

  欢迎各位开发者加入到我们的小项目当中
</div>


# 欢迎

💡这是一个非官方关于广州大学通用接口的仓库，制作了一个有效的通用接口，意想于提供一个“开放平台”API，供学校各个校园业务开发者提供便利。其中包括但不限于整合正方教务的一系列复杂接口，以及学生账户相关信息接口。显然，这并不排除过程中没有考虑到高并发和服务器负载的问题，甚至代码本身的异常处理也并非完善，甚至所谓“接口”的程序语言python并没有优势，因此这也只是一个简单的尝试，也希望更多优秀的校园开发者将优秀的插件与业务对接起来，丰富用户生态。

> 本项目旨在让校园业务开发者能够有一个便携规范的调用接口

# 目录
- [项目组成](#项目组成)
- [如何使用](#如何使用)
- [部署](#部署)

# 项目组成

🌏 项目的总体架构为 `Python` + `Flask` + `Redis`，

- Flask用于接收http请求以及返回

- Redis作为缓存，对token进行缓存



后续可能会考虑添加上`nginx`承载一些服务端的问题

```text
├── index.py //web后台入口
└── utils //
    ├── __init__.py //主体程序初始化
    ├── main.py // 获取信息代码实现
    ├── rsa.js // rsa前台数据包解密
    └── rsa.py // 打包rsa.js
``` 

与此同时，开放的相关接口可以通过 [Postman](https://documenter.getpostman.com/view/19271237/UVXqDXg7#fc92da40-d5ed-4ffd-9b83-a4c84778e717) 或 [Gitbook](https://docs.gzhuapi.xyz/) 查看。

# 如何使用


# 部署


# 关于授权

尚未获取官方授权，正在进行可用性测试中。

> 仅提供简单的模拟请求服务，原则上不对任何个人信息进行储存，若有违相关规定或信息变更，烦请联系 [favorhau@gmail.com](favorhau@gmail.com)
