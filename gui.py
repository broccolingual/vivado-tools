import os
import re
import subprocess
import threading

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

import tcl


class MyApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()
        self.title('Vivado Tools')
        self.geometry('640x480')
        self.resizable(width=False, height=False)

        self.frame_dnd = frameDnD(self)
        self.frame_dnd.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.slider = progressBar(self)
        self.slider.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.frame_log = frameLog(self)
        self.frame_log.grid(row=2, column=0, rowspan=1,
                            padx=5, pady=5, sticky='nsew')

        self.button = ttk.Button(self, text='Run', command=self.run)
        self.button.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def run(self):
        if self.frame_dnd.path == "":
            messagebox.showerror(
                'Error', 'Please load a Vivado project file first')
            return
        elif os.path.splitext(self.frame_dnd.path)[1] != '.xpr':
            messagebox.showerror(
                'Error', 'Please load a Vivado project file with .xpr extension')
            return

        self.slider.start()
        self.thread = threading.Thread(target=self.process)
        self.thread.start()

    def process(self):
        project_dir, project_name, bit_path, mcs_path = tcl.get_project_paths(
            self.frame_dnd.path)
        tcl.generate_tcl(self.frame_dnd.path, bit_path, mcs_path)
        p = tcl.run_tcl()
        for line in p.stdout:
            pattern = r"(INFO|ERROR|WARNING): (.+)"
            match = re.match(pattern, line)
            if match:
                if match.group(1) == 'ERROR':
                    messagebox.showerror('Error', match.group(2))
            self.frame_log.log.insert('end', line)
            self.frame_log.log.see('end')
        try:
            outs, errs = p.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            self.slider.stop()
        finally:
            p.terminate()
            self.slider.stop()


class frameDnD(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, padx=5, pady=5, height=300)
        self.path = ""
        self.text = tk.StringVar()
        self.text.set('Drop Vivado project file here')
        self.label = tk.Label(self, textvariable=self.text)
        self.label.pack(expand=True, fill='both')
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drag_and_drop)
        self.pack(expand=True, fill='both')

    def drag_and_drop(self, event):
        self.path = event.data
        self.text.set(f"Loaded file: {self.path}")


class progressBar(ttk.Progressbar):
    def __init__(self, parent):
        super().__init__(parent, orient='horizontal', mode='indeterminate')

    def update(self, value):
        self['value'] = value


class frameLog(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Log', padx=5, pady=5)
        self.log = tk.Text(self)
        self.scroll = tk.Scrollbar(self, command=self.log.yview)
        self.log.config(yscrollcommand=self.scroll.set)
        self.log.pack(side='left', fill='both', expand=True)
        self.scroll.pack(side='right', fill='y')


if __name__ == '__main__':
    app = MyApp()
    app.deiconify()
    app.mainloop()
