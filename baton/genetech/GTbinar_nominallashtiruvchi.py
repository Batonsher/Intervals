import pickle
# from model_settings import tanlanma_nomi
from baton import functions
import copy

tanlanma_nomi = 'genetech12'

with open(f"..\\..\\out_data\\{tanlanma_nomi}\\intervals.baton", 'rb') as baton_file:
    db = dict(pickle.load(baton_file))
    # print(db.keys())

DF2 = []
with open(f"..\\..\\init_data\\{tanlanma_nomi}\\Objects.csv") as in_file:
    for line in in_file:

        row = [int(x) for x in line.split(";")]
        DF2.append(row)
with open(f"..\\..\\init_data\\{tanlanma_nomi}\\Target.csv") as in_file:
    target = [int(x) for x in in_file]


k1_quvvat = target.count(1)
k2_quvvat = target.count(2)

obyektlar_soni = len(target)
alomatlar_soni = len(DF2[0])

DF9 = copy.deepcopy(DF2)
# [print(el) for el in DF2]
# print(f"\n\n{1}-alomat: \nMezon 2, -dan (kiradi), -gacha (kirmaydi), intervaldagi elementlar soni, f1(i)")

tochnost = dict()

for col in range(alomatlar_soni):
    tochnost1 = tochnost2 = 0
    for interval in db[col]:
        f = (interval[4] > 0.5) + 1
        # print(f)
        # print(interval[-1])

        # print("::", interval)

        for ind in interval[-1]:
            DF2[ind][col] = f

            if interval[4] > 0.5 and target[ind] == 1:
                tochnost1 += 1
            elif interval[4] < 0.5 and target[ind] == 2:
                tochnost2 += 1
        tochnost[col] = tochnost1, tochnost2, (tochnost1 + tochnost2) / (k1_quvvat + k2_quvvat)
        ...
    # print("\n")
    # break
col = 0
# for row in range(len(DF2)):
    # print(f"{row}:\t {DF2[row][col]} {DF9[row][col]}")
# for el in DF2:
#     print(el)

# for el in zip(DF2, DF9):
#     print(el[0][:10], el[1][:10])
for item in tochnost.items():
    print(item)

with open(f"..\\..\\init_data\\{tanlanma_nomi}\\ObjectsNominalBinar.csv", mode='w') as outfile:
    for row in DF2:
        s = [str(x) for x in row]
        s = ' '.join(s)
        print(s)
        outfile.write(s + '\n')

