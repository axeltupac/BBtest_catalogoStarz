import requests
import json


def get_pelis_ids():
    url = "https://playdata.starz.com/metadata-service/play/partner/Web_ES/v8/blocks?playContents=map&lang=es-" \
          "ES&pages=MOVIES&includes=title,releaseYear,logLine,directors,genres,actors,runtime"
    try:
        response = requests.get(url)
    except:
        print('An error has occurred: ')
    pelis = response.json()
    pelis = pelis['blocks'][-1]['playContentsById']
    return pelis
def get_series_ids():
    url_series="https://playdata.starz.com/metadata-service/play/partner/Web_ES/v8/blocks?playContents=map&lang=es-ES&pages=SERIES&includes=title,releaseYear,logLine,directors,genres,actors,runtime"
    try:
        response= requests.get(url_series)
    except:
        print('An error has ocurred: ')
    series= response.json()
    series= series['blocks'][-1]['playContentsById']
    return series
    
    
pelis = get_pelis_ids()
peli= open('pelis_info.txt', 'w')
peli.write(json.dumps(pelis, indent=4))
peli.close()

series=get_series_ids()
serie=open('series_info.txt', 'w')
serie.write(json.dumps(series, indent=4))
serie.close()
