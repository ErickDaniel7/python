import tkinter as tk
from tkinter import ttk, messagebox
import json
from PIL import Image, ImageTk
import subprocess
import threading
import time
import socket
import os
import csv
import ipaddress

def visualizar_json():
    try:
        with open('dados_maquinas.json', 'r') as file:
            data = json.load(file)
        json_text = json.dumps(data, indent=4)
    except FileNotFoundError:
        json_text = "Arquivo de dados não encontrado."

    view_json_window = tk.Toplevel(app)
    view_json_window.title('Visualizar JSON')
    view_json_window.geometry('600x400')

    json_textbox = tk.Text(view_json_window, font=('Courier', 12))
    json_textbox.pack(expand=True, fill=tk.BOTH)
    json_textbox.insert(tk.END, json_text)
    json_textbox.config(state=tk.DISABLED)

def validar_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def verificar_conexao(ip):
    try:
        socket.create_connection((ip, 80), timeout=5)
        return True
    except OSError:
        return False

def salvar_info():
    data = {'maquinas': maquinas}
    with open('dados_maquinas.json', 'w') as file:
        json.dump(data, file)

def verificar_ip_duplicado(ip, current_index=None):
    for index, maquina in enumerate(maquinas):
        if maquina['ip'] == ip and index != current_index:
            return True
    return False

def formatar_maquina(maquina):
    return f"{maquina['nome']} - {maquina['ip']} ({maquina['categoria']}, {maquina['sistema_operacional']})"

def listar_maquinas():
    lista_maquinas.delete(0, tk.END)
    for maquina in maquinas:
        lista_maquinas.insert(tk.END, formatar_maquina(maquina))

def exibir_quantidade_maquinas():
    quantidade_label.config(text=f"Quantidade de Máquinas: {len(maquinas)}")

def sair():
    if messagebox.askyesno("Confirmação", "Deseja realmente sair?"):
        salvar_info()
        app.quit()

def exibir_notificacao(tipo, titulo, mensagem):
    if tipo == 'info':
        messagebox.showinfo(titulo, mensagem)
    elif tipo == 'aviso':
        messagebox.showwarning(titulo, mensagem)
    elif tipo == 'erro':
        messagebox.showerror(titulo, mensagem)

def adicionar_maquina():
    nome = nome_entry.get()
    ip = ip_entry.get()

    if not nome or len(nome) < 3:
        exibir_notificacao('erro', 'Erro', 'Por favor, insira um nome de máquina com pelo menos três caracteres.')
        return

    if not categoria_var.get():
        exibir_notificacao('erro', 'Erro', 'Por favor, selecione uma categoria.')
        return
    
    if not sistema_operacional_var.get():
        exibir_notificacao('erro', 'Erro', 'Por favor, selecione um sistema operacional.')
        return

    if nome and ip:
        if validar_ip(ip):  
            if verificar_ip_duplicado(ip):  
                exibir_notificacao('erro', 'Erro', 'Endereço IP já foi adicionado. Por favor, insira um endereço IP diferente.')
            else:
                categoria = categoria_var.get()
                sistema_operacional = sistema_operacional_var.get()
                maquinas.append({'nome': nome, 'ip': ip, 'categoria': categoria, 'sistema_operacional': sistema_operacional})
                salvar_info()
                listar_maquinas()
                exibir_quantidade_maquinas()  # Adicione esta linha para exibir a quantidade correta
                exibir_notificacao('info', 'Sucesso', 'Máquina adicionada com sucesso!')
                nome_entry.delete(0, tk.END)
                ip_entry.delete(0, tk.END)
        else:
            exibir_notificacao('erro', 'Erro', 'Por favor, insira um endereço IP válido.')
    else:
        exibir_notificacao('erro', 'Erro', 'Por favor, preencha todos os campos.')

def filtrar_por_categoria():
    categoria_selecionada = categoria_filtro_var.get()
    if categoria_selecionada == 'Todas Categorias':
        listar_maquinas()
    else:
        lista_maquinas.delete(0, tk.END)
        for maquina in maquinas:
            if maquina['categoria'] == categoria_selecionada:
                lista_maquinas.insert(tk.END, f"{maquina['nome']} - {maquina['ip']}")

