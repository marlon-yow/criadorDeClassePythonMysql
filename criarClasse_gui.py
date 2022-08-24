#/usr/bin/python
# -*- coding: utf-8 -*-


## TODO: na pasta, no namespace, botão abrir pastas
## criar entidade
## sql criar SEQ

import os
import sys
import tkinter # apt install python3-tk
from tkinter import messagebox
from threading import Thread
import tkinter.filedialog

from zutils import Zutil
from funcoesExtracao import FunExtract
from funcoesEscrita import FunClass
from funcoesEscritaEntidade import FEE

class Principal():
	def __init__(self):
		
		self.t = "    "
		
		mainWindow = tkinter.Tk()
		mainWindow.geometry("850x570")
		# - TITULO
		titulo = tkinter.StringVar()
		label = tkinter.Label( mainWindow, textvariable = titulo)
		titulo.set("Criar Classe")
		label.pack()
		
		###
		### FRAME LEFT
		###
		
		self.FrameLeft = tkinter.Frame(mainWindow)
		
		self.F5 = tkinter.Frame(self.FrameLeft)
		self.L5 = tkinter.Label(self.F5, text="Copie o SQL de criação da tabela aqui")		
		self.L5.pack(side = tkinter.LEFT)	
		self.B2 = tkinter.Button(self.F5, text="Processar", command = self.processarSql)		
		self.B2.pack(side = tkinter.LEFT)
		
		self.F5.pack(side="top",fill="x",padx=10, pady=10)
		
		self.FrameSql = tkinter.Frame(self.FrameLeft)
		self.EntrySql = tkinter.Text(self.FrameSql, height = 60, width = 50)
		self.EntrySql.pack()
		self.FrameSql.pack(side="top",fill="x",padx=10, pady=10)
				
		
		###
		### FRAME RIGHT
		###
		
		self.FrameRight = tkinter.Frame(mainWindow)
		
		
		self.FrameCkecks = tkinter.Frame(self.FrameRight)
		
		self.usarNamespace = tkinter.IntVar()
		self.usarNamespace.set(1)
		self.CKNamespace = tkinter.Checkbutton(self.FrameCkecks, text='Usar Namespace',variable=self.usarNamespace, onvalue=1, offvalue=0,command=self.showHideNamespace)
		self.CKNamespace.pack()
		
		self.skeleton = tkinter.IntVar()
		self.skeleton.set(0)
		self.CKSkeleton = tkinter.Checkbutton(self.FrameCkecks, text='Usar Skeleton',variable=self.skeleton, onvalue=1, offvalue=0)
		self.CKSkeleton.pack()
		
		self.skeletonV2 = tkinter.IntVar()
		self.skeletonV2.set(1)
		self.CKSkeletonV2 = tkinter.Checkbutton(self.FrameCkecks, text='Usar SkeletonV2',variable=self.skeletonV2, onvalue=1, offvalue=0)
		self.CKSkeletonV2.pack()
		
		self.entidade = tkinter.IntVar()
		self.entidade.set(1)
		self.CKEntidade = tkinter.Checkbutton(self.FrameCkecks, text='Criar Entidade',variable=self.entidade, onvalue=1, offvalue=0)
		self.CKEntidade.pack()
		
		self.entidadeSk = tkinter.IntVar()
		self.entidadeSk.set(1)
		self.CKEntidadeSk = tkinter.Checkbutton(self.FrameCkecks, text='Usar Entidade Esqueleto',variable=self.entidadeSk, onvalue=1, offvalue=0)
		self.CKEntidadeSk.pack()
		
		self.service = tkinter.IntVar()
		self.service.set(1)
		self.CKService = tkinter.Checkbutton(self.FrameCkecks, text='Add Service no nome',variable=self.service, onvalue=1, offvalue=0)
		self.CKService.pack()
		
		self.FrameCkecks.pack()
		
		self.FrameNamespace = tkinter.Frame(self.FrameRight)
		self.BtnOpen = tkinter.Button(self.FrameNamespace,text='Namespace', command=self.escolherPasta,width=10)
		self.BtnOpen.pack(side = tkinter.LEFT)
		self.EntryNamespace = tkinter.Entry(self.FrameNamespace)
		self.EntryNamespace.pack(side = tkinter.RIGHT)
		self.FrameNamespace.pack(side="top",fill="x",padx=10, pady=10)
		
		
		self.FrameTabela = tkinter.Frame(self.FrameRight)
		self.L21 = tkinter.Label(self.FrameTabela, text="Tabela")		
		#self.L21 = tkinter.Button(self.FrameTabela, text="Tabela", command = self.criarTabela)		
		self.L21.pack(side = tkinter.LEFT)
		self.EntryTabela = tkinter.Entry(self.FrameTabela)
		self.EntryTabela.pack(side = tkinter.RIGHT)
		self.FrameTabela.pack(side="top",fill="x",padx=10, pady=10)
		
		self.FrameAlias = tkinter.Frame(self.FrameRight)		
		self.BtnAlias = tkinter.Button(self.FrameAlias, text="Alias", command = self.criarAlias)		
		self.BtnAlias.pack(side = tkinter.LEFT)
		self.EntryAlias = tkinter.Entry(self.FrameAlias)
		self.EntryAlias.pack(side = tkinter.RIGHT)
		self.FrameAlias.pack(side="top",fill="x",padx=10, pady=10)
		
		self.FramePrimaryKey = tkinter.Frame(self.FrameRight)
		self.L22 = tkinter.Label(self.FramePrimaryKey, text="Primary Key")				
		self.L22.pack(side = tkinter.LEFT)
		self.EntryPrimaryKey = tkinter.Entry(self.FramePrimaryKey)
		self.EntryPrimaryKey.pack(side = tkinter.RIGHT)
		self.FramePrimaryKey.pack(side="top",fill="x",padx=10, pady=10)
				
		self.FrameClasse = tkinter.Frame(self.FrameRight)
		#self.L2 = tkinter.Label(self.FrameClasse, text="Classe")
		self.L2 = tkinter.Button(self.FrameClasse, text="Classe", command = self.criarNomeClasse)		
		self.L2.pack(side = tkinter.LEFT)
		self.EntryClasse = tkinter.Entry(self.FrameClasse)
		self.EntryClasse.pack(side = tkinter.RIGHT)
		self.FrameClasse.pack(side="top",fill="x",padx=10, pady=10)
		
		#self.FrameSequencia = tkinter.Frame(self.FrameRight)		
		#self.L3 = tkinter.Button(self.FrameSequencia, text="Sequencia", command = self.criarNomeSeq)		
		#self.L3.pack(side = tkinter.LEFT)
		#self.EntrySequencia = tkinter.Entry(self.FrameSequencia)
		#self.EntrySequencia.pack(side = tkinter.RIGHT)
		#self.FrameSequencia.pack(side="top",fill="x",padx=10, pady=10)
		
		self.FrameEntidade = tkinter.Frame(self.FrameRight)
		#self.L4 = tkinter.Label(self.FrameEntidade, text="Entidade")
		self.L4 = tkinter.Button(self.FrameEntidade, text="Entidade", command = self.criarNomeEnt)		
		self.L4.pack(side = tkinter.LEFT)
		self.EntryEntidade = tkinter.Entry(self.FrameEntidade)
		self.EntryEntidade.pack(side = tkinter.RIGHT)
		self.FrameEntidade.pack(side="top",fill="x",padx=10, pady=10)
		
		self.F41 = tkinter.Frame(self.FrameRight)		
		self.L31 = tkinter.Label(self.F41, text="CAMPOS")		
		self.L31.pack(side = tkinter.LEFT)		
		B1 = tkinter.Button(self.F41, text = "Iniciar", command = self.iniciar)
		B1.pack(side = tkinter.RIGHT)
		self.F41.pack(side="top",fill="x",padx=10, pady=10)
		
		#self.FrameSequenciaSQL = tkinter.Frame(self.FrameRight)		
		#self.E31 = tkinter.Entry(self.FrameSequenciaSQL)
		#self.E31 = tkinter.Text(self.FrameSequenciaSQL, height = 20, width = 50)
		#self.E31.pack(side = tkinter.RIGHT)		
		#self.FrameSequenciaSQL.pack(side="top",fill=None,padx=10, pady=10)
		
		self.F6 = tkinter.Frame(self.FrameRight)
		self.E6 = tkinter.Text(self.F6, height = 60, width = 50)
		self.E6.pack()
		self.F6.pack(side="top",fill="x",padx=10, pady=10)
		
		
		
		##
		## FRAME BOTTOM
		##
		
		self.FrameBottom = tkinter.Frame(mainWindow)
		
		FBTN = tkinter.Frame(self.FrameBottom)
		FBTN.pack(side="top",fill="x",padx=10, pady=10)
		
				
		##
		## FIM
		##
		
		self.zz = Zutil(self)
		self.fc = FunClass(self)
		self.FunExtract = FunExtract(self)
		self.fee = FEE(self);
		
		
		self.FrameLeft.pack(side = tkinter.LEFT, fill='y',padx=10, pady=10)
		self.FrameRight.pack(side = tkinter.LEFT, fill='y',padx=10, pady=10)		
		self.FrameBottom.pack(side = tkinter.LEFT, fill='x',padx=10, pady=10)		
		
		mainWindow.mainloop()

		
		#self.zz.outText('Sincronizacao Iniciada')
	
	def processarSql(self):
		linhas = self.EntrySql.get("1.0", "end-1c")
		Lines = linhas.split('\n')
		
		#limpar classe, entidade e campos
		self.EntryClasse.delete(0, 'end')
		self.EntryEntidade.delete(0, 'end')
		self.EntryAlias.delete(0, 'end')
		#self.E6.delete(0, 'end')
		
		for l in Lines:
			print(l)
			arr = l.split(' ')
			print(arr)
			try:
				if (arr[0] == "CREATE"):
					if(arr[1] == "TABLE"):
						self.EntryTabela.delete(0, 'end')
						self.EntryTabela.insert(0,arr[2].replace('`',''))
				elif(arr[0] == ""):
					if(arr[1] == ""):
						if(arr[2] == "PRIMARY"):
							if(arr[3] == "KEY"):
								self.EntryPrimaryKey.delete(0, 'end')
								self.EntryPrimaryKey.insert(0,arr[4].replace('`','').replace('(','').replace(')',''))
						else:						
							self.E6.insert("end-1c",arr[2].replace('`','')+'\t'+arr[3]+'\n')
			except IndexError:
				pass
	
	def criarAlias(self):
		tabela = self.EntryTabela.get()
		alias = ''
		arr = tabela.split('_')
		for n in arr:
			alias += n[0:2]
			
		print("alias:")
		print(alias)
		
		self.EntryAlias.delete(0, 'end')
		self.EntryAlias.insert(0,alias)
		
	def criarNomeClasse(self):		
		classe = self.EntryClasse.get()
		if(classe == ''):
			tabela = self.EntryTabela.get()
			classe = tabela
		
		arr = classe.split('_')
		classe = ''
		for n in arr:
			classe += str.capitalize(n)
		
		ckService = self.service.get()		
		if(ckService):
			arr = classe.split('_')
			if(len(arr) > 1 or arr[-1] != 'SERVICE'):				
				classe = classe+"_SERVICE"
				
		print("classe:")
		print(classe)
		
		self.EntryClasse.delete(0, 'end')
		self.EntryClasse.insert(0,classe)
		
	def criarNomeEnt(self):
		entidade = self.EntryEntidade.get()
		if(entidade == ''):			
			tabela = self.EntryTabela.get()
			entidade = tabela
			
		arr = entidade.split('_')
		entidade = ''
		for n in arr:
			entidade += str.capitalize(n)
			
		ckEntidade = self.entidade.get()
		if(ckEntidade):
			arr = entidade.split('_')
			if(len(arr) > 1 or arr[-1] != 'ENTITY'):				
				entidade = entidade+"_ENTITY"
		
		print("Ent:")
		print(entidade)
		
		self.EntryEntidade.delete(0, 'end')
		self.EntryEntidade.insert(0,entidade)
	
	def showHideNamespace(self):
		ckNamespace = self.usarNamespace.get()
		if(ckNamespace):
			self.FrameNamespace.pack()			
		else:
			self.FrameNamespace.pack_forget()
	
	def escolherPasta(self):
		startPath = os.path.expanduser('~')+'/Downloads/CATALISE-MOUNT/serverHttp/DESENVOLVIMENTO/classes/'
		self.filePath = tkinter.filedialog.askdirectory(initialdir=startPath)
		print(self.filePath)
		
		namespace = self.filePath.replace(startPath,'').replace('/','\\')
		print(namespace)
		self.EntryNamespace.delete(0, 'end')
		self.EntryNamespace.insert(0,namespace)
		
	def iniciar(self):
		#recolher campos
		ckNamespace = self.usarNamespace.get()
		ckSkeleton = self.skeleton.get()
		ckSkeletonV2 = self.skeletonV2.get()
		ckEntidade = self.entidade.get()
		ckEntidadeSk = self.entidadeSk.get()
		ckService = self.service.get()		
		namespace = self.EntryNamespace.get().replace('/','\\')
		classe = self.EntryClasse.get()
		tabela = self.EntryTabela.get()
		alias = self.EntryAlias.get()
		primaryKey = self.EntryPrimaryKey.get()
		#sequencia = self.EntrySequencia.get()
		entidade = self.EntryEntidade.get()			
		linhas = self.E6.get("1.0", "end-1c")
		Lines = linhas.split('\n')
		fc = self.fc
		fee = self.fee
		# #
		escrever = True
		
		if(classe != ''):
			if(escrever):							
				fileOut = open(self.filePath+"/"+classe+'.php', 'w', encoding="UTF-8")
			
			resultado = self.FunExtract.processarLinhas(Lines)
			
			w = fc.cabecalhoService(ckNamespace,namespace,ckSkeleton,ckSkeletonV2,classe,ckEntidade,entidade)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)

			
			w = fc.criarConstruct(tabela,alias,primaryKey,entidade)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)
				
			w = fc.criarGetById(resultado.getById,ckEntidade)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)
			
			
			w = fc.criarFormatar(resultado.formata1,resultado.formata2)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)			

			w = fc.criarInserir(resultado.insere,resultado.insereV, resultado)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)

			w = fc.criarAtualizar(resultado.atualizar,primaryKey, resultado)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)
			
			w = fc.criarMakeselect(resultado.getById)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)
				
			w = fc.criarmakeWhere(resultado.makeWhere,resultado.excluido)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)
			
			w = fc.criarmakeOrder()
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)	
			
			w = fc.rodape(classe)
			if(escrever):
				fileOut.writelines(w)
			else:
				print(w)	
			
			if(escrever):
				fileOut.close()
			
			if(ckEntidade):
				if(escrever):
					fileEntity = open(self.filePath+"/"+entidade+'.php', 'w', encoding="UTF-8")
				
				w = fee.cabecalhoEntidade(ckNamespace,namespace,ckEntidadeSk,entidade)
				if(escrever):
					fileEntity.writelines(w)
				else:
					print(w)
				
				w = fee.criarCorpoEntidade(resultado.entidade,primaryKey)
				if(escrever):
					fileEntity.writelines(w)
				else:
					print(w)
				
				w = fee.rodapeEntidade()
				if(escrever):
					fileEntity.writelines(w)
				else:
					print(w)
				
				if(escrever):
					fileEntity.close()
			
			tkinter.messagebox.showinfo(title='Criar Classe', message='EU FIZ!')
			
			print("eu fiz")
		else:
			print("nome da classe não preenchido")
		
if __name__ == "__main__":
	app = Principal()
 
