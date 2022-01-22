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



# 如何使用

当前，程序提供了三种接口方式，相关源码部署在了伺服器当中 ~~（阿里云学生机)~~ ，显然不能高并发的请求，但是为了接口测试，提供了api的IP网址接口。当然，API更推荐直接部署在自己的服务器当中。

与此同时，因为代码相当于一个桥梁（教务系统与第三方Client客户端）,在鉴权方面可能会出现session或者cookie连接的问题，因此可能会出现储存在服务器的cookie失效，但是在缓存当中的token仍然能使用，因此在接口调用中出现`无法加载信息`的情况需要重新鉴权。

## 接口调用测试

我们已经将代码部署在了自己的服务器当中，请求的URL为

```curl
http://120.24.5.39:8080/v1/<method>
```

开放的相关接口可以通过 [Postman](https://documenter.getpostman.com/view/19271237/UVXqDXg7#fc92da40-d5ed-4ffd-9b83-a4c84778e717) 或 [Gitbook](https://docs.gzhuapi.xyz/) 查看，并且请依据文档进行调用。

⚠️ hints: 在调用查询接口前，必须通过`auth`进行鉴权，取得`token`之后将其添加到`header`后发起请求。

## 直接接口调用

请参考[部署](#部署)，将程序部署上服务器，设定端口


```bash
nohup python main.py >> main.log 2>&1 &
```

## 作为库引入


# 部署

1. 克隆本仓库

```
git clone git@github.com:favorhau/GZHU_API.git
```

2. 安装环境依赖

默认已经安装好python（或conda）环境，与此同时需要`Flask`、`requests`、`redis`等pypi库

```python
pip install flask redis execjs requests
# pip3 install flask redis execjs requests
```
3. redis安装

- 在Linux下，可以执行
```bash
$ sudo apt update
$ sudo apt install redis-server
```

并启动服务

```bash
$ sudo service redis start
```

- 在Macos下安装大同小异，可通过brew进行安装

4. 启动服务
```bash
python index.py

"""
 * Serving Flask app "index" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 """
```

# 常见问题

1. 连接断开无请求

```json
{
    "data": {},
    "msg": "Catch exception: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))"
}
```

2. 请求超时

```json
{
    "data": {},
    "msg": "Catch exception: HTTPSConnectionPool(host='newmy.gzhu.edu.cn', port=443): Read timed out. (read timeout=15)"
}
```

# 关于授权

尚未获取官方授权，正在进行可用性测试中。

> 仅提供简单的模拟请求服务，原则上不对任何个人信息进行储存，若有违相关规定或信息变更，烦请联系 [favorhau@gmail.com](favorhau@gmail.com)
