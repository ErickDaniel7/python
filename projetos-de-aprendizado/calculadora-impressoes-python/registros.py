import tkinter as tk
from tkinter import filedialog
import openpyxl
import os
from tkinter import ttk

#Author: Erick Daniel Teixeira Vier

def calcular_paginas(planilha):
    wb = openpyxl.load_workbook(planilha)
    sheet = wb.active

    coluna_paginas = 'G'
    coluna_documentos = 'H'
    coluna_paginas_impressas = 'I'

    documentos = sheet.max_row - 1
    paginas = 0

    for row in sheet.iter_rows(min_row=2, values_only=True):
        paginas_impressas = row[sheet[f'{coluna_paginas_impressas}1'].column - 1]
        if paginas_impressas:
            paginas += paginas_impressas

    sheet[f'{coluna_documentos}1'] = 'Documentos Impressos'
    sheet[f'{coluna_documentos}2'] = f'=CONT.NÚM({coluna_paginas}2:{coluna_paginas}101)'
    
    sheet[f'{coluna_paginas_impressas}1'] = 'Página(s) Impressas'
    sheet[f'{coluna_paginas_impressas}2'] = f'=SOMA({coluna_paginas}2:{coluna_paginas}102)'

    nome_planilha = os.path.basename(planilha)
    data = nome_planilha.split()[2].split(".")[0]
    return documentos, paginas, nome_planilha, data

def calcular_planilha():
    arquivo = filedialog.askopenfilename(filetypes=[('Planilhas Excel', '*.xlsx')])
    if arquivo:
        documentos, paginas, nome_planilha, data = calcular_paginas(arquivo)
        resultado_text.insert(tk.END, "Planilha selecionada: ")
        resultado_text.insert(tk.END, nome_planilha + "\n", "bold")
        resultado_text.insert(tk.END, "Quantidade de documentos: ")
        resultado_text.insert(tk.END, str(documentos) + "\n", "bold")
        resultado_text.insert(tk.END, "Quantidade de páginas impressas: ")
        resultado_text.insert(tk.END, str(paginas) + "\n", "bold")
        resultado_text.insert(tk.END, "\n")

def calcular_planilhas():
    global total_documentos
    global total_paginas
    arquivos = filedialog.askopenfilenames(filetypes=[('Planilhas Excel', '*.xlsx')])
    total_documentos = 0
    total_paginas = 0

    for arquivo in arquivos:
        documentos, paginas, nome_planilha, data = calcular_paginas(arquivo)
        resultado_text.insert(tk.END, "Planilha selecionada: ")
        resultado_text.insert(tk.END, nome_planilha + "\n", "bold")
        resultado_text.insert(tk.END, "Quantidade de documentos: ")
        resultado_text.insert(tk.END, str(documentos) + "\n", "bold")
        resultado_text.insert(tk.END, "Quantidade de páginas impressas: ")
        resultado_text.insert(tk.END, str(paginas) + "\n", "bold")
        resultado_text.insert(tk.END, "\n")
        total_documentos += documentos
        total_paginas += paginas

    resultado_text.insert(tk.END, "Quantidade total de documentos: ")
    resultado_text.insert(tk.END, str(total_documentos) + "\n", "bold")
    resultado_text.insert(tk.END, "Quantidade total de páginas impressas: ")
    resultado_text.insert(tk.END, str(total_paginas) + "\n", "bold")
    resultado_text.insert(tk.END, "\n")

def salvar_arquivo():
    global total_documentos
    global total_paginas
    nome_arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[('Arquivos de Texto', '*.txt')])
    if nome_arquivo:
        with open(nome_arquivo, 'w') as file:
            file.write("Quantidade total de documentos: " + str(total_documentos) + "\n")
            file.write("Quantidade total de páginas impressas: " + str(total_paginas) + "\n")
        resultado_text.insert(tk.END, "Arquivo salvo com sucesso!\n\n", "bold")

def limpar_resultado():
    resultado_text.delete("1.0", tk.END)
    global total_documentos
    global total_paginas
    total_documentos = 0
    total_paginas = 0

janela = tk.Tk()
janela.title("Calculadora de Planilhas")
janela.geometry("555x800")

titulo_label = tk.Label(janela, text="Calculadora de Planilhas", font=("Algerian", 24, "bold"), pady=10)
titulo_label.pack()

imagem_calculadora = tk.PhotoImage(file="calculadora.jpg")

fator_redimensionamento = 2  
imagem_calculadora_redimensionada = imagem_calculadora.subsample(fator_redimensionamento, fator_redimensionamento)
label_imagem = tk.Label(janela, image=imagem_calculadora_redimensionada)
label_imagem.pack(pady=10)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

style = ttk.Style()
style.configure('Custom.TButton', font=("Helvetica", 12), padding=10)

botao_planilha_unica = ttk.Button(frame_botoes, text="Selecionar uma Planilha", command=calcular_planilha, style='Custom.TButton')
botao_planilha_unica.pack(side=tk.LEFT, padx=10)

botao_planilhas_varias = ttk.Button(frame_botoes, text="Selecionar Várias Planilhas", command=calcular_planilhas, style='Custom.TButton')
botao_planilhas_varias.pack(side=tk.LEFT, padx=10)

botao_salvar = ttk.Button(janela, text="Salvar Resultados", command=salvar_arquivo, style='Custom.TButton')
botao_salvar.pack(pady=10)

resultado_text = tk.Text(janela, height=10, width=48, font=("Helvetica", 14))
resultado_text.pack(pady=10)

resultado_text.tag_configure("bold", font=("Helvetica", 14, "bold"))

botao_limpar = ttk.Button(janela, text="Limpar", command=limpar_resultado, style='Custom.TButton')
botao_limpar.pack(side=tk.TOP, pady=12) 

total_documentos = 0
total_paginas = 0

janela.mainloop()
