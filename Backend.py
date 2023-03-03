import requests
import math
import sqlite3

def addElement(userID, sort, height=3, warm=0, waterRes=3, color='', txt=('',), typee='', name=''):
	txtST = '/'
	for i in txt:
		txtST += str(i).lower() + '/'
	if sort == 'boots' or sort == 'pants' or sort == 'jacket':
		cur.execute(f'CREATE TABLE IF NOT EXISTS u{userID}t{sort} (name TEXT, height INT, warm INT, waterRes INT, color TEXT, txt TEXT)')
		cur.execute(f'INSERT INTO u{userID}t{sort} VALUES {(name, height, warm, waterRes, color, txtST)}')
	elif sort == 'cap' or sort == 'mask':
		cur.execute(f'CREATE TABLE IF NOT EXISTS u{userID}t{sort} (name TEXT, warm INT, color TEXT, txt TEXT)')
		cur.execute(f'INSERT INTO u{userID}t{sort} VALUES {(name, warm, color, txtST)}')
	elif sort == 'other':
		cur.execute(f'CREATE TABLE IF NOT EXISTS u{userID}t{sort} (name TEXT, type TEXT, height INT, warm INT, waterRes INT, color TEXT, txt TEXT)')
		cur.execute(f'INSERT INTO u{userID}t{sort} VALUES {(name, typee, height, warm, waterRes, color, txtST)}')
	con.commit()

def foundElements(userID, sort, warm, waterRes, txt, height=None):
	try:
		send = f'SELECT rowid, * FROM u{userID}t{sort} WHERE'

		if height is not None:
			send += f'(height BETWEEN {height[0]} AND {height[1]}) AND'
		if warm is not None:
			send += f'(warm BETWEEN {warm[0]} AND {warm[1]}) AND'
		if waterRes is not None:
			send += f'(waterRes BETWEEN {waterRes[0]} AND {waterRes[1]}) AND'
		for word in txt:
			send += f"(txt LIKE '%{word.lower()}%') AND"

		cur.execute(send.rstrip(' AND'))
		print(cur.fetchall())
		return cur.fetchall()
	except:
		return []

def deleteElement(userID, sort, rowid):
	cur.execute(f'''DELETE FROM u{userID}t{sort} WHERE rowid = {rowid}''')
	con.commit()


