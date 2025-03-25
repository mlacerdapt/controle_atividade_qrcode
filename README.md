# controle_atividade_qrcode
Controle de Atividade com QR Code

* Rotas de cadastro (Funcionário, Área e Equipamento).
* Função para gerar QR Codes e salvar o nome embaixo.
* Tela de registro de tarefas com leitura dos QR Codes.
* Sistema de finalização de tarefa via QR Code do funcionário.
* Página para exibir e imprimir os QR Codes organizados.

1. Estrutura do Projeto Flask
/sistema_qrcode_flask
│
├── app.py  <-- (o código principal que já criamos)
│
├── /templates  
│   ├── index.html  
│   └── cadastrar_funcionario.html  
│
└── /static  
    └── /qrcodes   <-- (pasta onde os QR Codes serão salvos)