"""
排序算法
冒泡排序｜选择排序｜插入排序｜快速排序｜堆排序｜归并排序｜希尔排序｜计数排序｜桶排序｜基数排序
"""
import random
from abc import ABCMeta, abstractmethod

from cal_time import cal_time


class Sort(metaclass=ABCMeta):
    """
    一个抽象类
    """

    @abstractmethod
    def sort(self, li):
        """
        一个抽象排序方法
        :param li: 无序列表
        :return: 有序列表
        """
        pass


class BubbleSort(Sort):
    """
    冒泡排序
    时间复杂度：最坏 O(n*n)、平均 O(n*n)、最优 O(n)
    空间复杂度：O(1)
    简介：
        1 循环一次列表，对每相邻两个元素做比较，决定是否交换
        2 一次循环后，有序区个数+1，无序区个数-1
        3 再对无序区重复步骤1
    """

    @cal_time
    def sort(self, li):
        """
        冒泡排序
        :param li:
        :return:
        """
        n = len(li)
        for n_ in range(n - 1):
            change_flag = False  # 判断原始数据是否是有序的标志
            for i in range(n - n_ - 1):
                if li[i] > li[i + 1]:  # 相邻元素做比较
                    li[i], li[i + 1] = li[i + 1], li[i]
                    change_flag = True
            if not change_flag:  # 最优时间复杂度O(n)
                break
        return li

    def __str__(self):
        return '冒泡排序'


class SelectSort(Sort):
    """
    选择排序
    时间复杂度：最坏 O(n*n)、平均 O(n*n)、最优 O(n*n)
    空间复杂度：O(1)
    简介：
        1 设列表第一个元素为有序区，后面元素为无序区
        2 遍历一遍无序区，找到无序区中比有序区最后一个元素更小的元素，并交换
        3 对无序区重复步骤1，有序区个数+1，无序区个数-1
    """

    @cal_time
    def sort(self, li):
        """
        选择排序
        :param li:
        :return:
        """
        n = len(li)
        for n_ in range(n - 1):
            min_loc = n_
            for i in range(n_ + 1, n):
                if li[i] < li[min_loc]:  # 找到无序区中比有序区最后一个元素更小的元素
                    min_loc = i
            li[n_], li[min_loc] = li[min_loc], li[n_]  # 元素交换
        return li

    def __str__(self):
        return '选择排序'


class InsertSort(Sort):
    """
    插入排序
    时间复杂度：最坏 O(n*n)、平均 O(n*n)、最优 O(n*n)
    空间复杂度：O(1)
    简介：
        1 设列表第一个元素为有序区，后面元素为无序区
        2 从无序区（右）选择一个元素，插入当前有序区（左）的正确位置
        3 重复步骤2，有序区个数+1，无序区个数-1
    """

    @cal_time
    def sort(self, li):
        """
        插入排序实现方式1
        :param li:
        :return:
        """
        n = len(li)
        for right in range(1, n):
            curr = li[right]
            for left in range(right - 1, -1, -1):
                if li[left] > curr:  # curr和有序区元素逐个比较
                    li[left + 1] = li[left]
                else:  # 直到找到正确的位置，退出循环
                    li[left + 1] = curr
                    break
            else:  # curr比有序区所有元素都小
                li[right % 1] = curr
        return li

    @cal_time
    def sort_2(self, li):
        """
        插入排序实现方式2
        :param li:
        :return:
        """
        n = len(li)
        for right in range(1, n):
            curr = li[right]
            left = right - 1
            while left >= 0 and li[left] > curr:  # curr和有序区元素逐个比较，直到找到正确的位置，退出循环
                li[left + 1] = li[left]
                left -= 1
            li[left + 1] = curr  # 补充空位
        return li

    def __str__(self):
        return '插入排序'