def filtrar_por_so():
    so_selecionado = sistema_operacional_filtro_var.get()
    if so_selecionado == 'Todos SO':
        listar_maquinas()
    else:
        lista_maquinas.delete(0, tk.END)
        for maquina in maquinas:
            if maquina['sistema_operacional'] == so_selecionado:
                lista_maquinas.insert(tk.END, f"{maquina['nome']} - {maquina['ip']}")

def filtrar_por_categoria_e_so():
    categoria_selecionada = categoria_filtro_var.get()
    so_selecionado = sistema_operacional_filtro_var.get()

    lista_maquinas.delete(0, tk.END)
    for maquina in maquinas:
        if (categoria_selecionada == 'Todas Categorias' or maquina['categoria'] == categoria_selecionada) and \
           (so_selecionado == 'Todos SO' or maquina['sistema_operacional'] == so_selecionado):
            lista_maquinas.insert(tk.END, f"{maquina['nome']} - {maquina['ip']}")

def excluir_maquina():
    index = lista_maquinas.curselection()
    if index:
        if messagebox.askyesno('Confirmação', 'Deseja excluir esta máquina?'):
            maquinas.pop(index[0])
            salvar_info()
            listar_maquinas()
    else:
        exibir_notificacao('erro', 'Erro', 'Por favor, selecione uma máquina na lista.')

def deletar_maquina(event):
    index = lista_maquinas.curselection()
    if index:
        if messagebox.askyesno('Confirmação', 'Deseja excluir esta máquina?'):
            maquinas.pop(index[0])
            salvar_info()
            listar_maquinas()

def editar_maquina():
    index = lista_maquinas.curselection()
    if index:
        editar_info_maquina(index[0])
    else:
        exibir_notificacao('erro', 'Erro', 'Por favor, selecione uma máquina na lista.')

def listar_maquinas():
    lista_maquinas.delete(0, tk.END)
    for maquina in maquinas:
        lista_maquinas.insert(tk.END, f"{maquina['nome']} - {maquina['ip']}")

def pesquisar_maquinas():
    texto_pesquisa = pesquisa_entry.get().lower()
    lista_maquinas.delete(0, tk.END)

    for maquina in maquinas:
        if texto_pesquisa in maquina['nome'].lower() or texto_pesquisa in maquina['ip']:
            lista_maquinas.insert(tk.END, f"{maquina['nome']} - {maquina['ip']}")

def exibir_resultado_ping(ip, resultado):
    result_window = tk.Toplevel(app)
    result_window.title(f'Resultado do Ping - {ip}')
    result_window.geometry('700x400')

    result_text = tk.Text(result_window, font=('Courier', 12), wrap=tk.WORD)
    result_text.pack(expand=True, fill=tk.BOTH)

    result_text.tag_configure('resposta', foreground='green')
    result_text.tag_configure('normal', foreground='black')

    animation_thread = threading.Thread(target=exibir_animacao, args=(result_text, resultado))
    animation_thread.start()

def exibir_animacao(result_text, resultado):
    lines = resultado.splitlines()
    for line in lines:
        if 'bytes=' in line:
            animar_texto(result_text, line + '\n', 'resposta')
        else:
            animar_texto(result_text, line + '\n', 'normal')

def animar_texto(text_widget, texto, tag):
    for char in texto:
        text_widget.insert(tk.END, char, tag)
        text_widget.see(tk.END)
        text_widget.update()
        time.sleep(0.01)

def ping_animation(ip):
    animation = "|/-\\"
    for i in range(55):
        ping_text.set(f"Ping {ip}... {animation[i%len(animation)]}")
        time.sleep(0.1)

