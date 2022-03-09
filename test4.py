### _ARISTOKRAT_ ###
### Baton 9-mart ###
### Voaleykum-Assalom ###
import pickle
from nominallashtiruvchi import tanlanma_nomi

with open(f"out_data\\{tanlanma_nomi}\\intervals.baton", 'rb') as baton_file:
    db = dict(pickle.load(baton_file))

DF = []
target = []
with open(f"out_data\\{tanlanma_nomi}\\Objects.csv") as in_file:
    for line in in_file:

        row = [int(x) for x in line.split()[:-1]]
        DF.append(row)
        target.append(int(float(line.split()[-1])))

k1_quvvat = target.count(1)
k2_quvvat = target.count(2)

obyektlar_soni = len(target)
alomatlar_soni = len(DF[0])

#########################################################
#    UXSHASHLIK va FARQ                                ##
#########################################################

sinflararo_farq = dict()
sinflararo_uxshashlik = dict()

# intervaldagi_vakillar = {x: {} for x in range(obyektlar_soni)}
intervaldagi_vakillar = dict()
for obj_key in range(obyektlar_soni):
    for feature_key in range(alomatlar_soni):
        intervaldagi_vakillar[obj_key] = {feature_key: 0}

for x in range(29):             # har bir Feature uchun
    featurening_sinflararo_farqi = 1
    featurening_sinflararo_uxshashligi = 0
    farq_summa = 0
    uxshash_summa = 0
    for interval in db[x]:      # har bir interval uchun
        k1_vakillari = k2_vakillari = 0
        # print(interval)
        for ind in interval[5]:   # feature'ning intervalidagi  har bir index uchun
            if target[ind] == 1:
                k1_vakillari += 1
            else:
                k2_vakillari += 1

        # print(k1_vakillari, k2_vakillari)
        farq_summa += k1_vakillari*k2_vakillari
        uxshash_summa += k1_vakillari*(k1_vakillari - 1) + k2_vakillari * (k2_vakillari - 1)

        # print(x, interval)#, intervaldagi_vakillar[x])
        for ind in interval[5]:
            intervaldagi_vakillar[ind][x] = (k1_vakillari, k2_vakillari)
            # print(ind, intervaldagi_vakillar[ind])
        # print(interval[], intervaldagi_vakillar[x])

    featurening_sinflararo_farqi -= farq_summa / (k1_quvvat * k2_quvvat)
    featurening_sinflararo_uxshashligi = uxshash_summa / (k1_quvvat ** 2 - k1_quvvat + k2_quvvat ** 2 - k2_quvvat)

    sinflararo_farq[x] = featurening_sinflararo_farqi
    sinflararo_uxshashlik[x] = featurening_sinflararo_uxshashligi

# VAZN
featurening_vazni = dict()
for x in sinflararo_uxshashlik.keys():
    featurening_vazni[x] = sinflararo_uxshashlik[x] * sinflararo_farq[x]
    # print(sinflararo_uxshashlik[x], sinflararo_farq[x], featurening_vazni[x])


####################################################
#     OBYEKTNING UMUMLASHGAN BAHOSI    #############
####################################################


obyektning_umulashgan_bahosi = dict()
for obj_key in range(obyektlar_soni):     # HAR BIR OBJECT UCHUN
    RS = 0
    for feature_key in range(alomatlar_soni):
        RS += featurening_vazni[feature_key] * \
              (intervaldagi_vakillar[obj_key][feature_key][0] \
               / k1_quvvat - intervaldagi_vakillar[obj_key][feature_key][1] / k2_quvvat)
        # print(feature_key, RS)
        # print(obj_key, feature_key, intervaldagi_vakillar[obj_key][feature_key][0] / k1_quvvat - intervaldagi_vakillar[obj_key][feature_key][1] / k2_quvvat)
    obyektning_umulashgan_bahosi[obj_key] = RS

# print(intervaldagi_vakillar[98][0][1])
for el in obyektning_umulashgan_bahosi.items():
    print(el)
# for obj_key in range(obyektlar_soni):
#     print(obj_key, intervaldagi_vakillar[obj_key][0])

