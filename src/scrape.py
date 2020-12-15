import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep

class TopSchool:
    URL = 'https://top-1000-sekolah.ltmpt.ac.id'
    RERATA = [
        'data_key',
        'urut_nasional',
        'urut_provinsi',
        'rerata',
        'npsn',
        'sekolah',
        'provinsi',
        'kota_kab',
        'jenis'
    ]
    DETAIL = [
        'data_key',
        'urut_nasional',
        'npsn',
        'sekolah',
        'provinsi',
        'rerata',
        'tertinggi',
        'terendah',
        'std_deviasi',
        'jenis'
    ]

    def response(self):
        status_code = None
        while status_code != 200:
            try:
                res = requests.get(self.URL)
                status_code = res.status_code
                return res
            except Exception as err:
                print(err)
                sleep(5)
                continue

    def content(self):
        return BeautifulSoup(self.response().content, features='html.parser')

    def page(self):
        page = self.content().find('ul', {'class': 'pagination pagination-lg d-flex justify-content-center'})
        page = page.find_all('a', href=True)
        page = [x['href'] for x in page][:-1]
        page = [self.URL + x for x in page]

        return page

    def get_table(self, url, content_index):
        status_code = None
        while status_code != 200:
            try:
                res = requests.get(url)
                status_code = res.status_code
                content = BeautifulSoup(res.content, features='html.parser')
                content = content.find_all('table', {'class': 'table table-striped table-bordered'})
                table = content[content_index].find('tbody')
                return table
            except Exception as err:
                print(err)
                sleep(5)
                continue

    def dataframe(self, table, cols):
        data = table.find_all('tr')
        data_key = [x.get('data-key') for x in data]
        data = [x.find_all('td') for x in data]
        data = [[j.text for j in data[i]] for i in range(len(data))]
        [data[i].insert(0, data_key[i]) for i in range(len(data))]
        df = pd.DataFrame(data, columns=cols)

        return df

if __name__ == "__main__":
    top_school = TopSchool()
    page = top_school.page()
    def to_csv(content_index, cols, file_name):
        df = [top_school.get_table(x, content_index) for x in page]
        df = [top_school.dataframe(x, cols) for x in df]
        df = pd.concat(df, sort=False)
        df.to_csv(f'data/{file_name}.csv', index=False)
    
    to_csv(0, top_school.RERATA, 'rerata-nilai-tps')
    to_csv(1, top_school.DETAIL, 'detail-nilai-tps')
