import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class ContactManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Contact Manager")
        master.geometry("800x600")

        # Define the specific columns you want
        self.columns = ['Name', 'Course', 'Age', 'Email', 'Phone', 'Parents Phone']
        self.df = self.load_data()

        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Contact List Frame
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Contacts", padding="10")
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Details Frame
        self.details_frame = ttk.LabelFrame(self.main_frame, text="Details", padding="10")
        self.details_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Input Frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Add New Contact", padding="10")
        self.input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Contact Listbox
        self.contact_listbox = tk.Listbox(self.list_frame, height=15)
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.contact_listbox.bind("<<ListboxSelect>>", self.on_contact_select)

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.contact_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_listbox.config(yscrollcommand=self.scrollbar.set)

        # Contact Details
        self.detail_labels = {}
        self.detail_text_vars = {}
        for row_idx, col in enumerate(self.columns):
            label = ttk.Label(self.details_frame, text=f"{col}:")
            label.grid(row=row_idx, column=0, sticky="w", pady=2)

            text_var = tk.StringVar()
            self.detail_text_vars[col] = text_var
            entry_widget = ttk.Entry(self.details_frame, textvariable=text_var, state='readonly')
            entry_widget.grid(row=row_idx, column=1, sticky="ew", pady=2, padx=5)

        self.details_frame.grid_columnconfigure(1, weight=1)

        # Input Fields
        self.input_vars = {}
        for i, col in enumerate(self.columns):
            label = ttk.Label(self.input_frame, text=f"{col}:")
            label.grid(row=i, column=0, sticky="w", pady=2)

            input_var = tk.StringVar()
            entry = ttk.Entry(self.input_frame, textvariable=input_var, width=30)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            self.input_vars[col] = input_var

        # Buttons
        self.add_button = ttk.Button(self.input_frame, text="Add New Contact", command=self.add_contact)
        self.add_button.grid(row=len(self.columns), column=0, columnspan=2, pady=10)

        self.delete_button = ttk.Button(self.input_frame, text="Delete Selected Contact", 
                                      command=self.delete_contact)
        self.delete_button.grid(row=len(self.columns)+1, column=0, columnspan=2, pady=5)

        # New JSON Export Button
        self.export_json_button = ttk.Button(self.input_frame, text="Export to JSON", 
                                           command=self.export_to_json)
        self.export_json_button.grid(row=len(self.columns)+2, column=0, columnspan=2, pady=5)

        self.input_frame.grid_columnconfigure(1, weight=1)

        self.populate_listbox()
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_data(self):
        try:
            df = pd.read_csv('contacts.csv')
            # Ensure all required columns exist
            for col in self.columns:
                if col not in df.columns:
                    df[col] = ""
            df = df[self.columns]  # Keep only the columns we want
            if 'ID' not in df.columns:
                df['ID'] = range(1, len(df) + 1)
            df = df.set_index('ID')
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.columns)
            df['ID'] = range(1, 1)  # Empty DataFrame with ID column
            df = df.set_index('ID')
        return df

    def save_data(self):
        self.df.to_csv('contacts.csv')
    
    def populate_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for name in self.df['Name'].tolist():
            self.contact_listbox.insert(tk.END, name)

    def on_contact_select(self, event):
        selected_indices = self.contact_listbox.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        selected_name = self.contact_listbox.get(selected_index)
        
        try:
            selected_contact = self.df[self.df['Name'] == selected_name].iloc[0]
            for col in self.columns:
                self.detail_text_vars[col].set(str(selected_contact[col]))
        except IndexError:
            pass

    def add_contact(self):
        new_data = {col: self.input_vars[col].get() for col in self.columns}
        
        if not new_data['Name'].strip():
            messagebox.showwarning("Input Error", "Name cannot be empty!")
            return
            
        new_id = self.df.index.max() + 1 if not self.df.empty else 1
        new_row = pd.DataFrame([new_data], index=[new_id])
        self.df = pd.concat([self.df, new_row])
        self.df = self.df.sort_values(by='Name')
        
        self.populate_listbox()
        for var in self.input_vars.values():
            var.set("")
        self.save_data()
        messagebox.showinfo("Success", f"Contact '{new_data['Name']}' added!")

    def delete_contact(self):
        selected_indices = self.contact_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")
            return
            
        selected_index = selected_indices[0]
        name_to_delete = self.contact_listbox.get(selected_index)
        
        # Delete from DataFrame
        self.df = self.df[self.df['Name'] != name_to_delete]
        
        # Update the listbox
        self.populate_listbox()
        
        # Clear the details view
        for col in self.columns:
            self.detail_text_vars[col].set("")
        
        # Save changes
        self.save_data()
        messagebox.showinfo("Success", f"Contact '{name_to_delete}' deleted!")

    def export_to_json(self):
        try:
            # Convert DataFrame to JSON
            json_data = self.df.reset_index().to_json(orient='records', indent=4)
            
            # Write to file
            with open('contacts.json', 'w') as f:
                f.write(json_data)
            
            messagebox.showinfo("Success", "Contacts exported to contacts.json")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def on_closing(self):
        self.save_data()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()