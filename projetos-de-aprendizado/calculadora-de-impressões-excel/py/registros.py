import os
import tkinter as tk
from tkinter import messagebox, filedialog
from github import Github
import datetime
from ttkthemes import ThemedTk
import glob
from PIL import Image, ImageTk
import keyboard

def on_key_press(event):
    if event.name == 'down':
        if window.focus_get() == id_entry:
            nome_usuario_entry.focus_set()
        elif window.focus_get() == nome_usuario_entry:
            id_usuario_entry.focus_set()
        elif window.focus_get() == id_usuario_entry:
            nome_arquivo_entry.focus_set()
        elif window.focus_get() == nome_arquivo_entry:
            estado_entry.focus_set()
        elif window.focus_get() == estado_entry:
            paginas_entry.focus_set()
        elif window.focus_get() == paginas_entry:
            documentos_impressos_entry.focus_set()
        elif window.focus_get() == documentos_impressos_entry:
            paginas_impressas_entry.focus_set()
    elif event.name == 'up':
        if window.focus_get() == paginas_impressas_entry:
            documentos_impressos_entry.focus_set()
        elif window.focus_get() == documentos_impressos_entry:
            paginas_entry.focus_set()
        elif window.focus_get() == paginas_entry:
            estado_entry.focus_set()
        elif window.focus_get() == estado_entry:
            nome_arquivo_entry.focus_set()
        elif window.focus_get() == nome_arquivo_entry:
            id_usuario_entry.focus_set()
        elif window.focus_get() == id_usuario_entry:
            nome_usuario_entry.focus_set()
        elif window.focus_get() == nome_usuario_entry:
            id_entry.focus_set()    

keyboard.on_press(on_key_press)

def registrar_impressoes():
    id = id_entry.get()
    nome_usuario = nome_usuario_entry.get()
    id_usuario = id_usuario_entry.get()
    nome_arquivo = nome_arquivo_entry.get()
    estado = estado_entry.get()
    paginas = paginas_entry.get()
    documentos_impressos = documentos_impressos_entry.get()
    paginas_impressas = paginas_impressas_entry.get()

    data_atual = datetime.date.today()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    hora_atual = datetime.datetime.now().strftime("%I:%M:%S %p")
    registro = f"{id},{nome_usuario},{id_usuario},{nome_arquivo},{estado},{paginas},{hora_atual} - {data_formatada},{documentos_impressos},{paginas_impressas}"

    nome_arquivo = f"registros_{data_atual}.txt"
    caminho_arquivo = os.path.join("F:/ERICK/Registros Impressões", nome_arquivo)
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    with open(caminho_arquivo, "a") as arquivo:
        arquivo.write(registro + "\n")

    # Iniciar sessão no GitHub
    ACCESS_TOKEN = "" #Token individualmente obtido
    REPO_OWNER = "ErickDaniel7" #Meu nome de usuario
    REPO_NAME = "registro-impressoes-python" #Nome do meu repositorio

    # Iniciar sessão no GitHub
    g = Github(ACCESS_TOKEN)
    repo = g.get_user(REPO_OWNER).get_repo(REPO_NAME)

    with open(caminho_arquivo, "r") as arquivo:
        conteudo = arquivo.read()

    arquivo_path = f"registros_{data_atual}.txt"
    arquivo_existe = False
    try:
        conteudo_arquivo = repo.get_contents(arquivo_path, ref="main")
        arquivo_existe = True
    except:
        pass

    if arquivo_existe:
        repo.update_file(conteudo_arquivo.path, "Atualização do registro diário de impressões", conteudo, conteudo_arquivo.sha, branch="main")
    else:
        repo.create_file(arquivo_path, "Registro diário de impressões", conteudo, branch="main")

    messagebox.showinfo("Registro de Impressões", "Registro salvo com sucesso!")

