import copy

import numpy as np
from data_solve import data_deal
import random 
import matplotlib.pyplot as plt 
#plt.rcParams['font.sans-serif'] = ['STSong'] 
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文
from matplotlib import cm
import matplotlib.patches as mpatches

class FJSP():
	def __init__(self,job_num,machine_num,P_GLR,parm_data,P_MSR):
		self.job_num=job_num     			#工件数
		self.machine_num=machine_num		#机器数
		self.p1=P_GLR[0] 						#全局选择的概率
		self.p2=P_GLR[1] 						#局部选择的概率
		self.Tmachine,self.Tmachinetime,self.tdx,self.work,self.tom=parm_data[0],parm_data[1],parm_data[2],parm_data[3],parm_data[4]
		self.machines=parm_data[5]
		self.p3=P_MSR[0] 						#剩余工序最大规则的概率
		self.p4=P_MSR[1] 						#加工时间最短的概率
		self.machine_end=np.zeros((1,machine_num))
		self.job_end=np.zeros((1,job_num))
		self.rest_time=[]
	def creat_Machine(self):
		# 选择机器
		job=np.copy(self.work)
		Ma_time=np.zeros((self.job_num,))
		machine,machine_time=[],[]  #初始化矩阵
		a_global=np.zeros((1,self.machine_num))
		r=np.random.rand()						
		for i in range(self.job_num):
			a_part=np.zeros((1,self.machine_num))
			time=0
			for j in range(self.machines[i]):
				highs=self.tom[i][j]
				lows=self.tom[i][j]-self.tdx[i][j]
				# 获取工序可选择机器编号
				n_machine=self.Tmachine[i,lows:highs].tolist()
				# 获取对应机器的处理时间
				n_time=self.Tmachinetime[i,lows:highs].tolist()
				index_select=[]
				if r<self.p1 or r>1-self.p2: 
					for k in range(len(n_machine)):
						m=int(n_machine[k])-1
						index_select.append(m)
						t=n_time[k]
						a_global[0,m]+=t               #全局负荷计算
						a_part[0,m]+=t 				   #局部负荷计算
					
					if r<self.p1:                       #全局选择
						select=a_global[:,index_select]
						idx_select=np.argmin(select[0])
					else:                               #局部选择
						select=a_part[:,index_select]
						idx_select=np.argmin(select[0])
					m_select=n_machine[idx_select]
					t_index=n_machine.index(m_select)
					machine.append(m_select)
					machine_time.append(n_time[t_index])
					time+=n_time[t_index]
				else:										#否则随机挑选机器								 
					index=np.random.randint(0,len(n_time),1)
					machine.append(n_machine[index[0]])
					machine_time.append(n_time[index[0]])
					time+=n_time[index[0]]
			Ma_time[i]=time
		return machine,machine_time,Ma_time
	def creat_job(self):
		# 选择工序
		count=np.zeros((1,self.job_num),dtype=int)
		machine,machine_time,Ma_time=self.creat_Machine()
		time_last=Ma_time.copy()
		left_opertion=self.machines.copy()
		rember=[sum(self.machines[:i]) for i in range(len(self.machines))]
		job=[]
		for i in  range(len(self.work)):
			r=np.random.rand()
			a=np.argwhere(time_last>0)                         #挑选剩余工件加工时间大于0的索引

			if r<self.p3+self.p4:                              #剩余工序最大规则和加工时间最短优先规则
				b=time_last[a].reshape(a.shape[0],).tolist()   #按照索引取出具体工件的加工时间
				if r<self.p3:                                  #剩余工序最大规则
					max_opertions = -1
					max_index = 0
					for i in range(len(left_opertion)):
						if(left_opertion[i]>0 and max_opertions<left_opertion[i]):
							max_opertions=left_opertion[i]
							max_index=i

					jobb=max_index
					job.append(jobb)
				else:                                         #加工时间最短优先规则
					a_index=b.index(min(b))
					jobb=int(a[a_index,0])
					job.append(jobb)
			else:                                             #随机选择规则
				index=np.random.randint(0,a.shape[0],1)
				jobb=int(a[index,0])
				job.append(jobb)
			left_opertion[jobb] -= 1
			loc=count[0,jobb]
			loc1=rember[jobb]+loc
			time=machine_time[loc1]
			time_last[jobb]-=time                             #更新剩余工件加工时间
			count[0,jobb]+=1
		return job,machine,machine_time
	def caculate(self,job,machine,machine_time):
		# 模拟运行
		jobtime=np.copy(self.job_end)
		tmm=np.copy(self.machine_end)
		tmmw=np.zeros((1,self.machine_num))			
	
		list_M,list_S,list_W=[],[],[]
		count=np.zeros((1,self.job_num),dtype=int)
		rest=copy.deepcopy(self.rest_time)
		signal=0
		if(len(rest)==0):
			for j in range(self.machine_num):
				rest.append([])
		# 工件的工序数累加和
		# rember=[sum(self.machines[:i]) for i in range(len(self.machines))]
		rember=np.zeros(len(self.machines),dtype=int)
		op_sum=0
		for i in range(len(self.machines)):
			if(self.machines[i]==0):
				continue
			rember[i]=op_sum
			op_sum+=self.machines[i]

		load_m=np.zeros((1,self.machine_num))
		for i in range(len(job)):
			# 获取工件序号
			svg=int(job[i])
			if(svg<0):
				continue
			# 获取工件对应的工序序号
			index=rember[svg]+count[0,svg]
			# 获取选定机器
			sig=int(machine[index])-1
			if jobtime[0,svg] >0 :                            #如果工序不是第一道工序
				if len(rest[sig])>0 :                         #如果空闲时间非空
					for m in range(len(rest[sig])-1,-1,-1):   #空闲时间从后往前遍历
						if rest[sig][m][1]<=jobtime[0,svg] :  #如果某个空闲时间段小于等于上一道工序的完工时间
							break                             #结束遍历
						else:                                 #否则
							begin=max(jobtime[0,svg],rest[sig][m][0])  #可开工时间是上一道工序的完工时间和空闲片段开始时间最大值
							
							if begin+machine_time[index] <= rest[sig][m][1] : #如果空闲时间段满足要求
								startime=begin                #更新开工时间
								signal=1
								del rest[sig][m]              #删掉空闲时间段
								break
			
			if signal==0 :                                    #如果不可插入
				startime=max(jobtime[0,svg],tmm[0,sig])       #开工时间是加工机器结束时间和上一道工序完工时间的最大值

			if startime>tmm[0,sig] and signal==0:             #如果不可插入且开工时间大于加工机器的完工时间
				rest[sig].append([tmm[0,sig],startime])	      #添加时间段到空闲时间里
			if signal==0 :                                    #如果不可插入
				tmm[0,sig]=startime+machine_time[index]       #更新机器的结束时间
			if signal>0 :                                     #如果可插入
				signal=0                                      #不更新机器结束时间，且可插入信号归零

			jobtime[0,svg]=startime+machine_time[index]       #更新工序完工时间
			load_m[0,sig]+=machine_time[index]                #更新对应机器的负荷

			# 加工机器的顺序添加
			list_M.append(sig+1)
			# 记录开始时间
			list_S.append(startime)
			# 记录加工时长
			list_W.append(machine_time[index])
			count[0,svg]+=1
					   
		tmax=np.argmax(tmm[0])+1		#结束最晚的机器
		C_finish=max(tmm[0])			#最晚完工时间
		
		return C_finish,list_M,list_S,list_W,tmax
	def draw(self,job,C_finish,list_M,list_S,list_W,tmax):#画图
		unique_jobs = set(job)
		num_unique_jobs = len(unique_jobs)
		cmap = cm.get_cmap('tab20', num_unique_jobs)  # 使用tab20 colormap，最多支持20种不同的颜色
		# C_finish,list_M,list_S,list_W,tmax=self.caculate(job,machine,machine_time)
		figure,ax=plt.subplots()
		count=np.zeros((1,self.job_num))
		for i in range(len(job)):
			process_width=list_W[i]
			# 根据工件编号选择颜色
			color = cmap(int(job[i]))  # 确保每个工件编号对应一个唯一颜色
			count[0][int(job[i])]+=1
			plt.bar(x=list_S[i], bottom=list_M[i], height=0.5, width=process_width, orientation="horizontal",color=color,edgecolor='black')
			plt.text(list_S[i]+process_width/4,list_M[i], f'{int(job[i])+1}-{int(count[0][int(job[i])])}',color='black',fontsize=6,weight='bold')#12是矩形框里字体的大小，可修改
		plt.plot([C_finish,C_finish],[0,tmax],c='black',linestyle='-.',label='完工时间=%.1f'% (C_finish))#用虚线画出最晚完工时间

		font1={'weight':'bold','size':22}#汉字字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.title("甘特图",font1)
		plt.ylabel("机器",font1)

		index_ls,scale_ls=[],[]
		for j in range(self.machine_num):
			index_ls.append(j+1)
			scale_ls.append('M%.0f'%(j+1))
		plt.yticks(index_ls,scale_ls)
		plt.axis([0,C_finish*1.1,0,self.machine_num+1])
		plt.tick_params(labelsize = 22)#坐标轴刻度字体大小，可以修改
		labels=ax.get_xticklabels()
		[label.set_fontname('SimHei')for label in labels]
		plt.legend(prop={'family' : ['SimHei'], 'size'   : 16})#标签字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.show()
	def draw_change(self,result):
		result=np.array(result).reshape(len(result),2)
		plt.plot(result[:,0],result[:,1])                   #画完工时间随迭代次数的变化
		font1={'weight':'bold','size':22}#汉字字体大小，可以修改
		plt.xlabel("迭代次数",font1)
		plt.title("完工时间变化图",font1)
		plt.ylabel("完工时间",font1)
		plt.show()

	def draw_insert(self,job,C_finish,list_M,list_S,list_W,tmax,insertTime):#画图
		unique_jobs = set(job)
		num_unique_jobs = len(unique_jobs)
		cmap = cm.get_cmap('tab20', num_unique_jobs)  # 使用tab20 colormap，最多支持20种不同的颜色
		# C_finish,list_M,list_S,list_W,tmax=self.caculate(job,machine,machine_time)
		figure,ax=plt.subplots()
		count=np.zeros((1,self.job_num))
		for i in range(len(job)):
			process_width=list_W[i]
			# 根据工件编号选择颜色
			color = cmap(int(job[i]))  # 确保每个工件编号对应一个唯一颜色
			count[0][int(job[i])]+=1
			plt.bar(x=list_S[i], bottom=list_M[i], height=0.5, width=process_width, orientation="horizontal",color=color,edgecolor='black')
			plt.text(list_S[i]+process_width/4,list_M[i], f'{int(job[i])+1}-{int(count[0][int(job[i])])}',color='black',fontsize=6,weight='bold')#12是矩形框里字体的大小，可修改
		plt.plot([C_finish,C_finish],[0,tmax],c='black',linestyle='-.',label='完工时间=%.1f'% (C_finish))#用虚线画出最晚完工时间
		if(insertTime>0):
			plt.plot([insertTime,insertTime],[0,self.machine_num+1],c='black',linestyle='-.',label='插入时间=%.1f'% (insertTime))#用虚线画出最晚完工时间


		font1={'weight':'bold','size':22}#汉字字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.title("甘特图",font1)
		plt.ylabel("机器",font1)

		index_ls,scale_ls=[],[]
		for j in range(self.machine_num):
			index_ls.append(j+1)
			scale_ls.append('M%.0f'%(j+1))
		plt.yticks(index_ls,scale_ls)
		plt.axis([0,C_finish*1.1,0,self.machine_num+1])
		plt.tick_params(labelsize = 22)#坐标轴刻度字体大小，可以修改
		labels=ax.get_xticklabels()
		[label.set_fontname('SimHei')for label in labels]
		plt.legend(prop={'family' : ['SimHei'], 'size'   : 16})#标签字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.show()

	def draw_break(self,job,C_finish,list_M,list_S,list_W,tmax,start,end,breakNum):#画图
		unique_jobs = set(job)
		num_unique_jobs = len(unique_jobs)
		cmap = cm.get_cmap('tab20', num_unique_jobs)  # 使用tab20 colormap，最多支持20种不同的颜色
		# C_finish,list_M,list_S,list_W,tmax=self.caculate(job,machine,machine_time)
		figure,ax=plt.subplots()
		count=np.zeros((1,self.job_num))
		for i in range(len(job)):
			process_width=list_W[i]
			# 根据工件编号选择颜色
			color = cmap(int(job[i]))  # 确保每个工件编号对应一个唯一颜色
			count[0][int(job[i])]+=1
			plt.bar(x=list_S[i], bottom=list_M[i], height=0.5, width=process_width, orientation="horizontal",color=color,edgecolor='black')
			plt.text(list_S[i]+process_width/4,list_M[i], f'{int(job[i])+1}-{int(count[0][int(job[i])])}',color='black',fontsize=6,weight='bold')#12是矩形框里字体的大小，可修改
		plt.plot([C_finish,C_finish],[0,tmax],c='black',linestyle='-.',label='完工时间=%.1f'% (C_finish))#用虚线画出最晚完工时间
		plt.plot([start, start], [0, self.machine_num + 1], c='black', linestyle='-.',
				 label='故障开始时间=%.1f' % (start))
		plt.plot([end, end], [0, self.machine_num + 1], c='black', linestyle='-.',
				 label='故障结束时间=%.1f' % (end))
		font1={'weight':'bold','size':22}#汉字字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.title("甘特图",font1)
		plt.ylabel("机器",font1)
		plt.bar(x=start, bottom=breakNum, height=0.5, width=end-start, orientation="horizontal", color='black',
				edgecolor='black')
		index_ls,scale_ls=[],[]
		for j in range(self.machine_num):
			index_ls.append(j+1)
			scale_ls.append('M%.0f'%(j+1))
		plt.yticks(index_ls,scale_ls)
		plt.axis([0,C_finish*1.1,0,self.machine_num+1])
		plt.tick_params(labelsize = 22)#坐标轴刻度字体大小，可以修改
		labels=ax.get_xticklabels()
		[label.set_fontname('SimHei')for label in labels]
		plt.legend(prop={'family' : ['SimHei'], 'size'   : 16})#标签字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.show()

	def draw_cancel(self,job,C_finish,list_M,list_S,list_W,tmax,cancelTime,jobNum):#画图
		unique_jobs = set(job)
		num_unique_jobs = len(unique_jobs)
		cmap = cm.get_cmap('tab20', num_unique_jobs)  # 使用tab20 colormap，最多支持20种不同的颜色
		# C_finish,list_M,list_S,list_W,tmax=self.caculate(job,machine,machine_time)
		figure,ax=plt.subplots()
		count=np.zeros((1,self.job_num))
		for i in range(len(job)):
			process_width=list_W[i]
			# 根据工件编号选择颜色
			color = cmap(int(job[i]))  # 确保每个工件编号对应一个唯一颜色
			count[0][int(job[i])]+=1
			plt.bar(x=list_S[i], bottom=list_M[i], height=0.5, width=process_width, orientation="horizontal",color=color,edgecolor='black')
			plt.text(list_S[i]+process_width/4,list_M[i], f'{int(job[i])+1}-{int(count[0][int(job[i])])}',color='black',fontsize=6,weight='bold')#12是矩形框里字体的大小，可修改
		plt.plot([C_finish,C_finish],[0,tmax],c='black',linestyle='-.',label='完工时间=%.1f'% (C_finish))#用虚线画出最晚完工时间

		plt.plot([cancelTime, cancelTime], [0, self.machine_num + 1], c='blue', linestyle=':',
				 label='工件取消时间=%.1f' % (cancelTime))
		custom_legend_item = mpatches.Patch(color='black', label=f'取消工件编号为{jobNum}')
		plt.legend(handles=[custom_legend_item])
		font1={'weight':'bold','size':22}#汉字字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.title("甘特图",font1)
		plt.ylabel("机器",font1)

		index_ls,scale_ls=[],[]
		for j in range(self.machine_num):
			index_ls.append(j+1)
			scale_ls.append('M%.0f'%(j+1))
		plt.yticks(index_ls,scale_ls)
		plt.axis([0,C_finish*1.1,0,self.machine_num+1])
		plt.tick_params(labelsize = 22)#坐标轴刻度字体大小，可以修改
		labels=ax.get_xticklabels()
		[label.set_fontname('SimHei')for label in labels]
		plt.legend(prop={'family' : ['SimHei'], 'size'   : 16})#标签字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.show()