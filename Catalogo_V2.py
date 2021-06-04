import requests
import json


def get_ids(info):
    ids_particulares = list()

    for element in info:
        ids_ = element.get('contentIds')
        if ids_ : 
            # print(ids_)
            ids_particulares += ids_

    # print(ids_particulares)
    return ids_particulares

def get_cast(data_content):
    credits_ = list()
    for credit in data_content:
        if credit['keyedRoles'][0]['key'] == 'C':
            credits_.append(credit['name'])
    return credits_

def  get_episode(episode):
    epi = dict()

    epi['title'] = episode.get('title',None)
    epi['id'] = episode.get('contentId',None)
    epi['duracion'] = episode.get('runtime',None)
    epi['anio'] = episode.get('releaseYear',None)
    epi['synopsis'] = episode.get('logLine',None)
    if 'credits' in episode.keys():
        epi['actores'] = get_cast(episode['credits'])
    return epi

def get_temporadas(data_content):
    temporadas = list()
    if data_content:
        for season in data_content:
            temp = {
                'title': season.get('title',None),
                'contentId': season.get('contentId',None),
                'logLine': season.get('logLine',None),
                'rating': season.get('ratingName',None)
                }
            if 'credits' in season.keys():
                temp['actores'] = get_cast(season['credits'])
            
            episodes = list()
            if 'childContent' in season.keys():    
                for episode in season['childContent']:
                    epi = get_episode(episode)
                    if epi:
                        episodes.append(epi)
            temp['episodios'] = episodes
            temporadas.append(temp)
    return temporadas

def get_content(id_):
    url = "https://playdata.starz.com/metadata-service/play/partner/Web_ES/v8/content?lang=es-ES&contentIds={}&includes=title,logLine,contentType,contentId,ratingName,properCaseTitle,topContentId,releaseYear,runtime,images,credits,episodeCount,seasonNumber,childContent,orderapi".format(id_)
    
    response = requests.get(url)
    response = response.json()

   
    try:
        print('entra')
        data_content = response['playContentArray']['playContents'][0]
    except Exception:
        print('no entra')
        return None

    info = dict()



    info['titulo'] = data_content.get('title',None)
    info['id'] = id_
    info['synopsis'] = data_content.get('logLine',None)
    info['actores'] = get_cast(data_content['credits'])

    if data_content.get('contentType').upper() != 'MOVIE':
        
        info['temporadas'] = get_temporadas(data_content.get('childContent',None))
    else:
        duracion = data_content.get('runtime',None)
        if  duracion:
            duracion = int(duracion / 60)
        info['duracion'] = duracion
        info['rating'] = data_content.get('ratingName',None) 
        info['anio'] = data_content.get('releaseYear',None)

    # print(info)
    return info

if __name__ == '__main__':
    print('itworks')

    api_para_conseguir_ids = "https://playdata.starz.com/metadata-service/play/partner/Web_ES/v8/blocks?playContents=map&lang=es-ES&pages=MOVIES,SERIES&includes=contentId,contentType,title,product,seriesName,seasonNumber,free,comingSoon,newContent,topContentId,properCaseTitle,categoryKeys,runtime,popularity,original,firstEpisodeRuntime,releaseYear,images,minReleaseYear,maxReleaseYear,episodeCount,detail"

    response = requests.get(api_para_conseguir_ids)

    response = response.json()

    info_1= response['blocks'][0]['blocks']
    info_2= response['blocks'][1]['blocks']
    
    ids = list()


    ids+= get_ids(info_1)
    ids+= get_ids(info_2)

    # print(ids)

    content_total = list()
    for id_ in ids:
        content = get_content(id_)
        if content:
            content_total.append(content)
    cont=str(content_total)
    toda_info=open('toda_lainfo.txt', 'w')
    toda_info.write(cont)
    toda_info.close()
    print(content_total)
