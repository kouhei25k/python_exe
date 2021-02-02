import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from align_tap import AlignTap

# フォルダ指定の関数
def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    entry1.set(iDirPath)


# 実行ボタン押下時の実行関数
def conductMain():
    text = ""
    dirPath = entry1.get()
    
    if dirPath:
        align_tap = AlignTap(dirPath)
        text = align_tap.align_tap()
    if text:
         messagebox.showinfo("info", text)
    else:
        messagebox.showerror("error", "パスの指定がありません。")

if __name__ == "__main__":

    # rootの作成
    root = Tk()
    root.title("サンプル")

    # Frame1の作成
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=0, column=1, sticky=E)

    # 「フォルダ参照」ラベルの作成
    IDirLabel = ttk.Label(frame1, text="フォルダ参照＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)

    # 「フォルダ参照」エントリーの作成
    entry1 = StringVar()
    IDirEntry = ttk.Entry(frame1, textvariable=entry1, width=30)
    IDirEntry.pack(side=LEFT)

    # 「フォルダ参照」ボタンの作成
    IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
    IDirButton.pack(side=LEFT)

    # Frame3の作成
    frame3 = ttk.Frame(root, padding=10)
    frame3.grid(row=5,column=1,sticky=W)

    # 実行ボタンの設置
    button1 = ttk.Button(frame3, text="実行", command=conductMain)
    button1.pack(fill = "x", padx=30, side = "left")

    # キャンセルボタンの設置
    # button2 = ttk.Button(frame3, text=("閉じる"), command=quit)
    # button2.pack(fill = "x", padx=30, side = "left")

    #psd保存フラグ
    root.mainloop()