"""Metrics intended for real-valued vector spaces:

  identifier	        class name	        args	        distance function
+ “euclidean”	        EuclideanDistance	                sqrt(sum((x - y)^2))
+ “manhattan”	        ManhattanDistance                   sum(|x - y|)
+ “Hemming”             HemmingDistance                     sum(|x - y|)
+ “chebyshev”	        ChebyshevDistance                   max(|x - y|)
+ “minkowski”	        MinkowskiDistance	p	            sum(|x - y|^p)^(1/p)
+ “wminkowski”	        WMinkowskiDistance	p, w	        sum(|w * (x - y)|^p)^(1/p)
6 “seuclidean”	        SEuclideanDistance	V	            sqrt(sum((x - y)^2 / V))
7 “mahalanobis”	        MahalanobisDistance	V or VI	        sqrt((x - y)' V^-1 (x - y))
"""


default_metric = 1
metric_dict = {
    1: "euclidean",
    2: "manhattan",
    3: "chebyshev",
    4: "minkowski",
    5: "hemming",
    # 5: "wminkowski",
    # 6: "seuclidean",
    # 7: "mahalanobis"
}


def validator(metric_name):

    if metric_name:

        # INT
        if type(metric_name) is int:
            if metric_dict.get(metric_name) is None:
                raise Exception(f"ERROR:\t unresolved metric_name:: continue working as default::")
            else:
                return metric_dict[metric_name]

        # FLOAT
        elif type(metric_name) is float:
            return validator(int(metric_name))

        # STR
        elif type(metric_name) is str:
            metric_name = metric_name.lower()
            for item in metric_dict.items():
                if metric_name == item[1]:
                    return item[0]
            else:  # if no matches
                raise Exception(f"ERROR:No such metric")

        # LIST or TUPLE
        elif (type(metric_name) is list or type(metric_name) is tuple) and metric_name:
            return validator(metric_name[0])

        # DICT or SET
        elif type(metric_name) is dict:
            for el in metric_name.items():
                return validator(el[1])
        elif type(metric_name) is set:
            for el in metric_name:
                return validator(el)

        # UNKNOWN type of value
        else:
            raise Exception(f"ERROR:\t unresolved type of metric value::\n\t")
    else:
        if metric_name is None:
            return default_metric
    return default_metric


def distance(object1, object2, *, metric=1, p=2, w=None):

    metric = validator(metric)
    if metric == 'euclidean':
        return __euclidean_distance(object1, object2)

    elif metric == 'chebyshev':
        return __chebyshev_distance(object1, object2)

    elif metric == 'manhattan' or metric == "hemming":
        return __manhattan_distance(object1, object2)

    elif metric == 'minkowski':
        return __minkowski_distance(object1, object2, p, w)

    # w - MUST BE A VECTOR
    elif metric == 'wminkowski':
        return __minkowski_distance(object1, object2, p, w)


def __euclidean_distance(obj1, obj2):
    """
    Calculates distance btw 2 obj using Euclidean metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param obj1:         # identifier of obj1
    :param obj2:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    r = None
    try:
        r = 0
        for feature_pair in zip(obj1, obj2):
            r += (feature_pair[0] - feature_pair[1]) ** 2
    except Exception as e:
        s = f"ERROR:\t on calculate distance:: Euclidean ::" \
            f"\n\thost_id:({obj1}); other_id:{obj2}; error:{e.args}"
        raise Exception(s)
    return r ** .5


def __minkowski_distance(obj1, obj2, p, w=None):
    """
    Calculates distance btw 2 obj using Minkowski's metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param obj1:         # identifier of obj1
    :param obj2:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    try:
        if not w: w = [1 for _ in range(len(obj1))]
        r = 0
        for x in range(len(obj1)):
            r += abs(w[x] * (obj1[x] - obj2[x])) ** p
    except Exception as e:
        s = f"ERROR:\t on calculate distance:: Euclidean ::" \
            f"\n\thost_id:({obj1}); other_id:{obj2}; error:{e.args}"
        raise Exception(s)
    return r ** (1 / p)


def __chebyshev_distance(obj1, obj2):
    """
    Calculates distance btw 2 obj using chebyshev's metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param obj1:         # identifier of obj1
    :param obj2:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    try:
        delta = []
        for feature_pair in zip(obj1, obj2):
            delta.append(abs(feature_pair[0] - feature_pair[1]))
    except Exception as e:
        import error_handler
        s = f"ERROR:\t on calculate distance:: __chebyshev_distance ::" \
            f"\n\thost_id:({obj1}); other_id:{obj2}; error:{e.args}"
        error_handler.write(s)
    return max(delta)


def __manhattan_distance(obj1, obj2):
    """
    Calculates distance btw 2 obj using Manhattan metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param obj1:         # identifier of obj1
    :param obj2:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    try:
        r = 0
        for feature_pair in zip(obj1, obj2):
            r += abs(feature_pair[0] - feature_pair[1])
    except Exception as e:
        import error_handler
        s = f"ERROR:\t on calculate distance:: __manhattan_distance ::" \
            f"\n\thost_id:({obj1}); other_id:{obj2}; error:{e.args}"
        error_handler.write(s)
    return r


if __name__ == '__main__':
    ...

