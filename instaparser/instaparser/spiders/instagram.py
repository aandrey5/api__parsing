import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.instaparser.items import InstaparserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'aandrey54321@gmail.com'
    inst_password = '#PWD_INSTAGRAM_BROWSER:10:1610487411:AZtQAKVeU+i26UNH76NtKSv+rQXBpeA30eUy7xNkZJ5ckJxxxFlN0Vj4ip5uO9JAZCX9rzCvVFuqokVBNwT0VCuQoOg9kvgbXrdIZsmQrfIieewumikNTA0S782Z/Jnw23boqazGa/Dm4bw/8A=='
    parse_users = ['kolia.baran', 'babai.vasia']
    num_of_users = len(parse_users)
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash_podpischik = '5aefa9893005572d237da5068082d8d5'
    posts_hash_podpiski = '3dec7e2c57367ef3da3d987d89f9dbc8'

# первоначальный запрос с входом по методу POST


    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)

        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_password},
            headers= {'X-CSRFToken': csrf_token}

        )

# здесь развилка на пользователей
    def user_login(self, response:HtmlResponse): # метод будем вызывать для каждого пользователя из списка
        j_data = response.json()
        if j_data['authenticated']:
            for n in range(self.num_of_users):
                yield response.follow(
                    f'/{self.parse_users[n-1]}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': self.parse_users[n-1]}
                )
            # print()


    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id, 'first': 12}

        url_podpischik = f'{self.graphql_url}query_hash={self.posts_hash_podpischik}&{urlencode(variables)}'
        url_podpiski = f'{self.graphql_url}query_hash={self.posts_hash_podpiski}&{urlencode(variables)}'

# ---- первый yield уходим на подписчиков ----
        yield response.follow(
            url_podpischik,
            callback=self.user_podpischik_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

# ---- второй yield уходим на подписки ----

        yield response.follow(
            url_podpiski,
            callback=self.user_podpiski_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

        # print()

# __________________ПОДПИСЧИКИ ______________________________________________________________

    def user_podpischik_parse(self, response:HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')

            url_podpischik = f'{self.graphql_url}query_hash={self.posts_hash_podpischik}&{urlencode(variables)}'
            yield response.follow(
                url_podpischik,
                callback=self.user_podpischik_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        podpischik = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for podpis in podpischik:
            item = InstaparserItem(
                type_data='podpischik',
                username = username,
                user_id = user_id,
                id_podpischik = podpis.get('node').get('id'),
                photo = podpis.get('node').get('profile_pic_url'),
                podpischik_name = podpis.get('node').get('username'),
                podpis_data = podpis.get('node')
            )
            yield item

            # print()

# ____________ ПОДПИСКИ _______________________________________________________________

    def user_podpiski_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')

            url_podpiski = f'{self.graphql_url}query_hash={self.posts_hash_podpiski}&{urlencode(variables)}'
            yield response.follow(
                url_podpiski,
                callback=self.user_podpiski_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        podpiski = j_data.get('data').get('user').get('edge_follow').get('edges')
        for podpiska in podpiski:
            item = InstaparserItem(
                type_data='podpiska',
                username=username,
                user_id=user_id,
                id_podpiska=podpiska.get('node').get('id'),
                photo=podpiska.get('node').get('profile_pic_url'),
                podpiska_name=podpiska.get('node').get('username'),
                podpiska_data=podpiska.get('node')
            )
            yield item

            # print()


        # #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


        # # Получаем id желаемого пользователя

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')