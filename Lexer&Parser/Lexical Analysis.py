from tkinter import *
from tkinter import ttk
from graphviz import Digraph
from queue import Queue


# 存储操作符和NFA的栈
class Stack:
    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


postack = Stack()
a = []  # 状态表
b = []  # 状态转换表
final_dfastate = []
final_transition = []
mappings = {}  # 新旧标号之间的映射


# 正则表达式转换为逆波兰表达式
def priority(c):  # 操作符优先级
    c1 = postack.top()
    priorities = {'*': 3, '.': 2, '|': 1, '(': 0}  # 优先级表
    if priorities[c] <= priorities[c1]:  # c是当前元素 c1是栈顶元素
        return True
    else:
        return False


# 在适当位置插入连接符确保表达式的正确性
def algorithm():
    try:
        s = reg.get()
        s1 = list(s)  # s1是list类型
        print(len(s1))
        nn = len(s1)
        i = 0
        while i < nn:
            if i < nn - 1:
                if 'a' <= s1[i] <= 'z':
                    if 'a' <= s1[i + 1] <= 'z':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '#':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '(':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                if s1[i] == '#':
                    if 'a' <= s1[i + 1] <= 'z':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '#':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '(':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                if s1[i] == ')':
                    if 'a' <= s1[i + 1] <= 'z':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '#':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '(':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                if s1[i] == '*':
                    if 'a' <= s1[i + 1] <= 'z':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '#':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
                    elif s1[i + 1] == '(':
                        s1.insert(i + 1, '.')
                        i = i + 1
                        nn = nn + 1
            i = i + 1
        s = ''.join(s1)
        print(s)
        # 逆波兰表达式
        res = list()
        i = 0
        while i < nn:
            # 操作数直接添加到结果列表
            if 'a' <= s1[i] <= 'z' or s1[i] == '#':
                res.append(s1[i])
            # 操作符根据优先级压入栈或弹出栈
            elif s1[i] == '(':
                postack.push(s1[i])
            elif s1[i] == ')':
                while not postack.top() == '(':
                    res.append(postack.top())
                    postack.pop()
                postack.pop()
            elif s1[i] == '*' or s1[i] == '|' or s1[i] == '.':
                if postack.empty():
                    postack.push(s1[i])
                elif postack.top() == '(':
                    postack.push(s1[i])
                elif priority(s1[i]):
                    while postack.size() > 0 and priority(s1[i]):
                        res.append(postack.top())
                        postack.pop()
                    postack.push(s1[i])
                else:
                    postack.push(s1[i])
            i = i + 1
        # 将栈中剩余的操作符依次弹出并添加到结果列表
        while not postack.empty():
            res.append(postack.top())
            postack.pop()
        s2.set(''.join(res))

    except ValueError:
        pass


# 定义NFA的状态和转换结构
class NFA:
    def __init__(self):
        self.state1 = state()
        self.state2 = state()
        self.tran = [transition() for _ in range(10)]


class state:
    def __init__(self):
        self.ID = 0  # 状态ID
        self.start = 0  # 起始状态
        self.accept = 0  # 接收状态


class transition:
    def __init__(self):
        self.sourcestate = state()  # 源状态
        self.targetstate = state()  # 目标状态
        self.ways = ''  # 转换方式


