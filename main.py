import aiohttp
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("loli", "YourName", "获取随机二次元图片", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("来点萝莉")
    async def loli(self, event: AstrMessageEvent):
        """获取随机二次元图片""" # 这是 handler 的描述
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.loliapi.com/acg/?type=url") as response:
                    if response.status == 200:
                        image_url = await response.text()
                        yield event.plain_result(image_url.strip())
                    else:
                        yield event.plain_result("获取图片失败，请稍后重试")
        except Exception as e:
            logger.error(f"获取二次元图片失败: {e}")
            yield event.plain_result("获取图片失败，请稍后重试")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
