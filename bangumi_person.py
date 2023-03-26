import requests
import time

if __name__ == '__main__':
    personId = input('请输入人物id: ')
    personUrl = f'https://api.bgm.tv/v0/persons/{personId}/subjects'
    userAgent = '434053/person-relation-script'
    s = requests.Session()
    s.headers.update({'User-Agent': userAgent})
    r = s.get(personUrl)
    if r.status_code != 200:
        print('请求失败, url: '+personUrl)
        exit()
    r = r.json()
    ids = [i['id'] for i in r]
    personDict = {}
    result = {}
    resultSubject = {}
    for id in ids:
        subjectUrl = f'https://api.bgm.tv/v0/subjects/{id}/persons'
        r = s.get(subjectUrl)
        if r.status_code != 200:
            print('请求失败, url: '+subjectUrl)
            continue
        r = r.json()
        time.sleep(1)
        personIds = [i['id'] for i in r]
        personDict.update({i['id']: i['name'] for i in r})
        # personIds去重
        personIds = list(set(personIds))
        for personId in personIds:
            if personId in result:
                result[personId] += 1
                resultSubject[personId].append(id)
            else:
                resultSubject[personId] = []
                resultSubject[personId].append(id)
                result[personId] = 1

    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    result = [(personDict[i[0]], i[0], i[1], resultSubject[i[0]])
              for i in result]
    with open('result.txt', 'w', encoding='utf-8') as f:
        for i in result:
            f.write(f'{i[0]} {i[1]} {i[2]} subject{i[3]}\n')
    print(result)