# 根据后缀表达式创建NFA
def createNFA():
    s22 = s2.get()
    s3 = list(s22)
    nfastack = Stack()  # 存放nfa的栈

    i = 0
    k = 0
    # 遍历后缀表达式
    while i < len(s3):
        if 'a' <= s3[i] <= 'z' or s3[i] == '#':  # 操作数
            # 创建一个新的NFA
            N1 = NFA()
            N1.state1.ID = k
            N1.state1.start = 1
            N1.state1.accept = 0
            k = k + 1
            N1.state2.ID = k
            N1.state2.start = 0
            N1.state2.accept = 1
            k = k + 1
            N1.tran[0].sourcestate = N1.state1
            N1.tran[0].targetstate = N1.state2
            N1.tran[0].ways = s3[i]
            # 将N1压入栈中，并将其状态和转换添加到全局列表a和b中
            nfastack.push(N1)
            a.append(N1.state1)
            a.append(N1.state2)
            b.append(N1.tran[0])
        elif s3[i] == '|':  # 选择操作符
            # 弹出两个NFA
            t1 = nfastack.top()
            nfastack.pop()
            t2 = nfastack.top()
            nfastack.pop()
            # 创建一个新的NFA
            N3 = NFA()
            num = 0
            N3.state1.ID = k
            N3.state1.start = 1
            N3.state1.accept = 0
            t1.state1.start = 0
            t1.state2.accept = 0
            k = k + 1
            N3.state2.ID = k
            N3.state2.start = 0
            N3.state2.accept = 1
            t2.state1.start = 0
            t2.state2.accept = 0
            k = k + 1
            # N3的起始状态连接到t1和t2的起始状态
            N3.tran[num].sourcestate = N3.state1
            N3.tran[num].targetstate = t1.state1
            N3.tran[num].ways = '#'
            num = num + 1
            N3.tran[num].sourcestate = N3.state1
            N3.tran[num].targetstate = t2.state1
            N3.tran[num].ways = '#'
            num = num + 1
            # t1和t2的结束状态连接到N3的结束状态
            N3.tran[num].sourcestate = t1.state2
            N3.tran[num].targetstate = N3.state2
            N3.tran[num].ways = '#'
            num = num + 1
            N3.tran[num].sourcestate = t2.state2
            N3.tran[num].targetstate = N3.state2
            N3.tran[num].ways = '#'
            num = num + 1

            # 将N3压入栈中，并将其状态和转换添加到全局列表a和b中
            nfastack.push(N3)
            a.append(N3.state1)
            a.append(N3.state2)
            for ii in range(0, num):
                b.append(N3.tran[ii])
        elif s3[i] == '.':  # 连接操作符
            # 弹出两个NFA
            t1 = nfastack.top()
            nfastack.pop()
            t2 = nfastack.top()
            nfastack.pop()
            # 创建一个新的NFA
            N3 = NFA()
            N3.state1.ID = k
            N3.state1.start = 1
            N3.state1.accept = 0
            k = k + 1
            N3.state2.ID = k
            N3.state2.start = 0
            N3.state2.accept = 1
            k = k + 1
            t1.state1.start = 0
            t1.state2.accept = 0
            t2.state1.start = 0
            t2.state2.accept = 0
            # N3的起始状态为t2的起始状态
            num = 0
            N3.tran[num].sourcestate = N3.state1
            N3.tran[num].targetstate = t2.state1
            N3.tran[num].ways = '#'
            # t2的结束状态连接到t1的起始状态
            num = num + 1
            N3.tran[num].sourcestate = t2.state2
            N3.tran[num].targetstate = t1.state1
            N3.tran[num].ways = '#'
            # N3的结束状态为t1的结束状态
            num = num + 1
            N3.tran[num].sourcestate = t1.state2
            N3.tran[num].targetstate = N3.state2
            N3.tran[num].ways = '#'
            # 将N3压入栈中，并将其状态和转换添加到全局列表a和b中
            nfastack.push(N3)
            a.append(N3.state1)
            a.append(N3.state2)
            for ii in range(0, 3):
                b.append(N3.tran[ii])
        elif s3[i] == '*':  # 闭包操作符
            # 弹出一个NFA
            t1 = nfastack.top()
            nfastack.pop()
            # 创建一个新的NFA
            N3 = NFA()
            N3.state1.ID = k
            N3.state1.start = 1
            N3.state1.accept = 0
            k = k + 1
            N3.state2.ID = k
            N3.state2.start = 0
            N3.state2.accept = 1
            k = k + 1
            t1.state1.start = 0
            t1.state2.accept = 0
            num = 0
            # N3的起始状态连接到t1的起始状态
            N3.tran[num].sourcestate = N3.state1
            N3.tran[num].targetstate = t1.state1
            N3.tran[num].ways = '#'
            num = num + 1
            # N3的起始状态连接到N3的结束状态
            N3.tran[num].sourcestate = N3.state1
            N3.tran[num].targetstate = N3.state2
            N3.tran[num].ways = '#'
            num = num + 1
            # t1的结束状态连接回t1的起始状态
            N3.tran[num].sourcestate = t1.state2
            N3.tran[num].targetstate = t1.state1
            N3.tran[num].ways = '#'
            num = num + 1
            # t1的结束状态连连接到N3的结束状态
            N3.tran[num].sourcestate = t1.state2
            N3.tran[num].targetstate = N3.state2
            N3.tran[num].ways = '#'
            num = num + 1
            nfastack.push(N3)
            a.append(N3.state1)
            a.append(N3.state2)
            for ii in range(0, num):
                b.append(N3.tran[ii])
        i = i + 1
    # 生成NFA图
    g = Digraph('测试NFA')
    for i in range(0, len(a)):
        if a[i].start == 1:
            g.edge('start', str(a[i].ID), color='blue')
            g.node(name=str(a[i].ID), color='red', shape='circle')
        elif a[i].accept == 1:
            g.node(name=str(a[i].ID), color='red', shape='doublecircle')
        else:
            g.node(name=str(a[i].ID), color='red', shape='circle')
    for j in range(0, len(b)):
        g.edge(str(b[j].sourcestate.ID), str(b[j].targetstate.ID), str(b[j].ways), color='green')
    g.view()