def visualizar_registros():
    registros_path = os.path.join("F:/ERICK/Registros Impressões", "registros_*.txt")
    registros_arquivos = glob.glob(registros_path)
    registros_arquivos.sort(reverse=True)
    if registros_arquivos:
        with open(registros_arquivos[0], "r") as arquivo:
            conteudo = arquivo.read()

        if conteudo:
            registros_formatados = []
            registros = conteudo.strip().split("\n")
            for registro in registros:
                informacoes = registro.strip().split(",")
                if len(informacoes) >= 9:  # Verificar se há elementos suficientes na lista
                    id_impressao = informacoes[0]
                    nome_usuario = informacoes[1]
                    id_usuario = informacoes[2]
                    nome_arquivo = informacoes[3]
                    estado = informacoes[4]
                    paginas = informacoes[5]
                    data_hora = informacoes[6].split("-")
                    data = data_hora[1].strip()
                    hora = data_hora[0].strip()
                    documentos_impressos = informacoes[7]
                    paginas_impressas = informacoes[8]

                    registro_formatado = f"ID: {id_impressao}\n" \
                                         f"Nome de Usuário: {nome_usuario}\n" \
                                         f"ID de Usuário: {id_usuario}\n" \
                                         f"Nome do Arquivo: {nome_arquivo}\n" \
                                         f"Estado: {estado}\n" \
                                         f"Páginas: {paginas}\n" \
                                         f"Documentos Impressos: {documentos_impressos}\n" \
                                         f"Páginas Impressas: {paginas_impressas}\n" \
                                         f"Data: {data}\n" \
                                         f"Hora: {hora}"

                    registros_formatados.append(registro_formatado)

            if registros_formatados:
                registros_exibicao = "\n\n".join(registros_formatados)

                # Criar uma nova janela para exibir os registros
                janela_registros = tk.Toplevel(window)
                janela_registros.title("Visualizar Registros")

                scrollbar = tk.Scrollbar(janela_registros)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                text_registros = tk.Text(janela_registros, yscrollcommand=scrollbar.set)
                text_registros.pack(fill="both", expand=True)

                text_registros.insert(tk.END, registros_exibicao)

                scrollbar.config(command=text_registros.yview)
            else:
                messagebox.showinfo("Visualizar Registros", "Nenhum registro encontrado.")
        else:
            messagebox.showinfo("Visualizar Registros", "Nenhum registro encontrado.")
    else:
        messagebox.showinfo("Visualizar Registros", "Nenhum registro encontrado.")

def editar_registro():
    file_path = filedialog.askopenfilename(title="Selecionar arquivo de registros")
    if not file_path:
        return

    with open(file_path, "r") as arquivo:
        registros = arquivo.readlines()

    editar_janela = tk.Tk()
    editar_janela.title("Editar Registro")
    editar_janela.geometry("500x400")  

    registros_listbox = tk.Listbox(editar_janela, selectmode=tk.SINGLE)
    registros_listbox.pack(fill="both", expand=True)

    for registro in registros:
        registros_listbox.insert(tk.END, registro)

    def editar_selecionado():
        selecionado = registros_listbox.curselection()
        if not selecionado:
            return

        indice = selecionado[0]

        registro_selecionado = registros[indice].strip()

        editar_registro_janela = tk.Toplevel(editar_janela)
        editar_registro_janela.title("Editar Registro")

        registro_text = tk.Text(editar_registro_janela)
        registro_text.pack(fill="both", expand=True)
        registro_text.insert(tk.END, registro_selecionado)

        def salvar_edicao():
            registro_editado = registro_text.get("1.0", tk.END).strip()

            registros[indice] = registro_editado + "\n"
            with open(file_path, "w") as arquivo:
                arquivo.writelines(registros)

            messagebox.showinfo("Editar Registro", "Registro editado com sucesso!")
            editar_registro_janela.destroy()

        salvar_button = tk.Button(editar_registro_janela, text="Salvar Edição", command=salvar_edicao)
        salvar_button.pack(pady=10)

    editar_selecionado_button = tk.Button(editar_janela, text="Editar Selecionado", command=editar_selecionado)
    editar_selecionado_button.pack(pady=10)

    editar_janela.mainloop()

def excluir_registro():
    file_path = filedialog.askopenfilename(title="Selecionar arquivo de registros")
    if not file_path:
        return

    with open(file_path, "r") as arquivo:
        registros = arquivo.readlines()

    excluir_janela = tk.Tk()
    excluir_janela.title("Excluir Registro")
    excluir_janela.geometry("500x400")  

    registros_listbox = tk.Listbox(excluir_janela, selectmode=tk.SINGLE)
    registros_listbox.pack(fill="both", expand=True)

    for registro in registros:
        registros_listbox.insert(tk.END, registro)

    def excluir_selecionado():
        # Obter o índice do registro selecionado
        selecionado = registros_listbox.curselection()
        if not selecionado:
            return

        indice = selecionado[0]

        with open(file_path, "w") as arquivo:
            registros.pop(indice)
            arquivo.writelines(registros)

        registros_listbox.delete(0, tk.END)
        for registro in registros:
            registros_listbox.insert(tk.END, registro)

        messagebox.showinfo("Excluir Registro", "Registro excluído com sucesso!")

    def excluir_todos():
        if messagebox.askyesno("Excluir Registros", "Tem certeza de que deseja excluir todos os registros?"):
            with open(file_path, "w") as arquivo:
                arquivo.write("")
            messagebox.showinfo("Excluir Registros", "Todos os registros foram excluídos com sucesso!")

    excluir_selecionado_button = tk.Button(excluir_janela, text="Excluir Selecionado", command=excluir_selecionado)
    excluir_selecionado_button.pack(pady=10)

    excluir_todos_button = tk.Button(excluir_janela, text="Excluir Todos", command=excluir_todos)
    excluir_todos_button.pack(pady=10)

    excluir_janela.mainloop()

