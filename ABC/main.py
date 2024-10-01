
import numpy as np
from data_solve import data_deal 
from fjsp import FJSP
from GABC import abc



P_GLR = [0.3, 0.3]  # 机器串生成规则 GS /LS /ＲS，依次是0.3,0.3，最后是1-0.3-0.3
P_MSR = [0.3, 0.3]  # 工序串的生成规则 MＲL /SPT /ＲS，依次是0.3,0.3，最后是1-0.3-0.3
# 记得修改迭代次数回来
parm_mo = [1, 10, 20, 5]  # 依次是迭代次数，种群规模，搜索次数，阈值
# path = 'excels/MK01.xlsx'
insert_path = './INSERT01.xlsx'
insertTime = 40
breakNum=3
breakTime=5
breakLen=30

jobNum=3
cancelTime=10
def do_tabc(job_num,machine_num,path):
    da = data_deal(job_num, machine_num, path)  # 工件数，机器数,读取文件路径
    Tmachine, Tmachinetime, tdx, work, tom, machines = da.cacu(da.read(path))  # mko1数据
    parm_data = [Tmachine, Tmachinetime, tdx, work, tom, machines]



    fj = FJSP(da.job_num, da.machine_num, P_GLR, parm_data, P_MSR)  # 前面两个数是工件数，机器数
    ho = abc(da.job_num,da.machine_num, fj, parm_mo, parm_data)


    # 记录结果
    w, m, t, result = ho.gabc()
    C_finish,list_M,list_S,list_W, tmax= fj.caculate(w, m, t)
    print(list_S)
    print(list_M)
    print(list_W)
    print(w)
    # 获取插入相关信息
    # 获取机器完工时间最晚的机器编号
    # tmax=np.argmax(machine_end)+1

    # 获取插入时最晚完工时间
    # C_finish=np.max(job_end)
    # print(C_finish)
    # fj.draw_change(result)  # 画完工时间变化图
    # fj.draw(w, C_finish,list_M,list_S,list_W,tmax)  # 画甘特图
    return da,ho,w,list_W,list_S,list_M,C_finish
def insert_jobs(da,ho,w,list_W,list_S,list_M,C_finish):
     # 记录插入之前的完成工件数量，机器完成时间以及工件完成时间还有是否保留排序
     job_count, machine_end, job_end, w = ho.insertJobs(insertTime, C_finish, list_M, list_S, list_W, w)

     # 记录在插入之前处理的工件顺序
     new_w = []
     new_list_M = []
     new_list_S = []
     new_list_W = []
     for i in range(len(w)):
         if (w[i] != -1):
             new_w.append(w[i])
             new_list_M.append(list_M[i])
             new_list_S.append(list_S[i])
             new_list_W.append(list_W[i])
     # 处理原始数据并与插入工件合并,生成新表
     data = da.insert(path, job_count,insert_path)

     # 重新运行
     Tmachine, Tmachinetime, tdx, work, tom, machines = da.cacu(data)  # 融合后数据
     parm_data = [Tmachine, Tmachinetime, tdx, work, tom, machines]

     fj = FJSP(da.job_num, da.machine_num, P_GLR, parm_data, P_MSR)  # 前面两个数是工件数，机器数
     # 处理多出来的工件
     old_jobnum = len(job_end[0])
     job_end = np.resize(job_end, (1, da.job_num))
     for i in range(fj.job_num - old_jobnum):
         job_end[0][i + old_jobnum] = insertTime

     # 传递参数
     fj.machine_end = machine_end
     fj.job_end = job_end

     ho = abc(da.job_num, da.machine_num, fj, parm_mo, parm_data)

     w, m, t, result = ho.gabc()
     C_finish, list_M, list_S, list_W, tmax = fj.caculate(w, m, t)

     # 合并安排结果
     for i in range(len(w)):
         new_w.append(w[i])
         new_list_M.append(list_M[i])
         new_list_S.append(list_S[i])
         new_list_W.append(list_W[i])

     # fj.draw(w, m, t)  # 画甘特图
     # fj.draw_change(result)  # 画完工时间变化图

     fj.draw_insert(new_w, C_finish, new_list_M, new_list_S, new_list_W, tmax, insertTime)  # 画甘特图

