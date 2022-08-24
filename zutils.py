#/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
from shutil import copyfile
import tkinter # apt intall python3-tk
from tkinter import messagebox

TERMINAL = True
 
class Zutil():
	def __init__(self,val):
		self.app=val
	
	def outText(self,text):
		if(TERMINAL):
			print(text+'')
		else:
			self.app.outtext.insert(tkinter.END,text+"\n")
			self.app.outtext.yview_pickplace("end")
		
	def sudo(self,cmd):

		p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True, shell = True)
		p.poll()

		while True:
			line = p.stdout.readline()
			self.app.outtext.insert(tkinter.END,line)
			self.app.outtext.see(tkinter.END)
			if not line and p.poll is not None: break

		while True:
			err = p.stderr.readline()
			self.app.outtext.insert(tkinter.END, err)
			self.app.outtext.see(tkinter.END)
			if not err and p.poll is not None: break
		
	def execute(self,command):
		cmd = command.split(' ');
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		out, err = p.communicate()
		#out,err = p.stdout.read()
		out = str(out)
		return out
	
	def misturarPastas(self,orig,dest):
		self.outText('Misturando pastas: '+orig+' e '+ dest)
		self.execute('meld '+orig+' '+dest)
		
	def diferenciarArquivos(self,a1,a2):		
		
		if not self.arquivoExiste(a2):
			self.criaCopia(a1,a2)
		elif not self.arquivoExiste(a1):
			self.criaCopia(a2,a1)
		else:
			cmd = 'cmp '+a1+' '+a2
			print(cmd)
			out = self.execute(cmd)		
			if(out != ''):
				self.outText('DIFERENTES ')
				print(out)
				self.outText(out)
				self.outText('---- ---- ---- ----')
				self.misturarPastas(a1,a2)
			else:
				self.outText('IGUAIS ')				
			
	def diferenciarArquivosOLD(self,a1,a2):		
		exclude_for_dirs = '--exclude=".svn" '
		exclude_for_dirs += '--exclude="log" '
		exclude_for_dirs += '--exclude="upload" '
		exclude_for_dirs += '--exclude="arquivos_Pdfs" '
		exclude_for_dirs += '--exclude="fotos_func" '
		
		cmd = 'diff -y --suppress-common-lines '+exclude_for_dirs+' '+a1+' '+a2
		out = self.execute('diff -y --suppress-common-lines '+exclude_for_dirs+' '+a1+' '+a2)
		if(out != ''):
			self.outText('DIFERENTES ')
			self.outText(out)
			self.outText('---- ---- ---- ----')
			self.misturarPastas(a1,a2)
		else:
			self.outText('IGUAIS ')	
			print(cmd)
	
	def criaCopia(self,orig,dest):
		directory = dest.split('/')
		directory.pop();
		folder = '/'.join(directory);
		exists2 = os.path.isdir(folder)
		if not exists2:							
			textoMensagem = folder+' É pasta, criar?'
			self.outText(textoMensagem)
			
			if(TERMINAL):
				print(textoMensagem+' (s/n)[n]')
				input1 = input() 
				if(input1 == 's'):
					copiar = True
				else:
					copiar = False
			else:
				copiar = messagebox.askyesno(title='Copiar',message=textoMensagem)
			
			
			if(copiar):
				self.outText('Sim, criando pasta...')
				os.mkdir(folder)
			else:
				self.outText('Não')						

		exists3 = os.path.isfile(orig)
		if exists3:
			textoMensagem = dest+' É arquivo, copiar?'
			self.outText(textoMensagem)
			
			if(TERMINAL):
				print(textoMensagem+' (s/n)[n]')
				input1 = input() 
				if(input1 == 's'):
					copiar = True
				else:
					copiar = False
			else:
				copiar = messagebox.askyesno(title='Copiar',message=textoMensagem)
								
			if(copiar):
				self.outText('Sim, copiando')
				copyfile(orig,dest);
			else:
				self.outText('Não')
	
	def getFileContents(self,fileName,splitChar):
		f = open(fileName, "r")
		if f.mode != 'r':
			quit("Oy! "+fileName)

		contents = f.read()
		f.close()
		return contents.split(splitChar)
		
	def getThisFolder(self):
		# A pasta onde tá
		folder = os.path.realpath(__file__);
		folderList = folder.split('/')
		folderList.pop();
		folder = '/'.join(folderList) + '/';
		return folder
		
	def comparaPastas(self,fulpath1,fulpath2):
		
		existsDIR = self.pastaExiste(fulpath1)
		existsFILE = self.arquivoExiste(fulpath1)
		prosseguir = False
		if existsDIR:
			exists2 = self.pastaExiste(fulpath2)
			prosseguir = True
		elif existsFILE:
			exists2 = self.arquivoExiste(fulpath2)
			prosseguir = True
		else:
			self.outText('Não Existe origem: '+fulpath1)
				
		if prosseguir:			
			if exists2:
				self.outText('Existe, comparar ')
				if existsFILE:
					self.outText('FILE...')
					self.diferenciarArquivos(fulpath1,fulpath2)
				elif existsDIR:
					self.outText('DIR...')
					self.misturarPastas(fulpath1,fulpath2)					
			else:
				self.outText('Nao Existe, copiar...'+'\n\t'+fulpath1+'\n\t'+fulpath2)
				self.criaCopia(fulpath1,fulpath2)
		else:
			self.outText('Inverter origem e destino: ')
			self.comparaPastas(fulpath2,fulpath1)
		
	def testaCopia(self,path1,path2):
		exists = self.arquivoExiste(path2)
		if not exists:
			self.outText('Não Existe')
			self.criaCopia(path1,path2)
	
	def pastaExiste(self,path):
		return os.path.isdir(path)
		
	def arquivoExiste(self,path):
		return os.path.isfile(path)
	
	def existe(self,path):
		if self.pastaExiste(path):
			return True
		elif self.arquivoExiste(path):
			return True
		return False
