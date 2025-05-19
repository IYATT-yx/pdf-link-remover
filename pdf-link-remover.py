from uimain import Main
from buildtime import buildTime

import tkinter as tk
import os

def main():
    root = tk.Tk()
    root.title(f"PDF 链接移除器（IYATT-yx iyatt@iyatt.com {buildTime}）")
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