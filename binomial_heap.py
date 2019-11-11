
class Node():
    def __init__(self, key):
        self.root = False
        self.key = key
        self.degree = 1
        self.children = []
        self.parent = []
        self.siblings = []
        self.root_degree = 1

def union(heap, temp):
    new = []
    pt_heap = 0
    pt_temp = 0
    while pt_heap < len(heap) and pt_temp < len(temp):
        if heap[pt_heap].degree <= temp[pt_temp].degree:
            new.append(heap[pt_heap])
            pt_heap += 1
        else:
            new.append(temp[pt_temp])
            pt_temp += 1
    while pt_heap < len(heap):
        new.append(heap[pt_heap])
        pt_heap += 1
    while pt_temp < len(temp):
        new.append(temp[pt_temp])
        pt_temp += 1
    return new


def mergeBinomialTrees(node1, node2):
    #print("bye", node1.key, node2.key)
    if node1.key > node2.key:
        temp = node2
        node2 = node1
        node1 = temp
    node1.degree += 1
    node2.parent = node1
    node2.siblings = node1.children
    node1.children = node2
    node1.root = True
    node2.root = False
    return node1

def adjust(heap):
    if len(heap) <= 1:
        #print("returning")
        return heap
    i1 = 0
    i2 = 0
    if len(heap) == 2:
        i2 += 1
        i3 = len(heap)
    else:
        i2 += 1
        i3 = i2
        i3 += 1

    while i1 != len(heap):
        if i2 == len(heap):
            i1 += 1
        elif heap[i1].degree < heap[i2].degree:
            i1 += 1
            i2 += 1
            if i3 != len(heap):
                i3 += 1
        elif i3 < len(heap) and heap[i1].degree == heap[i2].degree and heap[i1].degree == heap[i3].degree:
            i1 += 1
            i2 += 1
            i3 += 1
        elif heap[i1].degree == heap[i2].degree:
            #print(heap[i1].key, heap[i2].key)
            heap[i1] = mergeBinomialTrees(heap[i1], heap[i2])
            del(heap[i2])
            if i3 != len(heap):
                i3 += 1
    return heap

def insertTreeInHeap(heap, tree):
    temp = [tree]
    temp = union(heap, temp)

    return adjust(temp)

def insert(heap, key):
    tree = Node(key)
    return insertTreeInHeap(heap, tree)


def label_print_nodes(heap):
    for item in heap:
        root_degree = item.degree
        queue = [item]
        while len(queue) > 0:
            q = queue.pop(0)
            q.root_degree = root_degree
            child = q.children
            if child == []:
                continue
            child.root_degree = root_degree
            queue.append(child)
            while child.siblings != []:
                child = child.siblings
                queue.append(child)
                child.root_degree = root_degree

SYMBOLS = {1: "", 2: "|", 3: "/ \\", 4: "/  |  \\"}

def print_tree(heap):
    label_print_nodes(heap)
    queue = heap.copy()
    all_root_degress = []
    previous_line = []
    counter = 1
    i = 0
    while i < len(heap):
        if heap[i].degree == counter:
            print("{}{}".format("-" * 9, heap[i].key), end="")
            previous_line.append("{}{}".format(" " * 9, SYMBOLS[heap[i].degree]))
            all_root_degress.append(heap[i].degree)
            i += 1
        else:
            print("{}".format("-" * 9), end="")
            previous_line.append("{}".format(" " * 9))
        counter += 1

    print('\n')
    for item in previous_line:
        print(item, end="")
    print('\n')
    print("{}".format(" " * (heap[0].degree*9)), end="")
    previous_line = []
    queue.append("nl")
    level=2
    while len(queue) > 0:
        if len(queue) == 1 and queue[0] == "nl":
            break
        v = queue.pop(0)
        if v == "nl":
            print("\n")
            level += 0.5
            print("{}".format(" " * (heap[0].degree * 9)), end="")
            for item in previous_line:
                root_degree = item[1]
                item = item[0]
                if level == 2.5:
                    if item == 2 and root_degree == 3 and heap[0].degree == 1:
                        print("{}".format(" " * 18), end="")
                    elif item == 2 and root_degree == 3:
                        bit = 0 if heap[0].degree == 3 else 1
                        print("{}".format(" " * 9* bit), end="")
                    elif item == 3 and root_degree == 4:
                        print("{}".format(" " * 9*(4-heap[0].degree)), end="")
                elif level == 3.5:
                    if item == 2:
                        if heap[0].degree == 1 and root_degree == 2:
                            print("{}".format(" " * 9), end="")
                        elif heap[0].degree == 1 and root_degree == 4:
                            print("{}".format(" " * 27), end="")
                        elif heap[0].degree == 2 and root_degree == 4:
                            print("{}".format(" " * 18), end="")
                print(SYMBOLS[item], end=" ")
            print('\n')
            print("{}".format(" " * (heap[0].degree*9)), end="")
            previous_line = []
            queue.append("nl")
            level += 0.5
            continue


        child = v.children
        if child == []:
            continue
        if level == 2.0:
            if child.root_degree == heap[0].degree:
                pass
            else:
                prev_root = all_root_degress.index(v.root_degree) - 1
                print("{}".format(" " * (9 * (child.root_degree - heap[prev_root].degree))), end="")
        elif level == 3.0:
            if child.siblings == [] and child.degree == 1 and child.root_degree >3:
                pass
            elif child.root_degree == heap[0].degree:
                pass
            else:
                print("{}".format(" " * (9 * (child.root_degree - heap[0].degree))), end="")
        elif level == 4.0:
            print("{}".format(" " * (9 * (child.root_degree - heap[0].degree))), end="")
        queue.append(child)
        if level == 3.0 and child.degree == 1:
            print(" ", end='')
        print("{}".format(child.key), end="")
        previous_line.append((child.degree, child.root_degree))

        while child.siblings != []:
            child = child.siblings
            queue.append(child)
            print("  {}".format(child.key), end="")
            previous_line.append((child.degree, child.root_degree))


def main():
    user_input = input("Enter comma-separated list of integers (e.g. 6,5,4,3,2,1): ")
    int_list = [int(i) for i in user_input.split(",")]
    print("Input:::{}".format(int_list))

    binomial_heap = []
    for item in int_list:
        binomial_heap = insert(binomial_heap, item)
    print_tree(binomial_heap)


if __name__ == "__main__":
    main()