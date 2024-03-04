import csv
from googleapiclient.discovery import build
import scrapy


# Credențialele și cheia API
api_key = 'AIzaSyBapKfSZjCTomtTPYScTE1ShCwRqPhB4MA'
cse_id = '55dc8a7f4268b47dc'


class EconomieSpider(scrapy.Spider):
    name = 'economie'
    start_urls = ['https://cse.google.com/cse?cx=55dc8a7f4268b47dc']

    def parse(self, response):
        # Verificăm dacă răspunsul este valid
        if response.status == 200:
            for result in self.google_search('stiri despre economie'):
                yield scrapy.Request(url=result['link'], callback = self.parse_article, meta = {'title': result['title']})

    def parse_article(self, response):
        # Verificăm dacă răspunsul este valid
        if response.status == 200:
            paragraphs = self.extract_paragraphs(response)
            yield {
                'titlu': response.meta['title'],
                'link': response.url,
                'paragrafe': paragraphs
            }

    def extract_paragraphs(self, response):
        # Extragem paragrafele doar dacă răspunsul este valid
        if response.status == 200:
            paragraphs = response.css('p::text').getall()
            return paragraphs

    def google_search(self, query):
        service = build("customsearch", "v1", developerKey = api_key)
        res = service.cse().list(q = query, cx = cse_id, num = 8).execute()
        return res.get('items', [])

def write_to_csv(items):
    with open('search_results.csv', 'w', newline = '', encoding = 'iso-8859-1') as csvfile:
        # Creați un obiect writer
        csvwriter = csv.writer(csvfile, delimiter = ',')

        # Scrieți antetul (header-ul) în fișier
        csvwriter.writerow(['Titlu', 'Link', 'Paragrafe'])

        # Scrieți fiecare rând în fișierul CSV
        for item in items:
            titlu = item.get('titlu', '')
            link = item.get('link', '')
            paragrafe = item.get('paragrafe', [])

            # Scrieți datele în coloane separate
            csvwriter.writerow([titlu, link, '\n'.join(paragrafe)])