def ping(ip):
    try:
        resultado = subprocess.run(['ping', '-n', '4', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return resultado.stdout
    except subprocess.CalledProcessError:
        return "Erro ao executar o comando de ping."

def ping_ip():
    index = lista_maquinas.curselection()
    if index:
        maquina_selecionada = maquinas[index[0]]
        ip = maquina_selecionada['ip']
        ping_text.set(f"Ping {ip}") 

        ping_animation_thread = threading.Thread(target=ping_animation, args=(ip,))
        ping_animation_thread.start()

        resultado = ping(ip)

        exibir_resultado_ping(ip, resultado)
    else:
        exibir_notificacao('erro', 'Erro', 'Por favor, selecione uma máquina na lista.')    

def editar_info_maquina(index):
    maquina_selecionada = maquinas[index]

    edit_window = tk.Toplevel(app)
    edit_window.title('Editar Máquina')
    edit_window.geometry('300x200')

    nome_label = ttk.Label(edit_window, text='Nome da Máquina:')
    nome_label.pack(pady=5)

    nome_edit_entry = ttk.Entry(edit_window, font=('Helvetica', 14))
    nome_edit_entry.pack(pady=5)
    nome_edit_entry.insert(tk.END, maquina_selecionada['nome'])

    ip_label = ttk.Label(edit_window, text='IP da Máquina:')
    ip_label.pack(pady=5)

    ip_edit_entry = ttk.Entry(edit_window, font=('Helvetica', 14))
    ip_edit_entry.pack(pady=5)
    ip_edit_entry.insert(tk.END, maquina_selecionada['ip'])

    def salvar_edicao():
        nome_editado = nome_edit_entry.get()
        ip_editado = ip_edit_entry.get()

        if nome_editado and ip_editado:
            if validar_ip(ip_editado):
                if verificar_ip_duplicado(ip_editado, index):
                    exibir_notificacao('erro', 'Erro', 'Endereço IP já está em uso por outra máquina.')
                else:
                    maquinas[index]['nome'] = nome_editado
                    maquinas[index]['ip'] = ip_editado
                    salvar_info()
                    listar_maquinas()
                    edit_window.destroy()
        else:
            exibir_notificacao('erro', 'Erro', 'Por favor, preencha todos os campos.')

    salvar_btn = ttk.Button(edit_window, text='Salvar', command=salvar_edicao)
    salvar_btn.pack(side=tk.LEFT, padx=35, pady=15)

    def cancelar_edicao():
        edit_window.destroy()

    cancelar_btn = ttk.Button(edit_window, text='Cancelar', command=cancelar_edicao)
    cancelar_btn.pack(side=tk.RIGHT, padx=35, pady=15)

def on_listbox_select(event):
    index = lista_maquinas.curselection()
    if index:
        maquina_selecionada = maquinas[index[0]]
        ip = maquina_selecionada['ip']
        ping_text.set(f"Ping {ip}")

def validar_ip(ip):
    import re
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return bool(re.match(pattern, ip))

def limpar_filtros():
    categoria_filtro_var.set('Todas Categorias')
    sistema_operacional_filtro_var.set('Todos SO')
    listar_maquinas()

def ordenar_maquinas_por_nome():
    maquinas.sort(key=lambda x: x['nome'])
    listar_maquinas()

def ordenar_maquinas_por_ip():
    maquinas.sort(key=lambda x: x['ip'])
    listar_maquinas()

def monitorar_maquinas():
    while monitoramento_ativo:
        for maquina in maquinas:
            ip = maquina['ip']
            resultado = ping(ip)
            with open('log_ping.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([ip, resultado])
        time.sleep(60)

try:
    with open('dados_maquinas.json', 'r') as file:
        data = json.load(file)
        maquinas = data.get('maquinas', [])
except FileNotFoundError:
    maquinas = []

if not os.path.exists('log_ping.csv'):
    with open('log_ping.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['IP', 'Resultado do Ping'])

app = tk.Tk()
app.title('Cadastro de Máquinas')
app.geometry('900x1100')
app.resizable(False, False)
app.iconbitmap('icone_app.ico')

add_icon = Image.open('add_icon.png')
add_icon = add_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
add_icon = ImageTk.PhotoImage(add_icon)

edit_icon = Image.open('edit_icon.png')
edit_icon = edit_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
edit_icon = ImageTk.PhotoImage(edit_icon)

delete_icon = Image.open('delete_icon.png')
delete_icon = delete_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
delete_icon = ImageTk.PhotoImage(delete_icon)

ping_icon = Image.open('ping_icon.png')  # Substitua 'ping_icon.png' pelo ícone do botão de ping
ping_icon = ping_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
ping_icon = ImageTk.PhotoImage(ping_icon)

filtrar_icon = Image.open('filtrar_icon.png')
filtrar_icon = filtrar_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
filtrar_icon = ImageTk.PhotoImage(filtrar_icon)

limpar_filtro_icon = Image.open('limpar_filtro_icon.png')
limpar_filtro_icon = limpar_filtro_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
limpar_filtro_icon = ImageTk.PhotoImage(limpar_filtro_icon)

pesquisar_icon = Image.open('pesquisar_icon.png')
pesquisar_icon = pesquisar_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
pesquisar_icon = ImageTk.PhotoImage(pesquisar_icon)

limpar_pesquisa_icon = Image.open('limpar_pesquisa_icon.png')
limpar_pesquisa_icon = limpar_pesquisa_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
limpar_pesquisa_icon = ImageTk.PhotoImage(limpar_pesquisa_icon)

sair_icon = Image.open('sair_icon.png')
sair_icon = sair_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
sair_icon = ImageTk.PhotoImage(sair_icon)

json_icon = Image.open('json_icon.png')
json_icon = json_icon.resize((20, 20), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)
json_icon = ImageTk.PhotoImage(json_icon)

categorias = ['Desktop ', 'Notebook ', 'Aparelhos Moveis', 'Servidores/Getaway']
sistemas_operacionais = ['Windows', 'Linux', 'macOS', 'Android', 'iOS', 'Windows']

frame = ttk.Frame(app, padding=20)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

pesquisa_label = ttk.Label(frame, text='Pesquisar Máquinas:', font=('Helvetica', 20))
pesquisa_label.grid(row=12, column=0, padx=10, pady=5, sticky='e')

pesquisa_entry = ttk.Entry(frame, font=('Helvetica', 20))
pesquisa_entry.grid(row=12, column=1, padx=10, pady=5, sticky='we')

pesquisa_btn = ttk.Button(frame, text='Pesquisar', command=pesquisar_maquinas)
pesquisa_btn.grid(row=13, column=0, columnspan=1, padx=10, pady=5, sticky='we')

titulo_label = ttk.Label(frame, text='Cadastro de Máquinas', font=('Helvetica', 36, 'bold'))
titulo_label.grid(row=0, column=0, columnspan=3, padx=10, pady=30)

nome_label = ttk.Label(frame, text='Nome da Máquina:', font=('Helvetica', 20))
nome_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
nome_entry = ttk.Entry(frame, font=('Helvetica', 20))
nome_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

ip_label = ttk.Label(frame, text='IP da Máquina:', font=('Helvetica', 20))
ip_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
ip_entry = ttk.Entry(frame, font=('Helvetica', 20))
ip_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

categoria_filtro_var = tk.StringVar()
categoria_filtro_var.set('Todas Categorias')  # Valor padrão (todas as categorias)
categoria_combobox = ttk.Combobox(frame, font=('Helvetica', 16), textvariable=categoria_filtro_var, values=['Todas Categorias'] + categorias)
categoria_combobox.grid(row=10, column=0, columnspan=1, padx=10, pady=5, sticky='we')

sistema_operacional_filtro_var = tk.StringVar()
sistema_operacional_filtro_var.set('Todos SO')
sistema_operacional_combobox = ttk.Combobox(frame, font=('Helvetica', 16), textvariable=sistema_operacional_filtro_var, values=['Todos SO'] + sistemas_operacionais)
sistema_operacional_combobox.grid(row=10, column=1, columnspan=1, padx=10, pady=5, sticky='we')

categoria_label = ttk.Label(frame, text='Categoria:', font=('Helvetica', 20))
categoria_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
categoria_var = tk.StringVar()
categoria_combobox = ttk.Combobox(frame, font=('Helvetica', 16), textvariable=categoria_var, values=categorias)
categoria_combobox.grid(row=3, column=1, padx=10, pady=5, sticky='w')

sistema_operacional_label = ttk.Label(frame, text='Sistema Operacional:', font=('Helvetica', 20))
sistema_operacional_label.grid(row=4, column=0, padx=10, pady=5, sticky='e')
sistema_operacional_var = tk.StringVar()
sistema_operacional_combobox = ttk.Combobox(frame, font=('Helvetica', 16), textvariable=sistema_operacional_var, values=sistemas_operacionais)
sistema_operacional_combobox.grid(row=4, column=1, padx=10, pady=5, sticky='w')

def limpar_pesquisa():
    pesquisa_entry.delete(0, tk.END)
    listar_maquinas()

limpar_btn = ttk.Button(frame, text='Limpar Filtros', command=limpar_filtros)
limpar_btn.grid(row=11, column=1, columnspan=1, padx=10, pady=5, sticky='we')

adicionar_btn = ttk.Button(frame, text='Adicionar', image=add_icon, compound=tk.LEFT, command=adicionar_maquina)
adicionar_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky='we')

lista_maquinas = tk.Listbox(frame, font=('Helvetica', 18), height=8, bg='#FFFFFF', selectbackground='#007BFF', activestyle='none')
lista_maquinas.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky='we')

filtro_btn = ttk.Button(frame, text='Filtrar', image=filtrar_icon, compound=tk.LEFT, command=filtrar_por_categoria_e_so)
filtro_btn.grid(row=11, column=0, columnspan=1, padx=10, pady=5, sticky='we')

limpar_pesquisa_btn = ttk.Button(frame, text='Limpar Pesquisa', image=limpar_pesquisa_icon, compound=tk.LEFT, command=limpar_pesquisa)
limpar_pesquisa_btn.grid(row=13, column=1, columnspan=1, padx=10, pady=5, sticky='we')

limpar_btn = ttk.Button(frame, text='Limpar Filtros', image=limpar_filtro_icon, compound=tk.LEFT, command=limpar_filtros)
limpar_btn.grid(row=11, column=1, columnspan=1, padx=10, pady=5, sticky='we')

pesquisa_btn = ttk.Button(frame, text='Pesquisar', image=pesquisar_icon, compound=tk.LEFT, command=pesquisar_maquinas)
pesquisa_btn.grid(row=13, column=0, columnspan=1, padx=10, pady=5, sticky='we')

listar_maquinas()

# Adicionando botão para sair e mostrar a quantidade de máquinas cadastradas
sair_btn = ttk.Button(frame, text='Sair', image=sair_icon, compound=tk.LEFT, command=sair)
sair_btn.grid(row=14, column=1, columnspan=1, padx=10, pady=10, sticky='we')

quantidade_label = ttk.Label(frame, text='', font=('Helvetica', 14, 'bold'))
quantidade_label.grid(row=15, column=0, columnspan=2, padx=10, pady=5, sticky='we')
exibir_quantidade_maquinas()

# Adicionando scrollbar para a lista de máquinas
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=lista_maquinas.yview)
scrollbar.grid(row=6, column=2, pady=5, sticky='ns')
lista_maquinas.config(yscrollcommand=scrollbar.set)

view_json_btn = ttk.Button(frame, text='Visualizar JSON', image=json_icon, compound=tk.LEFT, command=visualizar_json)
view_json_btn.grid(row=14, column=0, columnspan=1, padx=10, pady=5, sticky='we')

excluir_btn = ttk.Button(frame, text='Excluir', image=delete_icon, compound=tk.LEFT, command=excluir_maquina)
excluir_btn.grid(row=7, column=0, padx=10, pady=5, sticky='we')

editar_btn = ttk.Button(frame, text='Editar', image=edit_icon, compound=tk.LEFT, command=editar_maquina)
editar_btn.grid(row=7, column=1, padx=10, pady=5, sticky='we')

ping_text = tk.StringVar()
ping_text.set('Ping')
ping_btn = ttk.Button(frame, textvariable=ping_text, image=ping_icon, compound=tk.LEFT, command=ping_ip)
ping_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=20, sticky='we')

