# -*- coding:utf-8 -*-


import datetime
import urllib
import urllib2
import tempfile
import time
import random
import redis
import urlparse
import json
import psutil
import re
import logging

from antigate import AntiGate as AGate

try:
    from django.conf import settings
except ImportError:
    import config as settings

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from celery import group

from .utils import parse_yandex, parse_google
from .tasks import app
from .utils import get_normal_url, get_normal_quote, parse_google_url

XPATH_CHECKBOX = '/html/body/form/fieldset[2]/dl[1]/dd/div/label[1]'
XPATH_BUTTON = '/html/body/form/div[4]/button[1]/span'

TODAY = datetime.date.today()
YANDEX_URL = 'http://yandex.ru/yandsearch?p=%d&text=%s&site=&rstr=&within=0&numdoc=50&lr=%d'
YANDEX_RANGE = range(2)
GOOGLE_URL = 'https://www.google.ru/search?num=100&q=%s'

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s')


class getSoupClass(object):
    def __init__(self, driver, url, antigate, save, normalize):
        self.antigate = antigate
        self.rds = redis.Redis(**settings.ANTI_REDIS_CONF)
        self.url = url
        parse_url = urlparse.urlparse(url)
        self.hostname = parse_url.hostname
        self.query = parse_url.query
        if isinstance(self.query, unicode):
            self.query = self.query.encode('utf8')

        self.driver = driver
        if 'yandex' in url:
            self.text = self.openYandex(url)
            soup = BeautifulSoup(self.text)
            if save:
                data = self.saveData(soup)
                if normalize:
                    self.text = data
        elif 'google' in url:
            self.text = self.openGoogle(url)
            soup = BeautifulSoup(self.text)
            if save:
                data = self.saveData(soup)
                if normalize:
                    self.text = data
        else:
            driver.get(url)
            self.text = driver.page_source.encode('utf8')

    def openYandex(self, link):
        if isinstance(link, unicode):
            link = link.encode('utf8')

        soup = None
        while soup is None:
            self.driver.get(link)
            try:
                self.driver.find_element_by_css_selector('.input__found_visibility_visible')
            except:
                pass
            soup = BeautifulSoup(self.driver.page_source)

            if 'showcaptcha?' in self.driver.current_url:
                soup = self.AntigateYandex(soup, link)

        return self.driver.page_source.encode('utf8')

    def formatData(self, soup):
        """ Формирование данных """
        data = None
        if 'yandex.ru' == self.hostname:
            data = parse_yandex(soup, self.query)
            if data is False:
                data = self.get_soup(self.url, self.save, self.counter, self.normalize)
        if 'www.google.ru' == self.hostname:
            data = parse_google(soup, self.query)
        return data

    def saveData(self, soup):
        """ Сохранение в базу """
        data = self.formatData(soup)
        self.rds.set('page:' + self.url, json.dumps(data))
        return data

    def AntigateYandex(self, soup, link=None):
        temp = tempfile.NamedTemporaryFile(suffix='.gif')
        fn = temp.name
        url = 'http://yandex.ru/checkcaptcha?'
        yakey = soup.find('input', {'name': 'key'})
        if not yakey:
            return self.openYandex(link, self.antigate)
        yakey = yakey.get('value')
        if not yakey:
            return self.openYandex(link, self.antigate)

        retpath = soup.find('input', {'name': 'retpath'})['value']
        if isinstance(retpath, unicode):
            retpath = retpath.encode('utf8')
        while True:
            try:
                img = urllib2.urlopen(soup.find('img', class_='form__captcha')['src'])
                break
            except (urllib2.HTTPError, urllib2.URLError):
                time.sleep(random.uniform(1, 2))
                img = urllib2.urlopen(soup.find('img', class_='form__captcha')['src'])

        temp.file.write(img.read())
        temp.file.close()

        config = {'is_russian': '1'}
        try:
            cap_text = AGate(self.antigate, fn, send_config=config)
        except Exception, e:
            logging.warning('String 138: %s' % e)
            logging.warning('Key antigate: %s' % self.antigate)
            return self.openYandex(link, self.antigate)

        data = urllib.urlencode({'rep': cap_text.get(), 'key': yakey, 'retpath': retpath})
        self.driver.get(url + data)
        soup = BeautifulSoup(self.driver.page_source)

        if 'showcaptcha?retpath' not in self.driver.current_url or soup is not None:
            return soup

        return self.AntigateYandex(soup, link)

    def openGoogle(self, link):
        if isinstance(link, unicode):
            link = link.encode('utf8')

        soup = None
        while soup is None:
            self.driver.get(link)
            soup = BeautifulSoup(self.driver.page_source)

        if 'IndexRedirect?' not in self.driver.current_url:
            return self.driver.page_source.encode('utf8')

        return self.AntigateGoogle(link, soup)

    def AntigateGoogle(self, link, soup):
        try:
            el = self.driver.find_element_by_tag_name('img')
            box = (el.location['x'], el.location['y'], el.location['x'] + el.size['width'], el.location['y'] + el.size['height'])
        except Exception, e:
            logging.warning('String 170: %s' % e)
            logging.warning('Key antigate: %s' % self.antigate)
            return self.openGoogle(link)

        fn1 = tempfile.NamedTemporaryFile(suffix='.png')
        self.driver.save_screenshot(fn1.name)
        im1 = Image.open(fn1.name)
        crop = im1.crop(box)
        fn2 = tempfile.NamedTemporaryFile(suffix='.png')
        crop.save(fn2.name)
        try:
            cap_text = AGate(self.antigate, fn2.name)
        except Exception, e:
            logging.warning('String 183: %s' % e)
            logging.warning('Key antigate: %s' % self.antigate)
            return self.openGoogle(link)
        self.driver.find_element_by_name('captcha').clear()
        self.driver.find_element_by_name('captcha').send_keys(cap_text.get())
        self.driver.find_element_by_tag_name('form').find_element_by_xpath('input[4]').click()

        soup = BeautifulSoup(self.driver.page_source)

        if 'IndexRedirect?' not in self.driver.current_url:
            return self.driver.page_source.encode('utf8')

        self.AntigateGoogle(link, soup)


