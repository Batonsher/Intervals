import functions
from model_settings import tanlanma_nomi
import pickle

# READ DATA
DF = []
target = []
with open(f"out_data\\{tanlanma_nomi}\\binar_nominal_objects.csv") as objfile, \
     open(f"init_data\\{tanlanma_nomi}\\Target.csv") as targetfile:

    for row in objfile:
        DF.append([int(x) for x in row.split()])

    for row in targetfile:
        target.append(int(row))

K1, K2 = target.count(1), target.count(2)
obyektlar_soni = len(target)
alomatlar_soni = len(DF[0])


with open(f"out_data\\{tanlanma_nomi}\\intervals.baton", 'rb') as baton_file:
    db = dict(pickle.load(baton_file))

# print(f"#-alomat \nMezon 2, -dan (kiradi), -gacha (kirmaydi), intervaldagi elementlar soni, f1(i)")
# db[<alomat nomeri>]:  [0] => alomat nomeri
# [1] => (Mezon 2, -dan (kiradi), -gacha (kirmaydi),
#         intervaldagi elementlar soni, f1(i), [intervalga kirgan ids] )


#  har bir alomat uchun alomatlar_turgunligi `ni topdik
alomatlar_turgunligi = []  # list(range(obyektlar_soni))
for feature_no in db.keys():
    summa = 0
    for interval in db[feature_no]:
        # print(interval[3], interval[4])
        if interval[4] < 0.5:
            summa += (1-interval[4]) * interval[3]
        else:
            summa += interval[4] * interval[3]
    alomatlar_turgunligi.append((feature_no, summa/obyektlar_soni))
    # print(f"{feature_no:2d}-alomat. PSI = {summa/obyektlar_soni:2.2f}")

#  tartiblangan_alomatlar_turgunligi `ni kamayish bo'yicha tartiblandi
tartiblangan_alomatlar_turgunligi = sorted(alomatlar_turgunligi, key=lambda x: x[1], reverse=True)

#  ПОДГОТОВКА
intervaldagi_vakillar = dict()
for obj_key in range(obyektlar_soni):
    for feature_key in range(alomatlar_soni):
        intervaldagi_vakillar[obj_key] = {feature_key: 0}

for x in range(alomatlar_soni):             # har bir Feature uchun
    for interval in db[x]:                  # har bir interval uchun
        k1_vakillari = k2_vakillari = 0
        # print(interval)
        for ind in interval[5]:             # feature'ning intervalidagi  har bir index uchun
            if target[ind] == 1:
                k1_vakillari += 1
            else:
                k2_vakillari += 1

        for ind in interval[5]:
            intervaldagi_vakillar[ind][x] = (k1_vakillari, k2_vakillari)
            # print(ind, intervaldagi_vakillar[ind])
        # print(interval[], intervaldagi_vakillar[x])

#  tartiblangan_alomatlar_turgunligi `ni TOQ o'rinda turganlari uchun alohida RS top
# print(tartiblangan_alomatlar_turgunligi[::2])
alomatlar_tuplami = [x[0] for x in tartiblangan_alomatlar_turgunligi[::2]]

# print(alomatlar_tuplami)
RS = functions.bittalik_rs(obyektlar_soni, alomatlar_tuplami, intervaldagi_vakillar, K1, K2)
ustun = [(item[0], item[1], target[item[0]]) for item in RS.items()]

v = functions.criteria1(ustun, K1, K2)
print(f"Criteria 1 qiymati = {v[0]:2.2f}, chegaraviy obyekt = {v[1]}")

#  tartiblangan_alomatlar_turgunligi `ni JUFT o'rinda turganlari uchun alohida RS top
# print(tartiblangan_alomatlar_turgunligi[1::2])
alomatlar_tuplami = [x[0] for x in tartiblangan_alomatlar_turgunligi[1::2]]

# print(alomatlar_tuplami)
RS = functions.bittalik_rs(obyektlar_soni, alomatlar_tuplami, intervaldagi_vakillar, K1, K2)
ustun = [(item[0], item[1], target[item[0]]) for item in RS.items()]

v = functions.criteria1(ustun, K1, K2)
print(f"Criteria 1 qiymati = {v[0]:2.2f}, chegaraviy obyekt = {v[1]}")

