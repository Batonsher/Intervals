def eta_finder(target, K1, K2):

    d1 = target.count(1)
    d2 = target.count(2)

    return d1 / K1, d2 / K2

def tegishlilik_func(target, K1, K2):
    a = eta_finder(target, K1, K2)
    return a[0] / (a[0] + a[1])


def gini_function(intervals, m):
    G = 0
    for interval in intervals:
        if interval[4] > 0.5:
            G += interval[4] * interval[3]
        else:
            G += (1 - interval[4]) * interval[3]
    G /= m
    return G


def intervalga_ajratish(ustun, target, K1, K2, result=None, indexlar=None):
    if not result:
        result = []
        indexlar = list(range(len(target)))

    if not target: return result
    # sorting
    zipped_lists = zip(ustun, target)
    sorted_pairs = sorted(zipped_lists)
    ustun, target = [list(tuple) for tuple in zip(*sorted_pairs)]
    #print(ustun)


    interval_uzunligi = maksi = float("-inf")

    #print(target)
    for chap_chegara in range(len(ustun)):
        for ung_chegara in range(chap_chegara+1, len(ustun)+1):
            eta = eta_finder(target[chap_chegara:ung_chegara], K1, K2)

            #print("ustun:", len(ustun), ung_chegara, ustun)
            if ung_chegara != len(ustun) \
                and ustun[ung_chegara] == ustun[ung_chegara-1]:
                continue
            if chap_chegara != 0 and ustun[chap_chegara] == ustun[chap_chegara-1]:
                continue

            mezon1 = abs(eta[0]-eta[1])
            if mezon1 > maksi:
                maksi = mezon1
                interval_uzunligi = ung_chegara - chap_chegara
                u = chap_chegara
                v = ung_chegara

    u2, v2 = indexlar[u], indexlar[v] if v < len(target) else indexlar[v-1]+1

    javob = (maksi, u2, v2, interval_uzunligi, tegishlilik_func(target[u:v], K1, K2))
    # print(maksi, u2, v2, interval_uzunligi, tegishlilik_func(target[u:v], K1, K2))

    result.append(javob)

    # qolgan intervallar uchun
    if target[:u]:
        result = intervalga_ajratish(ustun[:u], target[:u], K1, K2, result, indexlar[:u])
    if target[v:]:
        result = intervalga_ajratish(ustun[v:], target[v:], K1, K2, result, indexlar[v:])

    return result



