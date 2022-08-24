#TODO: formatar com OBJ

class FunClass():
	def __init__(self,val):
		self.app=val
		self.identacaoFuncao = "    "
		self.identacaoMiolo = "        "
		self.identacaoSQL = "                    "
		self.t = "    "

	### cabecalho CLASS ### COMPLETO
	def cabecalhoService(self, ckNamespace, namespace, ckSkeleton, ckSkeletonV2, classe, ckEntidade, entidade):
		out = "<?php" + " /*utf-8*/" + "\n" + "/*autogen v1*/" + "\n"
		if(ckNamespace):
			out +="namespace " + namespace +";" +"\n"
		
		if(ckEntidade):
			out += "require_once(__DIR__.'/"+entidade+".php');" +"\n"
			
		out += "\n" + "Class "+classe
		if(ckSkeleton):
			out +=" extends \\Skeleton{"
		elif(ckSkeletonV2):
			out +=" extends \\SkeletonV2{"
		else:
			out +=" {"
			
		out += "\n" +"\n"
		return out
   
	### __construtct ### COMPLETO
	def criarConstruct(self,tabela,alias,primaryKey,entidade):

		out = self.identacaoFuncao+"public function  __construct($db,\FUN $FUN = null){" +"\n"
		#out += self.identacaoMiolo+"$dbInfo = parse_ini_file(__DIR__.'/dbInfo.ini');" +"\n" +"\n"

		out += self.identacaoMiolo+"$this->NAMESPACE = __NAMESPACE__;" +"\n"
		out += self.identacaoMiolo+"$this->SCHEMA = $this->genSchema(__DIR__);" +"\n"
		out += self.identacaoMiolo+"$this->TABELA = '"+tabela+"';" +"\n"
		out += self.identacaoMiolo+"$this->ALIAS = '"+alias+"';" +"\n"
		out += self.identacaoMiolo+"//$this->SEQUENCIA = '';" +"\n"
		out += self.identacaoMiolo+"$this->ID = '"+primaryKey+"';" +"\n"
		out += self.identacaoMiolo+"$this->ENTIDADE = '"+entidade+"';" +"\n" +"\n"
		
		out += self.identacaoMiolo+"$this->db = $db;" +"\n"				
		out += self.identacaoMiolo+"$this->FUN = $FUN;" +"\n"
		
		out += self.identacaoFuncao+"}" +"\n" +"\n"

		return out

	### GET BY ID ### COMPLETO
	def criarGetById(self,getById,ckEntidade):
		out = self.identacaoFuncao+"public function getById($obj,$returnAsObj=false){" +"\n"
	
		if(ckEntidade):
			out += self.identacaoMiolo+"if($returnAsObj){" +"\n"		
			out += self.identacaoMiolo+ self.t+"$result = $this->getNewEntity();" +"\n"				
			out += self.identacaoMiolo+"}else{" +"\n"
			out += self.identacaoMiolo+ self.t+"$result  = array();" +"\n"
			out += self.identacaoMiolo+"}" +"\n"
			out += self.identacaoMiolo+"if(!$obj){" +"\n"
			out += self.identacaoMiolo+ self.t+"if(gettype($result) == 'object'){" +"\n"
			out += self.identacaoMiolo+ self.t+ self.t+"$result->erro = 1;" +"\n"
			out += self.identacaoMiolo+ self.t+ self.t+"$result->mensagem = 'parametro veio vazio';" +"\n"
			out += self.identacaoMiolo+ self.t+"}" +"\n"
			out += self.identacaoMiolo+ self.t+"return $result;" +"\n"
			out += self.identacaoMiolo+"}" +"\n" +"\n"
			
			out += self.identacaoMiolo+"if($this->testarEntidade($obj,$this->NAMESPACE,array('integer','string','double')) ){" +"\n"		
			out += self.identacaoMiolo+ self.t+"$id = $obj->{$this->ID};" +"\n"		
			out += self.identacaoMiolo+"}else{" +"\n"
			out += self.identacaoMiolo+ self.t+"$id = $obj;" +"\n"
			out += self.identacaoMiolo+"}" +"\n" +"\n"
		else:
			out += self.identacaoMiolo+"$result  = array();" +"\n"
			out += self.identacaoMiolo+"$id = intval($obj);" +"\n"
			
		if(ckEntidade):
			out += self.identacaoMiolo+"$id = intval($id);" +"\n"
			out += self.identacaoMiolo+"if(!$id){" +"\n"
			out += self.identacaoMiolo+ self.t+ "if(gettype($result) == 'object'){" +"\n"
			out += self.identacaoMiolo+ self.t+ self.t+ "$result->erro = 1;" +"\n"
			out += self.identacaoMiolo+ self.t+ self.t+ "$result->mensagem = 'id não numerico';" +"\n"
			out += self.identacaoMiolo+ self.t+ "}" +"\n"
			out += self.identacaoMiolo+ self.t+ "return $result;" +"\n"
			out += self.identacaoMiolo+"}" +"\n" +"\n"
		else:
			out += self.identacaoMiolo+"if(!$id){" +"\n"
			out += self.identacaoMiolo+  self.t+ "return $result;" +"\n"
			
		out += self.identacaoMiolo+"$select = \"SELECT" +"\n"
		out += self.identacaoMiolo+ self.t+ self.t+ self.t+"$this->ALIAS.$this->ID," +"\n"
		out += getById[:-2] +"\";\n" +"\n"
		out += self.identacaoMiolo+ "$from = $this->makeFrom();" +"\n"
		out += self.identacaoMiolo+ "$where =\" WHERE $this->ID = $id\";" +"\n" +"\n"
		
		out += self.identacaoMiolo+ "$param = $select.$from.$where;" +"\n" +"\n"
		
		out += self.identacaoMiolo+ "if($this->DBG) echo $param;" +"\n"
		out += self.identacaoMiolo+"$sql = $this->db->query($param);" +"\n"
		out += self.identacaoMiolo+"$rw = $this->db->fetch($sql);" +"\n" +"\n"

		if(ckEntidade):
			out += self.identacaoMiolo+"if($returnAsObj){" +"\n"
			out += self.identacaoMiolo+"    $result = $result->arrayToObject($rw,$result);" +"\n"
			out += self.identacaoMiolo+"}else{" +"\n"
			out += self.identacaoMiolo+"    $result = $rw;" +"\n"
			out += self.identacaoMiolo+"}" +"\n"
		else:
			out += self.identacaoMiolo+"    $result = $rw;" +"\n"
			
		out += self.identacaoMiolo+"return $result;" +"\n"		
		out += self.identacaoFuncao+"}" +"\n" +"\n"
		return out

	### formatar ### COMPLETA
	def criarFormatar(self,formata1,formata2):
		out = self.identacaoFuncao+"private function formatar($obj){" +"\n"		
		out += self.identacaoMiolo+"$obj2 = $this->getNewEntity();" +"\n"
		out += self.identacaoMiolo+"if(!$obj){" +"\n"
		out += self.identacaoMiolo+"    $obj2->erro = 1;" +"\n"
		out += self.identacaoMiolo+"    $obj2->mensagem = 'obj vazio';" +"\n" 
		out += self.identacaoMiolo+"}else if($this->testarEntidade($obj,$this->NAMESPACE,array('array')) ){" +"\n"
		out += formata1
		out += self.identacaoMiolo+"}else{" +"\n"
		out += formata2
		out += self.identacaoMiolo+"}" +"\n"
		
		out += self.identacaoMiolo+"//debug($obj2);" +"\n"		
		out += self.identacaoMiolo+"return $obj2;" +"\n"

		out += self.identacaoFuncao+"}" +"\n" +"\n"
		return out

	### INSERIR ### INCOMPLETA [falta o prepare]
	def criarInserir(self,insere,insereV,resultado):
		out = self.identacaoFuncao+"public function inserir($obj,$returnAsObj=false){"+"\n"
		out += self.identacaoMiolo+"if($this->testarEntidade($obj,$this->NAMESPACE,array('array')) ){" +"\n"
		out += self.identacaoMiolo+"    $result = $obj;" +"\n"
		out += self.identacaoMiolo+"}else{" +"\n"
		out += self.identacaoMiolo+"    $result = $this->getNewEntity();" +"\n"
		out += self.identacaoMiolo+"    $result = $result->arrayToObject($rw,$result);" +"\n"
		out += self.identacaoMiolo+"}" +"\n"
		out += self.identacaoMiolo+"$resultInt = 0;" +"\n" +"\n"		

		out += self.identacaoMiolo+"$obj = $this->formatar($obj);" +"\n"
		out += self.identacaoMiolo+"if(isset($obj->{$this->ID}) and $this->getById($obj->{$this->ID})) return $this->atualizar($obj);" +"\n" +"\n"

		#out += self.identacaoMiolo+"$obj->"+insereFirstElement+" = $this->getNextId();" +"\n" +"\n"

		out += self.identacaoMiolo+"$param = \"INSERT INTO $this->SCHEMA.$this->TABELA(" + "\n"
		out += insere[:-2] +"\n"
		out += self.identacaoMiolo + self.t+ self.t  +") VALUES ( " +"\n"
		out += insereV[:-2] +"\n"
		out += self.identacaoMiolo+ self.t+ self.t+")\";" +"\n" +"\n"
		
		out += self.identacaoMiolo+"if($this->DBG) echo $param;"+"\n"
		#print(resultado)
		if(resultado.prepare):
			if (len(resultado.prepare[0]) > 1):
				out += self.identacaoMiolo+"$pepares = array(\""+resultado.prepare[0]+"\",array("+resultado.prepare[1]+") ); //array('s',$texto);"+"\n"
			else:
			    out += self.identacaoMiolo+"$pepares = array(\""+resultado.prepare[0]+"\","+resultado.prepare[1]+"); //array('s',$texto);"+"\n"
		else:
			out += self.identacaoMiolo+"$pepares = array(); //array('s',$texto);"+"\n"
		out += self.identacaoMiolo+"if($this->db->query($param,$pepares)){" +"\n"
		out += self.identacaoMiolo+"    $result->erro = 0;" +"\n"
		out += self.identacaoMiolo+"    $result->mensagem = 'Salvo';" +"\n"
		out += self.identacaoMiolo+"    $result->{$this->ID} = $this->db->con->insert_id;" +"\n"
		out += self.identacaoMiolo+"    $resultInt = $this->db->con->insert_id;" +"\n"
		out += self.identacaoMiolo+"}" +"\n" +"\n"
		
		out += self.identacaoMiolo+"if($returnAsObj){" +"\n"
		out += self.identacaoMiolo+"    return $result;" +"\n"
		out += self.identacaoMiolo+"}" +"\n"
		out += self.identacaoMiolo+"return $resultInt;" +"\n"
		
		out += self.identacaoFuncao+"}" +"\n" +"\n"
		return out

	### Atualizar ### INCOMPLETA [falta o prepare]
	def criarAtualizar(self,atualizar,primaryKey,resultado):
		out = self.identacaoFuncao+"public function atualizar($obj,$returnAsObj=false){"+"\n"		
		out += self.identacaoMiolo+"if($this->testarEntidade($obj,$this->NAMESPACE,array('array')) ){" +"\n"
		out += self.identacaoMiolo+"    $result = $obj;" +"\n"
		out += self.identacaoMiolo+"}else{" +"\n"
		out += self.identacaoMiolo+"    $result = $this->getNewEntity();" +"\n"
		out += self.identacaoMiolo+"    $result = $result->arrayToObject($rw,$result);" +"\n"
		out += self.identacaoMiolo+"}" +"\n"
		out += self.identacaoMiolo+"$resultInt = 0;" +"\n" +"\n"

		out += self.identacaoMiolo+"$obj = $this->formatar($obj);" +"\n"
		out += self.identacaoMiolo+"if(!isset($obj->{$this->ID}) or !$this->getById($obj->{$this->ID})) return $this->inserir($obj);" +"\n" +"\n"

		out += self.identacaoMiolo+"$param = \"UPDATE $this->SCHEMA.$this->TABELA SET" +"\n"
		out += atualizar[:-2] +"\n"
		out += self.identacaoMiolo+ self.t+ self.t+"WHERE $this->ID = $obj->"+primaryKey+"\";" +"\n" +"\n"

		out += self.identacaoMiolo+"if($this->DBG) echo $param;"+"\n"
		#print(resultado)
		if(resultado.prepare):
			if (len(resultado.prepare[0]) > 1):
				out += self.identacaoMiolo+"$pepares = array(\""+resultado.prepare[0]+"\",array("+resultado.prepare[1]+") ); //array('s',$texto);"+"\n"
			else:
			    out += self.identacaoMiolo+"$pepares = array(\""+resultado.prepare[0]+"\","+resultado.prepare[1]+"); //array('s',$texto);"+"\n"
		else:
			out += self.identacaoMiolo+"$pepares = array(); //array('s',$texto);"+"\n"
		out += self.identacaoMiolo+"if($this->db->query($param,$pepares)){" +"\n"
		out += self.identacaoMiolo+"    $result->erro = 0;" +"\n"
		out += self.identacaoMiolo+"    $result->mensagem = 'Atualizado';" +"\n"		
		out += self.identacaoMiolo+"    $resultInt = $obj->{$this->ID};" +"\n"
		out += self.identacaoMiolo+"}" +"\n" +"\n"
		
		out += self.identacaoMiolo+"if($returnAsObj){" +"\n"
		out += self.identacaoMiolo+"    return $result;" +"\n"
		out += self.identacaoMiolo+"}" +"\n"
		out += self.identacaoMiolo+"return $resultInt;" +"\n"
		
		out += self.identacaoFuncao+"}" +"\n" +"\n"
		return out

	### Make Select ### COMPLETA
	def criarMakeselect(self,getById):
		out = self.identacaoFuncao+"protected function makeSelect(){"+"\n"		
		
		out += self.identacaoMiolo+"$param = \"SELECT" +"\n"
		out += self.identacaoMiolo+ self.t+ self.t+ self.t+"$this->ALIAS.$this->ID," +"\n"
		out += getById[:-2]+"\n"
		out += self.identacaoMiolo+ self.t+ self.t+ self.t+"\";" +"\n"
		out += self.identacaoMiolo+"return $param;" +"\n"
		out += self.identacaoFuncao+"}" +"\n" +"\n"
		
		return out
	
	### Make Where ### COMPLETA
	def criarmakeWhere(self,makeWhere,excluido):
		out = self.identacaoFuncao+"protected function makeWhere($busca){"+"\n"
		out += self.identacaoMiolo+"$busca = $this->FUN->protect($busca);" + "\n"
		out += self.identacaoMiolo+"if(!$busca) return '';" +"\n" +"\n"

		out += makeWhere
		
		if(excluido):
			out += self.identacaoMiolo+"if($busca['excluido']){" + "\n"
			out += self.identacaoMiolo+"    if($where) $where .= \" AND \";" + "\n"
			out += self.identacaoMiolo+"    $where .= \" excluido IS NOT NULL \";" + "\n"
			out += self.identacaoMiolo+"}else{" + "\n"
			out += self.identacaoMiolo+"    if($where) $where .= \" AND \";" + "\n"
			out += self.identacaoMiolo+"    $where .= \" excluido IS NULL \";" + "\n"
			out += self.identacaoMiolo+"}" + "\n" + "\n"

		out += self.identacaoMiolo+"if($where) $where = \"WHERE $where\";" +"\n"
		out += self.identacaoMiolo+"return $where;" +"\n"		
		out += self.identacaoFuncao+"}" +"\n" +"\n"
		return out
		
	### Make Order ### 
	def criarmakeOrder(self):
		out = self.identacaoFuncao+"protected function makeOrder($order){"+"\n"		
		out += self.identacaoMiolo+"$ordenar = '';" + "\n"
		out += self.identacaoMiolo+"switch ($order) {" + "\n"		
		out += self.identacaoMiolo+ self.t+ "case '1':" +"\n" 
		out += self.identacaoMiolo+ self.t+ self.t+ "$ordenar = \"ORDER BY $this->ID ASC\";" +"\n"
		out += self.identacaoMiolo+ self.t+ self.t+ "break;" +"\n"
		out += self.identacaoMiolo+ self.t+ "default:" +"\n"
		out += self.identacaoMiolo+ self.t+ self.t+ "$ordenar = \"ORDER BY $this->ID DESC\";" +"\n"
		out += self.identacaoMiolo+ self.t+ self.t+ "break;" +"\n"
		out += self.identacaoMiolo+"}" + "\n"				
		out += self.identacaoMiolo+"return $ordenar;" +"\n"		
		out += self.identacaoFuncao+"}" +"\n" +"\n"
		return out
	
	### rodape CLASS ### COMPLETO
	def rodape(self, classe):
		out = "}" +"\n" +"\n"

		out +="$"+classe+" = new "+classe+"($db,$FUN);"
				
		return out	
