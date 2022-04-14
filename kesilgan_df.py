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

with open(f"out_data\\{tanlanma_nomi}\\kesilgan_objects.csv", 'w') as outfile:
    for a in DF3['ids']:

        s = [str(x) for x in DF3[a]]
        s = ' '.join(s)
        # print(obj_no, s)
        outfile.write(str(a) + " " + s + '\n')

# Мера близости между парой номинальных признаков xi, xj на E0 вычисляется как
alomatlarning_yaqinlik_mezoni = []
for x in range(alomatlar_soni):
    alomatlarning_yaqinlik_mezoni.append([0]*alomatlar_soni)

for a in DF3['ids']:
    # obj_no = 62
    for b in DF3['ids']:
        obj1 = DF3[a]
        obj2 = DF3[b]

        # for Xai, Xbi in zip(obj1, obj2):
        #     print(f"Xai {Xai}, Xbi {Xbi}")
        # print(a, obj1)
        # print(b, obj2)

        if target[a] == target[b]:
            continue

        for i in range(len(obj1)):
            for j in range(len(obj1)):
                if obj1[i] != obj2[i] and obj1[j] != obj2[j]:
                    g = 2
                elif obj1[i] == obj2[i] or obj1[j] == obj2[j]:   # SO'RASH KERAK. MANTIQ QAYERDA???
                    g = 1
                elif obj1[i] == obj2[i] and obj1[j] == obj2[j]:
                    print('ishladi')
                    g = 0
                else:
                    # print(obj1[i] == obj2[i], obj1[j] == obj2[j])
                    # print("XATOLIK OOV")
                    g = 1

                if i != j:
                    alomatlarning_yaqinlik_mezoni[i][j] += g
                else:
                    alomatlarning_yaqinlik_mezoni[i][j] += 0

        # for x in range(len(obj1)):
        #     print(f"Xai {obj1[x]}, Xbi {obj2[x]}")

    break

kesilgan_k1_quvvat = kesilgan_k2_quvvat = 0
for obj_no in DF3['ids']:
    if target[obj_no] == 1:
        kesilgan_k1_quvvat += 1
    else:
        kesilgan_k2_quvvat += 1

kesilgan_mahraj = kesilgan_k1_quvvat * (len(DF3['ids']) - kesilgan_k1_quvvat) + \
                  kesilgan_k2_quvvat * (len(DF3['ids']) - kesilgan_k2_quvvat)
kesilgan_mahraj *= 2

for x in range(alomatlar_soni):
    for y in range(alomatlar_soni):
        alomatlarning_yaqinlik_mezoni[x][y] /= kesilgan_mahraj

for row in alomatlarning_yaqinlik_mezoni:
    print(row)

def logger(matrix, logfile):
    for row in matrix:
        s = [str(x) for x in row]
        s = ' '.join(s)
        logfile.write(s + '\n')
    logfile.write("#"*30 + '\n')


with open(f"out_data\\{tanlanma_nomi}\\log.txt", 'w') as log:


    # max qaydasan
    ignorelist = set()
    tartiblangan_juftalomatlar = []
    while len(ignorelist) < len(alomatlarning_yaqinlik_mezoni):
        maxq = float('-inf')
        maxi = (-1, -1)
        for x, row in enumerate(alomatlarning_yaqinlik_mezoni):
            for y, el in enumerate(row):
                if el > maxq and x not in ignorelist and y not in ignorelist:
                    maxq = el
                    maxi = (x, y)

        tartiblangan_juftalomatlar.append(maxi)
        ignorelist.add(maxi[0])
        ignorelist.add(maxi[1])
        log.write(f"ignorelist: {ignorelist}\n")
        log.write(f"maxq: {maxq}\tmax: {maxi}\n")
        alomatlarning_yaqinlik_mezoni[maxi[0]] = [0] * len(alomatlarning_yaqinlik_mezoni)
        alomatlarning_yaqinlik_mezoni[maxi[1]] = [0] * len(alomatlarning_yaqinlik_mezoni)
        logger(alomatlarning_yaqinlik_mezoni, log)

        s = [str(x) for x in tartiblangan_juftalomatlar]
        s = ' '.join(s)
        log.write("Juftliklar" + s + '\n')

    print("Juft:", tartiblangan_juftalomatlar)
