import functions
DF = []
#with open("init_data\\itburi\\Volki_Sobaki.csv") as objfile:
with open("init_data\\giper2\\Objects.csv") as objfile:
#with open("init_data\\giper\\Objects2.csv") as objfile:
    for row in objfile:
        DF.append([float(x) for x in row.split()])

target = []
#with open("init_data\\itburi\\Target.csv") as targetfile:
with open("init_data\\giper2\\Target.csv") as targetfile:
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

with open("out_data/outdata.csv", 'w') as outfile:
    for row in DF:
        a = ' '.join(map(str, row))
        outfile.write(a + '\n')

