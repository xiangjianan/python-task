"""
topk问题
获取一个大列表中值最大的前10个元素
"""
import random
from cal_time import cal_time


def sift(li, low, high):
    """
    向下调整实现
    :param li: 一个非堆结构的完全二叉树，其根结点的左右子树都是堆结构
    :param low: 堆的根节点位置
    :param high: 堆的最后一个元素的位置
    :return:
    """
    i = low  # i开始指向根节点
    j = 2 * i + 1  # j开始指向i的左子节点
    tmp = li[low]  # 把堆顶元素存起来
    while j <= high:  # 只要j位置有元素
        if j + 1 <= high and li[j + 1] < li[j]:  # 如果i有右子节点，且比左子节点大
            j = j + 1  # j指向i的右子节点
        if li[j] < tmp:  # 如果tmp不满足放在当前位置的条件，往下再走一层
            li[i] = li[j]
            i = j
            j = 2 * i + 1
        else:  # tmp满足放在当前位置的条件，把tmp放到i的位置上
            li[i] = tmp
            break
    else:  # tmp只能放在叶子节点上
        li[i] = tmp


@cal_time
def topk(li, k):
    """
    获取列表内最大的10个数
    :param li:
    :param k:
    :return:
    """
    heap = li[0:k]
    for i in range((k - 2) // 2, -1, -1):  # 建堆
        sift(heap, i, k - 1)
    for i in range(k, len(li) - 1):  # 遍历
        if li[i] > heap[0]:
            heap[0] = li[i]
            sift(heap, 0, k - 1)
    for i in range(k - 1, -1, -1):  # 取数
        heap[0], heap[i] = heap[i], heap[0]
        sift(heap, 0, i - 1)
    return heap


li_10 = list(range(100000))
random.shuffle(li_10)

print(topk(li_10, 10))
