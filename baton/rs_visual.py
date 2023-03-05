import matplotlib.pyplot as plt
from model_settings import tanlanma_nomi
import json
import numpy as np
import functions

with open(f"out_data\\{tanlanma_nomi}\\guruhlangan_rslar.json") as json_file, \
        open(f"init_data\\{tanlanma_nomi}\\Target.csv") as target_file:
    RSLAR = json.load(json_file)
    target = [int(x) for x in target_file.read().split()]
fig, ax = plt.subplots(figsize=(20, 10))
# plt.figure(figsize=(18, 6), dpi=300)
c = list(RSLAR['0'].values())
d = list(RSLAR['1'].values())
matrix = np.c_[c,d]
with open(f"out_data\\{tanlanma_nomi}\\RS_jadniy.csv", 'w') as wfile:
    for row in matrix:
        s = [str(x) for x in row]
        s = '; '.join(s)
        wfile.write(s + '\n')
marker = 'x^ov'
for class_label in set(target):
    # for group_key in RSLAR.keys():
    x_lar = []
    y_lar = []
    id_lar = []
    for object_id in RSLAR['0'].keys():
        if target[int(object_id)] == class_label:
            x_lar.append(RSLAR['0'][object_id])
            y_lar.append(RSLAR['1'][object_id])
            id_lar.append(object_id)
    ax.scatter(x_lar, y_lar, s=250, marker=marker[class_label], label=str(class_label))

    for n, txt in enumerate(id_lar):
        ax.annotate(txt, (x_lar[n], y_lar[n]))

ax.legend()

fig.savefig(f"out_data\\{tanlanma_nomi}\\fig1.pdf")
functions.start_file(f"out_data\\{tanlanma_nomi}\\fig1.pdf")
