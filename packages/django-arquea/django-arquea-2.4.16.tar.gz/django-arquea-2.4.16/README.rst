======
ARQUEA
======

Sistema de gestão de informações para projetos de pesquisa segundo regras estabelecidas pelo termo de outorga e manual de prestação de contas da FAPESP. Desenvolvido pelo NARA inicialmente para a ANSP e aperfeiçoado para o NeuroMat.

Instalação
..........

1. Instale os pacotes de desenvolvimento do ``python``, ``xml``, ``ffi``, ``xslt``, ``zlib`` e ``yaml``, o pacote de
fontes ``liberation`` e o ``pip`` para instalar pacotes python. No caso do Ubuntu, seria::

    apt-get install libffi-dev libpython-dev libxml2-dev libxslt1-dev zlib1g-dev libyaml-dev fonts-liberation python-pip

2. Instale o ``virtualenv``::

    pip install virtualenv

3. Crie o ambiente virtual::

    virtualenv <nome do ambiente>

4. Entre no diretório do ambiente virtual e ative-o::

    cd <nome do ambiente>
    source bin/activate

5. Instale o ``django-arquea``::

    pip install django-arquea

Configuração
............

1. Crie um novo projeto Django::

    django-admin startproject <nome do projeto>


2. Adicione a seguinte linha no final seu ``settings.py``::

    cd <nome do projeto>
    vi <nome do projeto>/settings.py
    INSTALLED_APPS += ('configuracao',)

3. Crie as configurações padrão::

    python manage.py criarsistema <nome do projeto>

4. Execute
   ::

    python manage.py migrate

   para criar a base de dados inicial e
   ::

    python manage.py loaddata initial_data.yaml

   para carregar os dados iniciais.

5. Execute
   ::

    python manage.py createsuperuser

   para criar o super usuário inicial.

6. Execute
   ::

    python manage.py runserver

   e acesse http://localhost:8000 para verificar se a aplicação está rodando.


Colocando em produção
.....................

1. Estando tudo ok nas etapas anteriores, é hora de colocar em produção. Por padrão, é criada
uma base de dados SQLite, que é ótima para testes, mas não é muito indicada para um ambiente de 
produção. Recomendamos utilizar o PostgreSQL ou o MySQL. Mostraremos como instalar e configurar 
o PostgreSQL no Ubuntu.

    a. Instale a biblioteca de desenvolvimento do PostgreSQL::

        apt-get install libpq-dev

    b. Instale o servidor do PostgreSQL::

        apt-get install postgresql

    c. Crie a base de dados::

        sudo su - postgres
        createdb <base>
        createuser <user>
        psql <base>
        grant all on database <base> to <user>;
        alter user <user> password '<pass>';
        quit
        CTRL+D

    d. Repita o passo 4 de "Instalação" e instale o ``psycopg``::

        pip install psycopg2

    e. Edite o arquivo ``settings.py`` e altere as informações do banco de dados::

        cd <nome do projeto>
        vi <nome do projeto>/settings.py
        
        DATABASES = {
	    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'localhost', # se instalar o servidor em outra máquina, ip ou hostname dele
            'NAME': '<base>',
            'USER': '<user>',
            'PASSWORD': '<pass>'
            } 
        }

    f. Execute os passos 4 e 5 de "Configuração".

    g. Execute o passo 6 de "Configuração" para verificar se com o PostgreSQL tudo continua funcionando.

2. Para colocarmos em produção, precisamos de um webserver. Abaixo, é utilizado o Apache + WSGI, mas
pode ser feito de outras maneiras, como descrito em https://docs.djangoproject.com/en/1.7/howto/deployment/ .

    a. Instale o ``apache2``, o ``mod_wsgi``;
    b. Habilite esses módulos;
    c. Configure o apache. Considerando que o sistema rodará sozinho na máquina, a configuração seria apenas
       modificar o arquivo ``/etc/apache2/sites-available/000-default``::

        WSGIScriptAlias / /path/to/your/project/project/wsgi.py
        WSGIPythonPath /path/to/your/project/project:/virtualenv/dir/lib/python2.7/site-packages
        <VirtualHost *:80>

                WSGIProcessGroup %{GLOBAL}
                WSGIApplicationGroup %{GLOBAL}

                Alias /files/   /var/www/files/
                Alias /static/  /var/www/static/

                <Directory /var/www/static>
                   Require all granted
                </Directory>

                <Directory /var/www/files>
                   Require all granted
                </Directory>

                <Directory /path/to/your/project/project>
                   <Files wsgi.py>
                      Require all granted
                   </Files>
                </Directory>

                <Location "/files">
                   AuthType Basic
                   AuthName "Sistema"
                   Require valid-user
                   AuthBasicProvider wsgi
                   WSGIAuthUserScript /path/to/your/project/project/wsgi.py
                </Location>

                ErrorLog ${APACHE_LOG_DIR}/error.log
                CustomLog ${APACHE_LOG_DIR}/access.log combined
        </VirtualHost>

       trocando os diretórios e arquivos informados pelos da sua instalação

    d. Execute, no diretório do projeto::

        python manage.py collectstatic


Referências
...........

[ANSP] an Academic Network at São Paulo, Rede Acadêmica do Estado de São Paulo  - projeto especial FAPESP coordenado pelo Prof. Dr. Luis Fernandez Lopez - www.ansp.br.

[FAPESP] Fundação de Amparo à Pesquisa do Estado de São Paulo - www.fapesp.br.

[NARA] Núcleo de Aplicações em Redes Avançadas - Equipe que operara e mantém o projeto Rede ANSP - www.ansp.br.

[NEUROMAT] Neuromatemática - Centro de Pesquisa, Inovação e Difusão (CEPID) da FAPESP coordenado pelo Prof. Dr. Antonio Galves - www.neuromat.numec.prp.usp.br.





