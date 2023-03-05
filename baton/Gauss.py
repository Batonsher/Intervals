from model_settings import tanlanma_nomi, tanlanma_nomi2
from math import exp


def kvadrat_masofa(obj1, obj2):
    rho = 0
    for features in zip(obj1, obj2):
        rho += (features[0] - features[1]) ** 2
    return rho


def dispersion(dataframe, seeking_obj, obj_count=0):

    summa = 0
    if not obj_count: obj_count = len(dataframe)
    if type(seeking_obj) == float or type(seeking_obj) == int:
        seeking_obj = dataframe[seeking_obj]

    for obj in dataframe:
        summa += kvadrat_masofa(seeking_obj, obj)
    return summa / (obj_count - 1)


def gaussian_density(dataframe, obj_no1, obj_no2):

    surat = exp(-kvadrat_masofa(dataframe[obj_no1], dataframe[obj_no2]) / dispersion_table[obj_no1])

    mahraj = 0
    for obj in dataframe:
        mahraj += exp(-kvadrat_masofa(dataframe[obj_no1], obj) / dispersion_table[obj_no1])

    return surat / mahraj


def gaussian_density_old(dataframe, obj_no1, obj_no2):

    surat = exp(-kvadrat_masofa(dataframe[obj_no1], dataframe[obj_no2]) / dispersion(dataframe, obj_no1))

    mahraj = 0
    for obj in dataframe:
        mahraj += exp(-kvadrat_masofa(dataframe[obj_no1], obj) / dispersion(dataframe, obj_no1))

    return surat / mahraj


with open(f"init_data\\{tanlanma_nomi}\\Objects.csv") as bfile, \
     open(f"init_data\\{tanlanma_nomi}\\Target.csv") as tfile:
    DF = []
    lines = bfile.readlines()
    for line in lines:
        DF.append(
            [int(x) for x in line.split()]
        )
        # print(DF2[-1])
    target = [int(x) for x in tfile.read().split()]
    k1_quvvat = target.count(1)
    k2_quvvat = target.count(2)

obyektlar_soni = len(target)
alomatlar_soni = len(DF[0])

# [print(x) for x in DF]
# print("\n\n\n\n", target)

guruh0 = {0, 1, 2, 3, 8, 9, 11, 12, 13, 14, 16, 17, 18, 20, 21, 22}
guruh1 = {4, 5, 6, 7, 10, 15, 19, 23}


dispersion_table = [0]*obyektlar_soni

c = 0
for guruh in (guruh0, guruh1):
    guruh = list(guruh)

    gaussosovskithuy = [[0]*obyektlar_soni for x in range(obyektlar_soni)]
    DF2 = [[] for x in range(obyektlar_soni)]
    for obj_no in range(obyektlar_soni):
        for feature in guruh:
            DF2[obj_no].append(
                DF[obj_no][feature]
            )

    # [print(len(x)) for x in DF2]
    for obj_no in range(obyektlar_soni):
        dispersion_table[obj_no] = dispersion(DF2, obj_no)
    print(f"{guruh} guruh uchun:\n")
    for obj_no1 in range(obyektlar_soni):
        for obj_no2 in range(obj_no1+1, obyektlar_soni):
            gaussosovskithuyok = gaussian_density(DF2, obj_no1, obj_no2) + gaussian_density(DF2, obj_no2, obj_no1)
            gaussosovskithuyok /= 2
            gaussosovskithuy[obj_no1][obj_no2] = gaussosovskithuyok

    [print(F"{len(row)}") for row in gaussosovskithuy]
    print(f"asd {len(gaussosovskithuy)}")
    with open(f"init_data\\{tanlanma_nomi2}\\guruh{c}.csv", 'w') as ofile:
        for row in gaussosovskithuy:
            s = [str(x) for x in row]
            s = '; '.join(s)
            ofile.write(s + '\n')
        c += 1



