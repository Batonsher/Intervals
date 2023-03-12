from baton import functions
import os
import pickle
# from model_settings import tanlanma_nomi  # pastda yozildi


if __name__ == '__main__':
    tanlanma_nomi = "genetech12"
    DF = []
    if not os.path.exists(f"..\\..\\out_data\\{tanlanma_nomi}"):
        os.mkdir(f"..\\..\\out_data\\{tanlanma_nomi}")

    with open(f"..\\..\\init_data\\{tanlanma_nomi}\\ObjectsNominalBinar.csv") as objfile:
        for row in objfile:
            DF.append([float(x) for x in row.split()])

    target = []

    with open(f"..\\..\\init_data\\{tanlanma_nomi}\\Target.csv") as targetfile:
        for row in targetfile:
            target.append(int(row))

    K1, K2 = target.count(1), target.count(2)

    DF2 = DF.copy()

    # with open(f"out_data\\{tanlanma_nomi}\\intervals.txt", 'w'):
    #     pass

    pickle_dict = dict()
    turgun = []
    for c in range(len(DF[0])):
        print(f"\n\n{c+1}-alomat: \nMezon 2, -dan (kiradi), -gacha (kirmaydi), intervaldagi elementlar soni, f1(i)")
        ustun = [x[c] for x in DF]
        intervals = functions.intervalga_ajratish_nominal(ustun, target, K1, K2)

        intervals = sorted(intervals, key=lambda x: x[0])

        pickle_dict[c] = intervals

        for x, interval in enumerate(intervals):
            # for ind in interval[5]:
            #     DF2[ind][c] = x + 1
            print(interval)
        # [print(interval) for interval in intervals]
        G = functions.gini_function(intervals, len(target))
        turgun.append(G)
    print("Alomat turg'unligi:", sorted(turgun, reverse=True))
    print(len(turgun))

    # for x in range(len(DF)):
    #     print("-", DF[x])
    #     print("+", DF2[x])

    # with open(f"..\\..\\init_data\\{tanlanma_nomi}\\ObjectsNominal.csv", 'w') as outfile:
    #     for row in DF:
    #         a = ' '.join(map(str, row))
    #         outfile.write(a + '\n')

    with open(f"..\\..\\out_data\\{tanlanma_nomi}\\intervals.baton", 'wb') as outfile:
        pickle.dump(pickle_dict, outfile)
