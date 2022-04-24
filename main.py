import httpx, json, threading, time, random, string, itertools
from colorama import Fore, init; init()

__config__, __proxies__, __lock__ = json.load(open('./config.json')), itertools.cycle(open('./proxies.txt').read().splitlines()), threading.Lock()

class GenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def get_random_string(self):
        return ''.join(random.choice(string.ascii_letters) for _ in range(15))

    def printf(self, content: str):
        __lock__.acquire()
        print(content)
        __lock__.release()

    def run(self):
        with httpx.Client(proxies= f'http://{next(__proxies__)}', headers= {'User-agent': 'S4A/2.0.15 (com.spotify.s4a; build:201500080; iOS 13.4.0) Alamofire/4.9.0','Content-Type': 'application/x-www-form-urlencoded; charset=utf-8','Accept': 'application/json, text/plain;q=0.2, */*;q=0.1','App-Platform': 'IOS','Spotify-App': 'S4A','Accept-Language': 'en-TZ;q=1.0','Accept-Encoding': 'gzip;q=1.0, compress;q=0.5','Spotify-App-Version': '2.0.15'}) as client:
            
            magic_string = self.get_random_string()

            profil = {
                'gender': 'female',
                'birth_year': 2000,
                'birth_month': 7,
                'birth_day': 5,
                'password': magic_string + '1337',
                'username': magic_string,
                'email': magic_string + '@gmail.com'
            }

            payload = 'creation_point=lite_7e7cf598605d47caba394c628e2735a2&password_repeat={0}&platform=Android-ARM&iagree=true&password={1}&gender={2}&key=a2d4b979dc624757b4fb47de483f3505&birth_day={3}&birth_month={4}&email={5}&birth_year={6}'.format(profil['password'],profil['password'],profil['gender'],profil['birth_day'],profil['birth_month'],profil['email'],profil['birth_year'])
            response = client.post('https://spclient.wg.spotify.com/signup/public/v1/account', data= payload)

            if response.status_code == 429:
                self.printf(f'({magic_string}) {Fore.YELLOW}Ratelimited{Fore.RESET}.')
            else:
                if 'status' in str(response.json()):
                    if response.json()['status'] == 1:
                        combo = f'{magic_string}@gmail.com:{magic_string}1337'

                        self.printf(f'({magic_string}) {Fore.LIGHTGREEN_EX}{combo}{Fore.RESET}.')
                        with open('./acc.txt', 'a+') as f:
                            f.write(f'{combo}\n')
                    
                    if response.json()['status'] == 320:
                        self.printf(f'({magic_string}) {Fore.LIGHTCYAN_EX}Proxies detected{Fore.RESET}.')

if __name__ == '__main__':
    while True:
        while threading.active_count() >= __config__['threads']:
            time.sleep(1)
        
        GenThread().start()