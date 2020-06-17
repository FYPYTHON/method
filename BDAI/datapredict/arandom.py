# coding=utf-8
from random import randint
start = 1
end = 100


def check_leve(num_ori):
    num = num_ori * 100 / 100
    if 0 < num <= 19:
        level = 1
    elif 19 < num <= 19 + 17:
        level = 2
    elif 36 < num <= 36 + 15:
        level = 3
    elif 51 < num <= 51 + 13:
        level = 4
    elif 64 < num <= 64 + 11:
        level = 5
    elif 75 < num <= 75 + 9:
        level = 6
    elif 84 < num <= 84 + 7:
        level = 7
    elif 91 < num <= 91 + 5:
        level = 8
    elif 96 < num <= 96 + 3:
        level = 9
    elif 99 < num <= 100:
        level = 10
    else:
        level = 0
    return level

def get_fre():
    data_fre = dict()
    num_data = 1000
    for i in range(num_data):
        rd = randint(start, end)
        rkey = check_leve(rd)
        if rkey in data_fre.keys():
            data_fre[rkey] += 1
        else:
            data_fre[rkey] = 1

    data_p = sorted(data_fre.items(), key=lambda d: d[1], reverse=True)
    print(data_p)
    for data in data_p:
        # print(type(data[1]))
        print(data[0], "%.2f" % (data[1] / num_data * 100))


def get_char():
    cha_s = 0x4e00
    cha_e = 0x9fa5
    c_num = 100
    for i in range(c_num):
        # cchar = randint(cha_s, cha_e)
        # print(chr(cchar))
        i = i + 19968 + 100 * 2
        print(i, chr(i))
if __name__ == "__main__":
    # get_fre()
    get_char()
