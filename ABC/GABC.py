
import numpy as np
import random 
import time





class abc():
	def __init__(self,job_num,machine_num,to,parm_mo,parm_data):
		self.job_num=job_num
		self.machine_num=machine_num
		self.generation=parm_mo[0]                  #迭代次数
		self.popsize = parm_mo[1]                      # 种群规模
		self.limit=parm_mo[2]
		self.threshold=parm_mo[3]
		self.to=to
		self.Tmachine,self.Tmachinetime,self.tdx,self.work,self.tom,self.machines=parm_data[0],parm_data[1],parm_data[2],parm_data[3],parm_data[4],parm_data[5]

	def change_to_min(self,machine_index,M,T):
		rember = [sum(self.machines[:i]) for i in range(len(self.machines))]
		# print(rember)
		for i in range(self.job_num):
			for j in range(self.machines[i]):
				op_index=rember[i]+j
				if(M[op_index]==machine_index):
					r=random.random()
					# 定位后找最小
					# 读取工序的可加工机器和工序
					highs = self.tom[i][j]
					lows = self.tom[i][j] - self.tdx[i][j]
					n_machine = self.Tmachine[i, lows:highs].tolist()
					n_time = self.Tmachinetime[i, lows:highs].tolist()
					if(r<0.6):


						new_time_index=n_time.index(min(n_time))
						new_machine_index=new_time_index

		# 				修改

						M[op_index]=n_machine[new_machine_index]
						T[op_index]=n_time[new_time_index]
					else:
						new_time_index = random.randint(0,len(n_time)-1)
						new_machine_index = new_time_index

						# 				修改

						M[op_index] = n_machine[new_machine_index]
						T[op_index] = n_time[new_time_index]
		return M,T

	def IPOX(self,chrom_L1,chrom_L2):       #工序的ipox交叉
		# print(chrom_L1)
		num=np.arange(self.job_num)
		np.random.shuffle(num)
		index=np.random.randint(0,len(num),1)[0]
		jpb_set1=num[:index+1]                  #固定不变的工件
		jpb_set2=num[index+1:]                  #按顺序读取的工件
		C1,C2=np.zeros((1,chrom_L1.shape[0]))-1,np.zeros((1,chrom_L1.shape[0]))-1
		sig,svg=[],[]
		# print(chrom_L1)
		for i in range(chrom_L1.shape[0]):#固定位置的工序不变
			ii,iii=0,0
			for j in range(len(jpb_set1)):
				# print(chrom_L1[i])
				# print(jpb_set1[j])
				if(chrom_L1[i]==jpb_set1[j]):
					C1[0,i]=chrom_L1[i]
				else:
					ii+=1
				if(chrom_L2[i]==jpb_set1[j]):
					C2[0,i]=chrom_L2[i]
				else:
					iii+=1
			if(ii==len(jpb_set1)):
				sig.append(chrom_L1[i])
			if(iii==len(jpb_set1)):
				svg.append(chrom_L2[i])
		signal1,signal2=0,0             #为-1的地方按顺序添加工序编码
		for i in range(chrom_L1.shape[0]):
			if(C1[0,i]==-1):
				C1[0,i]=svg[signal1]
				signal1+=1
			if(C2[0,i]==-1):
				C2[0,i]=sig[signal2]
				signal2+=1
		return C1[0],C2[0]

	def MX(self,WS):
		WS_X=np.zeros((self.job_num,len(self.work)),dtype=int)
		WS_X[:]=-1
		for i in range(len(WS)):
			W=WS[i]
			for j in range(len(self.work)):
				if(W[j]==i):
					WS_X[i][j]=W[j]

		for i in range(0,len(WS)-1):
			j=i+1
			W = [x for x in WS[i] if x != j]
			W_X=WS_X[j]
			l = 0
			for k in range(len(self.work)):
				if(W_X[k] != j):
					if(W[l]!=j) and (l < len(W)):
						W_X[k] = W[l]
						l = l+1
			WS_X[j]=W_X
		W = [x for x in WS[-1] if x != 0]
		W_X = WS_X[0]
		l = 0
		j=0
		for k in range(len(self.work)):
			if (W_X[k] != j) :
				if (W[l] != j) and (l < len(W)):
					W_X[k] = W[l]
					l = l + 1
		WS_X[0] = W_X
		return WS_X




	def ma_cross(self,m1,t1,m2,t2):  #机器嵌合交叉
		MC1,MC2,TC1,TC2=[],[],[],[]
		for i in range(len(m1[0])):
			index=np.random.randint(0,2,1)[0]
			if(index==0):  #为0时继承父代的机器选择
				MC1.append(m1[0][i]),MC2.append(m2[0][i]),TC1.append(t1[0][i]),TC2.append(t2[0][i]);
			else:                #为1时继承另一个父代的加工机器选择
				MC2.append(m1[0][i]),MC1.append(m2[0][i]),TC2.append(t1[0][i]),TC1.append(t2[0][i]);
		return MC1,TC1,MC2,TC2
	def select(self,work_job,work_M,work_T,answer):    #轮盘赌选择
		fit=[]
		index=[]
		for i in range(len(answer)):
			fit.append(1/(1+answer[i]))
			index.append(i)
		chose_index=random.choices(index,weights=fit,k=len(answer))
		new_answer=[]
		new_work_job=[]
		new_work_M=[]
		new_work_T=[]

		for i in range(len(answer)):
			index=chose_index[i]
			new_answer.append(answer[index])
			new_work_job.append(work_job[index])
			new_work_M.append(work_M[index])
			new_work_T.append(work_T[index])
		new_work_job=np.array(new_work_job)
		new_work_M=np.array(new_work_M)
		new_work_T=np.array(new_work_T)
		return new_work_job,new_work_M,new_work_T,new_answer

	def uniform_machine_cross(self,m1,t1,m2,t2):
		for i in range(len(m1)):
			r=random.random()
			if(r<0.6):
				temp=m1[i]
				m1[i]=m2[i]
				m2[i]=temp

				temp=t1[i]
				t1[i]=t2[i]
				t2[i]=temp

		return m1,t1,m2,t2
	def twomachine_cross(self,m1,t1,m2,t2):
		index1=[]
		index1.append(random.randint(0,len(m1)-5))
		index1.append(index1[0]+2)


		temp_m=np.copy(m1)
		temp_t=np.copy(t1)
		for i in range(index1[0],index1[1]+1):
			m1[i]=m2[i]
			t1[i]=t2[i]

		for i in range(index1[0],index1[1]+1):
			m2[i]=temp_m[i]
			t2[i]=temp_t[i]

		return m1,t1,m2,t2
	def Job_vara(self,W1):       #工序的逆序变异(大步长)
		index1=random.sample(range(W1.shape[0]),2)
		index1.sort()
		L1=W1[index1[0]:index1[1]+1]
		W_all=W1.copy()
		for i in range(L1.shape[0]):
			W_all[index1[0]+i]=L1[L1.shape[0]-1-i]  #反向读取工序编码
		return W_all
	def mutation_W(self,W): #两点交叉(小步长)
		location=random.sample(range(W.shape[0]),2)
		W[location[0]],W[location[1]]=W[location[1]],W[location[0]]
		return W

	def insert_W(self, W):
		location = random.sample(range(W.shape[0]), 2)
		data_to_insert = W[location[0]]  # 获取要插入的数据
		W = np.delete(W, location[0], axis=0)  # 删除要插入的数据
		W = np.insert(W, location[1], data_to_insert, axis=0)  # 将数据插入到指定位置
		return W

	def ma_mul(self,W,M,T):

		index=np.random.randint(self.job_num)

		while(self.machines[index]==0):
			index = np.random.randint(self.job_num)

		sig=np.random.randint(self.machines[index])
		#读取工序的可加工机器和工序
		highs=self.tom[index][sig]
		lows=self.tom[index][sig]-self.tdx[index][sig]
		n_machine=self.Tmachine[index,lows:highs].tolist()
		n_time=self.Tmachinetime[index,lows:highs].tolist()
		loc=0
		for i in range(0,index):
			loc=loc+self.machines[i]
		loc=loc+sig
		index=np.random.randint(0,len(n_time),1)  #随机选择加工机器
		M[loc]=n_machine[index[0]]              #更新编码
		T[loc]=n_time[index[0]]

		return M,T
	def search(self,W,M,T,W2,M2,T2,scores):       						#侦查蜂操作
		# 更新：实现ANS
		# 代表算子得分，0 insert_W，1 mutation_W，2 Job_vara

		# 总得分
		score_sum=sum(scores)

		# 计算概率
		probability=[]
		for score in scores:
			probability.append(score/score_sum)
		answer,_,_,_,_=self.to.caculate(W,M,T)
		answer2,_,_,_,_=self.to.caculate(W2,M2,T2)
		# # 选择的算子索引记录
		# i=0
		for i in range(self.limit):                    #搜索次数
			# 计算选择概率
			p=random.random()
			if(p<probability[0]):
				W=self.insert_W(W)
				op_index=0
			elif(p>=probability[0] and p<probability[1]):
				W=self.mutation_W(W)
				op_index=1
			else:
				W=self.Job_vara(W)
				op_index=2


			C_finish,_,_,_,_=self.to.caculate(W,M,T)
			if C_finish<answer:
				scores[op_index]+=0.3
			else:
				if(C_finish>answer):
					scores[op_index]-=0.5
				else:
					scores[op_index] += 0.1

			r=random.random()
			if(r<0.7):
				M,T,M2,T2=self.uniform_machine_cross(M,T,M2,T2)
			else:
				M, T, M2, T2 = self.twomachine_cross(M, T, M2, T2)
			# M,T,M2,T2=self.uniform_machine_cross(M,T,M2,T2)

			C_finish1,_,_,_,_=self.to.caculate(W,M,T)
			C_finish2, _, _, _, _ = self.to.caculate(W2, M2, T2)
			if C_finish1 < answer :
				return W, M, T,W2,M2,T2,C_finish1,C_finish2

		#如果大于20次，按上面的方法生成一个新的
		W,M,T=self.to.creat_job()
		C_finish1,_,_,_,_=self.to.caculate(W,M,T)
		C_finish2, _, _, _, _ = self.to.caculate(W2, M2, T2)
		return  W, M, T,W2, M2, T2, C_finish1,C_finish2


	def insertJobs(self,insertTime,C_finish,list_M,list_S,list_W,planJobs):
		# 同时也要对已经安排好的计划进行处理
		# 获取总的工序数量
		opertionNums=len(list_M)
		# 记录已经执行的工件的工序数
		count = np.zeros((1, self.job_num), dtype=int)
		# 记录机器的完工时间
		machine_end=np.zeros((1, self.machine_num))
		machine_end[0,:]=insertTime
		# 记录工件的上一次完工时间
		job_end=np.zeros((1, self.job_num))
		job_end[0,:]=insertTime
		# 这里仅考虑在运行时间内
		if(insertTime<C_finish):
			for i in range(opertionNums):
				if(list_S[i]<insertTime):
					count[0][int(planJobs[i])] += 1
					if(list_S[i]+list_W[i]>insertTime):
			# 			如果没有就记录当前机器的执行完成时间，按照编号存储
						machine_end[0][list_M[i]-1]=list_S[i]+list_W[i]
		# 				同时也记录工件的完工时间
						job_end[0][int(planJobs[i])]=list_S[i]+list_W[i]
				else:
					planJobs[i]=-1
		return count,machine_end,job_end,planJobs

	def machineBreak(self,breakNum,breakTime,breakLen,C_finish,list_M,list_S,list_W,planJobs):
		breakEnd=breakTime+breakLen
		# 同时也要对已经安排好的计划进行处理
		# 获取总的工序数量
		opertionNums=len(list_M)
		# 记录已经执行的工件的工序数
		count = np.zeros((1, self.job_num), dtype=int)
		# 记录机器的完工时间
		machine_end=np.zeros((1, self.machine_num))
		# 记录工件的上一次完工时间
		job_end=np.zeros((1, self.job_num))
		# 记录机器空闲时间
		rest=[]
		for j in range(self.machine_num):
			rest.append([])
		# 这里仅考虑在运行时间内
		if(breakTime<C_finish):
			for i in range(opertionNums):
				if(list_S[i]<breakTime):
					if(list_S[i]+list_W[i]>breakTime and list_M[i]==breakNum):
					# 	取消加工
						planJobs[i] = -1
						continue
					job_index=int(planJobs[i])
					count[0][job_index]+=1
					machine_end[0][list_M[i] - 1] = max(list_S[i] + list_W[i],machine_end[0][list_M[i] - 1])
					job_end[0][job_index] = max(list_S[i] + list_W[i],job_end[0][job_index])
				else:
					planJobs[i]=-1

		# if(machine_end[0][breakNum-1]<breakTime):
		# 	rest[breakNum-1].append([machine_end[0][breakNum-1],breakTime])
		machine_end[0][breakNum - 1]=breakEnd


		return count,machine_end,job_end,planJobs,rest

	def cancelJob(self,jobNum,cancelTime,C_finish,list_M,list_S,list_W,planJobs):
		# 同时也要对已经安排好的计划进行处理
		# 获取总的工序数量
		opertionNums=len(list_M)
		# 记录已经执行的工件的工序数
		count = np.zeros((1, self.job_num), dtype=int)
		# 记录机器的完工时间
		machine_end=np.zeros((1, self.machine_num))
		# 记录工件的上一次完工时间
		job_end=np.zeros((1, self.job_num))
		# 这里仅考虑在运行时间内
		if(cancelTime<C_finish):
			for i in range(opertionNums):
				if(list_S[i]<cancelTime):
					# if(int(planJobs[i])==jobNum):
					# 	machine_end[0][list_M[i] - 1]=cancelTime
					# 	continue
					count[0][int(planJobs[i])] += 1
		# 			如果没有就记录当前机器的执行完成时间，按照编号存储
					machine_end[0][list_M[i]-1]=max(list_S[i]+list_W[i],machine_end[0][list_M[i]-1])
	# 				同时也记录工件的完工时间
					job_end[0][int(planJobs[i])]=max(list_S[i]+list_W[i],job_end[0][int(planJobs[i])])
				else:
					planJobs[i]=-1

		count[0][jobNum]=self.machines[jobNum]
		return count,machine_end,job_end,planJobs

	def gabc(self):
		answer=[]
		result=[]
		work_job=np.zeros((self.popsize,len(self.work)))
		work_M=np.zeros((self.popsize,len(self.work)))
		work_T=np.zeros((self.popsize,len(self.work)))
		pre_best_index = 0  # 最优个体的索引
		pre_best_answer = 1000
		pre_best_index_job = []
		pre_best_index_M = []
		pre_best_index_T = []
		for gen in range(self.generation):
			if(gen<1):                      #第一次生成多个可行的工序编码，机器编码，时间编码
				for i in range(self.popsize):
					job,machine,machine_time=self.to.creat_job()
					C_finish,_,_,_,_=self.to.caculate(job,machine,machine_time)
					answer.append(C_finish)
					work_job[i]=job
					work_M[i]=machine
					work_T[i]=machine_time

			# best_index=answer.index(min(answer))
			#
			# for i in range(len(answer)):
			# 	W1,M1,T1=np.copy(work_job[i]),np.copy(work_M[i]),np.copy(work_T[i])
			# 	if np.random.rand()<0.5:                   #另一个工序串是全局最优
			# 		index=best_index
			#
			# 	else:                                      #另一个工序串是随机选择且与原工序串不同
			# 		a=np.arange(i)
			# 		b=np.arange(i+1,len(answer),1)
			# 		c=np.hstack((a,b))
			# 		index=np.random.choice(c,1)[0]
			# 	W2,M2,T2=np.copy(work_job[index]),np.copy(work_M[index]),np.copy(work_T[index])
			# 	W1,W2=self.IPOX(W1,W2)                 #工序交叉
			#
			# 	C_finish,_,_,_,_=self.to.caculate(W1,M1,T1)
			# 	if C_finish<answer[i]:                     #完工时间比父代短就替换
			# 		work_job[i]=W1
			# 		answer[i]=C_finish

			# 新增代码:多父代交叉
			answer_indexs=[random.randint(0, len(answer) - 1) for _ in range(self.job_num)]
			WS=[]
			for index in answer_indexs:
				WS.append(np.copy(work_job[index]))
			WS_X=self.MX(WS)
			for i in range(self.job_num):
				C_finish,_,_,_,_=self.to.caculate(WS_X[i],work_M[answer_indexs[i]],work_T[answer_indexs[i]])
				if C_finish<answer[answer_indexs[i]]:                     #完工时间比父代短就替换
					work_job[answer_indexs[i]]=WS_X[i]
					answer[answer_indexs[i]]=C_finish

			# 检查最优个体


			# 对每个个体缩短最大加工时间
			for i in range(self.popsize):
				for j in range(1):
					job, machine, machine_time = np.copy(work_job[i]), np.copy(work_M[i]), np.copy(work_T[i])
					C_finish, _, _, _, tmax = self.to.caculate(job, machine, machine_time)
					# 获取最长加工时间的机器

					# 为该机器上加工的每个工序寻找更短加工时间的机器
					machine, machine_time = self.change_to_min(tmax, machine, machine_time)

					# 	更新时间
					C_finish, _, _, _, _ = self.to.caculate(job, machine, machine_time)
					if (C_finish < answer[i]):
						work_job[i], work_M[i], work_T[i] = job, machine, machine_time
						answer[i] = C_finish
						break
			# 		work_job[i], work_M[i], work_T[i]=job, machine, machine_time
			# 		answer[i]=C_finish



			for i in range(0,self.popsize,2):    			 #种群规模下每次选2个个体
				W1,M1,T1=work_job[i:i+1],work_M[i:i+1],work_T[i:i+1]

				W2,M2,T2=work_job[i+1:i+2],work_M[i+1:i+2],work_T[i+1:i+2]
				# W2, M2, T2 = [best_index_job],[best_index_M],[best_index_T]
				new_M1,new_T1,new_M2,new_T2=self.ma_cross(np.copy(M1),np.copy(T1),np.copy(M2),np.copy(T2))      #机器嵌合交叉
				C_finish,_,_,_,_=self.to.caculate(W1[0],new_M1,new_T1)
				# answer[i] = C_finish
				if C_finish<answer[i]:                     #完工时间比父代短就替换
					work_M[i]=new_M1
					work_T[i]=new_T1
					answer[i]=C_finish
				C_finish,_,_,_,_=self.to.caculate(W2[0],new_M2,new_T2)
				# answer[i+1] = C_finish
				if C_finish<answer[i+1]:                     #完工时间比父代短就替换
					work_M[i]=new_M2
					work_T[i]=new_T2
					answer[i]=C_finish


			best_index = answer.index(min(answer))  # 最优个体的索引
			best_answer=answer[best_index]
			best_index_job=np.copy(work_job[best_index])
			best_index_M=np.copy(work_M[best_index])
			best_index_T=np.copy(work_T[best_index])

			work_job,work_M,work_T,answer=self.select(work_job,work_M,work_T,answer)#轮盘赌选择

			# 避免丢失最优个体
			for index in range(len(answer)):
				if (answer[index] == best_answer):
					break
				if(answer[index]>best_answer):
					answer[index]=best_answer
					work_job[index]=best_index_job
					work_M[index]=best_index_M
					work_T[index]=best_index_T
					best_index=index
					break


			# 侦察蜂阶段
			scores = [1, 1, 1]
			for i in range(len(answer)):

				if(sum(scores)==0):
					scores = [1, 1, 1]
				if(i!=best_index):
					W1,M1,T1=np.copy(work_job[i]),np.copy(work_M[i]),np.copy(work_T[i])
					W2,M2,T2=np.copy(best_index_job),np.copy(best_index_M),np.copy(best_index_T)
					# W2, M2, T2 =self.to.creat_job()
					W1,M1,T1,W2,M2,T2,C_finish1,C_finish2=self.search(W1,M1,T1,W2,M2,T2,scores)
					work_job[i]=W1
					work_M[i]=M1
					work_T[i]=T1
					answer[i]=C_finish1

				# work_job[best_index]=W2
				# work_M[best_index]=M2
				# work_T[best_index]=T2
				# answer[best_index]=C_finish2

			# for i in range(self.popsize):
			# 	C_finish,_,_,_,_=self.to.caculate(work_job[i],work_M[i],work_T[i])
			# 	if(C_finish!=answer[i]):
			# 		print('********{}*****'.format(gen))
			# 		print(C_finish)
			# 		print(answer[i])
			# 		print('wrong')
			# if(min(answer)<pre_best_answer):
			#
			# 	pre_best_index = answer.index(min(answer))  # 最优个体的索引
			# 	pre_best_answer = answer[pre_best_index]
			# 	pre_best_index_job = np.copy(work_job[pre_best_index])
			# 	pre_best_index_M = np.copy(work_M[pre_best_index])
			# 	pre_best_index_T = np.copy(work_T[pre_best_index])
			#
			# else:
			# 	pre_best_index=answer.index(max(answer))
			# 	answer[pre_best_index]=pre_best_answer
			# 	work_job[pre_best_index]=np.copy(pre_best_index_job)
			# 	work_M[pre_best_index]=np.copy(pre_best_index_M)
			# 	work_T[pre_best_index]=np.copy(pre_best_index_T)
			result.append([gen + 1, min(answer)])
			print(min(answer))
		# print('*********')
		result_index = answer.index(min(answer))
		# print(answer[result_index])
		C_finish=self.to.caculate(work_job[result_index],work_M[result_index],work_T[result_index])
		# print(C_finish)
		return work_job[result_index],work_M[result_index],work_T[result_index],result
				

