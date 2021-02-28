"""
数据结构
栈｜队列｜链表
"""


class MyStack(object):
    """
    自定义栈类
    """

    def __init__(self):
        self.stack = []

    def push(self, data=None):
        """
        入栈
        :param data: 入栈数据
        :return:
        """
        self.stack.append(data)

    def pop(self):
        """
        出栈
        :return: 出栈数据
        """
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError('stack is empty!')

    def is_empty(self):
        """
        判断栈是否为空
        :return:
        """
        return len(self.stack) == 0

    def get_pop(self):
        """
        获取栈顶元素
        :return:
        """
        return self.stack[-1]

    def __str__(self):
        """
        字符串方法
        :return:
        """
        stack_str = ''
        for data in self.stack:
            stack_str += f' -> {data}'
        return stack_str[4:]


class MyQueue(object):
    """
    自定义环形队列类
    """

    def __init__(self, size=100):
        self.size = size
        self.queue = [None for _ in range(size)]
        self.front = 0  # 首位下标
        self.rear = 0  # 末位下标

    def append(self, data=None):
        """
        末位入队列
        :param data: 入队数据
        :return:
        """
        if not self.is_filled():
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = data
        else:
            raise IndexError('queue is filled!')

    def pop(self):
        """
        末位出队列
        :return: 出队数据
        """
        if not self.is_empty():
            self.rear = (self.rear - 1) % self.size
            return self.queue[self.rear]
        else:
            raise IndexError('queue is empty!')

    def appendleft(self, data=None):
        """
        首位入队列
        :param data: 入队数据
        :return:
        """
        if not self.is_filled():
            self.queue[self.front] = data
            self.front = (self.front - 1) % self.size
        else:
            raise IndexError('queue is filled!')

    def popleft(self):
        """
        首位出队列
        :return: 出队数据
        """
        if not self.is_empty():
            self.front = (self.front + 1) % self.size
            return self.queue[self.front]
        else:
            raise IndexError('queue is empty!')

    def is_empty(self):
        """
        判断队列是否为空
        :return:
        """
        return self.rear == self.front

    def is_filled(self):
        """
        判断队列是否已满
        :return:
        """
        return self.front == (self.rear + 1) % self.size

    def __str__(self):
        """
        字符串方法
        :return:
        """
        queue_str = ''
        if not self.is_empty():
            if self.rear > self.front:
                for i in range(self.front + 1, self.rear + 1):
                    queue_str += f' -> {self.queue[i]}'
            elif self.rear < self.front:  # rear和front跨过0号下标的情况
                for i in range(self.front + 1, self.size):
                    queue_str += f' -> {self.queue[i]}'
                for i in range(self.rear + 1):
                    queue_str += f' -> {self.queue[i]}'
        else:
            queue_str = ' -> NULL'
        return queue_str[4:]


class Node(object):
    """
    节点类
    """

    def __init__(self, data=None):
        self.data = data
        self.next = None  # 子节点
        self.prev = None  # 父节点

    def free(self):
        """
        回收节点内存
        :return:
        """
        self.data = self.next = self.prev = None

    def __str__(self):
        return str(self.data)


class MyLinkList(object):
    """
    自定义双向链表类
    """

    def __init__(self):
        self.head = self.tail = self.curr = None

    def append(self, data):
        """
        在尾部追加节点
        :param data:
        :return:
        """
        p = Node(data)
        if self.is_empty():  # 空链表
            self.head = self.tail = p
            p.prev = p.next = None
        else:  # 非空链表
            self.tail.next = p
            p.prev = self.tail
            p.next = None
            self.tail = p

    def pop(self):
        """
        删除尾部节点
        :return:
        """
        if not self.is_empty():
            self.curr = self.tail
            self.tail = self.curr.prev
            self.tail.next = None
            self.curr.free()
        else:
            raise IndexError('link is empty!')

    def appendleft(self, data):
        """
        在头部追加节点
        :param data:
        :return:
        """
        p = Node(data)
        if self.is_empty():  # 空链表
            self.head = self.tail = p
            p.prev = p.next = None
        else:  # 非空链表
            self.head.prev = p
            p.next = self.head
            p.prev = None
            self.head = p

    def popleft(self):
        """
        删除头部节点
        :return:
        """
        if not self.is_empty():
            self.curr = self.head
            self.head = self.curr.next
            self.head.prev = None
            self.curr.free()
        else:
            raise IndexError('link is empty!')

    def insert(self, data, new_data):
        """
        在内容为data的节点后插入新节点
        :param data:
        :param new_data:
        :return:
        """
        self.curr = self.find_node_by_data(data)
        if self.curr:
            p = Node(new_data)
            if self.curr == self.tail:  # 在尾部插入节点
                self.tail.next = p
                p.prev = self.tail
                p.next = None
            else:  # 在中间插入节点
                p.next = self.curr.next
                self.curr.next.prev = p
                self.curr.next = p
                p.prev = self.curr

    def delete(self, data):
        """
        删除内容为data的节点
        :param data:
        :return:
        """
        self.curr = self.find_node_by_data(data)
        if self.curr:
            if self.curr == self.head:  # 删除头节点
                self.head = self.curr.next
                self.head.prev = None
            elif self.curr == self.tail:  # 删除尾节点
                self.tail = self.curr.prev
                self.tail.next = None
            else:  # 删除中间节点
                self.curr.prev.next = self.curr.next
                self.curr.next.prev = self.curr.prev
            self.curr.free()  # 回收内存

    def extend(self, li):
        """
        通过列表批量添加节点
        :param li:
        :return:
        """
        for data in li:
            self.append(data)

    def find_node_by_data(self, data):
        """
        根据数据查找节点
        :param data: 数据内容
        :return:
        """
        if not self.is_empty():
            self.curr = self.head
            while self.curr:
                if self.curr.data == data:
                    return self.curr
                self.curr = self.curr.next

    def is_empty(self):
        """
        判断链表是否为空
        :return:
        """
        return self.head is None

    def __str__(self):
        """
        字符串方法
        :return:
        """
        link_str = ''
        self.curr = self.head
        while self.curr:
            link_str += f' <-> {self.curr.data}'
            self.curr = self.curr.next
        return link_str[5:]


if __name__ == '__main__':
    s = MyStack()
    s.push(1)
    s.push(2)
    s.push(3)
    s.push(4)
    print(s)
    s.pop()
    print(s)

    q = MyQueue()
    q.append('a')
    q.append('b')
    q.append('c')
    q.append('d')
    print(q)
    q.popleft()
    print(q)

    link = MyLinkList()
    link.append(1)
    link.append(2)
    link.extend([1, 2, 3, '4', 'eee'])
    link.append('abc')
    link.append({22: 'a'})
    link.popleft()
    print(link)
    a = link.find_node_by_data({22: 'a'})
    print(a)
