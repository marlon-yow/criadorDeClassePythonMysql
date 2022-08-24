class FEE():
	def __init__(self,val):
		self.app=val
		self.identacaoFuncao = "    "
		self.identacaoMiolo = "        "
		self.identacaoSQL = "                    "
		self.t = "    " 

	### cabecalho ENTITY### COMPLETO
	def cabecalhoEntidade(self, ckNamespace, namespace, ckSkeleton, entidade):
		out = "<?php" +"\n"
		if(ckNamespace):
			out +="namespace " + namespace +";" +"\n"
		
		out += "\n" + "if (!class_exists('"
		if(ckNamespace):
			out +="\\" +namespace +"\\"
		out += entidade+"')){" +"\n"

		out += "\n" + "Class "+entidade
		if(ckSkeleton):
			out +=" extends \\EntidadeEsqueleto{"
		else:
			out +=" {"
			
		out += "\n" +"\n"
		return out

	### CRIAR CORPO ENTIDADE
	def criarCorpoEntidade(self,campos,primaryKey):
		out = campos +"\n" +"\n"
		
		out += self.identacaoFuncao+"public function __construct($id=0){" +"\n"
		out += self.identacaoMiolo+"$this->"+primaryKey+" = $id;" +"\n"
		out += self.identacaoFuncao+"}" +"\n" +"\n"
		
		return out

	### rodape ENTIDADE ### COMPLETO
	def rodapeEntidade(self):
		out = "} //end class" +"\n"
		out += "} //endif"

		return out