def drop_browsers():
    processes = psutil.Process(1)
    for process in processes.children():
        try:
            if 'phantom' in ' '.join(process.cmdline()):
                process.kill()
        except (psutil.ZombieProcess, psutil.NoSuchProcess, psutil.AccessDenied):
            pass


@app.task(bind=True, acks_late=True, soft_time_limit=120, max_retries=5)
def getSoup(self, url, antigate, save, normalize):
    try:
        if not hasattr(self, 'driver'):
            drop_browsers()
            user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = user_agent
            self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
            self.driver.set_window_size(1280, 600)
            # self.driver = webdriver.Chrome('/etc/init.d/chromedriver')
            self.driver.implicitly_wait(10)
            self.driver.get('https://yandex.ru/search/customize')
            self.driver.find_element_by_xpath(XPATH_CHECKBOX).click()
            self.driver.find_element_by_xpath(XPATH_BUTTON).click()
        obj = getSoupClass(self.driver, url, antigate, save, normalize)
        return obj.text
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)


class openYandex():
    def __init__(self, key):
        self.rds = redis.Redis(**settings.ANTI_REDIS_CONF)
        self.antigate = key

    def get_soup(self, url, save=True, counter=0, normalize=False):
        """ Получение супа в ответе сервера """
        task = getSoup.delay(url, self.antigate, save, normalize)
        task.wait()
        return task.result

    def get_yandex_cache_pos(self, phrase, lr=213, save=True, normalize=True, storage=True, result=True):
        """ data = obj.get_yandex_cache_pos(phrase, lr?). Получим позиции по ключевой фразе(первые 100)"""
        phrase_quote = get_normal_quote(phrase)
        res = []
        urls = []
        for i in YANDEX_RANGE:
            url = YANDEX_URL % (i, phrase_quote, lr)
            data = self.rds.get('page:' + url)
            if data:
                res += json.loads(data)
            elif storage:
                urls.append(getSoup.s(url, self.antigate, save, normalize))
        if urls:
            job = group(urls)
            result = job.apply_async()
            while not result.ready():
                pass
            res = [item for lst in result.get() for item in lst]
        return res

    def get_google_cache_pos(self, phrase, storage=True, normalize=True):
        phrase_quote = get_normal_quote(phrase)
        url = GOOGLE_URL % phrase_quote
        data = self.rds.get('page:' + url)
        res = []
        if data:
            res = json.loads(data)
        elif storage:
            res = self.get_soup(url, normalize=normalize)
        return res

    def clear_yandex_cache_pos(self, phrase, lr=213):
        phrase_quote = get_normal_quote(phrase)
        for i in YANDEX_RANGE:
            url = YANDEX_URL % (i, phrase_quote, lr)
            self.rds.delete('page:' + url)

    def clear_google_cache_pos(self, phrase):
        phrase_quote = get_normal_quote(phrase)
        url = GOOGLE_URL % phrase_quote
        self.rds.delete('page:' + url)

    def pages_of_site_in_index_yandex(self, site, pages=None, link=None):
        """ Получение данных по страницам сайта в индексе yandex """
        if pages is None:
            pages = []
        if isinstance(site, unicode):
            site = site.encode('utf8')

        if not link:
            link = u'http://yandex.ru/yandsearch?text=host:%s | host:www.%s&site=&rstr=&within=0&numdoc=50&lr=213'\
                % (urllib.quote_plus(site), urllib.quote_plus(site))
        soup = self.get_soup(link, save=False)
        blocks = soup.find_all(class_='serp-block')
        if blocks:
            blocks = [item for item in blocks
                      if len(item.attrs.get('class')) < 3 or 'serp-block_type_site' in item.attrs.get('class')]

            for block in blocks:
                for item in block:
                    tlink = item.find('a', class_='serp-url__link')
                    if tlink:
                        host = get_normal_url(tlink['href'])
                        if 'yandex.ru' not in host and 'infected?' not in host:
                            url = item.find('a', class_='serp-item__title-link').get('href')
                            title = item.find('a', class_='serp-item__title-link').text
                            desc = item.find('div', class_='serp-item__text')
                            desc = desc.text if desc else None
                            if url not in [i['url'] for i in pages]:
                                pages.append({'url': url, 'title': title, 'desc': desc})

        link = soup(text=u'Следующая')
        if link:
            link = 'http://yandex.ru' + link[0].parent.parent['href']
            self.pages_of_site_in_index_yandex(site, pages, link)
        return pages

    def pages_of_site_in_index_google(self, site, pages=None, start=0):
        """ Получение данных по страницам сайта в индексе google """
        if pages is None:
            pages = []

        if isinstance(site, unicode):
            site = site.encode('utf8')
        link = 'https://www.google.ru/search?num=100&start=%d&q=site:%s' % (start, urllib.quote_plus(site))
        soup = self.get_soup(link, save=False)

        # Добавляем данные со страницы
        for item in soup.findAll('li', {'class': 'g'}):
            url = parse_google_url(item.find('h3', {'class': 'r'}).find('a')['href'])
            title = item.find('h3', {'class': 'r'}).find('a').text
            desc = item.find('span', {'class': 'st'}).text
            pages.append({'url': url, 'title': title, 'desc': desc})

        # Проверяем следующую страницу из пагинатора
        test = re.search('Следующая', str(soup))
        if test:
            start += 100
            self.pages_of_site_in_index_google(site, pages, start)
        return pages

    def clear_redis(self):
        """ Очистить базу redis """
        for key in self.rds.keys():
            self.rds.delete(key)

    def load_core(self, phrase, lr=213):
        phrase_quote = get_normal_quote(phrase)
        urls = []
        for i in YANDEX_RANGE:
            url = YANDEX_URL % (i, phrase_quote, lr)
            urls.append(getSoup.s(url, self.antigate, save=True, normalize=True))
            job = group(urls)
            job.apply_async()
        phrase_quote = get_normal_quote(phrase)
        url = GOOGLE_URL % phrase_quote
        getSoup.delay(url, self.antigate, save=True, normalize=True)


openGoogle = openYandex
