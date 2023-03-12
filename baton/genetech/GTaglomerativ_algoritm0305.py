import pickle
# from model_settings import tanlanma_nomi
from baton import functions

tanlanma_nomi = 'genetech12'

with open(f"..\\..\\out_data\\{tanlanma_nomi}\\intervals.baton", 'rb') as baton_file:
    db = dict(pickle.load(baton_file))

DF = []

with open(f"..\\..\\init_data\\{tanlanma_nomi}\\Objects.csv") as in_file:
    for line in in_file:

        row = [int(x) for x in line.split(";")]
        DF.append(row)

with open(f"..\\..\\init_data\\{tanlanma_nomi}\\Target.csv") as in_file:
    target = [int(x) for x in in_file]


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

for x in range(alomatlar_soni):             # har bir Feature uchun
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
    #print(featurening_vazni[x])


# ####################################################
# #     OBYEKTNING UMUMLASHGAN BAHOSI    #############
# ####################################################
#
#
# obyektning_umulashgan_bahosi = dict()
# for obj_key in range(obyektlar_soni):     # HAR BIR OBJECT UCHUN
#     RS = 0
#     for feature_key in range(alomatlar_soni):
#         RS += featurening_vazni[feature_key] * \
#               (intervaldagi_vakillar[obj_key][feature_key][0] \
#                / k1_quvvat - intervaldagi_vakillar[obj_key][feature_key][1] / k2_quvvat)
#
#     obyektning_umulashgan_bahosi[obj_key] = RS
#
#
# # I-Kriteriyga tushuramiz, ya'ni RS'ni 2-ta intervalga bo'lamiz
# RS = [0]*len(obyektning_umulashgan_bahosi)
# for x, el in enumerate(obyektning_umulashgan_bahosi.items()):
#     RS[x] = (*el, target[x])
#     # print(el)
#
# a = functions.criteria1(RS, k1_quvvat, k2_quvvat)

# print(f"1-kriteriya qiymati: {a[0]:2.2f}; chegara:[0:{a[1]-1}]({a[1]-1}:{len(RS)})")  # BATON
# print(f"1-kriteriya qiymati: {a[0]:2.2f}; chegara:[0:{a[1]})[{a[1]}:{len(RS)})")        # _A_
# print("t/r: DF:t/r, RS-qiymat, sinf")
# for x, el in enumerate(a[2]):
#     print(f"{x+1}: {el}")

####################################################
#     АГЛОМЕРАТИВ АЛГОРИТМ  (Батон версия)  ########
####################################################
fv = featurening_vazni.copy()
fv2 = featurening_vazni.copy()

# Шаг 1. P={i | xi∈X(n)\Z }. mikdor=0.
# P      => kamayuvchi_alomatlar_tuplami.
# TYPLAM => kupayuvchi_alomatlar_tuplami
# mikdor => len(kupayuvchi_alomatlar_tuplami)
kamayuvchi_alomatlar_tuplami = set(range(alomatlar_soni))
RSLAR = dict()

