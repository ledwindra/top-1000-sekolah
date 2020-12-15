import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep


class SchoolDetail:
    URL = 'https://top-1000-sekolah.ltmpt.ac.id/site/page?id='
    COLUMNS = [
        'data_key',
        'detail',
        'urut_nasional',
        'urut_provinsi',
        'rerata',
        'nilai_tertinggi',
        'nilai_terendah',
        'standar_deviasi'
    ]

    def __init__(self, school_id):
        self.school_id = school_id

    def response(self):
        status_code = None
        while status_code != 200:
            try:
                res = requests.get(f'{self.URL}{self.school_id}')
                status_code = res.status_code
                return res
            except Exception as err:
                print(err)
                sleep(5)
                continue

    def content(self):
        return BeautifulSoup(self.response().content, features='html.parser')

    def dataframe(self, tab_id, detail):
        tab = self.content().find('div', {'id': tab_id})
        row =  tab.find('div', {'class': 'row'})
        span = [x.text for x in row.find_all('span', {'data-toggle': 'counter-up'})]
        h3 = [x.text for x in row.find_all('h3', {'class': 'card-title'})]
        data = span + h3
        data = [x.replace(',', '.') for x in data]
        convert = lambda x: int(x) if (float(x) * 2 % 2) == 0 else float(x)
        data = [convert(x) for x in data]
        data.insert(0, self.school_id)
        data.insert(1, detail)
        df = pd.DataFrame([data], columns=school_detail.COLUMNS)

        return df

if __name__ == "__main__":    
    data_key = pd.read_csv('data/rerata-nilai-tps.csv')
    data_key = data_key.loc[:, 'data_key']
    data = []
    for school in data_key:
        school_detail = SchoolDetail(school)
        keyval = {
            'tab-1': 'Kemampuan Kuantitatif',
            'tab-2': 'Kemampuan Memahami Bacaan dan Menulis',
            'tab-3': 'Kemampuan Penalaran Umum',
            'tab-4': 'Pengetahuan dan Pemahaman Umum'
        }
        df = [school_detail.dataframe(key, value) for key, value in keyval.items()]
        df = pd.concat(df, sort=False)
        df = df.reset_index(drop=True)
        data.append(df)

    df = pd.concat(data, sort=False)
    df.to_csv('data/school-detail.csv', index=False)
