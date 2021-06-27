from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import time
import json
from unidecode import unidecode
from datetime import datetime
from datetime import timedelta
import urllib.request
from urllib.parse import quote
from elasticsearch import Elasticsearch
from tweepy import Stream
import re

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

es = Elasticsearch()


def check_sentiment(text):
    sentiment = urllib.request.urlopen(
        'http://localhost:8095/sentiment?text=' + quote(text, safe = '')
    ).read()
    decode = json.loads(sentiment.decode('utf-8'))
    return decode['label'], decode['string']


class StdOutListener(StreamListener):
    def on_data(self, data):
        global conn, curr, es
        try:
            tweet = json.loads(data)
            # elastic assumed we passed UTC
            tweettime = datetime.strftime(
                datetime.strptime(
                    tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
                )
                + timedelta(hours = 0),
                '%Y-%m-%d %H:%M:%S',
            )
        except:
            return False
        text = re.sub(r'[^\x00-\x7F]+', '', tweet['text'])
        data_text = text
        id_str = tweet['id_str']
        screen_name = re.sub(r'[^\x00-\x7F]+', '', tweet['user']['screen_name'])
        followers_count = tweet['user']['followers_count']
        friends_count = tweet['user']['friends_count']
        listed_count = tweet['user']['listed_count']
        favourites_count = tweet['user']['favourites_count']
        statuses_count = tweet['user']['statuses_count']
        retweet_count = int(tweet['retweet_count'])
        quote_count = 0
        favorite_count = 0
        reply_count = 0
        if 'retweeted_status' in tweet:
            retweet_count = int(tweet['retweeted_status']['retweet_count'])
            quote_count = int(tweet['retweeted_status']['quote_count'])
            favorite_count = int(tweet['retweeted_status']['favorite_count'])
            reply_count = int(tweet['retweeted_status']['reply_count'])
        if 'quoted_status' in tweet:
            quoted_status_text = re.sub(
                r'[^\x00-\x7F]+', '', tweet['quoted_status']['text']
            )
        else:
            quoted_status_text = 'NULL'
        lang = tweet['lang']
        if lang not in ['in', 'en']:
            print('pass, lang not supported')
            return True
        if 'retweeted_status' in tweet:
            retweet = 'true'
            retweet_text = re.sub(
                r'[^\x00-\x7F]+', '', tweet['retweeted_status']['text']
            )
            data_text = retweet_text
            if 'extended_tweet' in tweet['retweeted_status']:
                retweet_text_full = re.sub(
                    r'[^\x00-\x7F]+',
                    '',
                    tweet['retweeted_status']['extended_tweet']['full_text'],
                )
                data_text = retweet_text_full
            else:
                retweet_text_full = 'NULL'
        else:
            retweet = 'false'
            retweet_text = 'NULL'
            retweet_text_full = 'NULL'
        sentiment, processed_string = check_sentiment(data_text)
        doc = {
            'datetime': tweettime.replace(' ', 'T'),
            'body': unidecode(text),
            'screen_name': unidecode(screen_name),
            'followers_count': followers_count,
            'friends_count': friends_count,
            'listed_count': listed_count,
            'favourites_count': favourites_count,
            'statuses_count': statuses_count,
            'quoted_status_text': unidecode(quoted_status_text),
            'lang': lang,
            'retweet': retweet,
            'retweet_text': unidecode(retweet_text),
            'retweet_text_full': unidecode(retweet_text_full),
            'sentiment': sentiment,
            'retweet_count': retweet_count,
            'quote_count': quote_count,
            'favorite_count': favorite_count,
            'reply_count': reply_count,
            'processed_string': processed_string,
        }
        es.index(
            index = 'twitter_streaming',
            doc_type = 'tweet',
            id = id_str,
            body = doc,
        )
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    while True:
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            stream = Stream(auth, l)
            stream.filter(
                track = [
                    'parliament malaysia',
                    'parlimen',
                    'ge 14',
                    'pilihan raya',
                    'pru 14',
                    'najib razak',
                    'mahathir',
                    'dr mahathir',
                    'barisan nasional',
                    'pakatan harapan',
                    'guan eng',
                    'anwar ibrahim',
                    'umno',
                    'rafizi ramli',
                    'tun m',
                    'perlis',
                    'kedah',
                    'kelantan',
                    'penang',
                    'sabah',
                    'johor',
                    'selangor',
                    'sarawak',
                    'melaka',
                    'malacca',
                    'pulau pinang',
                    'perak',
                    'pahang',
                    'terengganu',
                    'negeri sembilan',
                    'reformasi',
                    'himpunan merdeka',
                    'malay mail',
                    'gst',
                    '1mdb',
                    'edge markets',
                    'new malaysia',
                    'bursa',
                    'ekonomi',
                    'kewangan',
                    'petronas',
                    'pdrm',
                    'pkr',
                    'keadilan rakyat',
                    'parti islam',
                    'ptptn',
                    'felda',
                    'kwsp',
                    'segamat',
                    'sekijang',
                    'labis',
                    'pagoh',
                    'ledang',
                    'bakri',
                    'muar',
                    'parit sulong',
                    'ayer hitam',
                    'sri gading',
                    'batu pahat',
                    'simpang renggam',
                    'kluang',
                    'sembrong',
                    'mersing',
                    'tenggara',
                    'kota tinggi',
                    'pengerang',
                    'tebrau',
                    'pasir gudang',
                    'johor bahru',
                    'pulai',
                    'gelang patah',
                    'kulai',
                    'pontian',
                    'tanjong piai',
                    'langkawi',
                    'jerlun',
                    'kubang pasu',
                    'padang terap',
                    'pokok sena',
                    'alor star',
                    'kuala kedah',
                    'pendang',
                    'jerai',
                    'sik',
                    'merbok',
                    'sungai petani',
                    'baling',
                    'padang serai',
                    'kulim-bandar baharu',
                    'tumpat',
                    'pengkalan chepa',
                    'kota bharu',
                    'pasir mas',
                    'rantau panjang',
                    'kubang kerian',
                    'bachok',
                    'ketereh',
                    'tanah merah',
                    'pasir puteh',
                    'machang',
                    'jeli',
                    'kuala krai',
                    'gua musang',
                    'masjid tanah',
                    'alor gajah',
                    'tangga batu',
                    'bukit katil',
                    'kota melaka',
                    'jasin',
                    'jelebu',
                    'jempol',
                    'seremban',
                    'kuala pilah',
                    'rasah',
                    'rembau',
                    'telok kemang',
                    'tampin',
                    'cameron highlands',
                    'lipis',
                    'raub',
                    'jerantut',
                    'indera mahkota',
                    'kuantan',
                    'paya besar',
                    'pekan',
                    'maran',
                    'kuala krau',
                    'temerloh',
                    'bentong',
                    'bera',
                    'rompin',
                    'gerik',
                    'lenggong',
                    'larut',
                    'parit buntar',
                    'bagan serai',
                    'bukit gantang',
                    'taiping',
                    'padang rengas',
                    'sungai siput',
                    'tambun',
                    'ipoh timor',
                    'ipoh barat',
                    'batu gajah',
                    'kuala kangsar',
                    'beruas',
                    'parit',
                    'kampar',
                    'gopeng',
                    'tapah',
                    'pasir salak',
                    'lumut',
                    'bagan datok',
                    'telok intan',
                    'tanjong malim',
                    'padang besar',
                    'kangar',
                    'arau',
                    'kepala batas',
                    'tasek gelugor',
                    'bagan',
                    'permatang pauh',
                    'bukit mertajam',
                    'batu kawan',
                    'nibong tebal',
                    'bukit bendera',
                    'tanjong',
                    'jelutong',
                    'bukit gelugor',
                    'bayan baru',
                    'balik pulau',
                    'kudat',
                    'kota marudu',
                    'kota belud',
                    'tuaran',
                    'sepanggar',
                    'kota kinabalu',
                    'putatan',
                    'penampang',
                    'papar',
                    'kimanis',
                    'beaufort',
                    'sipitang',
                    'ranau',
                    'keningau',
                    'tenom',
                    'pensiangan',
                    'beluran',
                    'libaran',
                    'batu sapi',
                    'sandakan',
                    'kinabatangan',
                    'silam',
                    'semporna',
                    'tawau',
                    'kalabakan',
                    'mas gading',
                    'santubong',
                    'petra jaya',
                    'bandar kuching',
                    'stampin',
                    'kota samarahan',
                    'mambong',
                    'serian',
                    'batang sadong',
                    'batang lupar',
                    'sri aman',
                    'lubok antu',
                    'betong',
                    'saratok',
                    'tanjong manis',
                    'igan',
                    'sarikei',
                    'julau',
                    'kanowit',
                    'lanang',
                    'sibu',
                    'mukah',
                    'selangau',
                    'kapit',
                    'hulu rajang',
                    'bintulu',
                    'sibuti',
                    'miri',
                    'baram',
                    'limbang',
                    'lawas',
                    'sabak bernam',
                    'sungai besar',
                    'hulu selangor',
                    'tanjong karang',
                    'kuala selangor',
                    'selayang',
                    'gombak',
                    'ampang',
                    'pandan',
                    'hulu langat',
                    'serdang',
                    'puchong',
                    'kelana jaya',
                    'petaling jaya selatan',
                    'petaling jaya utara',
                    'subang',
                    'shah alam',
                    'kapar',
                    'klang',
                    'kota raja',
                    'kuala langat',
                    'sepang',
                    'besut',
                    'setiu',
                    'kuala nerus',
                    'kuala terengganu',
                    'marang',
                    'hulu terengganu',
                    'dungun',
                    'kemaman',
                    'kepong',
                    'batu',
                    'wangsa maju',
                    'segambut',
                    'setiawangsa',
                    'titiwangsa',
                    'bukit bintang',
                    'lembah pantai',
                    'seputeh',
                    'cheras',
                    'bandar tun razak',
                    'putrajaya',
                    'labuan',
                    'teknologi',
                    'pendidikan',
                    'kerajaan',
                    'pembangkang',
                ]
            )
        except Exception as e:
            print('outer exception:', e)
            time.sleep(15 * 60)
            continue
