# 读取文档信息
f = open('./instance/1010.txt')
# 读取第一行
line=list(f.readline().split())
job_num=int(line[0])
machine_num=int(line[1])
# 结果
result=[]
# 开始处理数据
for i in range(job_num):
    line=list(map(int,f.readline().split()))
    block_num=line[0]
    newline=[block_num]
    # start=1
    for j in range(block_num):
        start=j*machine_num+1
        end=start+machine_num
        block=line[start:end]
        newblock=[]
        for k in range(len(block)):
            index=k+1
            if(block[k]!=0):
                newblock.extend([index,block[k]])
        if(len(block)>0):
            select_machine_num=int(len(newblock)/2)
            newblock.insert(0,select_machine_num)
            newline.extend(newblock)
    result.append(newline)
f.close()
for i in range(len(result)):
    print(result[i])

with open('./instance/kacem1010.txt', 'w', encoding='utf-8') as f:
    f.write('10 10\n')
    # 遍历列表中的每个元素
    for line in result:
        # 将元素写入文件，并添加换行符
        for item in line:
            f.write('{} '.format(item))
        f.write('\n')