monitoramento_ativo = False

def alternar_monitoramento():
    global monitoramento_ativo
    if not monitoramento_ativo:  # Se o monitoramento ainda não estiver ativo
        if messagebox.askyesno('Confirmação', 'Deseja iniciar o monitoramento?'):
            monitoramento_ativo = True
            monitoramento_btn.config(text='Parar Monitoramento', style='Red.TButton')
            monitoramento_thread = threading.Thread(target=monitorar_maquinas)
            monitoramento_thread.start()
    else:  # Caso contrário, se o monitoramento já estiver ativo
        monitoramento_ativo = False
        monitoramento_btn.config(text='Iniciar Monitoramento', style='Green.TButton')
        
# Botão para iniciar/parar o monitoramento contínuo
monitoramento_btn = ttk.Button(frame, text='Iniciar Monitoramento', style='Green.TButton', command=alternar_monitoramento)
monitoramento_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky='we')

# Associe a função deletar_maquina ao evento da tecla "Delete"
lista_maquinas.bind('<Delete>', deletar_maquina)

# Estilo para o botão de monitoramento
app.style = ttk.Style()
app.style.configure('Red.TButton', foreground='black', background='red', font=('Helvetica', 12, 'bold'))
app.style.configure('Green.TButton', foreground='black', background='green', font=('Helvetica', 12, 'bold'))

lista_maquinas.bind('<<ListboxSelect>>', on_listbox_select)

# Execução do aplicativo
app.protocol("WM_DELETE_WINDOW", sair)  # Chamar a função sair quando o botão de fechar for pressionado

app.mainloop()
