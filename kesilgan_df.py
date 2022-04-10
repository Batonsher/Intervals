from model_settings import tanlanma_nomi


with open(f"out_data\\{tanlanma_nomi}\\binar_nominal_objects.csv") as bfile, \
     open(f"init_data\\{tanlanma_nomi}\\Target.csv") as tfile:
    DF2 = []
    lines = bfile.readlines()
    for line in lines:
        DF2.append(
            [int(x) for x in line.split()]
        )
        # print(DF2[-1])
    target = [int(x) for x in tfile.read().split()]
    k1_quvvat = target.count(1)
    k2_quvvat = target.count(2)

obyektlar_soni = len(target)
alomatlar_soni = len(DF2[0])

# Chizgandan keyin, yoqmaganini kesib tashlandi.
urtaga_tushgan_g = {86, 82, 99, 77, 89, 28, 87, 98, 83, 45, 12, 9, 73, 95, 48, 79,
                    42, 56, 52, 44, 64, 84, 57, 60, 74, 13, 96, 65, 47, 61, 36, 22}

DF3 = {'ids': set(range(obyektlar_soni)) - urtaga_tushgan_g}
for x, row in enumerate(DF2):
    if x in DF3['ids']:
        DF3[x] = row.copy()

for item in DF3.items():
    print(item)
print(len(DF3))
