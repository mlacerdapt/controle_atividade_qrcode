# controle_atividade_qrcode
Controle de Atividade com QR Code

Perfeito! Ajustamos as entidades e o diagrama do banco de dados, e definimos Python com Flask para o backend e HTML/CSS para o frontend. Vamos refinar o planejamento e iniciar o desenvolvimento.

1. Estrutura do Projeto Flask
Vamos criar a estrutura básica do projeto Flask:

nome_do_projeto/
├── app.py          # Arquivo principal do Flask
├── templates/      # Pasta para os arquivos HTML
│   ├── cadastro_funcionario.html
│   ├── cadastro_area.html
│   ├── cadastro_equipamento.html
│   ├── registrar_tarefa.html
│   └── ...
├── static/         # Pasta para arquivos CSS, JavaScript e imagens
│   ├── style.css
│   ├── script.js
│   └── ...
└── database.db     # Banco de dados SQLite (para desenvolvimento)