import json
import requests

cookies = {
    'locality': json.dumps(
        {"city": "Екатеринбург", "cityId": 55, "longitude": 60.597474, "latitude": 56.838011}
    )
}

headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    # 'cache-control': 'max-age=0',
    # # 'cookie': 'i18n_redirected=ru; token=0b38ec1f683af977cf6d2319225e63a2; tmr_lvid=20ed071dff25ab204669cccf87e2df26; tmr_lvidTS=1731858070574; _ym_uid=1731858071698105551; _ym_d=1731858071; is-logged=; _ymab_param=GZjJbxL_wlJaPO8mpEJBRJoMRsQlLS2_qDRCab8MrTCow-ar98VXfUf4OC3Ucbj-YaknRnxu1UR1CcUBgiVOUO1uDXg; visited=true; domain_sid=mD3Z8VgNky1j9y0tNboY0%3A1731858073795; _ym_isad=2; _cfuvid=zJhyjjCsnJqNSFQnuLfNOenx567zeF3clLRUkOniqRs-1731861602658-0.0.1.1-604800000; cf_clearance=llx9phkRCLAr8BUhrKczMKV1MUeQXm_MeaDP1PwePpg-1731861604-1.2.1.1-sdEZ55lJOHaAdyejiRr6eRws3fCe5UcfiiAOYk5H9zoCQEmPk6TZaLrp4OarIQa2j0jrb96_F4A7xIdTuiJiFoUVKjS7UiW0tmr0HBvETgEnfJvgEP3pPBkbtt7b8WqNSq1ZCMilF.AKmxX5wvTHHlHv3XgKAz8zxaOA8i48YlSzD7hLJxu6HZbh_5sInlM1y1.59SimIgyvH1V0H6uRiQEX8T_nQg9U9Tp4sPwFImkLE29pumZ7q5t_jzLSE3SKTr6sLUn8aoGL3L2iZD0VGdoYDN841JJhYTogj0oecob40NQJyaQs6Kd6cOsnziDE9SajLIrUv8ljeCxti_bNFu9_iSCzPlB7whPZSTr_8.BIZjpFvvPEjUbFbTM5DdavNqp0ZIunbjjdfVI0vu3E68LNGMbfAnCeqMtMQa38BaU; _ym_visorc=b; skip-city=true; tmr_detect=0%7C1731861743261; locality=%7B%22city%22%3A%22%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%22%2C%22cityId%22%3A55%2C%22longitude%22%3A60.597474%2C%22latitude%22%3A56.838011%2C%22prefix%22%3A%22%D0%B3%22%7D',
    # 'priority': 'u=0, i',
    # 'referer': 'https://fix-price.com/',
    # 'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'same-origin',
    # 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
}

response = requests.get(
    'https://fix-price.com/catalog/kosmetika-i-gigiena/ukhod-za-polostyu-rta',
    cookies = cookies,
    headers = headers,
)

from scrapy.selector import Selector

content = Selector(text = response.text)
city = content.xpath("//span[@class='geo']").getall()
print('-----------', city)