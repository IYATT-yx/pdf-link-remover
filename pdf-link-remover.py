from uimain import Main

import tkinter as tk
import os

def main():
    root = tk.Tk()
    root.title("PDF 链接移除器")
    root.iconbitmap(
        os.path.join(
            os.path.dirname(__file__),
            'icon.ico'
        )
    )
    app = Main(root)
    app.create()
    root.mainloop()

if __name__ == '__main__':
    main()