class QuickSort(Sort):
    """
    快速排序
    时间复杂度：最坏 O(n*n)、平均 O(n*logn)、最优 O(n*logn)
    空间复杂度：最坏 O(n)、平均 O(logn)
    简介：
        1 找到列表最左边的元素，将其归位，归位后左边元素都比这个元素小，右边元素都比这个元素大
        2 归位的元素将列表分为左右两部分，这两部分又可以看成两个新列表，再对这两个新列表递归执行步骤一，直到不能再分
    补充：
        避免最坏时间复杂度O(n*n)：
            当列表为有序的情况时，要归位n-1次，效率很低；
            可以在递归时，先将首个元素随机和列表中任意元素替换，再对替换后的首位元素归位
    """

    @staticmethod
    def partition(li, left, right):
        """
        在 li[left, right] 中，对left下标元素进行归位
        :param li: 无序列表
        :param left: 左下标
        :param right: 右下标
        :return: 归位后的下标
        """
        curr = li[left]
        while left < right:
            while left < right and li[right] >= curr:  # 从右侧找到比curr小的
                right -= 1
            li[left] = li[right]  # 换位
            while left < right and li[left] <= curr:  # 从左侧找到比curr大的
                left += 1
            li[right] = li[left]  # 换位
        li[left] = curr  # 原值归位
        return left

    def _sort(self, li, left, right):
        """
        递归调用归位方法，以实现排序
        :param li: 无序列表
        :param left: 左下标
        :param right: 右下标
        :return:
        """
        if left < right:
            # 避免最坏时间复杂度
            rand = random.randint(left, right)
            li[left], li[rand] = li[rand], li[left]

            # 归位
            mid = self.partition(li, left, right)

            # 对左右两个新列表递归执行以上操作
            self._sort(li, left, mid - 1)
            self._sort(li, mid + 1, right)

    @cal_time
    def sort(self, li):
        """
        快速排序
        :param li:
        :return:
        """
        self._sort(li, 0, len(li) - 1)
        return li

    def __str__(self):
        return '快速排序'


