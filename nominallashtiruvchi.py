import functions
DF = []
tanlanma_nomi = "giper2"
# tanlanma_nomi = "itburi"
# tanlanma_nomi = "giper"


with open(f"init_data\\{tanlanma_nomi}\\Objects.csv") as objfile:
    for row in objfile:
        DF.append([float(x) for x in row.split()])

target = []

with open(f"init_data\\{tanlanma_nomi}\\Target.csv") as targetfile:
    for row in targetfile:
        target.append(int(row))

K1, K2 = target.count(1), target.count(2)

DF2 = DF.copy()

for c in range(len(DF[0])-1):
    print(f"\n\n{c+1}-alomat: \nMezon 2, -dan (kiradi), -gacha (kirmaydi), intervaldagi elementlar soni, f1(i)")
    ustun = [x[c] for x in DF]
    intervals = functions.intervalga_ajratish(ustun, target, K1, K2)

    intervals = sorted(intervals, key=lambda x: x[0])
    for x, interval in enumerate(intervals):
        for ind in interval[5]:
            DF2[ind][c] = x + 1
        print(interval)
    # [print(interval) for interval in intervals]
    G = functions.gini_function(intervals, len(target))
    print("Alomat turg'unligi:", G)

# for x in range(len(DF)):
#     print("-", DF[x])
#     print("+", DF2[x])

with open(f"out_data\\{tanlanma_nomi}\\Objects.csv", 'w') as outfile:
    for row in DF:
        a = ' '.join(map(str, row))
        outfile.write(a + '\n')

