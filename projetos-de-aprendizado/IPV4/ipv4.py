import socket
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PrinterMapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detecção de IPV4 do Adaptador Ethernet 2 e Mapeamento de Impressora")
        self.root.geometry("830x430")
        self.root.configure(bg="#f0f0f0")  # Background color

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")  # Use a different theme for a modern look

        self.style.configure("Title.TLabel", font=("Arial", 24, "bold"), foreground="#333", background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("Arial", 18, "bold"), foreground="#007acc", background="#f0f0f0")
        self.style.configure("Info.TLabel", font=("Arial", 12), foreground="#555", background="#f0f0f0")
        self.style.configure("Name.TLabel", font=("Arial", 18, "bold"), foreground="#333", background="#f0f0f0")
        self.style.configure("Value.TLabel", font=("Arial", 14), foreground="#333", background="#f0f0f0")
        self.style.configure("Red.TButton", font=("Arial", 14), foreground="white", background="#d9534f", padding=10)  # Red
        self.style.configure("Green.TButton", font=("Arial", 14), foreground="white", background="#5cb85c", padding=10)  # Green
        self.style.configure("Custom.TFrame", background="#f0f0f0")

        self.frame = ttk.Frame(self.root, padding=20, style="Custom.TFrame")
        self.frame.pack(fill="both", expand=True)

        ## Carregar as imagens com tamanho ajustado para ficarem pequenas
        self.left_image = tk.PhotoImage(file="F:/ipv4/IMG/mapeamento.png")
        self.left_image = self.left_image.subsample(6, 6)  # Reduzir ainda mais o tamanho

        self.right_image = tk.PhotoImage(file="F:/ipv4/IMG/zebrazd220.png")
        self.right_image = self.right_image.subsample(6, 6)  # Reduzir ainda mais o tamanho

        # Adicionar os labels para exibir as imagens
        self.left_image_label = ttk.Label(self.frame, image=self.left_image, background=self.root.cget("bg"), compound="top")
        self.left_image_label.pack(side="left", padx=5, pady=(250, 5))  # Ajuste o valor de pady para mover a imagem para baixo

        self.right_image_label = ttk.Label(self.frame, image=self.right_image, background=self.root.cget("bg"), compound="top")
        self.right_image_label.pack(side="right", padx=10, pady=(250, 10))  # Ajuste o valor de pady para mover a imagem para baixo

        self.title_label = ttk.Label(self.frame, text="Detecção de Adaptador Ethernet 2", style="Title.TLabel")
        self.title_label.pack(pady=(0, 5))

        self.header_label = ttk.Label(self.frame, text="Mapear Impressora LPT2", style="Header.TLabel", anchor="center")
        self.header_label.pack(fill="x", pady=(5, 10))

        self.info_label = ttk.Label(self.frame, text="Programa criado por", style="Info.TLabel")
        self.info_label.pack(pady=(5, 0))

        self.name_label = ttk.Label(self.frame, text="ERICK", style="Name.TLabel")
        self.name_label.pack(pady=(0, 5))

        self.separator = ttk.Separator(self.frame, orient="horizontal")
        self.separator.pack(fill="x", pady=10)

        self.ipv4_label = ttk.Label(self.frame, text="Endereço IPv4 do Adaptador Ethernet 2:", style="Value.TLabel")
        self.ipv4_label.pack(pady=5)

        self.ipv4_value = tk.StringVar()
        self.ipv4_display = ttk.Label(self.frame, textvariable=self.ipv4_value, style="Value.TLabel", relief="solid", width=25, anchor="center")
        self.ipv4_display.pack(pady=5)

        self.unmap_button = ttk.Button(self.frame, text="Desmapear Impressora", command=self.unmap_printer, style="Red.TButton")
        self.unmap_button.pack(pady=10)

        self.map_button = ttk.Button(self.frame, text="Mapear Impressora", command=self.map_printer, style="Green.TButton")
        self.map_button.pack(pady=10)

        self.update_ipv4()

    def update_ipv4(self):
        ipv4_ethernet2 = self.get_ipv4_ethernet2()
        self.ipv4_value.set(ipv4_ethernet2 if ipv4_ethernet2 else "Não disponível")

    def get_ipv4_ethernet2(self):
        try:
            hostname = socket.gethostname()
            ip_addresses = socket.gethostbyname_ex(hostname)[-1]
            ipv4_ethernet2 = [ip for ip in ip_addresses if ip.startswith("10.")]
            return ipv4_ethernet2[0] if ipv4_ethernet2 else ""
        except socket.gaierror:
            return ""

    def is_lpt2_mapped(self):
        try:
            subprocess.run("net use lpt2", check=True, shell=True, stdout=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    def unmap_printer(self):
        try:
            subprocess.run("net use lpt2 /delete", check=True, shell=True, stdout=subprocess.PIPE)
            self.update_ipv4()
            messagebox.showinfo("Desmapear Impressora", "A impressora foi desmapeada da porta LPT2.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao desmapear a impressora:\n{e}")

    def map_printer(self):
        ipv4_ethernet2 = self.get_ipv4_ethernet2()

        if ipv4_ethernet2:
            self.unmap_printer()
            command = f"net use lpt2 \\\\{ipv4_ethernet2}\\ZD220 /persistent:yes"
            try:
                subprocess.run(command, check=True, shell=True)
                self.ipv4_value.set(ipv4_ethernet2)
                message = f"A impressora foi mapeada em LPT2 com o IP {ipv4_ethernet2}.\n\nVocê pode agora imprimir usando a porta LPT2."
                messagebox.showinfo("Mapeamento concluído", message)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao mapear a impressora:\n{e}")
        else:
            messagebox.showerror("Erro", "Não foi possível obter o endereço IPv4 do Adaptador Ethernet 2.")

def main():
    root = tk.Tk()
    app = PrinterMapperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
