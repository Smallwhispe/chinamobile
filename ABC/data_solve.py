
import numpy as np 
import pandas as pd

class data_deal:
	def __init__(self,job_num,machine_num,path):
		self.job_num=job_num
		self.machine_num=machine_num
	def read(self,path):
		# 读取excel文件,将excel文件转换为列表
		file=(path)
		df=pd.read_excel(file,0,index_col=0)
		row=df.shape[0]
		col=df.columns.size

		data=[]
		for i in range(row):
			data.append([])
			for j in range(col):
				signal=str(df.iloc[i,j])
				if signal=='nan' :
					break
				data[i].append(int(df.iloc[i,j]))
		return data
	def translate(self,tr1):
		# tr1为单个工件的工序说明
		sigdex,mac,mact,sdx=[],[],[],[]
		# 获取工序总数
		sigal=tr1[0]
		# 去除第一个元素
		tr1=tr1[1:len(tr1)+1]
		index=0
		for j in range(sigal):
			# 可处理该工序的机器数
			sig=tr1[index]
			sdx.append(sig)
			# 记录可用机器数量的位置
			sigdex.append(index)
			# 由于后续是设备号以及时间，所以是乘二
			index=index+1+2*sig
		# 删除机器的数量
		for ij in range(sigal):
			del tr1[sigdex[ij]-ij]
		for ii in range(0,len(tr1)-1,2):
			mac.append(tr1[ii])
			mact.append(tr1[ii+1])
		# 返回的是可用机器编号，对应时长，工序可用机器数量
		return mac,mact,sdx
	def widthxx(self,strt):
		widthx=[]
		for i in range(self.job_num):
			mac,mact,sdx=self.translate(strt[i])
			siga=len(mac)
			widthx.append(siga)
		width=max(widthx)
		return width
	def tcaculate(self,strt):
		# 工序可用机器的最大值
		width=self.widthxx(strt)
		Tmachine,Tmachinetime=np.zeros((self.job_num,width)),np.zeros((self.job_num,width))
		tdx=[]
		for i in range(self.job_num):
			# 可用机器编号，对应时长，工序可用机器数量
			mac,mact,sdx=self.translate(strt[i])
			tdx.append(sdx)
			siga=len(mac)
			# 对应到工件的需要机器的编号
			Tmachine[i,0:siga]=mac
			Tmachinetime[i,0:siga]=mact
		return Tmachine,Tmachinetime,tdx
	def cacu(self,strt):
		# 获取列表数据,改为参数获取
		# strt=self.read(self.path)
		# 按照工件序号从左到右
		# 需要机器的编号，机器对应的处理时间，工序可用机器数量
		Tmachine,Tmachinetime,tdx=self.tcaculate(strt)
		to,tom,work,machines=0,[],[],[]
		for i in range(self.job_num):
			to+=len(tdx[i])
			tim=[]
			for j in range(1,len(tdx[i])+1,1):
				tim.append(sum(tdx[i][0:j]))
				work.append(i)
			tom.append(tim)
			machines.append(len(tdx[i]))
		return Tmachine,Tmachinetime,tdx,work,tom,machines
		# 返回结果
		# 每个工件的工序对应机器编号
		# 每个工件的工序对应机器处理时间
		# 每个工序可加工的机器数
		# 工件工序数（按照编号）
		# 工序的叠加机器数
		# 工件工序数

	def insert(self,path,job_count,insert_path):
		# 获取原始数据
		data=self.read(path)
		# 更新已完成工件的工序信息
		for i in range(len(job_count[0])):
			finished_job_num = job_count[0][i]
			start=1
			# 如果已完成的工序大于0
			if(finished_job_num>0):
				data[i][0]-=finished_job_num
				for j in range(finished_job_num):
					machine_num=data[i][start]
					end=start+2*machine_num
					# 更新起点
					start=end+1

				del data[i][1:end + 1]
		# 读取插入工件信息
		if(insert_path!=''):
			insert_data = self.read(insert_path)

			for insert_item in insert_data:
				data.append(insert_item)
		# 更新工件数量
		self.job_num=len(data)
		return data
