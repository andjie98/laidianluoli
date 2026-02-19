# AstrBot 萝莉图片插件

一个简单的 AstrBot 插件，用于获取随机二次元图片。

## 功能

- 发送 `/来点萝莉` 命令获取随机二次元图片
- 支持自定义 API 地址
- 支持自定义触发命令
- 完善的错误处理和 URL 验证

## 安装

1. 在 AstrBot 插件市场搜索 `laidianluoli` 并安装
2. 或通过 Git 仓库 URL 安装

## 配置

插件提供了以下配置项（可在 AstrBot WebUI 插件配置中修改）：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `api_url` | string | `https://www.loliapi.com/acg/` | 图片 API 地址 |
| `command` | string | `来点萝莉` | 触发命令 |

## 使用

安装后，在聊天中发送 `来点萝莉` 即可获取随机二次元图片。

## API

默认使用 [LoliAPI](https://api.loliapi.com/docs/acg/) 提供的随机二次元图片服务。

## 支持与反馈

- [AstrBot 官方仓库](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot 插件开发文档](https://docs.astrbot.app/dev/star/plugin-new.html)
