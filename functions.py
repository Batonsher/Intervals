def criteria1(ustun, k1_quvvat, k2_quvvat):
    ustun = sorted(ustun, key=lambda x: x[1])
    # ustun = [ (DF t/r, RS qiymati, sinf), ... ]

    # print(ustun)
    maxi = float('-inf'); qaytadigan_chegara = 0
    for chegara in range(1, len(ustun)+1):
        # uid hisobla
        # chegarani chap qismi
        chap_k1_vakillar = chap_k2_vakillar = 0
        for el in ustun[:chegara]:
            if el[2] == 1:
                chap_k1_vakillar += 1
            else:
                chap_k2_vakillar += 1

        # chegarani o'ng qismi
        ung_k1_vakillar = ung_k2_vakillar = 0
        for el in ustun[chegara:]:
            if el[2] == 1:
                ung_k1_vakillar += 1
            else:
                ung_k2_vakillar += 1
        chap_surat = chap_k1_vakillar**2 - chap_k1_vakillar + ung_k1_vakillar**2 - ung_k1_vakillar
        chap_surat += chap_k2_vakillar**2 - chap_k2_vakillar + ung_k2_vakillar**2 - ung_k2_vakillar

        chap_mahraj = k1_quvvat ** 2 - k1_quvvat + k2_quvvat ** 2 - k2_quvvat

        ung_surat  = chap_k1_vakillar * (k2_quvvat - chap_k2_vakillar)
        ung_surat += chap_k2_vakillar * (k1_quvvat - chap_k1_vakillar)
        ung_surat += ung_k1_vakillar * (k2_quvvat - ung_k2_vakillar)
        ung_surat += ung_k2_vakillar * (k1_quvvat - ung_k1_vakillar)

        ung_mahraj = 2 * k1_quvvat * k2_quvvat

        summa = chap_surat / chap_mahraj * ung_surat / ung_mahraj

        if summa > maxi:
            qaytadigan_chegara = chegara
            maxi = summa

    return maxi, qaytadigan_chegara, ustun


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


def intervalga_ajratish(ustun, target, K1, K2, result=None, indexlar=None, unsorted_indexlar=None):
    if not result:
        result = []
        indexlar = list(range(len(target)))
        unsorted_indexlar = indexlar[:]

    if not target: return result
    # sorting
    zipped_lists = zip(ustun, target, unsorted_indexlar)
    sorted_pairs = sorted(zipped_lists)
    ustun, target, unsorted_indexlar = [list(tuple) for tuple in zip(*sorted_pairs)]
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

    javob = (maksi, u2, v2, interval_uzunligi, tegishlilik_func(target[u:v], K1, K2), unsorted_indexlar[u:v])
    # print(maksi, u2, v2, interval_uzunligi, tegishlilik_func(target[u:v], K1, K2), indexlar)

    result.append(javob)

    # qolgan intervallar uchun
    if target[:u]:
        result = intervalga_ajratish(ustun[:u], target[:u], K1, K2, result, indexlar[:u], unsorted_indexlar[:u])
    if target[v:]:
        result = intervalga_ajratish(ustun[v:], target[v:], K1, K2, result, indexlar[v:], unsorted_indexlar[v:])

    return result


def yangi_df(fullpath):
    with open(fullpath) as infile:
        pass


def bittalik_rs(obyektlar_soni, featuralar_soni, intervaldagi_vakillar, K1, K2):
    """
    umumlashgan baxo
    :return:
    """
    if type(featuralar_soni) == type(1): featuralar_soni = range(featuralar_soni)

    obyektning_umulashgan_bahosi = dict()
    for obj_key in range(obyektlar_soni):
        RS = 0
        for feature_key in featuralar_soni:
            RS += (intervaldagi_vakillar[obj_key][feature_key][0] / K1 -
                   intervaldagi_vakillar[obj_key][feature_key][1] / K2)

        obyektning_umulashgan_bahosi[obj_key] = RS
    return obyektning_umulashgan_bahosi


