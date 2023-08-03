# Interface de Mapeamento de Impressora de Etiqueta. Permite desmapear porta lpt2 e mapear com IPV4.

Essa é uma interface básica em Python que permite desmapear e mapear impressora ZebraZD220 em porta LPT2. 
Ele puxa apenas o Adaptador Ethernet Ethernet 2, que é usado quando a Sophos VPN está ativada.

Basicamente usa esses comandos de forma automatica

net use lpt2 /delete 
###Comando para desmapear impressora


net use lpt2 \\192.168.100.98\ZD220 /persistent:yes
###Comando para mapear impressora em porta LPT2, IP FICTICO: 192.168.100.98 NOME IMPRESSORA FICTICIO: ZD220


![Interface]([https://github.com/ErickDaniel7/python/blob/main/projetos-de-aprendizado/IP's/IMG/Interface.jpg](https://github.com/ErickDaniel7/python/blob/main/projetos-de-aprendizado/IPV4/IMG/Interface.jpg))

![Notificações Sucesso]([https://github.com/ErickDaniel7/python/blob/main/projetos-de-aprendizado/IP's/IMG/Interface.jpg](https://github.com/ErickDaniel7/python/blob/main/projetos-de-aprendizado/IPV4/IMG/Sucesso.jpg))

![Notificações Erros]([https://github.com/ErickDaniel7/python/blob/main/projetos-de-aprendizado/IP's/IMG/Interface.jpg](https://github.com/ErickDaniel7/python/blob/main/projetos-de-aprendizado/IPV4/IMG/Erro.jpg)https://github.com/ErickDaniel7/python/blob/main/projetos-de-aprendizado/IPV4/IMG/Erro.jpg)
