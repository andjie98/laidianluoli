import aiohttp
import re
from urllib.parse import urlparse
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import Image

@register("loli", "andjie98", "获取随机二次元图片", "1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    def _is_valid_url(self, url: str) -> bool:
        """验证 URL 是否有效"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @filter.command("来点萝莉")
    async def loli(self, event: AstrMessageEvent):
        """获取随机二次元图片"""
        api_url = self.config.get("api_url", "https://www.loliapi.com/acg/")
        
        # 验证 API URL
        if not self._is_valid_url(api_url):
            logger.error(f"无效的 API URL: {api_url}")
            yield event.plain_result("配置的 API URL 无效，请检查插件配置")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{api_url}?type=url", timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        image_url = await response.text()
                        image_url = image_url.strip()
                        
                        # 验证图片 URL
                        if not self._is_valid_url(image_url):
                            logger.error(f"API 返回的图片 URL 无效: {image_url}")
                            yield event.plain_result("获取图片失败，返回的 URL 无效")
                            return
                        
                        yield event.image_result(image_url)
                    else:
                        logger.error(f"API 返回状态码: {response.status}")
                        yield event.plain_result(f"获取图片失败，API 返回状态码: {response.status}")
        except aiohttp.ClientTimeout:
            logger.error("请求 API 超时")
            yield event.plain_result("获取图片失败，请求超时")
        except Exception as e:
            logger.error(f"获取二次元图片失败: {e}")
            yield event.plain_result("获取图片失败，请稍后重试")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
