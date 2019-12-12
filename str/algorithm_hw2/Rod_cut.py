# 作者：张子威
# 完成日期：2019/12/11
# 输入：钢管长度 钢管价格
# 功能：计算最佳钢管切割方法
# 输出：钢管切割位置，最优价格
# 注意事项：1.本方法适用于price价格为1，2，3...的连续整数，如果不然需要更改部分程序
#           2.本方法相对于普通的动态规划理论上效能提升4倍
from time import perf_counter
############
# 尾端递归钢管切割函数，P[i]为i长度钢管价格，n为目前钢管长度,切割点默认为
############
def Z_rod_cut(P,n,F,C):
    q = 0
    if n==0:
        return 0
    for x in range(2,n+1):    # range(1,3)=[1,2],range(1,1)=[]
        q=P[x-1]      # 不切割价格
        cut=[0,x]
        for y in range(x//2):
            if q<F[x-y-2]+F[y]:    # 发生切割
                q =F[x - y - 2] + F[y]
                cut[0]=y+1
                cut[1]=x-y-1
            # q=max(q,F[x-y-2]+F[y])  # 应该是1-x//2，但是range会小1，x大1，为(x-1)-(y+1)
        F.append(q)
        C[x]=cut
###########
# 切割点输出
###########
def print_cutsize(C,n):
    if C.get(n)[0] == 0:
        print(C.get(n)[1], ' ', end='')  # end默认为'\n'
    else:
        print_cutsize(C, C.get(n)[0])
        print_cutsize(C, C.get(n)[1])

###########
# 暴力法
###########
def shemedongxi(P,n):
    q=0
    if n==1:
        return 1
    for x in range(1,n+1):
        q=max(q,P[x-1]+shemedongxi(P,n-x))
    return q
############
# 主程序
############
# 资料读取
# 注意！！！要运行的话记得改这里的address！！！
# 如果放在根目录请执行以下这行
f = open("hw2_rc2.txt")
# 如果在其他目录请更改
# f = open("D:\program code/Pycharm/algorithm_hw2/hw2_rc2.txt")
temp = f.readline()
price=[]    # P[i]为i长度钢管价格，n为目前钢管长度
flength=[]  # 不同长度钢管最优解
# price init
while (temp):
    str=temp.split()
    if(str):        # 去除读取文件格式错误
        price.append(int(str[1]))
    temp = f.readline()
f.close()
# flength init
flength.append(price[0])
k=len(price)
n=20     # n可改为任意值，由于题意不明，这里默认为列出的最大长度k
i=0     # 长度溢出值
while(n>k):
    i+=1
    n-=k
# n超过40时，测试太久可以将testbd改小一点，让暴力法计算比较小的钢管长度,n小于40时请不要更改
testbd=n+k*i
# cut_set dic init
# 记录不同长度最佳切割点位置，形成2个最佳子结构（需要继续往下切）
# 由于可能会频繁插入和查询，这里用dic来节省时间
cut_set={}
cut_set[1] = [0, 1]
# 计算开始
if i == 0:
    # 计算执行时间
    start = perf_counter()
    Z_rod_cut(price, n, flength,cut_set)  # 函数引用
    end = perf_counter()
    print('使用方法：尾端递归动态规划')
    print('time cost:',end-start,'s')
    print('钢管长度：', n)
    print('最佳切割后金额：', flength[n-1])
    # print(cut_set.get(2)[0])
    print('切割后每段长度：', end='')
    print_cutsize(cut_set, n)
    print('\n\n', '使用方法：暴力法')
    print('钢管长度：', n)
    start = perf_counter()
    print('最佳切割后金额：', shemedongxi(price, n))
    end = perf_counter()
    print('time cost2:',end-start,'s')
else:
    start = perf_counter()
    Z_rod_cut(price, k, flength, cut_set)  # 函数引用
    end = perf_counter()
    print('使用方法：尾端递归动态规划')
    print('time cost:', end - start, 's')
    print('钢管长度：', n+k*i)
    print('最佳切割后金额：', flength[n - 1]+flength[k-1]*i)
    print('切割后每段长度：', end='')
    print_cutsize(cut_set, n)
    for z in range(i):
        print_cutsize(cut_set, k)
    print('\n\n', '使用方法：暴力法')
    print('钢管长度：', testbd)
    start = perf_counter()
    print('最佳切割后金额：', shemedongxi(price, testbd))
    end = perf_counter()
    print('time cost2:', end - start, 's')