def combine(startstate):  # 合并具有epsilon转换的状态
    fstate = []
    while not startstate.empty():
        t = startstate.get()
        fstate.append(t)
        for j in range(0, len(b)):
            if b[j].sourcestate.ID == t and b[j].ways == '#':
                startstate.put(b[j].targetstate.ID)
    return fstate


def createDFA():
    startstate = Queue(maxsize=500)  # NFA开始状态
    for i in range(0, len(a)):
        if a[i].start == 1:
            startstate.put(a[i].ID)
            break
    fstate = combine(startstate)
    statetrans = []  # 存储DFA的状态转换关系
    dfastate = [fstate]  # 存储已经生成的DFA状态
    # 对dfastate中的每个状态进行扩展
    nn = 0
    sizee = 1
    while nn < sizee:
        for c in range(0, 26):  # 假设字母表有ab
            char = chr(c + 97)
            temp = Queue(maxsize=2000)  # 存储可能到达的状态
            for j in range(0, len(dfastate[nn])):
                for k1 in range(0, len(b)):
                    if b[k1].sourcestate.ID == dfastate[nn][j] and b[k1].ways == str(char):  # 条件判断没进去
                        temp.put(b[k1].targetstate.ID)

            temp1 = combine(temp)  # 合并temp队列中的状态
            temp1_set = set(temp1)
            temp1 = list(temp1_set)  # 去重
            if temp1 not in dfastate:
                dfastate.append(temp1)
                sizee = sizee + 1
            statetrans.append([dfastate[nn], char, temp1])
        nn = nn + 1
    # 创建最终的DFA状态列表
    cnt = 0
    startnum = 0  # 存储NFA的起始状态ID
    endnum = 0  # 存储NFA的接受状态ID
    for i in range(0, len(a)):
        if a[i].start == 1:
            startnum = a[i].ID
        if a[i].accept == 1:
            endnum = a[i].ID
    for i in range(0, len(dfastate)):  # 遍历dfastate列表中的每个DFA状态
        flag = 0
        for j in range(0, len(dfastate[i])):
            if endnum in dfastate[i]:  # 包含接受状态
                s = state()  # 创建一个新状态
                s.start = 0
                s.accept = 1
                s.ID = cnt
                mappings[cnt] = dfastate[i]  # 将该状态添加到dfastate列表，并在mappings字典中建立该状态ID和对应DFA状态的映射
                cnt = cnt + 1
                final_dfastate.append(s)
                flag = 1
                break
            elif startnum in dfastate[i]:  # 包含起始状态
                s = state()
                s.start = 1
                s.accept = 0
                s.ID = cnt
                mappings[cnt] = dfastate[i]
                cnt = cnt + 1
                final_dfastate.append(s)
                flag = 1
                break
        if flag == 0:  # 既不包含起始状态也不包含接受状态
            s = state()
            s.start = 0
            s.accept = 0
            s.ID = cnt
            mappings[cnt] = dfastate[i]
            cnt = cnt + 1
            final_dfastate.append(s)
    # 创建最终的状态转换列表
    for i in range(0, len(statetrans)):  # 遍历statetrans列表中的每个元素
        ttr = transition()
        if statetrans[i][0]:  # 检查并处理非空的转换
            ttr.sourcestate = list(mappings.keys())[list(mappings.values()).index(statetrans[i][0])]
            ttr.targetstate = list(mappings.keys())[list(mappings.values()).index(statetrans[i][2])]
            ttr.ways = statetrans[i][1]  # 设置转换方式
            final_transition.append(ttr)
    # 生成DFA图
    g = Digraph('测试DFA')
    for i in range(0, len(final_dfastate)):
        if mappings[final_dfastate[i].ID]:
            if final_dfastate[i].start == 1:  # 开始状态
                g.edge('start', str(final_dfastate[i].ID), color='blue')  # 边
                g.node(name=str(final_dfastate[i].ID), color='red', shape='circle')  # 节点
            elif final_dfastate[i].accept == 1:  # 接受状态
                g.node(name=str(final_dfastate[i].ID), color='red', shape='doublecircle')
            else:
                g.node(name=str(final_dfastate[i].ID), color='red', shape='circle')
    # 添加状态转换
    for j in range(0, len(final_transition)):
        if mappings[final_transition[j].sourcestate] != [] and mappings[final_transition[j].targetstate] != []:
            g.edge(str(final_transition[j].sourcestate), str(final_transition[j].targetstate),
                   str(final_transition[j].ways), color='green')
    g.view()
    return 0