for y in range(1000):
    # Шаг 2. Вычислить crit=10. u=arg max wj. TYPLAM={u}.   mikdor= mikdor+1.
    umumiy_mezon = float('inf')
    u = max(fv, key=fv.get)  # MANASHU JOY YEDIRYAPTI\
    # print("::", u)
    # print(fv,"\n\n", u)
    fv.pop(u)

    kupayuvchi_alomatlar_tuplami = {u}
    print("P, TYPLAM")
    print(kamayuvchi_alomatlar_tuplami, kupayuvchi_alomatlar_tuplami, fv2[u])


    # Цикл по t∊{1,…,h} R(St) = ηu(atu). Конец цикла; cr1=10. P=P\{u}.
    RS = functions.bittalik_rs_vaznli(
        obyektlar_soni, {u},
        intervaldagi_vakillar,
        k1_quvvat, k2_quvvat, fv2)
    tmp_mezon = float('inf')
    kamayuvchi_alomatlar_tuplami.discard(u)

    # print(kamayuvchi_alomatlar_tuplami, kupayuvchi_alomatlar_tuplami,
    #       u, umumiy_mezon, tmp_mezon, RS, sep='\n\n')

    # Шаг 3.
    for x in range(1000):
        # Цикл по u ∊P.
        # Цикл по t∊{1,…,h}  bt=  R(St) +  ηu(atu). Конец цикла;
        #  ;	 ;	θ=0;	γ=0
        # Цикл по t∊{1,…,h}
        # Если St ∊ K1, то θ= θ +|bt – M1|, γ= γ + |bt – M2|. Иначе θ= θ +|bt – M2|, γ= γ + |bt – M1|. Конец цикла;
        # Если θ/γ < cr1, то cr1= θ/ γ, q=u.
        # Конец цикла;
        for candidate_feature in kamayuvchi_alomatlar_tuplami:  # Цикл по u ∊P.
            # for obj_key in range(obyektlar_soni):       # Цикл по t∊{1,…,h}
            #     tmp_RS = functions.bittalik_rs_vaznli(         # bt=  R(St) +  ηu(atu).
            #         obyektlar_soni, {candidate_feature},
            #         intervaldagi_vakillar,
            #         k1_quvvat, k2_quvvat, fv2)

            tmp_RS = functions.bittalik_rs_vaznli(
                    obyektlar_soni, {candidate_feature},
                    intervaldagi_vakillar,
                    k1_quvvat, k2_quvvat, fv2)

            mat_kutilish1 = mat_kutilish2 = 0  # M1=...; M2=...	 ;	θ=0;	γ=0
            for obj_key in range(obyektlar_soni):
                if target[obj_key] == 1:
                    mat_kutilish1 += RS[obj_key] + tmp_RS[obj_key]
                else:
                    mat_kutilish2 += RS[obj_key] + tmp_RS[obj_key]
            mat_kutilish1 /= k1_quvvat
            mat_kutilish2 /= k2_quvvat
            tetta = gamma = 0
            for obj_key in range(obyektlar_soni): # Цикл по t∊{1,…,h}
                # Если St ∊ K1, то θ= θ +|bt – M1|, γ= γ + |bt – M2|.
                # Иначе θ= θ +|bt – M2|, γ= γ + |bt – M1|.
                if target[obj_key] == 1:
                    tetta += abs(RS[obj_key] + tmp_RS[obj_key] - mat_kutilish1)
                    gamma += abs(RS[obj_key] + tmp_RS[obj_key] - mat_kutilish2)
                else:
                    tetta += abs(RS[obj_key] + tmp_RS[obj_key] - mat_kutilish2)
                    gamma += abs(RS[obj_key] + tmp_RS[obj_key] - mat_kutilish1)

            # Если θ/γ < cr1, то cr1= θ/ γ, q=u.
            # print(f";{candidate_feature:2d},\t{tetta:2.4f}/{gamma:2.4f} =\t{tetta/gamma:2.4f}")
            if tetta / gamma < tmp_mezon:
                tmp_mezon = tetta / gamma
                found_candidate_feature = candidate_feature


        # Шаг 4.
        # Если cr1< crit,  то
        #  Идти 3;
        #  Иначе  вывод {R(St)}t ∊{1,…,h}, TYPLAM.
        if tmp_mezon < umumiy_mezon:
            # crit=cr1. P=P\{q}. TYPLAM=TYPLAM ∪{q}.  cr1=10.

            # print(f"^{tmp_mezon} < {umumiy_mezon}")
            # print("found_candidate_feature=", found_candidate_feature)

            umumiy_mezon = tmp_mezon
            tmp_mezon = float('inf')
            kamayuvchi_alomatlar_tuplami.discard(found_candidate_feature)
            kupayuvchi_alomatlar_tuplami.add(found_candidate_feature)
            ###
            fv.pop(found_candidate_feature)
            # Цикл по t ∊{1,…,h}  R(St)= R(St) + ηq(atq).   Конец цикла;
            tmp_RS = functions.bittalik_rs_vaznli(
                obyektlar_soni, {found_candidate_feature},
                intervaldagi_vakillar,
                k1_quvvat, k2_quvvat, fv2)
            for obj_key in range(obyektlar_soni):
                RS[obj_key] += tmp_RS[obj_key]

            # continue
        else:
            print(f'{y}-Guruh Shakillandi: {len(kupayuvchi_alomatlar_tuplami)}-ta element',
                  kupayuvchi_alomatlar_tuplami, "\n\n")  # , RS)
            RSLAR[y] = RS.copy()
            break
        # if not fv:
        #     print("FV tugadi1")
        #     print('BREAK#1:', kupayuvchi_alomatlar_tuplami, "\n\n")  # , RS)
        #     break
    else:
        print("XATOLIK Bo'lishi mumkin. tekshir")

    # Шаг 5. Если   |P|≥2, то идти 2; Иначе вывод  mikdor.
    if len(kamayuvchi_alomatlar_tuplami) >= 2:
        print("if len(kamayuvchi_alomatlar_tuplami) >= 2:", kamayuvchi_alomatlar_tuplami)

        continue
    else:
        print("BREAK#2: ", len(kupayuvchi_alomatlar_tuplami), kupayuvchi_alomatlar_tuplami)

    if not fv:
        print("FV tugadi2")
        break
else:
    print("XATOLIK2 Bo'lishi mumkin.")

# Шаг 6. Конец.
print("# Шаг 6. Конец.")


##  Topilgan RSlarni alohida faylga saqlab olish
import json
with open(f"..\\..\\out_data\\{tanlanma_nomi}\\guruhlangan_rslar.json", 'w') as json_file:
    json.dump(RSLAR, json_file)

print("\n\n:::\n")
# for item in RSLAR.items(): print(item)
# ID RS-val label
