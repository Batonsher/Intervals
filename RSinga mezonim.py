from model_settings import tanlanma_nomi
import json
import functions

with open(f"out_data\\{tanlanma_nomi}\\guruhlangan_rslar.json") as jfile, \
     open(f"init_data\\{tanlanma_nomi}\\Target.csv") as tfile:
    # data = jfile.read()
    RSlar = json.load(jfile)
    target = [int(x) for x in tfile.read().split()]
    k1_quvvat, k2_quvvat = target.count(1), target.count(2)

# ustun => [[ID, RS-val, label], .... ]
for group_no in RSlar.keys():
    ustun = []
    for item in RSlar[group_no].items():
        ustun.append(
            (int(item[0]), item[1], target[int(item[0])])
        )
    # print(RSlar[group_no])
    a = functions.criteria1(ustun, k1_quvvat, k2_quvvat)

    # print(f"1-kriteriya qiymati: {a[0]:2.2f}; chegara:[0:{a[1]-1}]({a[1]-1}:{len(RS)})")  # BATON
    print(f"RS-{group_no}:: 1-kriteriya qiymati: {a[0]:2.2f}")  # _A_

    # break

# print(ustun)
