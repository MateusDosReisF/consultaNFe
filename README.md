# 📄 ConsultaNFe - Consulta de Notas Fiscais por CNPJ
ConsultaNFe é uma aplicação web desenvolvida com Django que permite a consulta de Notas Fiscais Eletrônicas (NF-e) associadas a um CNPJ, utilizando integrações com serviços de consulta pública e/ou APIs específicas (pynfe).

# 🚀 Funcionalidades
    🔍 Consulta automática de NF-es vinculadas a um CNPJ.
    
    📥 Armazenamento e listagem das notas consultadas.
    
    📄 Visualização e download dos XMLs das notas.
    
    📆 Filtro por data de emissão.
    
    📊 Dashboard com informações consolidadas das notas.
    
    ⚙️ Interface simples e intuitiva para facilitar a operação.

# 🛠️ Tecnologias Utilizadas
    Python 3.x
    
    Django
    
    SQLite / PostgreSQL (ajustável)
    
    Bootstrap / TailwindCSS (para interface)
    
    pynfe (para integração com serviços de consulta)

# Instale as dependências

  pip install -r requirements.txt

# Configure o banco de dados
  python manage.py migrate

# OBS
O DASHBOARD NÃO ESTA VINCULADO AS NOTAS PUXADAS POIS ESSE DASH EU UTILIZAVA PARA CONSULTA EM UM BANCO MAIS ROBUSTO NO SQL SERVER, SINTA-SE A VONTADE PARA MODIFICAR E FAZER DA FORMA QUE DESEJE! 
