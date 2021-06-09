import csv
import json


# класс для хранения значения выделяемой тепловой мощности в момент времени x
class Point:
    x = None
    y = None

    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def serialize(self):
        return {"x": self.x, "y": self.y}


# класс для хранения информации об оборудовании
class Equipment:
    id = None
    offset = None
    data = None

    def __init__(self, id, offset, data):
        self.id = id
        self.offset = offset
        self.data = data

    def serialize(self):
        return {"id": self.id, "offset": self.offset, "data": [i.serialize() for i in self.data]}


# функция чтения данных их CSV-файла
def parseCSV(csv_path):
    local_equipment = {}
    with open(csv_path, "r") as fileObj:
        reader = csv.reader(fileObj, delimiter=';')
        # пропускаем заголовок CSV-файла
        next(reader, None)
        # просматриваем каждую строку файла
        for row in reader:
            # если найдено новое оборудование
            if local_equipment.get(int(row[0])) is None:
                local_equipment[int(row[0])] = [Point(float(row[1]), float(row[2]))]
            # если добавляем данные в уже существующую запись
            else:
                local_equipment[int(row[0])].append(Point(float(row[1]), float(row[2])))
    return local_equipment


# функция конвертации списка смещений оборудования к словарю
def convertOffsetsToDict(local_offsets, keys):
    offsets_dict = {}
    index = 0
    for key in keys:
        offsets_dict[key] = local_offsets[index]
        index += 1
    return offsets_dict


# парсим данные из csv-файла
equipmentList = parseCSV('SourceData.csv')
offsetsValues = [0, -6, 9, -15, -12, 7, 12, -3]
# формируем смещения
offsets = convertOffsetsToDict(offsetsValues, equipmentList.keys())
# формируем объекты оборудования
equipment = []
for i in equipmentList:
    data = []
    for j in equipmentList[i]:
        data.append(j)
    e = Equipment(i, offsets[i], data)
    equipment.append(e)
# переводим в json
result = json.dumps([m.serialize() for m in equipment],
                    ensure_ascii=False,
                    default=str),
print(result[0])
# сохраняем в файл
# f = open("result.json", "w")
#
# for i in result:
#     f.write(i)
#
# f.close()