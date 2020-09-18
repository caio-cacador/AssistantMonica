import re
import sys
from collections import namedtuple

from requests import Session
from lxml import html
from AssistantMonica.utils import normalize_str


TrakingNamedTuple = namedtuple('traking', ['location', 'text', 'title'])


class ObjectNotFoundException(Exception):
    pass


class UnavailableServiceException(Exception):
    pass


class Correio:

    @staticmethod
    def _clear_tracking(str_array):
        array = [s.strip() for s in str_array]
        str_ = ' '.join(array)
        text = normalize_str(str_)
        text = re.sub('\\r|\\t|\\n', '', text)

        while '  ' in text:
            text = text.replace('  ', ' ')

        return text


    @staticmethod
    def _get_correio_session() -> Session():
        session = Session()
        session.headers.update({
            'Host': 'www2.correios.com.br',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www2.correios.com.br/sistemas/rastreamento/default.cfm',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '37',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        return session

    def get_all_tracking_info(self, tracking_code):
        session = self._get_correio_session()
        result = session.post('https://www2.correios.com.br/sistemas/rastreamento/resultado.cfm?',
                              data=dict(objetos=tracking_code, btnPesq='+Buscar'), allow_redirects=True)
        result.encoding = 'ISO-8859-1'

        if result.status_code == 502:
            raise UnavailableServiceException()

        if result.status_code == 200:
            if result.text.find('listEvent') == -1:
                raise ObjectNotFoundException()

        tree = html.fromstring(result.text.encode('latin1'))
        trs = tree.xpath('//table[contains(@class,"listEvent")]/tr')

        object_movements = []
        for tr in trs:
            tds = tr.xpath('./td')

            location = self._clear_tracking(tds[0].xpath('./text() | ./label/text()'))
            text = self._clear_tracking(tds[1].xpath('./text()'))
            title = tds[1].xpath('./strong/text()')[0]

            object_movements.append(TrakingNamedTuple(location=location, title=title, text=text))

        return object_movements

    def get_last_tracking_info(self, tracking_code):
        trackings = self.get_all_tracking_info(tracking_code)
        return trackings[0]