def get_weather(city):
    # Функция для получения погоды.
    # Входные данные city- название города на анг с большой буквы

    city_id = 0
    appid = "ef244d6ee28299c4fc2c5080b4c603b7"
    r = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = r.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
              for d in data['list']]
    city_id = data['list'][0]['id']
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'id': city,'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    os = data['weather'][0]['description']
    t = data['main']['temp']
    dryness = res.json()['main'][0]['humidity']
    re = requests.get('http://api.openweathermap.org/data/2.5/wind',
                      params={'id': city, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    fast = re.json()['wind'][0]['speed']
    power = re.json()['wind'][0]['deg']

    return t, os, dryness, fast, power

    # t - температура
    # os - тип осадков
    # dryness - влажность в %
    # fast - скорость ветра в м/с
    # power - ветер в градусах
    return t, os, dryness, fast, power

def get_cloth(city):
    # Получение данных о погоде
    temperature,weather,humidity,wind=get_weather(city)

    # Вычесление t°C для одежды
    temperature_cofficient=(wind+humidty)*0.5
    temperature_parameter=temperature-temperature_coefficient
    temperature_parameter=temperature_parameter+35
    temperature_level=temperature_parameter/10
    temperature_level=math.floor(temperature_level)
    temperature_level=temperature_level+1


    # Дико тупой код, извените. Я потом сделаю что то лучше
    if temperature_level==1:
        if weather=="Дождь":
            parameter_cloth_list=[   [ [] , [[3,4]] , [ ] , [[3,4]] ],   [ ["umbrella"] , [[2,3,4]] , [ ] , [[2,3]] ],   [ ["raincoat"] , [[2,3]] , [ ] , [[3,4]] ]   ]
        elif weather=="Снег":
            parameter_cloth_list=[   [ [] , [[]] , [] , [[]] ], ]
        elif weather=="Ливень":
            parameter_cloth_list=[   [ [] , [[4,5]] , [ ] , [[4,5]] ],   [ ["umbrella"] , [[4,5]] , [ ] , [[4,5]] ],   [ ["raincoat"] , [[4,5]] , [ ] , [[4,5]] ]   ]
        elif weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[1,2,3]] , [ ] , [[1,2,3]] ]    ]

    if temperature_level==1:#-35 - -25
        if weather=="Снег":
            parameter_cloth_list=[   [ [] , [[],[5]] , [[],[5]] , [[],[5]] ] ]
        elif weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[],[5]] , [[],[5]] , [[],[5]] ] ]

    elif temperature_level==2:#-25 - -15
        if weather=="Снег":
            parameter_cloth_list=[   [ [] , [[],[4,5]] , [[],[3,4]] , [[],[4,5]] ] ]
        elif weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[],[4,5]] , [[],[3,4]] , [[],[4,5]] ] ]  

    elif temperature_level==3:#-15 - -5
        if weather=="Снег":
            parameter_cloth_list=[   [ [] , [[2,3,4,5],[4]] , [[],[2,3]] , [[2,3,4,5],[4]] ] ]
        elif weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[2,3,4,5],[4]] , [[],[2,3]] , [[2,3,4,5],[4]] ] ] 

    elif temperature_level==4: #-5 - 5
        if weather=="Снег":
            parameter_cloth_list=[   [ [] , [[2,3],[3,4]] , [[],[]] , [[2,3],[3,4]] ], ]
        elif weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[1,2,3],[3,4]] , [[],[]] , [[1,2,3],[3,4]] ]    ]     
        elif weather=="Дождь":
            parameter_cloth_list=[   [ [] , [[3,4],[3,4]] , [ ] , [[3,4],[3,4]] ],   [ ["umbrella"] , [[2,3,4],[3,4]] , [ ] , [[2,3],[3,4]] ],   [ ["raincoat"] , [[2,3],[3,4]] , [ ] , [[3,4],[3,4]] ]   ]
        elif weather=="Ливень":
            parameter_cloth_list=[   [ [] , [[4,5],[3,4]] , [ ] , [[4,5],[3,4]] ],   [ ["umbrella"] , [[3,4,5],[3,4]] , [ ] , [[2,3],[4,5]] ],   [ ["raincoat"] , [[3,4,5],[3,4]] , [ ] , [[4,5],[3,4]] ]   ]

    elif temperature_level==5: #5 - 15
        if weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[1,2,3],[2,3]] , [[],[]] , [[1,2,3],[2,3]] ]    ]     
        elif weather=="Дождь":
            parameter_cloth_list=[   [ [] , [[3,4],[2,3]] , [ ] , [[3,4],[2,3]] ],   [ ["umbrella"] , [[2,3,4],[2,3]] , [ ] , [[2,3],[2,3]] ],   [ ["raincoat"] , [[2,3],[2,3]] , [ ] , [[3,4],[2,3]] ]   ]
        elif weather=="Ливень":
            parameter_cloth_list=[   [ [] , [[4,5],[2,3]] , [ ] , [[4,5],[2,3]] ],   [ ["umbrella"] , [[3,4,5],[2,3]] , [ ] , [[2,3],[2,3]] ],   [ ["raincoat"] , [[3,4,5],[2,3]] , [ ] , [[4,5],[2,3]] ]   ]  

    elif temperature_level==6: #15 - 25
        if weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[1,2,3],[1,2]] , [[],[]] , [[1,2,3],[1,2]] ]    ]     
        elif weather=="Дождь":
            parameter_cloth_list=[   [ [] , [[3,4],[1,2]] , [ ] , [[3,4],[1,2]] ],   [ ["umbrella"] , [[2,3,4],[1,2]] , [ ] , [[2,3],[1,2]] ],   [ ["raincoat"] , [[2,3],[1,2]] , [ ] , [[3,4],[1,2]] ]   ]
        elif weather=="Ливень":
            parameter_cloth_list=[   [ [] , [[4,5],[1,2]] , [ ] , [[4,5],[1,2]] ],   [ ["umbrella"] , [[3,4,5],[1,2]] , [ ] , [[2,3],[1,2]] ],   [ ["raincoat"] , [[3,4,5],[1,2]] , [ ] , [[4,5],[1,2]] ]   ]

    elif temperature_level==6: #25 - 35
        if weather=="Ясно" or "Облачно":
            parameter_cloth_list=[   [ [] , [[1,2,3],[1]] , [[],[]] , [[1,2,3],[1]] ]    ]     
        elif weather=="Дождь":
            parameter_cloth_list=[   [ [] , [[3,4],[1]] , [ ] , [[3,4],[1]] ],   [ ["umbrella"] , [[2,3,4],[1]] , [ ] , [[2,3],[1]] ],   [ ["raincoat"] , [[2,3],[1]] , [ ] , [[3,4],[1]] ]   ]
        elif weather=="Ливень":
            parameter_cloth_list=[   [ [] , [[4,5],[1]] , [ ] , [[4,5],[1]] ],   [ ["umbrella"] , [[3,4,5],[1]] , [ ] , [[2,3],[1]] ],   [ ["raincoat"] , [[3,4,5],[1]] , [ ] , [[4,5],[1]] ]   ]

    combo=[]
    m_combo=[]

    for i in range(len(parameter_cloth_list)):
        parameter_cloth=parameter_cloth_list.pop(0)

        other=parameter_cloth.pop(0)
        k_jacket=parameter_cloth.pop(0)
        jacket=parameter_cloth.pop(0)
        pants=parameter_cloth.pop(0)

        other_name=other.pop(0)

        k_jacket_name="k"
        k_jacket_wr=k_jacket.pop(0)
        k_jacket_t=k_jacket.pop(0)

        jacket_wr=jacket.pop(0)
        jacket_t=jacket.pop(0)

        pants_wr=pants.pop(0)
        pants_t=pants.pop(0)

        combo=[foundElements(0,"other",None,None,other_name),
        foundElements(0,"other",k_jacket_t,k_jacket_wr,"k"),
        foundElements(0,"jacket",jacket_t,jacket_wr,None),
        foundElements(0,"pants",pants_t,pants_wr,None)]

        m_combo.append(combo)
    return combo
print(get_cloth(a=input()))