def machine_break(da,ho,w,list_W,list_S,list_M,C_finish):
    # 记录插入之前的完成工件数量，机器完成时间以及工件完成时间还有是否保留排序
    job_count, machine_end, job_end, w ,rest= ho.machineBreak(breakNum,breakTime,breakLen,C_finish, list_M, list_S, list_W, w)


    # 记录在插入之前处理的工件顺序
    new_w = []
    new_list_M = []
    new_list_S = []
    new_list_W = []
    for i in range(len(w)):
        if (w[i] != -1):
            new_w.append(w[i])
            new_list_M.append(list_M[i])
            new_list_S.append(list_S[i])
            new_list_W.append(list_W[i])
    # 处理原始数据并与插入工件合并,生成新表
    data = da.insert(path, job_count, '')

    # 重新运行
    Tmachine, Tmachinetime, tdx, work, tom, machines = da.cacu(data)  # 融合后数据
    parm_data = [Tmachine, Tmachinetime, tdx, work, tom, machines]

    fj = FJSP(da.job_num, da.machine_num, P_GLR, parm_data, P_MSR)  # 前面两个数是工件数，机器数


    # 传递参数
    fj.machine_end = machine_end
    fj.job_end = job_end
    fj.rest_time=rest

    ho = abc(da.job_num, da.machine_num, fj, parm_mo, parm_data)

    w, m, t, result = ho.gabc()
    C_finish, list_M, list_S, list_W, tmax = fj.caculate(w, m, t)

    # 合并安排结果
    for i in range(len(w)):
        new_w.append(w[i])
        new_list_M.append(list_M[i])
        new_list_S.append(list_S[i])
        new_list_W.append(list_W[i])

    # fj.draw(w, m, t)  # 画甘特图
    # fj.draw_change(result)  # 画完工时间变化图

    fj.draw_break(new_w, C_finish, new_list_M, new_list_S, new_list_W, tmax, breakTime,breakTime+breakLen,breakNum)  # 画甘特图


def cancel_job(da, ho, w, list_W, list_S, list_M, C_finish):
    # 记录插入之前的完成工件数量，机器完成时间以及工件完成时间还有是否保留排序
    job_count, machine_end, job_end, w = ho.cancelJob(jobNum,cancelTime, C_finish, list_M, list_S, list_W, w)

    # 记录在插入之前处理的工件顺序
    new_w = []
    new_list_M = []
    new_list_S = []
    new_list_W = []
    for i in range(len(w)):
        if (w[i] != -1):
            new_w.append(w[i])
            new_list_M.append(list_M[i])
            new_list_S.append(list_S[i])
            new_list_W.append(list_W[i])
    # 处理原始数据并与插入工件合并,生成新表
    data = da.insert(path, job_count, '')

    # 重新运行
    Tmachine, Tmachinetime, tdx, work, tom, machines = da.cacu(data)  # 处理后数据
    parm_data = [Tmachine, Tmachinetime, tdx, work, tom, machines]

    fj = FJSP(da.job_num, da.machine_num, P_GLR, parm_data, P_MSR)  # 前面两个数是工件数，机器数


    # 传递参数
    fj.machine_end = machine_end
    fj.job_end = job_end

    ho = abc(da.job_num, da.machine_num, fj, parm_mo, parm_data)

    w, m, t, result = ho.gabc()
    C_finish, list_M, list_S, list_W, tmax = fj.caculate(w, m, t)

    # 合并安排结果
    for i in range(len(w)):
        new_w.append(w[i])
        new_list_M.append(list_M[i])
        new_list_S.append(list_S[i])
        new_list_W.append(list_W[i])

    # fj.draw(w, m, t)  # 画甘特图
    # fj.draw_change(result)  # 画完工时间变化图

    fj.draw_cancel(new_w, C_finish, new_list_M, new_list_S, new_list_W, tmax, cancelTime,jobNum)  # 画甘特图

if __name__ == "__main__":

    da,ho,w,list_W,list_S,list_M,C_finish=do_tabc(10,6,'excels/MK01.xlsx')
    # insert_jobs(da, ho, w, list_W, list_S, list_M, C_finish)
    # print('机器故障')
    #
    # machine_break(da,ho,w,list_W,list_S,list_M,C_finish)

    # cancel_job(da,ho,w,list_W,list_S,list_M,C_finish)
    #
    # for i in range(1,11):
    #     if(i<10):
    #         filename = './instance/Mk0{}.txt'.format(i)
    #         path = './excels/MK0{}.xlsx'.format(i)
    #     else:
    #         filename = './instance/Mk{}.txt'.format(i)
    #         path = './excels/MK{}.xlsx'.format(i)
    #     # 获取工件数和机器数
    #     f = open(filename)
    #     line = list(f.readline().split())
    #
    #     jobs_sum=int(line[0])
    #     machines_sum=int(line[1])
    #     # 运行十次
    #     final_result=[]
    #     for j in range(3):
    #
    #         da,ho,w,list_W,list_S,list_M,C_finish=do_tabc(jobs_sum,machines_sum)
    #         final_result.append(C_finish)
    #         # print(final_result)
    #     average=sum(final_result)/len(final_result)
    #     print(final_result)
    #     print('MK{}'.format(i)+'最好结果为{}'.format(min(final_result))+'运行十次平均为{}'.format(average))
    # path='./excels/kacem1010.xlsx'
    # da,ho,w,list_W,list_S,list_M,C_finish=do_tabc(10,10)