window = ThemedTk(theme="equilux")  
window.title("Registro de Impressões")

imagem = Image.open("sp52s.jpg")
imagem = imagem.resize((250, 250))  

imagem_tk = ImageTk.PhotoImage(imagem)

imagem_label = tk.Label(window, image=imagem_tk)
imagem_label.grid(row=2, column=2, columnspan=2, rowspan=6, padx=10, pady=10)  # Definir a posição do widget na grade

canvas = tk.Canvas(window, width=250, height=30)
canvas.grid(row=1, column=2,columnspan=2, padx=10, pady=10)

canvas.create_rectangle(0, 0, 250, 30, fill="White")

nome_impressora = "RICOH Aficio SP 5210SF"
canvas.create_text(135, 15, text=nome_impressora, font=("Bernard MT Condensed", 15), fill="Black", justify="center")

id_label = tk.Label(window, text="ID:")
id_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)
id_entry = tk.Entry(window)
id_entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

nome_usuario_label = tk.Label(window, text="Nome de Usuário:")
nome_usuario_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.E)
nome_usuario_entry = tk.Entry(window)
nome_usuario_entry.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)

id_usuario_label = tk.Label(window, text="ID de Usuário:")
id_usuario_label.grid(row=2, column=0, pady=10, padx=10, sticky=tk.E)
id_usuario_entry = tk.Entry(window)
id_usuario_entry.grid(row=2, column=1, pady=10, padx=10, sticky=tk.W)

nome_arquivo_label = tk.Label(window, text="Nome do Arquivo:")
nome_arquivo_label.grid(row=3, column=0, pady=10, padx=10, sticky=tk.E)
nome_arquivo_entry = tk.Entry(window)
nome_arquivo_entry.grid(row=3, column=1, pady=10, padx=10, sticky=tk.W)

estado_label = tk.Label(window, text="Estado:")
estado_label.grid(row=4, column=0, pady=10, padx=10, sticky=tk.E)
estado_entry = tk.Entry(window)
estado_entry.grid(row=4, column=1, pady=10, padx=10, sticky=tk.W)

paginas_label = tk.Label(window, text="Páginas:")
paginas_label.grid(row=5, column=0, pady=10, padx=10, sticky=tk.E)
paginas_entry = tk.Entry(window)
paginas_entry.grid(row=5, column=1, pady=10, padx=10, sticky=tk.W)

documentos_impressos_label = tk.Label(window, text="Documentos Impressos:")
documentos_impressos_label.grid(row=6, column=0, pady=10, padx=10, sticky=tk.E)
documentos_impressos_entry = tk.Entry(window)
documentos_impressos_entry.grid(row=6, column=1, pady=10, padx=10, sticky=tk.W)

paginas_impressas_label = tk.Label(window, text="Páginas Impressas:")
paginas_impressas_label.grid(row=7, column=0, pady=10, padx=10, sticky=tk.E)
paginas_impressas_entry = tk.Entry(window)
paginas_impressas_entry.grid(row=7, column=1, pady=10, padx=10, sticky=tk.W)

registrar_button = tk.Button(window, text="Registrar Impressões", command=registrar_impressoes)
registrar_button.grid(row=8, column=0, pady=10, padx=10, sticky=tk.W)

visualizar_button = tk.Button(window, text="Visualizar Registros", command=visualizar_registros)
visualizar_button.grid(row=8, column=1, pady=10, padx=10, sticky=tk.E)

excluir_button = tk.Button(window, text="Excluir Registro", command=excluir_registro)
excluir_button.grid(row=8, column=2, pady=10, padx=10, sticky=tk.E)

editar_button = tk.Button(window, text="Editar Registro", command=editar_registro)
editar_button.grid(row=8, column=3, pady=10, padx=10, sticky=tk.E)

window.mainloop()
