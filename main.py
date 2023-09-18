KEY_WORDS = ['Django', 'Flask']

import requests
from bs4 import BeautifulSoup
import fake_useragent
import unicodedata

words = {'Django', 'Flask'}
json_dic = {}
result_json = {'vacancy': []}

def search_key_words(url, words):
    search = words

    ua = fake_useragent.UserAgent()
    header = {'User-Agent':str(ua.chrome)}
    url = url
    r = requests.get(url, headers=header)

    soup = BeautifulSoup(r.content, 'lxml')
    text_vacancy = soup.find('div', class_='g-user-content')

    if text_vacancy != None:

        text_vacancy = text_vacancy.find_all('li')
        text = ''
        new_text = []
        var_set = set()
        for element in text_vacancy:
            text += str(element.contents[0]) + '\n'

        text = text.split('\n')
        for element in text:
            new_text += element.split()

        for item in new_text:
            if item.replace(',','') in search:
                var_set.add(item.replace(',',''))
        if (var_set & search) == search:
            return True
    else:
        return False

ua = fake_useragent.UserAgent()
url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

ret = requests.get(url=url, headers = {'user-agent':ua.random})
soup = BeautifulSoup(ret.content, 'lxml')

pages = int(soup.find('div', attrs={'class':'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)

for val in range(pages):
    url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={val}'
    ret = requests.get(url=url, headers = {'user-agent':ua.random})
    soup2 = BeautifulSoup(ret.content, 'lxml')
    vacancy = soup2.find('main', attrs={'class':'vacancy-serp-content'})

    #Находит блоки с вакансиями
    vacancy = vacancy.find_all('div', attrs={'class':'vacancy-serp-item-body__main-info'})


    #Находит ссылки и текст с названиями вакансий

    for position in vacancy:
        company_name = ''
        salary_range = ''
        city = ''
        company = position.find('a', attrs={'class':'bloko-link bloko-link_kind-tertiary'})
        if company != None:
            for value in range(len(company.contents)):
                company_name += company.contents[value]
            city = position.find('div', attrs={'data-qa':'vacancy-serp__vacancy-address'})
            city = city.contents[0]
            salary = position.find('span', attrs={'class':'bloko-header-section-2'})
            if salary:
                for value in range(len(salary.contents)):
                    salary_range += salary.contents[value]
            else:
                salary_range = 'ЗП не указана'

            position = position.find('a', attrs={'class':'serp-item__title'})

            if search_key_words(position['href'], words):
                json_dic = {'company name': unicodedata.normalize('NFKD',company_name),
                            'city': unicodedata.normalize('NFKD',city),
                            'position': unicodedata.normalize('NFKD',position.contents[0]),
                            'salary range': unicodedata.normalize('NFKD',salary_range),
                            'link':position['href']}
                result_json['vacancy'].append(json_dic)
print(result_json)