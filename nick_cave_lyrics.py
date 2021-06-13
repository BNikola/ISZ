import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import time

data = []


address = "https://www.nickcave.com/lyrics/"
r = requests.get(address)
c = r.content
soup = BeautifulSoup(c, "html.parser")
links = soup.select('div.lyric-album-list > a')
links = [k.attrs['href'] for k in links]

def process(l):
    d = {}
    r = requests.get(l)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    d['title'] = soup.find('h1').text
    lyrics = soup.select('div.lyrics > p')
    d['lyrics']= [line.text for line in lyrics]
    d['link'] = l
    # print(d)
    data.append(d)

start_time = time.time()
pool = ThreadPool(20)
pool.map(process, links)

df = pd.DataFrame(data)
df['lyrics_all'] = [','.join(map(str,ll)) for ll in df.lyrics]

f_dog = df.lyrics_all.str.contains('dog', case=False)
f_rain = df.lyrics_all.str.contains('rain', case=False)
print(df[f_dog & f_rain])
print(time.time() - start_time)
