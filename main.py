import aiohttp
from urllib.parse import urlparse
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Image

@register("loli", "AndJie98", "获取随机二次元图片", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("来点萝莉")
    async def loli(self, event: AstrMessageEvent):
        """获取随机二次元图片"""
        api_url = "https://www.loliapi.com/acg/"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{api_url}?type=url", timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        image_url = await response.text()
                        image_url = image_url.strip()
                        yield event.image_result(image_url)
                    else:
                        logger.error(f"API 返回状态码: {response.status}")
                        yield event.plain_result("获取图片失败，请稍后重试")
        except aiohttp.ClientTimeout:
            logger.error("请求 API 超时")
            yield event.plain_result("获取图片失败，请求超时")
        except Exception as e:
            logger.error(f"获取二次元图片失败: {e}")
            yield event.plain_result("获取图片失败，请稍后重试")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
