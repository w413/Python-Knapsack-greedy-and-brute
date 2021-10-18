import random
import cProfile
import pstats

file = open("results.txt", 'w')
def create_items(n):
    items = []
    for i in range(n):
        items.append({
            'value': random.randint(50, 500000),
            'weight': random.randint(1, 10000)
        })
    file.write("Item set:\n")
    for i in range(n):
        file.write(str(items[i]))
        file.write('\n')
    return items


def super_set(items):
    a = []
    n = len(items)
    for i in range(pow(2, n)):
        a.append([])
        temp = i
        for j in range(n):
            if temp == 0:
                a[i].append(0)
            else:
                a[i].append(temp % 2)
                temp = temp // 2
    return a


def knapsack_brute(item):
    n = len(item)
    maxweight = 10000
    superset = super_set(item)
    currentweight = 0
    currentval = 0
    maxval = 0
    items = {
        'total weight': 0,
        'total value': 0
    }
    for i in range(len(superset)):
        for j in range(n):
            if superset[i][j] == 1:
                currentweight += item[j]["weight"]
                currentval += item[j]["value"]
            if currentweight > maxweight:
                currentval = 0
                break
        if currentval > maxval:
            maxval = currentval
            items['total weight'] = currentweight
            items['total value'] = currentval
        currentweight = 0
        currentval = 0
    return items


def knapsack_greedy(item):
    n = len(item)
    items = {
        'total weight': 0,
        'total value': 0
    }
    item = sorted(item, key=lambda k: k['value'])
    items['total weight'] += item[n-1]['weight']
    items['total value'] += item[n-1]['value']
    maxweight = 10000 - items['total weight']
    n-=1
    while n > 0:
        if item[n-1]['weight'] < maxweight:
            maxweight -= item[n-1]['weight']
            items['total weight'] += item[n - 1]['weight']
            items['total value'] += item[n - 1]['value']
        n-=1
    return items

'''
Sorry for the poor formatting
'''
for n in range(3, 16):
    file.write("n=%i\n" % (n))
    item = create_items(n)
    file.write("\nBrute force results:")
    file.write(str(knapsack_brute(item)))
    file.write('\n')
    cProfile.run('knapsack_brute(item)', 'restats')
    p = pstats.Stats('restats', stream=file)
    p.strip_dirs().print_stats(10)
    file.write("\nGreedy results:")
    file.write(str(knapsack_greedy(item)))
    file.write('\n')
    cProfile.run('knapsack_greedy(item)', 'restats')
    p = pstats.Stats('restats', stream=file)
    p.strip_dirs().print_stats(10)
    file.write("\n\n\n")

file.close()