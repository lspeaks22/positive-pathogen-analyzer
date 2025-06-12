import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

class PathogenDetectorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Positive Pathogen Detector")
        self.master.geometry("960x640")
        self.master.configure(bg="#d0ecf2")  #background

        #Header
        header = tk.Label(
            master,
            text="Pathogen Lab Result Viewer",
            font=("Courier", 24, "bold"),
            bg="#d0ecf2",
            fg="#003f5c",
            pady=20
        )
        header.pack()

        #Upload Button
        tk.Button(
            master,
            text="Upload CSV File",
            font=("Courier", 12),
            bg="#a7d7c5",
            fg="black",
            relief="raised",
            bd=2,
            command=self.upload_csv
        ).pack(pady=8)

        #Pathogen dropdown
        self.pathogen_var = tk.StringVar()
        self.pathogen_dropdown = ttk.Combobox(
            master,
            textvariable=self.pathogen_var,
            state="readonly",
            width=60,
            font=("Courier", 11)
        )
        self.pathogen_dropdown.pack(pady=10)

        #Filter Button
        tk.Button(
            master,
            text= "Filter by Pathogen",
            font=("Courier", 12),
            bg="#f2b5d4",
            fg="black",
            relief="raised",
            bd=2,
            command=self.filter_data
        ).pack(pady=6)

        #Table setup
        self.table = ttk.Treeview(master, show="headings")
        self.table.pack(expand=True, fill="both", pady=12, padx=10)

        #scrollbar
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        #Footer
        footer = tk.Label(
            master,
            font=("Courier", 10, "italic"),
            bg="#d0ecf2",
            fg="#5e5e5e",
            pady=10
        )
        footer.pack(side="bottom")

        self.df = None

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            self.df = pd.read_csv(file_path)

            if "Result" not in self.df.columns or "Pathogen" not in self.df.columns:
                raise ValueError("CSV must contain 'Result' and 'Pathogen' columns.")

            self.df = self.df[self.df["Result"].str.upper() == "POSITIVE"]
            unique_pathogens = sorted(self.df["Pathogen"].dropna().unique())

            if not unique_pathogens:
                messagebox.showinfo("No Positives", "No positive results found.")
                return

            self.pathogen_dropdown["values"] = unique_pathogens
            self.pathogen_dropdown.set(unique_pathogens[0])
            self.display_data(self.df)

        except Exception as e:
            messagebox.showerror("Error.", str(e))

    def filter_data(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Upload a CSV file first.")
            return

        selected_pathogen = self.pathogen_var.get()
        filtered = self.df[self.df["Pathogen"] == selected_pathogen]
        self.display_data(filtered)

    def display_data(self, dataframe):
        self.table.delete(*self.table.get_children())
        self.table["columns"] = list(dataframe.columns)
        for col in dataframe.columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=150)
        for _, row in dataframe.iterrows():
            self.table.insert("", "end", values=list(row))

if __name__ == "__main__":
    root = tk.Tk()
    app = PathogenDetectorApp(root)
    root.mainloop()
