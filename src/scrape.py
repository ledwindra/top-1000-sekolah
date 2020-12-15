import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep

class TopSchool:
    URL = 'https://top-1000-sekolah.ltmpt.ac.id'
    COLUMNS = [
        'urut_nasional',
        'urut_provinsi',
        'rerata',
        'npsn',
        'sekolah',
        'provinsi',
        'kota_kab',
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

    def get_table(self, url):
        status_code = None
        while status_code != 200:
            try:
                res = requests.get(url)
                status_code = res.status_code
                content = BeautifulSoup(res.content, features='html.parser')
                content = content.find('table', {'class': 'table table-striped table-bordered'})
                table = content.find('tbody')
                return table
            except Exception as err:
                print(err)
                sleep(5)
                continue

    def dataframe(self, table):
        data = table.find_all('tr')
        data = [x.find_all('td') for x in data]
        data = [[j.text for j in data[i]] for i in range(len(data))]
        df = pd.DataFrame(data, columns=self.COLUMNS)

        return df

if __name__ == "__main__":
    top_school = TopSchool()
    page = top_school.page()
    table = [top_school.get_table(x) for x in page]
    df = [top_school.dataframe(x) for x in table]
    df = pd.concat(df, sort=False)
    df.to_csv('data/top-1000-sekolah.csv', index=False)