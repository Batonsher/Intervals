import pickle
from nominallashtiruvchi import tanlanma_nomi
import functions
import copy

with open(f"out_data\\{tanlanma_nomi}\\intervals.baton", 'rb') as baton_file:
    db = dict(pickle.load(baton_file))

DF2 = []
target = []
with open(f"out_data\\{tanlanma_nomi}\\Objects.csv") as in_file:
    for line in in_file:

        row = [int(x) for x in line.split()[:-1]]
        DF2.append(row)
        target.append(int(float(line.split()[-1])))

k1_quvvat = target.count(1)
k2_quvvat = target.count(2)

obyektlar_soni = len(target)
alomatlar_soni = len(DF2[0])

DF9 = copy.deepcopy(DF2)
# [print(el) for el in DF2]
# print(f"\n\n{1}-alomat: \nMezon 2, -dan (kiradi), -gacha (kirmaydi), intervaldagi elementlar soni, f1(i)")


for col in range(alomatlar_soni):
    for interval in db[col]:
        f = (interval[4] > 0.5) + 1
        # print(f)
        # print(interval[-1])
        for ind in interval[-1]:
            DF2[ind][col] = f
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

with open(f"out_data\\{tanlanma_nomi}\\binar_nominal_objects.csv", mode='w') as outfile:
    for row in DF2:
        s = [str(x) for x in row]
        s = ' '.join(s)
        print(s)
        outfile.write(s + '\n')
