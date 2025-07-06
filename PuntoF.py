import tkinter as tk
from tkinter import messagebox
import os

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación CRUD con Archivo de Texto")
        self.file_path = "datos.txt"
        
        # Crear el archivo si no existe
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write("")
        
        # Variables de control
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        
        # Interfaz gráfica
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Etiquetas
        tk.Label(main_frame, text="ID:").grid(row=0, column=0, sticky='w', pady=5)
        tk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky='w', pady=5)
        tk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        tk.Label(main_frame, text="Teléfono:").grid(row=3, column=0, sticky='w', pady=5)
        
        # Campos de entrada
        tk.Entry(main_frame, textvariable=self.id_var, width=30).grid(row=0, column=1, pady=5)
        tk.Entry(main_frame, textvariable=self.nombre_var, width=30).grid(row=1, column=1, pady=5)
        tk.Entry(main_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, pady=5)
        tk.Entry(main_frame, textvariable=self.telefono_var, width=30).grid(row=3, column=1, pady=5)
        
        # Botones CRUD
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(buttons_frame, text="Crear", command=self.create_record, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Leer", command=self.read_record, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Actualizar", command=self.update_record, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Eliminar", command=self.delete_record, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Limpiar", command=self.clear_fields, width=10).pack(side=tk.LEFT, padx=5)
        
        # Lista de registros
        self.listbox = tk.Listbox(main_frame, width=50, height=10)
        self.listbox.grid(row=5, column=0, columnspan=2, pady=10)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Cargar todos los registros al iniciar
        self.load_all_records()
    
    def load_all_records(self):
        self.listbox.delete(0, tk.END)
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if line.strip():
                        self.listbox.insert(tk.END, line.strip())
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo no encontrado")
    
    def on_select(self, event):
        try:
            index = self.listbox.curselection()[0]
            selected = self.listbox.get(index)
            id_, nombre, email, telefono = selected.split('|')
            self.id_var.set(id_.strip())
            self.nombre_var.set(nombre.strip())
            self.email_var.set(email.strip())
            self.telefono_var.set(telefono.strip())
        except IndexError:
            pass
    
    def clear_fields(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.email_var.set("")
        self.telefono_var.set("")
    
    def create_record(self):
        if not self.validate_fields():
            return
            
        id_ = self.id_var.get()
        nombre = self.nombre_var.get()
        email = self.email_var.get()
        telefono = self.telefono_var.get()
        
        # Verificar si el ID ya existe
        if self.id_exists(id_):
            messagebox.showerror("Error", "El ID ya existe")
            return
            
        with open(self.file_path, 'a') as file:
            file.write(f"{id_}|{nombre}|{email}|{telefono}\n")
        
        messagebox.showinfo("Éxito", "Registro creado correctamente")
        self.clear_fields()
        self.load_all_records()
    
    def read_record(self):
        id_ = self.id_var.get()
        if not id_:
            messagebox.showwarning("Advertencia", "Ingrese un ID para buscar")
            return
            
        found = False
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.startswith(id_ + '|'):
                    _, nombre, email, telefono = line.strip().split('|')
                    self.nombre_var.set(nombre.strip())
                    self.email_var.set(email.strip())
                    self.telefono_var.set(telefono.strip())
                    found = True
                    break
        
        if not found:
            messagebox.showinfo("Información", "Registro no encontrado")
    
    def update_record(self):
        if not self.validate_fields():
            return
            
        id_ = self.id_var.get()
        nombre = self.nombre_var.get()
        email = self.email_var.get()
        telefono = self.telefono_var.get()
        
        # Leer todos los registros y actualizar el correspondiente
        lines = []
        updated = False
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if line.startswith(id_ + '|'):
                        lines.append(f"{id_}|{nombre}|{email}|{telefono}\n")
                        updated = True
                    else:
                        lines.append(line)
            
            if updated:
                with open(self.file_path, 'w') as file:
                    file.writelines(lines)
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                self.load_all_records()
            else:
                messagebox.showerror("Error", "ID no encontrado para actualizar")
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo no encontrado")
    
    def delete_record(self):
        id_ = self.id_var.get()
        if not id_:
            messagebox.showwarning("Advertencia", "Ingrese un ID para eliminar")
            return
            
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
            return
            
        # Leer todos los registros y excluir el que se va a eliminar
        lines = []
        deleted = False
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if not line.startswith(id_ + '|'):
                        lines.append(line)
                    else:
                        deleted = True
            
            if deleted:
                with open(self.file_path, 'w') as file:
                    file.writelines(lines)
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.clear_fields()
                self.load_all_records()
            else:
                messagebox.showerror("Error", "ID no encontrado para eliminar")
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo no encontrado")
    
    def id_exists(self, id_):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if line.startswith(id_ + '|'):
                        return True
            return False
        except FileNotFoundError:
            return False
    
    def validate_fields(self):
        if not self.id_var.get():
            messagebox.showerror("Error", "El campo ID es obligatorio")
            return False
        if not self.nombre_var.get():
            messagebox.showerror("Error", "El campo Nombre es obligatorio")
            return False
        if not self.email_var.get():
            messagebox.showerror("Error", "El campo Email es obligatorio")
            return False
        if not self.telefono_var.get():
            messagebox.showerror("Error", "El campo Teléfono es obligatorio")
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()