from pdftools import PdfTools

import tkinter as tk
from tkinter import filedialog
import os

class Main(tk.Frame):
    delimiter = '|'

    def __init__(self, master):
        super().__init__(master)
        self.pack()

    def create(self):
        tk.Label(self, text='目标文件：').grid(row=0, column=0, sticky=tk.W)
        tk.Label(self, text='移除元素包含的文本（默认移除包含链接的元素）：').grid(row=1, column=0, sticky=tk.W)

        self.filesValue = tk.StringVar()
        self.keyTextValue = tk.StringVar()

        tk.Entry(self, textvariable=self.filesValue, width=100).grid(row=0, column=1, sticky=tk.EW)
        tk.Entry(self, textvariable=self.keyTextValue).grid(row=1, column=1, sticky=tk.EW)

        tk.Button(self, text='选择文件', command=self.onOpenFiles).grid(row=0, column=2, sticky=tk.NSEW)

        self.executableButton = tk.Button(self, text='执行', bd=5, command=self.onExecutable)
        self.executableButton.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW)
        
    def onOpenFiles(self):
        files = filedialog.askopenfilenames(title='选择文件', filetypes=[('PDF', '*.pdf')])
        files = Main.delimiter.join(files)
        self.filesValue.set(files)

    def getInput(self) -> tuple[list, str]:
        files = self.filesValue.get()
        files = files.strip()
        if files == '':
            files = None
        else:
            files = files.split(Main.delimiter)
            files = [file.strip() for file in files]
            files = [os.path.normpath(file) for file in files]

        keyText = self.keyTextValue.get()
        keyText = keyText.strip()
        if keyText == '':
            keyText = None

        return files, keyText
    
    def modifyExecutableButtonText(self, text: str):
        self.executableButton.config(text=text)

    def resetExecutableButtonText(self, time=3000):
        self.after(time, self.modifyExecutableButtonText, '执行')

    def checkFilesExist(self, files: list) -> str:
        for file in files:
            if not os.path.exists(file):
                return file
        return None

    def onExecutable(self):
        files, keyText = self.getInput()
        if files is None:
            self.modifyExecutableButtonText('请输入或选择文件后，再点击执行')
            self.resetExecutableButtonText()
            return
        
        result = self.checkFilesExist(files)
        if result is not None:
            self.modifyExecutableButtonText(f'{result}：文件不存在，请纠正后重试')
            self.resetExecutableButtonText(time=5000)
            return
        
        nums = len(files)
        for count in range(nums):
            file = files[count]
            self.modifyExecutableButtonText(f'{count+1}/{nums} {file}：正在处理中...')
            PdfTools.removeUrlTextElements(file, file + '.pdf', keyText)
        self.modifyExecutableButtonText(f'{nums}个文件处理完成')
        self.resetExecutableButtonText()

        

