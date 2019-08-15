# coding=utf-8

from functools import reduce


def lists_combination(lists, code=''):
    '''输入多个列表组成的列表, 输出其中每个列表所有元素可能的所有排列组合
    code用于分隔每个元素'''
    try:
        import reduce
    except:
        from functools import reduce

    def myfunc(list1, list2):
        return [str(i) + code + str(j) for i in list1 for j in list2]

    return reduce(myfunc, lists)


def get_fn():
    fn = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
    return fn


def get_arrs(num):
    a = [1, 2, 3, 4, 5, 6]
    lists = []
    for i in range(num):
        lists.append(a)
    return lists


def all_perm(lists):
    func_perm = lambda x, code=',': reduce(lambda x, y: ['%s,%s' % (i,j) for i in x for j in y], x)
    lists = func_perm(lists)
    func_to_int = lambda x: [int(i) for i in x.split(',')]

    return [func_to_int(i) for i in lists]


def cal_freq(lists):
    freq_dict = dict()
    for i in range(len(lists)):
        temp = lists[i]
        key = sum(temp)
        if freq_dict.__contains__(key):
            freq_dict[key] += 1
        else:
            freq_dict[key] = 1
    return freq_dict


def get_max_freq(freq_dict):
    valuse = freq_dict.values()
    max_freq = max(list(valuse))
    print("max:", max_freq)
    res = [(k, v) for k, v in freq_dict.items() if v == max_freq]
    return res

def main():
    ori_lists = get_arrs(6)
    res_lists = all_perm(ori_lists)
    freq_res = cal_freq(res_lists)
    print(freq_res)
    max_res = get_max_freq(freq_res)
    print(max_res)


if __name__ == "__main__":
    main()