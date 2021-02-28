# coding: utf-8
import re
from time import sleep
import random
import json
import requests
from lxml import etree

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions

import settings


def rand_sleep():
    """
    随机一个时间
    :return:
    """
    sleep(random.randint(80, 120) / 100)


class Browser(object):
    """
    配置浏览器对象的类
    """
    # 浏览器驱动路径
    bro_path = settings.BROWSER_PATH

    # 无可视化界面
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    def __init__(self):
        # self.bro = webdriver.Chrome(executable_path=self.bro_path, options=self.option)
        self.bro = webdriver.Chrome(executable_path=self.bro_path, chrome_options=self.chrome_options,
                                    options=self.option)


class GetMovieInfo(object):
    """
    获取电影分类下电影详情信息的类
    """
    movie_type = None
    movie_info_dict = {}

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.bro = Browser().bro
        self.headers = {
            'User-Agent': random.choice(settings.USER_AGENT_LIST)
        }
        self.proxy = random.choice(settings.PROXY_HTTPS)

    @property
    def all_movie_url(self):
        """
        获取所有电影的URL
        :return:
        """
        # 进入起始页
        self.bro.get(self.url)
        rand_sleep()

        # 点击"登录"链接，进入登录界面
        self.bro.find_element_by_xpath('//*[@id="db-global-nav"]/div/div[1]/a').click()
        # self.bro.find_element_by_xpath('/html/body/a').click()
        print('进入登录界面...')
        rand_sleep()

        # 点击"密码登录"，切换到密码登录模式
        self.bro.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()
        print('切换到密码登录')
        rand_sleep()

        # 定位，并输入账号、密码
        self.bro.find_element_by_id('username').send_keys(self.username)
        print(f'输入账号******')
        rand_sleep()
        self.bro.find_element_by_id('password').send_keys(self.password)
        print(f'输入密码******')
        rand_sleep()

        # 登录，进入首页
        self.bro.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()
        print('登录中...')
        sleep(10)
        print('登录成功！')

        # 点击排行榜
        self.bro.find_element_by_xpath('//*[@id="db-nav-movie"]/div[2]/div/ul/li[5]/a').click()
        print('点击排行榜...')
        rand_sleep()

        # 点击任意分类
        num = random.randint(1, 29)
        current_type = self.bro.find_element_by_xpath(f'//*[@id="content"]/div/div[2]/div[1]/div/span[{num}]/a')
        self.movie_type = current_type.text
        current_type.click()
        print(f'点击{self.movie_type}分类...')
        rand_sleep()

        # 屏幕向下滚动2000像素
        self.bro.execute_script('window.scrollTo(0, 2000)')
        print('屏幕向下滚动2000像素...')
        rand_sleep()

        # 获取当前页面加载到的所有电影信息
        movie_url_list = etree.HTML(self.bro.page_source).xpath('//div[@class="movie-content"]/a/@href')
        print(movie_url_list)
        print('成功获取到当前页面所有电影的URL！')
        rand_sleep()

        self.bro.quit()

        return movie_url_list

    def get_movie_info(self):
        """
        获取所有电影的详细信息
        :return:
        """
        for url in self.all_movie_url:
            if settings.PROXY_FLAG:
                response_text = requests.get(url=url, headers=self.headers, proxies=self.proxy, timeout=10).text
            else:
                response_text = requests.get(url=url, headers=self.headers, timeout=10).text
            tree = etree.HTML(response_text)

            title = ''.join(tree.xpath('//*[@id="content"]/h1/span[1]/text()'))
            print('正在下载：', title)

            # 电影名称、海报url、导演、编剧、主演、类型、语言、上映日期、片长、豆瓣评分
            self.movie_info_dict[title] = {
                'title': title,
                'poster_url': ''.join(tree.xpath('//*[@id="mainpic"]//img/@src')),
                'director': ''.join(tree.xpath('//*[@id="info"]/span[1]/span[2]//text()')),
                'screenwriter': ''.join(tree.xpath('//*[@id="info"]/span[2]/span[2]//text()')),
                'star': ''.join(tree.xpath('//*[@id="info"]/span[3]/span[2]//text()')),
                'movie_type': ' / '.join(tree.xpath('//*[@id="info"]//span[@property="v:genre"]/text()')),
                'language': ''.join(re.findall('语言:</span>(.*?)<span', response_text, re.S)).split('<')[0],
                'date': ''.join(tree.xpath('//*[@id="info"]//span[@property="v:initialReleaseDate"]/text()')),
                'length': ''.join(tree.xpath('//*[@id="info"]//span[@property="v:runtime"]/text()')),
                'score': ''.join(tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')),
            }

    def save(self):
        """
        json序列化
        :return:
        """
        with open(f'./{self.movie_type}.json', 'w', encoding='utf-8') as fp:
            json.dump(self.movie_info_dict, fp=fp, ensure_ascii=False)

    def run(self):
        """
        主函数
        :return:
        """
        self.get_movie_info()
        self.save()


if __name__ == '__main__':
    GetMovieInfo(settings.START_URL, settings.USERNAME, settings.PASSWORD).run()
