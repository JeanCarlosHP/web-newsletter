from imaplib import IMAP4_SSL
from email import message_from_bytes
from bs4 import BeautifulSoup
from quopri import decodestring

from backend.credentials import getEmail, getPassword


def extractContent():
    host = 'imap.gmail.com'
    port = 993

    server = IMAP4_SSL(host, port)
    server.login(getEmail(), getPassword())
    server.select()
    status, data = server.search(
        None, '(FROM "newsletter@filipedeschamps.com.br")')

    status, data = server.fetch(data[0].split()[-1], '(RFC822)')
    email_msg = data[0][1]

    soup = BeautifulSoup(markup=email_msg, features='lxml')
    td = soup.find_all('td')[0]
    news = [x.extract() for x in td.findAll('p')]

    message = message_from_bytes(email_msg)
    raw_date = message['Date'].replace(',', '').split()

    translation_day = {
        'Mon': 'Seg',
        'Tue': 'Ter',
        'Wed': 'Qua',
        'Thu': 'Qui',
        'Fri': 'Sex',
    }

    translation_month = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    dayOfWeek = translation_day[raw_date[0]]
    day = raw_date[1]
    month = translation_month[raw_date[2]]
    year = raw_date[3]

    date = f'{dayOfWeek}, {day}/{month}/{year}'

    utf = decodestring(str(news))
    text = utf.decode('utf-8')

    text = text.replace('</p>, <p', '</p><br><p').replace('[', '').replace(
        ']', '').replace('&lt;/strong&gt;', '</strong>').replace('strong&gt;', '</strong>')

    return {'date': date, 'content': text}
