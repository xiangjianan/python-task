import random
from fang58 import settings


class Fang58DownloaderMiddleware(object):
    """
    下载器中间件
    """

    def process_request(self, request, spider):
        """
        拦截请求
        :param request:
        :param spider:
        :return:
        """
        # UA伪装
        request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)
        return None

    def process_response(self, request, response, spider):
        """
        拦截响应
        :param request:
        :param response:
        :param spider:
        :return:
        """
        pass
        return response

    def process_exception(self, request, exception, spider):
        """
        拦截发生异常的请求，使用代理IP进行重新请求发送
        :param request:
        :param exception:
        :param spider:
        :return:
        """
        if request.url.split(':')[0] == 'http':
            request.meta['proxy'] = 'http://' + random.choice(settings.PROXY_HTTP)
        else:
            request.meta['proxy'] = 'https://' + random.choice(settings.PROXY_HTTPS)
        return request
