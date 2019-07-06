# Maquina-de-busca-Python
API Maquina de busca implementada em Python com Flask e SQLAlchemy

#==================================================================
#For Windows
#==================================================================

#Instalar gerenciador de ambiente
pip install virtualenv

#Criar ambiente
mkvirtualenv Maquina-de-busca-Python

#Ativar ambiente
workon Maquina-de-busca-Python

#Instalar dependências no ambiente ativado
pip install Flask 
pip install flask_sqlalchemy 
pip install sqlalchemy
pip install mysql-connector-python
pip install pymysql
pip install requests
pip install beautifulsoup4
pip install Paginator
pip install paginate
pip install UserManager
pip install flask-login

#Iniciar servidor
#Dentro do diretório /src
set FLASK_APP=api.py
flask run


#setar ambiente no vscode
1-ctrl+shift+p
python: <selecionar>

2-Menu: Debug > add config
	-python
	-Flask
-editar o arquivo 'launch.json' e mudar para src/api.py
-F5 Rodar com debug


#Rodar Servidor em ambiente já configurado
#Dentro do diretório /src
workon Maquina-de-busca-Python
set FLASK_APP=api.py
flask run




#==================================================================
#For Linux/Mac (ps. no linux temos python(que corresponde ao 2.x) e python3, vamos utilizar o python3)
#==================================================================

#Instalar gerenciador de ambiente python3
$sudo apt install python3-venv --default-timeout=1000

#Criar ambiente
$python3 -m venv my-project-env

#Ativar ambiente
$ source my-project-env/bin/activate
(my-project-env) $

#Instalar dependências no ambiente ativado 
#(caso ocorra erros na instalação siga os passos para a correção do certificado no final deste arquivo*)
$pip3 install Flask --default-timeout=1000
$pip3 install flask_sqlalchemy --default-timeout=1000
$pip3 install mysql-connector-python --default-timeout=1000
$pip3 install sqlalchemy --default-timeout=1000
$pip3 install pymysql --default-timeout=1000
$pip3 install requests --default-timeout=1000
$pip3 install beautifulsoup4 --default-timeout=1000
$pip3 install Paginator --default-timeout=1000
$pip3 install paginate --default-timeout=1000
$pip3 install UserManager --default-timeout=1000
$pip3 install flask-login --default-timeout=1000

#desativando ambiente
deactive


#Iniciar servidor
#Dentro da pasta /src
$ export FLASK_APP=hello.py
$ flask run


#setar ambiente no vscode
1-ctrl+shift+p
python: <selecionar>

2-Menu: Debug > add config
	-python
	-Flask
-editar o arquivo 'launch.json' e mudar para src/api.py
-F5 Rodar com debug


#Rodar Servidor em ambiente já configurado
#Dentro do diretório /src
$ export FLASK_APP=hello.py
$ flask run





#==================================================================
# *Correção do erro de certificado do pip install no linux xubuntu
#==================================================================
#crie o arquivo pip.conf  conforme abaixo
#
#$ mkdir ~/.pip 
#$ vim ~/.pip/pip.conf

#----------------------------------
#[global]
#index-url = http://mirrors.aliyun.com/pypi/simple/
#[install]
#trusted-host = mirrors.aliyun.com
#----------------------------------

#Execute o comando
#$ python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade pip