class HeapSort(Sort):
    """
    堆排序
    时间复杂度：最坏 O(n*logn)、平均 O(n*logn)、最优 O(n*logn)
    空间复杂度：O(1)
    简介：
        堆结构：一种特殊的完全二叉树结构
            大根堆：一个完全二叉树，满足任意节点都比其子节点大
            小根堆：一个完全二叉树，满足任意节点都比其子节点小
        向下调整特性：
            一个非堆结构的完全二叉树，当根结点的左右子树都是堆结构时，可以通过一次向下调整，将其变换成一个堆结构
        构建堆：
            1 找到最后一个非叶子节点，利用向下调整特性，将其还原成堆结构
            2 继续找到上一个非叶子节点，利用向下调整特性，将其还原成堆结构
            3 重复步骤2，直到找到最后一个非叶子节点，即跟节点为止，此时构建成堆结构
        顺序取堆内的元素：
            1 拿出堆顶元素
            2 堆尾元素放到堆顶
            3 利用向下调整特性，将其还原成一个新的堆
            4 重复步骤1，直到数据全部取出
    """

    @staticmethod
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
            if j + 1 <= high and li[j + 1] > li[j]:  # 如果i有右子节点，且比左子节点大
                j = j + 1  # j指向i的右子节点
            if li[j] > tmp:  # 如果tmp不满足放在当前位置的条件，往下再走一层
                li[i] = li[j]
                i = j
                j = 2 * i + 1
            else:  # tmp满足放在当前位置的条件，把tmp放到i的位置上
                li[i] = tmp
                break
        else:  # tmp只能放在叶子节点上
            li[i] = tmp

    @cal_time
    def sort(self, li):
        """
        堆排序
        :param li:
        :return:
        """
        n = len(li)
        for i in range((n - 2) // 2, -1, -1):  # 构建堆，i表示所有非叶子节点的下标
            self.sift(li, i, n - 1)
        for i in range(n - 1, -1, -1):  # 顺序取堆内元素，i指向当前堆的最后一个元素
            li[0], li[i] = li[i], li[0]  # 将堆顶元素和堆尾元素交换
            self.sift(li, 0, i - 1)  # 利用向下调整特性将其还原成长度减1的新堆结构
        return li

    def __str__(self):
        return '堆排序'


class MergeSort(Sort):
    """
    归并排序
    时间复杂度：最坏 O(n*logn)、平均 O(n*logn)、最优 O(n*logn)
    空间复杂度：O(n)
    简介：
        1 递归将列表越分越小，直到分成一个元素，一个即有序
        2 递归将两个有序列表归并，列表越来越大
    缺点：需要额外内存开销
    """

    @staticmethod
    def merge(li, low, mid, high):
        """
        将两段有序列表归并：列表左段[low, mid]，列表右段[mid+1, high]
        :param li:
        :param low:
        :param mid:
        :param high:
        :return:
        """
        curr_list = []
        left = low
        right = mid + 1
        while left <= mid and right <= high:  # 归并结束条件
            if li[left] < li[right]:  # 左右逐个比较，小的存到临时列表
                curr_list.append(li[left])
                left += 1
            else:
                curr_list.append(li[right])
                right += 1
        while left <= mid:  # 归并结束后，左边剩余
            curr_list.append(li[left])
            left += 1
        while right <= high:  # 归并结束后，右边剩余
            curr_list.append(li[right])
            right += 1
        li[low:high + 1] = curr_list

    def _sort(self, li, low, high):
        """
        递归将列表越分越小，再递归调用归并，最终实现排序
        :param li:
        :param low:
        :param high:
        :return:
        """
        if low < high:
            # 递归将列表越分越小，直到一个元素
            mid = (low + high) // 2
            self._sort(li, low, mid)
            self._sort(li, mid + 1, high)

            # 递归将两个有序列表归并，列表越来越大
            self.merge(li, low, mid, high)

    @cal_time
    def sort(self, li):
        """
        归并排序
        :param li:
        :return:
        """
        self._sort(li, 0, len(li) - 1)
        return li

    def __str__(self):
        return '归并排序'


class ShellSort(Sort):
    """
    希尔排序（一种分组插入排序算法）
    时间复杂度：取决于Gap序列（https://en.wikiredia.com/wiki/Shellsort#Gap_sequences）
    空间复杂度：O(1)
    简介：
        Gap序列为 n/2, n/4, n/8 ..., 1 的希尔排序算法实现：
            1 取一个整数d1=n/2，将列表分为d1个组，此时每组相邻的两个元素之间的下标间距为d1，再对每个组的元素直接进行插入排序
            3 取一个整数d2=d1/2，将列表分为d2个组，此时每组相邻的两个元素之间的下标间距为d2，再对每个组的元素直接进行插入排序
            3 重复以上操作，直到di=1，即所有元素在同一个组内，此时进行插入排序即可得到最终有序列表
    """

    @staticmethod
    def sort_gap(li, gap):
        """
        分组插入排序实现方式1
        :param li:
        :param gap: 分组间距
        :return:
        """
        n = len(li)
        for right in range(gap, n):
            curr = li[right]
            for left in range(right - gap, -1, -gap):
                if li[left] > curr:  # curr和当前组内的有序区元素逐个比较
                    li[left + gap] = li[left]
                else:  # 直到找到正确的位置，退出循环
                    li[left + gap] = curr
                    break
            else:  # curr比当前组内的有序区所有元素都小
                li[right % gap] = curr  # right % gap 为当前组的第一个元素下标
        return li

    @staticmethod
    def sort_gap_2(li, gap):
        """
        分组插入排序实现方式2
        :param li:
        :param gap: 分组间距
        :return:
        """
        n = len(li)
        for right in range(gap, n):
            curr = li[right]
            left = right - gap
            while left >= 0 and li[left] > curr:  # curr和有序区元素逐个比较，直到找到正确的位置，退出循环
                li[left + gap] = li[left]
                left -= gap
            li[left + gap] = curr  # 补充空位
        return li

    @cal_time
    def sort(self, li):
        """
        希尔排序
        :param li:
        :return:
        """
        n = len(li) // 2
        while n >= 1:
            self.sort_gap(li, n)
            n //= 2
        return li

    def __str__(self):
        return '希尔排序'


class CountSort(Sort):
    """
    计数排序
    时间复杂度：O(n)
    空间复杂度：O(n)
    简介：
        适用条件
            假设已知列表中数据范围在0-100之间
        1 生成一个长度为100的列表
        2 遍历列表，对1-100之间的元素出现次数做统计，并存储
        3 更具统计后的数据按顺序展开，生成新的列表即排序完成
    """

    @staticmethod
    def count_sort(li, max_count=100):
        """
        计数排序
        :param li:
        :param max_count:
        :return:
        """
        count = [0 for _ in range(max_count + 1)]  # 生成一个长度为100的列表
        for val in li:
            count[val] += 1  # 对1-100之间的元素出现次数做统计
        li.clear()
        for ind, val in enumerate(count):
            for _ in range(val):
                li.append(ind)

    @cal_time
    def sort(self, li):
        """
        计数排序
        :param li:
        :return:
        """
        self.count_sort(li, 100)
        return li

    def __str__(self):
        return '计数排序'


class BucketSort(Sort):
    """
    桶排序
    时间复杂度：平均O(n+k)、最坏O(n*n*k)
    空间复杂度：O(n*k)
    简介：
        适用条件
            假设已知列表内元素都在1-10000范围内
        1 构建100个桶，每个桶内存放固定范围内的元素
        2 遍历列表，根据元素范围确定该放哪个桶内
        3 对每个桶内元素排序，所有桶加起来即为有序列表
    效率：
        取决于数据的分布，对不同数据排序时采取不同对分桶策略
    """

    @staticmethod
    def bucket_sort(li, n=100, max_num=10000):
        buckets = [[] for _ in range(n)]  # 创建桶
        for val in li:
            i = min(val // (max_num // n), n - 1)  # i 表示var放到几号桶里
            buckets[i].append(val)  # 把val加到桶里
            for j in range(len(buckets[i]) - 1, 0, -1):  # 同时保持桶内的顺序
                if buckets[i][j] < buckets[i][j - 1]:
                    buckets[i][j], buckets[i][j - 1] = buckets[i][j - 1], buckets[i][j]
                else:
                    break
        sorted_li = []
        for buc in buckets:
            sorted_li.extend(buc)
        return sorted_li

    @cal_time
    def sort(self, li):
        """
        桶排序
        :param li:
        :return:
        """
        return self.bucket_sort(li, 10, 100)

    def __str__(self):
        return '桶排序'


class RadixSort(Sort):
    """
    基数排序
    时间复杂度：O(n*k)
    空间复杂度：O(n+k)
    简介：
        1 找到元素中最大值，并得到其位数k
        2 分0-9十个桶，
        3 对列表中元素的个位进行分桶排序
        4 对列表中元素的十位进行分桶排序
        5 重复操作，直到k位
    """

    @cal_time
    def sort(self, li):
        """
        基数排序
        :param li:
        :return:
        """
        max_num = max(li)
        it = 0
        while 10 ** it <= max_num:
            buckets = [[] for _ in range(10)]
            for var in li:  # 分桶
                digit = (var // 10 ** it) % 10
                buckets[digit].append(var)
            li.clear()
            for buc in buckets:  # 把分桶后的元素重新写回li
                li.extend(buc)
            it += 1
        return li

    def __str__(self):
        return '基数排序'


def run():
    sort_obj_list = list()
    sort_obj_list.append(QuickSort())
    sort_obj_list.append(HeapSort())
    sort_obj_list.append(MergeSort())
    sort_obj_list.append(ShellSort())
    sort_obj_list.append(CountSort())
    sort_obj_list.append(BucketSort())
    sort_obj_list.append(RadixSort())
    sort_obj_list.append(BubbleSort())
    sort_obj_list.append(SelectSort())
    sort_obj_list.append(InsertSort())

    a = [random.randint(0, 100) for i in range(10000)]
    line = '='.join(['' for i in range(50)])

    for sort_obj in sort_obj_list:
        random.shuffle(a)
        print(f'''{line}\n{sort_obj}...''')
        res = sort_obj.sort(a)
        # print(res)


if __name__ == '__main__':
    run()
