""" :: Asosiy class :: """
import re, copy, pickle
import metric
import os, datetime
import matplotlib.pyplot as plt


def start_file(path):
    import os
    cmd = f"start {path}"
    os.system(cmd)


class Bahriddin:
    """
    df                  list m*n:   o'rgatuvchi tanlanma. m*n list
    df_nominal          list m*n:   Nominallashgan tanlanma
    df_binar            list m*n:   Binarlashgan tanlanma. f1(c)>0.5=1, else 0
    df_name             str:        tanlanma nomi
    intervals           dict:       keys->feature ids. values-> <interval>
        dict_value      tuple:      alomat intervallaridan tashkil topgan tuple
            interval    tiple:      Mezon2,-dan (kiradi), -gacha (kirmaydi),
                                    "intervaldagi elementlar soni, f1(i)\n"
    feature_weight      dict:       featurening_vazni
    generalized_estimate dict:      har bir obyektning umulashgan baholari. RS
    nominal_features_set set:       nominal ustunlarning to'plami.
                                    (#) {0,5,9}-aynan shu alomatlar. None->Hammasi miqdoriy
    """

    ################################################################################
    def __init__(self, df_name="Tanlanma nomi",
                 path2df="Path to Objects.csv and Target.csv folder",
                 *, path2out="", metric=(1, 2, None),
                 nominal_features_set=False, binar=False):
        # region SETTINGS
        self.epsilon = 10**-9
        # endregion

        # region DF location
        if df_name == "Tanlanma nomi":
            if path2df == "Path to Objects.csv and Target.csv folder":
                raise Exception("Error:: Need DataFrame name or path")
            else:
                path2df = path2df.strip("\\")
                self.df_name = path2df.split("\\")[-1]
                self.path2df = path2df + "\\"
        else:
            self.df_name = df_name
            self.path2df = f"init_data\\{df_name}\\"

        self.create_folders()
        self.path2out = path2out if path2out else "out_data\\"

        self.nominal_features_set = nominal_features_set if nominal_features_set else {}
        # if not nominal_features_set:
        #     self.nominal_features_set = {}
        # elif nominal_features_set is True:
        #     self.nominal_features_set = set(range(self.n))
        # else:
        #     self.nominal_features_set
        # endregion

        # region Load DATA
        self.current_df = []        # E0`ni hozir ishlatilayotgani
        self.original_df = []           # O'rgatucvhi tanlanma. m*n tartibli list()
        self.df_nominal = []    # E0`ni nominallashgani
        self.df_binar = []      # E0`ni nominallashgandan so'ng, binarlashgani
        self.m = 0          # Obyektlar soni
        self.n = 0          # alomatlar soni
        self.class_names = []    # sinf nomlari
        self.class_power = dict()# sinf quvvatlari

        self.load_data()
        self.current_df = self.original_df[:]
        self.binar = binar
        # endregion

        # region Metric settings
        self.metric, self.p, self.w = metric  # self.metric haqida metric.py da o'qing
        # m*m  matritsa. barcha obyektlar munosabatlari jadvali
        self.distance_table = None
        self.nearest_enemy_dist = dict()
        self.calc_metric_table()
        # endregion

        self.run()

    ################################################################################
    def load_data(self):
        #region E0 ni o'qib olish
        DF = []
        with open(self.path2df + "Objects.csv") as objfile:
            for row in objfile:
                row = row.strip()
                DF.append([float(x) for x in re.split(",| |;|\t", row)])
        self.original_df = DF
        self.m = len(DF)
        self.n = len(DF[0])
        #endregion

        #region sinf haqida o'qib olish
        target = []
        with open(self.path2df + "Target.csv") as targetfile:
            for row in targetfile:
                target.append(row.strip())
        self.target = target

        self.class_names = list(set(target))
        for class_name in self.class_names:
            self.class_power[class_name] = target.count(class_name)

        if self.nominal_features_set == True:
            self.nominal_features_set = list(range(self.m))
        elif self.nominal_features_set == False:
            self.nominal_features_set = {}
        # endregion

    ################################################################################
    def distance(self, object1_id, object2_id):
        return metric.distance(self.original_df[object1_id], self.original_df[object2_id],
                               metric=self.metric, p=self.p, w=self.w)

    ################################################################################
    def calc_metric_table(self):
        self.distance_table = []
        self.nearest_enemy_dist = [float('inf') for x in range(self.m)]
        for x in range(self.m):
            row = []
            distance2enemy = float("inf")
            x_class = self.target[x]
            for y in range(self.m):
                d = self.distance(x, y)
                row.append(d)
                if x_class != self.target[y] and d < distance2enemy:
                    self.nearest_enemy_dist[x] = d
                    distance2enemy = d

            self.distance_table.append(row)

    ################################################################################
    def eta_finder(self, target):
        """Eta larni topuvchi funksiya"""
        result = []
        for class_name in self.class_names:
            result.append(target.count(class_name) / self.class_power[class_name])

        return result

    ################################################################################
    def membership_func(self, target):
        """Tegishlilik funk"""
        a = self.eta_finder(target)

        # TODO: for more classes
        return a[0] / (a[0] + a[1])

    ################################################################################
    def criteria1(self, ustun):
        """
        ustun: => [(ID, RS-val, label), .... ]
        """
        ustun = sorted(ustun, key=lambda x: x[1])
        # ustun = [ (DF t/r, RS qiymati, sinf), ... ]

        # print(ustun)
        maxv = float('-inf')
        qaytadigan_chegara = -1
        for chegara in range(1, len(ustun) + 1):
            # uid hisobla
            # chegarani chap qismi
            chap_k1_vakillar = chap_k2_vakillar = 0  # K1->self.class_names[0], K2->Qolgan silflar
            for el in ustun[:chegara]:
                if el[2] == self.class_names[0]:
                    chap_k1_vakillar += 1
                else:
                    chap_k2_vakillar += 1

            # chegarani o'ng qismi
            ung_k1_vakillar = ung_k2_vakillar = 0
            for el in ustun[chegara:]:
                if el[2] == self.class_names[0]:
                    ung_k1_vakillar += 1
                else:
                    ung_k2_vakillar += 1
            chap_surat =  chap_k1_vakillar ** 2 - chap_k1_vakillar + ung_k1_vakillar ** 2 - ung_k1_vakillar
            chap_surat += chap_k2_vakillar ** 2 - chap_k2_vakillar + ung_k2_vakillar ** 2 - ung_k2_vakillar

            k1_quvvat = self.class_power[self.class_names[0]]
            k2_quvvat = sum(self.class_power.values()) - k1_quvvat
            chap_mahraj = k1_quvvat ** 2 - k1_quvvat + k2_quvvat ** 2 - k2_quvvat

            ung_surat = chap_k1_vakillar * (k2_quvvat - chap_k2_vakillar)
            ung_surat += chap_k2_vakillar * (k1_quvvat - chap_k1_vakillar)
            ung_surat += ung_k1_vakillar * (k2_quvvat - ung_k2_vakillar)
            ung_surat += ung_k2_vakillar * (k1_quvvat - ung_k1_vakillar)

            ung_mahraj = 2 * k1_quvvat * k2_quvvat

            summa = chap_surat / chap_mahraj * ung_surat / ung_mahraj

            if summa > maxv:
                qaytadigan_chegara = chegara
                maxv = summa

        return maxv, qaytadigan_chegara, ustun

    ################################################################################
    def gini_function(self, intervals):
        G = 0
        for interval in intervals:
            if interval[4] > 0.5:
                G += interval[4] * interval[3]
            else:
                G += (1 - interval[4]) * interval[3]
        G /= self.m
        return G

    ################################################################################
    def create_intervals(self, df):
        """ DF`ni nominallashtiradi.
                agar nominal_features_set berilgan bolsa,
                    ko'rsatilgan alomatlar uchun nominal qoidalar bajariladi
        """
        # import pickle

        if not df: df = copy.deepcopy(self.original_df)

        time = str(datetime.datetime.now())[:10]
        with open(f"out_data\\{self.df_name}\\{time}LOG.nominalizer.txt", 'w') as logfile:
            pickle_dict = dict()
            turgun = []
            for c in range(self.n):
                logfile.write(
                    f"\n\n{c}-alomat {'nominal' if c in self.nominal_features_set else 'miqdoriy'}: "
                    f"\nMezon 2, -dan (kiradi), -gacha (kirmaydi), "
                    f"intervaldagi elementlar soni, f1(i), ["
                    f"ids]\n")
                ustun = [x[c] for x in df]

                if c in self.nominal_features_set:
                    intervals = self.nominal_interval_maker(ustun, self.target)
                else:
                    intervals = self.interval_maker(ustun, self.target)

                intervals = sorted(intervals, key=lambda x: x[0])
                [logfile.write(str(interval)) for interval in intervals]

                pickle_dict[c] = intervals

            logfile.write(f"\n\n{'#' * 20}\nAlomat turg'unligi:{sorted(turgun, reverse=True)}")

        with open(f"out_data\\{self.df_name}\\intervals.baton", 'wb') as outfile:
            pickle.dump(pickle_dict, outfile)

        self.intervals = pickle_dict
        pass

    ################################################################################
    def interval_maker(self, feature_col, target, result=None, indexlar=None, unsorted_indexlar=None):
        # target = self.target
        if not result:
            result = []
            indexlar = list(range(len(target)))
            unsorted_indexlar = indexlar[:]

        if not target: return result
        # sorting
        zipped_lists = zip(feature_col, target, unsorted_indexlar)
        sorted_pairs = sorted(zipped_lists)
        feature_col, target, unsorted_indexlar = [list(tuple) for tuple in zip(*sorted_pairs)]
        # print(ustun)

        interval_uzunligi = maxv = float("-inf")

        # print(target)
        for chap_chegara in range(len(feature_col)):
            for ung_chegara in range(chap_chegara + 1, len(feature_col) + 1):
                eta = self.eta_finder(target[chap_chegara:ung_chegara])

                # print("ustun:", len(ustun), ung_chegara, ustun)
                if ung_chegara != len(feature_col) \
                        and feature_col[ung_chegara] == feature_col[ung_chegara - 1]:
                    continue
                if chap_chegara != 0 and feature_col[chap_chegara] == feature_col[chap_chegara - 1]:
                    continue

                mezon2 = abs(eta[0] - eta[1])
                if mezon2 > maxv:
                    maxv = mezon2
                    interval_uzunligi = ung_chegara - chap_chegara
                    u = chap_chegara
                    v = ung_chegara

        u2, v2 = indexlar[u], indexlar[v] if v < len(target) else indexlar[v - 1] + 1

        javob = (maxv, u2, v2, interval_uzunligi, self.membership_func(target[u:v]), unsorted_indexlar[u:v])
        # print(maksi, u2, v2, interval_uzunligi, tegishlilik_func(target[u:v], K1, K2), indexlar)

        result.append(javob)

        # qolgan intervallar uchun
        if target[:u]:
            result = self.interval_maker(feature_col[:u], target[:u], result, indexlar[:u], unsorted_indexlar[:u])
            #def criteria2(self, feature_col, result=None, indexlar=None, unsorted_indexlar=None):
        if target[v:]:
            result = self.interval_maker(feature_col[v:], target[v:], result, indexlar[v:], unsorted_indexlar[v:])

        return result

     ################################################################################
    def nominal_interval_maker(self, feature_col, target, result=None,
                               indexlar=None, unsorted_indexlar=None):

        if not result:
            result = []
            indexlar = list(range(len(target)))
            unsorted_indexlar = indexlar[:]
        if not target: return result

        # sorting
        zipped_lists = zip(feature_col, target, unsorted_indexlar)
        sorted_pairs = sorted(zipped_lists)
        feature_col, target, unsorted_indexlar = [list(tuple) for tuple in zip(*sorted_pairs)]

        cur_val = feature_col[0]
        c = float('inf')
        for chegara in range(1, len(target)+1):
            # print('$$', chegara, feature_col, target)
            if chegara == len(feature_col) or feature_col[chegara] != cur_val:

                u = indexlar[0]
                v = indexlar[chegara] if chegara < len(target) else indexlar[chegara - 1] + 1

                eta = self.eta_finder(target[:chegara])
                # print(f"#{target}\t{target[:chegara]}")
                javob = (abs(eta[0] - eta[1]), u, v, v-u,
                         self.membership_func(target[:chegara]), unsorted_indexlar[:chegara])
                result.append(javob)

                # print("$$$$\t ", javob, target[chegara:])
                c = chegara
                break
        if target[c:]:
            result = self.nominal_interval_maker(feature_col[c:],
                     target[c:], result,
                     indexlar[c:], unsorted_indexlar[c:])

        return result

    ################################################################################
    def nominalizer(self):
        """ DF`ni nominallashtiradi.
        agar nominal_features_set berilgan bolsa,
            ko'rsatilgan alomatlar uchun nominal qoidalar bajariladi
        """

        DF2 = copy.deepcopy(self.original_df)
        self.create_intervals(DF2)
        intervals = copy.deepcopy(self.intervals)

        for c in range(self.n):
            for x, interval in enumerate(intervals[c]):
                for ind in interval[5]:
                    DF2[ind][c] = x

        with open(f"init_data\\{self.df_name}\\ObjectsNominal.csv", 'w') as outfile:
            for row in DF2:
                a = ' '.join(map(str, row))
                outfile.write(a + '\n')

        self.df_nominal = DF2

    ################################################################################
    def binanizer(self):
        import copy

        new_df = copy.deepcopy(self.df_nominal)
        self.create_intervals(new_df)
        db = copy.deepcopy(self.intervals)
        # db = self.intervals
        # target = self.target

        for feature_no in range(self.n):
            # print(f"\n\n{1}-alomat: \nMezon 2, -dan (kiradi), -gacha (kirmaydi), intervaldagi elementlar soni, f1(i)")
            for interval in db[feature_no]:
                f = int(interval[4] > 0.5)

                for ind in interval[-1]:
                    new_df[ind][feature_no] = f

        with open(f"init_data\\{self.df_name}\\ObjectsNominalBinar.csv", mode='w') as outfile:
            for row in new_df:
                s = [str(x) for x in row]
                s = ' '.join(s)
                outfile.write(s + '\n')

        self.df_binar = new_df

    ################################################################################
    def generalized_estimate_func(self):

        db = self.intervals
        DF = self.df_binar
        target = self.target

        k1_quvvat = target.count(self.class_names[0])
        k2_quvvat = sum(self.class_power.values()) - k1_quvvat

        obyektlar_soni = self.m
        alomatlar_soni = self.n

        #########################################################
        #    UXSHASHLIK va FARQ                                ##
        #########################################################

        sinflararo_farq = dict()
        sinflararo_uxshashlik = dict()

        # intervaldagi_vakillar = {x: {} for x in range(obyektlar_soni)}
        intervaldagi_vakillar = dict()
        for obj_key in range(obyektlar_soni):
            for feature_key in range(alomatlar_soni):
                intervaldagi_vakillar[obj_key] = {feature_key: 0}

        for x in range(alomatlar_soni):  # har bir Feature uchun
            featurening_sinflararo_farqi = 1
            featurening_sinflararo_uxshashligi = 0
            farq_summa = 0
            uxshash_summa = 0
            #
            # print('#################')
            # for item in db.items():
            #     print(item)

            for interval in db[x]:  # har bir interval uchun
                k1_vakillari = k2_vakillari = 0
                # print(interval)
                for ind in interval[5]:  # feature'ning intervalidagi  har bir index uchun
                    if target[ind] == self.class_names[0]:
                        k1_vakillari += 1
                    else:
                        k2_vakillari += 1

                # print(k1_vakillari, k2_vakillari)
                farq_summa += k1_vakillari * k2_vakillari
                uxshash_summa += k1_vakillari * (k1_vakillari - 1) + k2_vakillari * (k2_vakillari - 1)

                # print(x, interval)#, intervaldagi_vakillar[x])
                for ind in interval[5]:
                    intervaldagi_vakillar[ind][x] = (k1_vakillari, k2_vakillari)
                    # print(ind, intervaldagi_vakillar[ind])
                # print(interval[], intervaldagi_vakillar[x])

            featurening_sinflararo_farqi -= farq_summa / (k1_quvvat * k2_quvvat)
            featurening_sinflararo_uxshashligi = uxshash_summa / (
                        k1_quvvat ** 2 - k1_quvvat + k2_quvvat ** 2 - k2_quvvat)

            sinflararo_farq[x] = featurening_sinflararo_farqi
            sinflararo_uxshashlik[x] = featurening_sinflararo_uxshashligi

        # VAZN
        featurening_vazni = dict()
        for x in sinflararo_uxshashlik.keys():
            featurening_vazni[x] = sinflararo_uxshashlik[x] * sinflararo_farq[x]
            # print(featurening_vazni[x])

        self.feature_weight = featurening_vazni
        ####################################################
        #     OBYEKTNING UMUMLASHGAN BAHOSI    #############
        ####################################################

        obyektning_umulashgan_bahosi = dict()
        for obj_key in range(obyektlar_soni):  # HAR BIR OBJECT UCHUN
            RS = 0
            for feature_key in range(alomatlar_soni):
                # print(intervaldagi_vakillar[obj_key][feature_key])
                RS += featurening_vazni[feature_key] * \
                      (intervaldagi_vakillar[obj_key][feature_key][0] \
                       / k1_quvvat - intervaldagi_vakillar[obj_key][feature_key][1] / k2_quvvat)

            obyektning_umulashgan_bahosi[obj_key] = RS

        self.generalized_estimate = obyektning_umulashgan_bahosi

    ################################################################################
    def generalized_estimate_func2(self, features_set=None):
        """ Umumlashgan baxoni topuvchifunksiya

        :param features_set: Agar berilgan bo'lsa faqat o'shalar uchun topiladi
        :return: vektor size m.
        """

        if features_set is None: features_set = set(range(self.n))
        # print(f"{features_set} Ustunlar uchun:")

        db = self.intervals
        target = copy.deepcopy(self.target[:])

        k1_quvvat = target.count(self.class_names[0])
        k2_quvvat = sum(self.class_power.values()) - k1_quvvat

        obyektlar_soni = self.m
        alomatlar_soni = self.n

        #########################################################
        #    UXSHASHLIK va FARQ                                ##
        #########################################################

        sinflararo_farq = dict()
        sinflararo_uxshashlik = dict()

        # intervaldagi_vakillar = {x: {} for x in range(obyektlar_soni)}
        intervaldagi_vakillar = dict()
        for obj_key in range(obyektlar_soni):
            for feature_key in features_set:
                intervaldagi_vakillar[obj_key] = {feature_key: 0}

        for x in features_set:  # har bir Feature uchun
            featurening_sinflararo_farqi = 1
            featurening_sinflararo_uxshashligi = 0
            farq_summa = 0
            uxshash_summa = 0
            #
            # print('#################')
            # for item in db.items():
            #     print(item)

            for interval in db[x]:  # har bir interval uchun
                k1_vakillari = k2_vakillari = 0
                # print(interval)
                for ind in interval[5]:  # feature'ning intervalidagi  har bir index uchun
                    if target[ind] == self.class_names[0]:
                        k1_vakillari += 1
                    else:
                        k2_vakillari += 1

                # print(k1_vakillari, k2_vakillari)
                farq_summa += k1_vakillari * k2_vakillari
                uxshash_summa += k1_vakillari * (k1_vakillari - 1) + k2_vakillari * (k2_vakillari - 1)

                # print(x, interval)#, intervaldagi_vakillar[x])
                for ind in interval[5]:
                    intervaldagi_vakillar[ind][x] = (k1_vakillari, k2_vakillari)
                    # print(ind, intervaldagi_vakillar[ind])
                # print(interval[], intervaldagi_vakillar[x])

            featurening_sinflararo_farqi -= farq_summa / (k1_quvvat * k2_quvvat)
            featurening_sinflararo_uxshashligi = uxshash_summa / (
                    k1_quvvat ** 2 - k1_quvvat + k2_quvvat ** 2 - k2_quvvat)

            sinflararo_farq[x] = featurening_sinflararo_farqi
            sinflararo_uxshashlik[x] = featurening_sinflararo_uxshashligi
            # print(f"{x} ustunning sinflararo farqi={featurening_sinflararo_farqi}, uxshash{featurening_sinflararo_uxshashligi}")

        # VAZN
        featurening_vazni = dict()
        for x in sinflararo_uxshashlik.keys():
            featurening_vazni[x] = sinflararo_uxshashlik[x] * sinflararo_farq[x]
            # print(featurening_vazni[x])

        self.feature_weight = featurening_vazni
        ####################################################
        #     OBYEKTNING UMUMLASHGAN BAHOSI    #############
        ####################################################

        obyektning_umulashgan_bahosi = dict()
        for obj_key in range(obyektlar_soni):  # HAR BIR OBJECT UCHUN
            RS = 0
            for feature_key in features_set:
                # print(intervaldagi_vakillar[obj_key][feature_key])
                RS += featurening_vazni[feature_key] * \
                      (intervaldagi_vakillar[obj_key][feature_key][0] \
                       / k1_quvvat - intervaldagi_vakillar[obj_key][feature_key][1] / k2_quvvat)

            obyektning_umulashgan_bahosi[obj_key] = RS

        self.generalized_estimate = obyektning_umulashgan_bahosi
        return obyektning_umulashgan_bahosi

    def scatter(self, feature1, feature2):
        """RASMINI CHIZAMIZ
        feature1, feature2      dict:   size m.
        """

        fig, ax = plt.subplots(figsize=(20, 10))

        ids = feature1.keys() if type(feature1) == dict else range(len(feature1))

        marker = 'x^ov'
        for class_label in self.class_names:

            x_lar = []
            y_lar = []
            id_lar = []
            for object_id in ids:
                if self.target[object_id] == class_label:
                    x_lar.append(feature1[object_id])
                    y_lar.append(feature2[object_id])
                    id_lar.append(object_id)

            ax.scatter(x_lar, y_lar, s=250, marker=marker[int(class_label)], label=str(class_label))

            for n, txt in enumerate(id_lar):
                ax.annotate(txt, (x_lar[n], y_lar[n]))

        ax.legend()

        # time = str(datetime.datetime.now())[:20].replace(":", "..")
        time = str(datetime.datetime.now())[:10]

        fig.savefig(f"out_data\\{self.df_name}\\{time}fig.pdf")
        start_file(f"out_data\\{self.df_name}\\{time}fig.pdf")

    # region Self service
    def print_df(self):
        for x in range(self.m):
            print(self.original_df[x], "\t", self.target[x])
        pass

    def __str__(self):
        for item in self.__dict__.items():
            if item[0] not in ['df', "target", 'df_nominal', "distance_table"]:
                self.mprint(item)
        return ""

    def mprint(self, collection, intend=''):
        # print(type(collection))
        # if type(collection) == type({0:0}.items()):
        #     print(f"{intend}{collection[0]}:{collection[1]} asd{type(collection)}")
        if type(collection) in (list, tuple):
            for element in collection:
                if type(element) in (list, tuple, set, dict):
                    print()
                    self.mprint(element, intend + "    ")
                else:
                    print(f"{intend}{element}", end=" ")
        elif type(collection) == dict:
            for element in collection.items():
                if type(element[1]) in (list, tuple, set, dict):
                    self.mprint(element, intend + "    ")
                else:
                    print(f"{intend}{element[0]}:{element[1]}")
        elif type(collection) == set:
            for element in collection:
                print(element, end=' ')
            print()

        else:
            print(f"{collection}")
        print()

    ################################################################################
    def run(self):
        # if features_set is None: features_set = set(range(self.n))
        self.nominalizer()
        # self.binanizer()

        self.generalized_estimate_func2()
        pass

    ################################################################################
    def create_folders(self):
        if not os.path.exists(f"out_data\\{self.df_name}"):
            os.mkdir(f"out_data\\{self.df_name}")
        if not os.path.exists(f"out_data\\{self.df_name}\\logs"):
            os.mkdir(f"out_data\\{self.df_name}\\logs")
        if not os.path.exists(f"out_data\\{self.df_name}\\figures"):
            os.mkdir(f"out_data\\{self.df_name}\\figures")
    # endregion

