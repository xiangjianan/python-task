"""
LSC最长公共子序列问题
1、动态优化，要先找到最优子结构
    根据问题总结以下特性：
        特性1：如果两个序列的最后一个元素相同，都为x，则去掉最后一个元素的两序列的最长公共子序列 比 原两序列的最长公共子序列少一个x
        特性2：如果两个序列的最后一个元素不相同，那么两序列的最长公共子序列，一定是只去掉任意序列最后一个元素后 的两种情况下的最长公共子序列中 最长的那一个
    由此，在遇到最后一个元素相同时，同时去掉两序列的最后一个元素；最后一个元素不同时，根据具体情况去掉其中一个序列的最后一个元素，即转为求更短序列的最长公共子序列问题
    即转化为解决最优子问题
2、确定公式
    设：序列X(m) = [x1,x2,x3,...,xi,...,xm], 序列Y(n) = [y1,y2,y3,...,yi,...,yn], c[i,j] = X(i)和Y(i)的LSC长度
        根据特性1，有：
            c[i,j] = c[i-i][j-1] + 1                   (xi=yi)
        根据特性2，有：
            c[i,j] = max(c[i][j-1], c[i-1][j])         (xi!=yi)
3、编写代码
    根据两序列长度，构建一个初始化内容为0二维列表，从[1,1]位置开始，根据公式逐行或逐列补充列表，如：
        （数字表示c[i,j] = X(i)和Y(i)的LSC长度）
             A  B  C  B  D  A  B
         [0, 0, 0, 0, 0, 0, 0, 0]
       B [0, 0, 1, 1, 1, 1, 1, 1]
       D [0, 0, 1, 1, 1, 2, 2, 2]
       C [0, 0, 1, 2, 2, 2, 2, 2]
       A [0, 1, 1, 2, 2, 2, 3, 3]
       B [0, 1, 2, 2, 3, 3, 3, 4]
       A [0, 1, 2, 2, 3, 3, 4, 4]
    为了能回溯最长的公共子序列，需要建一个路线对照表，如：
        （数字表示回溯路线：1为斜向[i-1][j-1]、2为向上[i-1][j]、3为向左[i][j-1]、4为向上向左均可）
             A  B  C  B  D  A  B
         [0, 0, 0, 0, 0, 0, 0, 0]
       B [0, 4, 1, 3, 1, 3, 3, 1]
       D [0, 4, 2, 4, 4, 1, 3, 3]
       C [0, 4, 2, 1, 3, 4, 4, 4]
       A [0, 1, 4, 2, 4, 4, 1, 3]
       B [0, 2, 1, 4, 1, 3, 4, 1]
       A [0, 1, 2, 4, 2, 4, 1, 4]
"""


def lsc(left_right, up_down):
    """
    构建最长公共子序列对照列表、路径指向列表
    :param left_right: 序列1，横行展开
    :param up_down: 序列2，纵向展开
    :return:
    """
    n_lr = len(left_right)
    n_ud = len(up_down)
    li = [[0 for _ in range(n_lr + 1)] for _ in range(n_ud + 1)]  # 最长公共子序列对照列表
    path = [[0 for _ in range(n_lr + 1)] for _ in range(n_ud + 1)]  # 路径指向列表
    for i in range(1, n_ud + 1):
        for j in range(1, n_lr + 1):
            # 斜向：尾元素相同（公式1）
            if left_right[j - 1] == up_down[i - 1]:
                li[i][j] = li[i - 1][j - 1] + 1
                path[i][j] = 1
            # 向上：尾元素不相同，且上方的LSC更大（公式2）
            elif li[i - 1][j] > li[i][j - 1]:
                li[i][j] = li[i - 1][j]
                path[i][j] = 2
            # 向左：尾元素不相同，且左方的LSC更大（公式2）
            elif li[i - 1][j] < li[i][j - 1]:
                li[i][j] = li[i][j - 1]
                path[i][j] = 3
            # 左和上相等（公式2）
            else:
                li[i][j] = li[i][j - 1]
                path[i][j] = 4
    return li, path


def lsc_path(left_right, up_down):
    """
    路线回溯
    :param left_right:
    :param up_down:
    :return:
    """
    li, c = lsc(left_right, up_down)
    n_lr = len(left_right)
    n_ud = len(up_down)
    res = []
    while n_lr > 0 and n_ud > 0:
        if c[n_ud][n_lr] == 1:  # 斜向回溯
            res.append(left_right[n_lr - 1])
            n_lr -= 1
            n_ud -= 1
        elif c[n_ud][n_lr] == 2:  # 向上回溯
            n_ud -= 1
        elif c[n_ud][n_lr] == 3:  # 向左回溯
            n_lr -= 1
        else:  # 向上向左回溯均可
            n_lr -= 1
    return ''.join(reversed(res))


if __name__ == '__main__':
    a = 'AB43CB2352346DAB'
    b = 'BD23CA246435675BA'
    r = lsc_path(a, b)
    print(r)