# 最小化DFA
def createminimizedDFA():
    # ori_cata字典初始化 记录每个状态所属的类别
    ori_cata = {}
    # 根据DFA状态的接受情况对状态进行分类
    for i in range(len(final_dfastate)):
        if mappings[final_dfastate[i].ID]:
            if final_dfastate[i].accept == 1:
                ori_cata[final_dfastate[i].ID] = 2
            else:
                ori_cata[final_dfastate[i].ID] = 1
    kinds = 2
    previous = 1
    # 构建状态转换表mata 记录每个状态及其对应的转换
    mata = {}
    ll = 0
    for i in range(len(final_transition)):
        if final_transition[i].sourcestate not in mata.keys():
            mata[final_transition[i].sourcestate] = {ord(final_transition[i].ways): final_transition[i].targetstate}
            ll = ll + 1
        elif final_transition[i].sourcestate in mata.keys():
            mata[final_transition[i].sourcestate].update(
                {ord(final_transition[i].ways): final_transition[i].targetstate})
    for key, value in mata.items():
        sorted(value.items(), key=lambda k: k[0])
    # 状态合并循环
    maps = {}  # 更新后节点的类号
    while not kinds == previous:
        cnt = 1
        if len(maps) is not 0:
            for key, value in maps.items():
                ori_cata[key] = value
        maps = {}
        set1 = {}
        previous = kinds
        for key, value in mata.items():
            state1 = [ori_cata[key]]
            for key1, value1 in value.items():
                if mappings[value1]:
                    state1.append(ori_cata[value1])
                else:
                    state1.append(-1)
            if tuple(state1) not in set1.keys():
                maps[key] = cnt
                set1[tuple(state1)] = cnt
                cnt = cnt + 1
            else:
                maps[key] = set1[tuple(state1)]
        kinds = cnt - 1
    # 构建新状态表
    new_states1 = []
    new_transition = []
    for i in range(len(final_dfastate)):
        ss1 = state()
        if mappings[final_dfastate[i].ID]:
            ss1.ID = ori_cata[final_dfastate[i].ID]
            if final_dfastate[i].accept == 1:
                ss1.accept = 1
                ss1.start = 0
            elif final_dfastate[i].start == 1:
                ss1.start = 1
                ss1.accept = 0
            else:
                ss1.start = 0
                ss1.accept = 0
            if ss1 not in new_states1:
                new_states1.append(ss1)
    # 构建新状态转换表
    for i in range(len(final_transition)):
        if mappings[final_transition[i].sourcestate] != [] and mappings[final_transition[i].targetstate] != []:
            tran = [ori_cata[final_transition[i].sourcestate], ori_cata[final_transition[i].targetstate],
                    final_transition[i].ways]
            if tran not in new_transition:
                new_transition.append(tran)
    # 生成最小化DFA图
    g = Digraph('测试最小化DFA')
    for i in range(0, len(new_states1)):
        if new_states1[i].start == 1:
            g.edge('start', str(new_states1[i].ID), color='blue')
            g.node(name=str(new_states1[i].ID), color='red', shape='circle')
        elif new_states1[i].accept == 1:
            g.node(name=str(new_states1[i].ID), color='red', shape='doublecircle')
        else:
            g.node(name=str(new_states1[i].ID), color='red', shape='circle')
    for j in range(0, len(new_transition)):
        g.edge(str(new_transition[j][0]), str(new_transition[j][1]), str(new_transition[j][2]), color='green')
    g.view()
    return 0


# 创建根窗口
root = Tk()
root.title("Regex to NFA and DFA")
# 创建主框架
mainframe = ttk.Frame(root, padding="5 3 12 12")  # 设置框架的内边距
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# 添加标签和输入框
label1 = Label(mainframe, text="请输入正则表达式（epsilon用#代替）：")
label1.grid(row=1, column=1)
reg = StringVar()  # 存储用户输入的正则表达式
reg_entry = ttk.Entry(mainframe, width=15, textvariable=reg)
reg_entry.grid(row=1, column=2, rowspan=1, columnspan=2)
# 添加提交按钮
Button(mainframe, text="提交", command=algorithm).grid(row=1, column=6)
# 添加逆波兰表达式显示
s2 = StringVar()  # 存储逆波兰表达式
ttk.Label(mainframe, text="逆波兰表达式为：").grid(row=2, column=1)
ttk.Label(mainframe, textvariable=s2).grid(row=2, column=2)
# 添加生成NFA、DFA和最小化DFA的按钮
Button(mainframe, text="generate NFA", command=createNFA).grid(row=3, column=1)  # 点击后执行createNFA函数
Button(mainframe, text="generate DFA", command=createDFA).grid(row=3, column=3)  # 点击后执行createDFA函数
Button(mainframe, text="generate minimized DFA", command=createminimizedDFA).grid(row=3,
                                                                                  column=6)  # 点击后执行createminimizedDFA函数
# 绑定回车键事件
root.bind("<Return>", algorithm)  # 按下回车键时执行algorithm函数
# 运行主循环
root.mainloop()  # 启动Tkinter主循环，使得窗口保持运行状态，可以响应用户的操作
