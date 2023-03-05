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

# functions.mprint(tartiblangan_alomatlar_turgunligi)

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

#  tartiblangan_alomatlar_turgunligi `ni BIRINCHI 8tasi uchun alohida RS top
# print(tartiblangan_alomatlar_turgunligi[::2])
alomatlar_tuplami = [x[0] for x in tartiblangan_alomatlar_turgunligi[:8]]

# print(alomatlar_tuplami)
RS1 = functions.bittalik_rs(obyektlar_soni, alomatlar_tuplami, intervaldagi_vakillar, K1, K2)
ustun = [(item[0], item[1], target[item[0]]) for item in RS1.items()]
v = functions.criteria1(ustun, K1, K2)
#print(f"Criteria 1 qiymati = {v[0]:2.2f}, chegaraviy obyekt = {v[1]}")


#  tartiblangan_alomatlar_turgunligi `ni IKKINCHI 8tasi uchun alohida RS top
# print(tartiblangan_alomatlar_turgunligi[::2])
alomatlar_tuplami = [x[0] for x in tartiblangan_alomatlar_turgunligi[8:16]]

# print(alomatlar_tuplami)
RS2 = functions.bittalik_rs(obyektlar_soni, alomatlar_tuplami, intervaldagi_vakillar, K1, K2)
ustun = [(item[0], item[1], target[item[0]]) for item in RS2.items()]
v = functions.criteria1(ustun, K1, K2)
#print(f"Criteria 1 qiymati = {v[0]:2.2f}, chegaraviy obyekt = {v[1]}")


#  tartiblangan_alomatlar_turgunligi `ni UCHUNCHI 8tasi uchun alohida RS top
# print(tartiblangan_alomatlar_turgunligi[::2])
alomatlar_tuplami = [x[0] for x in tartiblangan_alomatlar_turgunligi[16:]]

# print(alomatlar_tuplami)
RS3 = functions.bittalik_rs(obyektlar_soni, alomatlar_tuplami, intervaldagi_vakillar, K1, K2)
ustun = [(item[0], item[1], target[item[0]]) for item in RS3.items()]
v = functions.criteria1(ustun, K1, K2)
#print(f"Criteria 1 qiymati = {v[0]:2.2f}, chegaraviy obyekt = {v[1]}")


# #  tartiblangan_alomatlar_turgunligi `ni TO'RTINCHI 4tasi uchun alohida RS top
# # print(tartiblangan_alomatlar_turgunligi[::2])
# alomatlar_tuplami = [x[0] for x in tartiblangan_alomatlar_turgunligi[18:]]
#
# # print(alomatlar_tuplami)
# RS4 = functions.bittalik_rs(obyektlar_soni, alomatlar_tuplami, intervaldagi_vakillar, K1, K2)
# ustun = [(item[0], item[1], target[item[0]]) for item in RS4.items()]
# v = functions.criteria1(ustun, K1, K2)
# print(f"Criteria 1 qiymati = {v[0]:2.2f}, chegaraviy obyekt = {v[1]}")




#####################
import numpy as np
from sklearn.manifold import TSNE
RS1 = [RS1[key] for key in RS1.keys()]
RS2 = [RS2[key] for key in RS2.keys()]
RS3 = [RS3[key] for key in RS3.keys()]
# for i in range(len(RS1)):
#     print(RS1[i], RS2[i], RS3[i])
#RS4 = [RS4[key] for key in RS4.keys()]
# print(type(RS4), RS4)
X = np.array([RS1, RS2, RS3])
# print(X)
# print(X)
X_embedded = TSNE(n_components=2,
                   init='random').fit_transform(X)



##########################################
#
#
# RASMINI CHIZAMIZ
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(figsize=(20, 10))
#
# marker = 'x^ov'
# for class_label in set(target):
#
#     # for group_key in RSLAR.keys():
#     x_lar = []
#     y_lar = []
#     id_lar = []
#
#     for n in range(len(X[0])):  # object_id in RS1.keys():
#         if target[n] == class_label:
#             x_lar.append(X[0, n])
#             y_lar.append(X[1, n])
#             id_lar.append(n)
#     # print(x_lar, "\n\n\n", y_lar)
#     ax.scatter(x_lar, y_lar, s=250, marker=marker[class_label], label=str(class_label))
#
#     for x in range(len(x_lar)):
#         ax.annotate(x, (x_lar[x], y_lar[x]))
#
# ax.legend()
#
# fig.savefig(f"out_data\\{tanlanma_nomi}\\fig3x.pdf")
# functions.start_file(f"out_data\\{tanlanma_nomi}\\fig3x.pdf")