def split_list(list, n):
    target_list = []
    cut = int(len(list) / n)
    if cut == 0:
        list = [[x] for x in list]
        none_array = [[] for i in range(0, n - len(list))]
        return list + none_array
    for i in range(0, n - 1):
        target_list.append(list[cut * i:cut * (1 + i)])
    target_list.append(list[cut * (n - 1):len(list)])
    return target_list


if __name__ == '__main__':
    list = [x for x in range(1040)]
    result = split_list(list, 50)
    print(result)
