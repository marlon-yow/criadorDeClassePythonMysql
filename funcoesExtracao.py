class Resultados:	
	getById = ""
	formata1 = ""
	formata2 = ""
	insereFirstElement=""
	insere = ""
	insereV = ""
	atualizar = ""
	makeWhere = ""
	entidade = ""
	prepare = {}
	excluido = False
	

class FunExtract():
	def __init__(self,val):
		self.app=val
		self.identacaoFuncao = "    "
		self.identacaoMiolo = "        "
		self.identacaoSQL = "                    "
		self.t = "    " 
		
		self.primeiro = True
		
		self.textoFormata1 = '';
		self.textoFormata2 = '';
		self.textoInsere = '';
		self.textoUpdate = '';
		self.textoWhere = '';
		self.textoEntidade = '';
		self.textoGetById = '';
		self.textoV = '';
		self.textoPrepare = {};
		
		
	#processar os dados da abela#
	def processarLinhas(self,Lines):
		retorno = Resultados()
		self.primeiro = True
		
		for line in Lines:

			if(len(line) > 1):				
				li = line.strip()
				li2 = li.split();

				print(li2)
				
				if(li2[0].lower() == 'excluido'):
					retorno.excluido = True
				else:
					self.textoGetById = li2[0]+","

					self.textoFormata1 = "$obj2->"+li2[0]+" = "
					self.textoFormata2 = "$obj2->"+li2[0]+" = "
					self.textoInsere = li2[0]+","
					self.textoUpdate = li2[0]+" = "
					self.textoWhere = self.identacaoMiolo+ "if($busca['"+li2[0]+"']){" +"\n"
					self.textoWhere += self.identacaoMiolo+ self.t +"if($where) $where .= \" AND \";" +"\n"
					self.textoEntidade = "$"+li2[0]+";"
					
					if(li2[1].lower() == 'datetime'):
						self.processarDateTime(li2)
					elif(li2[1].lower() == 'int'):
						self.processarInt(li2)										
					else:
						textoGet = li2[0]+","

						li3 = li2[1].split('(')
					
						try:
							#pegar só o numero de li[3] usando filter
							li3[0] = ''.join(filter(str.isalnum, li3[0]))
							li3[1] = ''.join(filter(str.isdigit,li3[1]))
						except IndexError:
							# Key is not present
							print('nao tratar li3[1]')
							pass
											
					
						if(li3[0].lower() == 'int'):
							self.processarInt(li2)						
						elif(li3[0].lower() == 'varchar'):
							self.processarVarchar(li2,li3)
						elif(li3[0].lower() == 'longtext'):
							self.processarLongtext(li2)
							
						#elif(li3[0] == 'LONG'):
						#	self.textoFormata1 += "intval($obj->"+li2[0]+");"
						#	self.textoFormata2 += "intval($obj['"+li2[0].lower()+"']);"
						#	self.textoUpdate += "$obj->"+li2[0]+","
						#	self.textoV = "$obj->"+li2[0]+","
						#	
						#	self.textoWhere += self.identacaoMiolo + self.t +"$where .= \" "+li2[0]+" = \".intval($busca['"+li2[0].lower()+"']).\" \";" +"\n"					
						#	self.textoWhere += self.identacaoMiolo +"}" +"\n"
						else:
							raise ValueError('A very specific bad thing happened. TIPO: '+li2[1]+' => '+li3[0]+' não tratado pelo codigo ainda.' )

					# GET BY ID
					if(not self.primeiro):
						retorno.getById += self.identacaoMiolo+ self.t+ self.t+ self.t+"$this->ALIAS."+ self.textoGetById+ "\n"
					# FORMATAR
					retorno.formata1 += self.identacaoMiolo+self.t+self.textoFormata1+"\n"
					retorno.formata2 += self.identacaoMiolo+self.t+self.textoFormata2+"\n"
					# INSERIR
					retorno.insere += self.identacaoSQL+self.textoInsere+"\n"
					if(self.primeiro):        
						retorno.insereV += self.identacaoSQL+"null,"+"\n"
					else:
						retorno.insereV += self.identacaoSQL+self.textoV+"\n"
					# ATUALIZAR	
					if(not self.primeiro):
						retorno.atualizar += self.identacaoSQL+self.textoUpdate+"\n"
					# WHERE	
					retorno.makeWhere += self.textoWhere +"\n"
					
					#ins e Atz com prepare
					if(self.textoPrepare):
						try:						
							_prepared0 = self.textoPrepare[0]
							_prepared1 = self.textoPrepare[1]
							_prepare0 = retorno.prepare[0]
							_prepare1 = retorno.prepare[1] + ', '
						except KeyError:
							# Key is not present
							_prepare0 = '';
							_prepare1 = '';
							print('nao tratar li3[1]')
							pass
			
						_prepare0 += _prepared0
						_prepare1 += "$obj->"+li2[0]
						retorno.prepare[0] = _prepare0
						retorno.prepare[1] = _prepare1
						self.textoPrepare = {}
						
					if(self.primeiro):        
						self.primeiro = False
					
					retorno.entidade += self.identacaoFuncao+"public "+self.textoEntidade+ "\n"

		return retorno


	def processarDateTime(self,li2):		
		self.textoFormata1 += "$this->db->sqldate($obj->"+li2[0]+");"
		self.textoFormata2 += "$this->db->sqldate($obj['"+li2[0]+"']);"
		self.textoUpdate += "$obj->"+li2[0]+","
		
		self.textoV = "$obj->"+li2[0]+","
		
		
		self.textoWhere += self.identacaoMiolo + self.t +"$where .= \" "+li2[0]+" = \".$this->db->sqldate($busca['"+li2[0]+"'], 'DD/MM/YYYY').\" \";" +"\n"
		self.textoWhere += self.identacaoMiolo +"}" +"\n"
		
		
	def processarInt(self,li2):
		self.textoFormata1 += "intval($obj->"+li2[0]+");"
		self.textoFormata2 += "intval($obj['"+li2[0]+"']);"
		self.textoUpdate += "$obj->"+li2[0]+","
		self.textoV = "$obj->"+li2[0]+","
		
		self.textoWhere += self.identacaoMiolo + self.t +"$where .= \" "+li2[0]+" = \".intval($busca['"+li2[0]+"']).\" \";" +"\n"					
		self.textoWhere += self.identacaoMiolo +"}" +"\n"
		
	def processarVarchar(self,li2,li3):
		self.textoFormata1 += "substr($this->FUN->protect($obj->"+li2[0]+"),0,"+li3[1]+");"
		self.textoFormata2 += "substr($this->FUN->protect($obj['"+li2[0]+"']),0,"+li3[1]+");"
		self.textoUpdate += "'$obj->"+li2[0]+"',"
		self.textoV = "'$obj->"+li2[0]+"',"
		
		if(int(li3[1]) < 20):
			self.textoWhere += self.identacaoMiolo + self.t +"$where .= \" "+li2[0]+" = '\".$this->FUN->protect($busca['"+li2[0]+"']).\"' \";" +"\n"					
		else:
			self.textoWhere += self.identacaoMiolo + self.t +"$where .= \" UPPER("+li2[0]+") LIKE UPPER('%\".$this->FUN->protect($busca['"+li2[0]+"']).\"%') \";" +"\n"
			
		self.textoWhere += self.identacaoMiolo +"}" +"\n"
		
	def processarLongtext(self,li2):
		self.textoFormata1 += "$obj->"+li2[0]+";"
		self.textoFormata2 += "$obj['"+li2[0]+"'];"
		self.textoUpdate += "?,"
		self.textoV = "?,"
		
		self.textoPrepare[0] = 's'
		self.textoPrepare[1] = "$obj->"+li2[0]
		
		self.textoWhere += self.identacaoMiolo + self.t +"$where .= \" UPPER("+li2[0]+") LIKE UPPER('%\".$this->FUN->protect($busca['"+li2[0]+"']).\"%') \";" +"\n"
			
		self.textoWhere += self.identacaoMiolo +"}" +"\n"
		
