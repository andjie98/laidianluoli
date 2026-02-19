import aiohttp
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Image

@register("loli", "YourName", "获取随机二次元图片", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.config = self.load_config()

    def load_config(self):
        """加载配置文件"""
        from astrbot.api.provider import AstrBotConfigProvider
        config_provider = self.context.get_provider(AstrBotConfigProvider)
        
        default_config = {
            "api_url": "https://www.loliapi.com/acg/",
            "command": "来点萝莉"
        }
        
        try:
            if config_provider:
                config = config_provider.get_plugin_config(self.register_info.name)
                if config:
                    return config
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
        
        return default_config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        command = self.config.get("command", "来点萝莉")
        self.__dict__[command] = self._loli_handler

    async def _loli_handler(self, event: AstrMessageEvent):
        """获取随机二次元图片""" # 这是 handler 的描述
        api_url = self.config.get("api_url", "https://www.loliapi.com/acg/")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{api_url}?type=url") as response:
                    if response.status == 200:
                        image_url = await response.text()
                        yield event.image_result(image_url.strip())
                    else:
                        yield event.plain_result("获取图片失败，请稍后重试")
        except Exception as e:
            logger.error(f"获取二次元图片失败: {e}")
            yield event.plain_result("获取图片失败，请稍后重试")

    @filter.command("来点萝莉")
    async def loli(self, event: AstrMessageEvent):
        async for result in self._loli_handler(event):
            yield result

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
