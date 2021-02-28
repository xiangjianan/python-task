"""
2-sum问题
给定一个列表和一个整数，从列表中找到两个数，使得两数之和等于给定的数，返回两个数的下标。题目保证有且只有一组解
"""
import random
from cal_time import cal_time


@cal_time
def two_sum_1(nums, target):
    """
    方法1：遍历列表，逐个取元素n1，同时再逐个取n1右侧数n2，判断 n1 + n2 是否满足条件，满足条件时直接返回两者下标
    时间复杂度：O(n*n)
    :param nums:
    :param target:
    :return:
    """
    n = len(nums)
    for i in range(n - 1):
        n1 = nums[i]
        for j in range(i + 1, n):
            n2 = nums[j]
            if n1 + n2 == target:
                return i, j


@cal_time
def two_sum_2(nums, target):
    """
    方法2：遍历列表，逐个取元素n1，计算出另一个数 n2 = target - n1，判断n2是否在列表内
    时间复杂度：O(n*k)，k为python查找某个元素是否在列表内的时间复杂度
    :param nums:
    :param target:
    :return:
    """
    for n1 in nums:
        n2 = target - n1
        if n2 in nums:  # 判断n2是否在列表内
            if n1 != n2:
                return nums.index(n1), nums.index(n2)
            else:  # n1和n2重复
                return nums.index(n1), nums.index(n2, nums.index(n1) + 1)


def search(li, val):
    """
    二分查找方法
    :param li:
    :param val:
    :return:
    """
    left = 0
    right = len(li) - 1
    while left <= right:
        mid = (left + right) // 2
        if val == li[mid][0]:
            return mid
        elif val > li[mid][0]:
            left = mid + 1
        elif val < li[mid][0]:
            right = mid - 1
    else:
        return -1


@cal_time
def two_sum_3(nums, target):
    """
    方法3：在方法2的基础上，将列表排序，以用二分法判断n2是否在列表内，提高查找效率
    时间复杂度：O(n*logn)
    :param nums:
    :param target:
    :return:
    """
    nums_ = [[num, index] for index, num in enumerate(nums)]
    nums_.sort(key=lambda x: x[0])  # 按值排序
    for i in range(len(nums_)):
        n1 = nums_[i][0]
        n2 = target - n1
        j = search(nums_, n2)  # 二分法判断n2是否在列表内
        if j >= 0:
            if n1 != n2:
                return nums_[i][1], nums_[j][1]
            else:  # n1和n2重复
                return nums.index(n1), nums.index(n2, nums.index(n1) + 1)


if __name__ == '__main__':
    a = [i for i in range(10001)]
    s = 19999
    random.shuffle(a)
    print(two_sum_1(a, s))
    print(two_sum_2(a, s))
    print(two_sum_3(a, s))
