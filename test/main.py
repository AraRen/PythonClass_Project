import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
from youbikeTreeView import YoubikeTreeView
from threading import Timer
import datasource as ds

class TKLable(tk.Label):
    def __init__(self,parents,**kwargs):
        super().__init__(parents,**kwargs)
        helv26=tkFont.Font(family='微軟正黑體',size=12,weight='bold') #先設定字體格式
        self.config(font=helv26) #,foreground="#FFFFFF"

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #---------更新資料庫資料-----------------#
        try:
            ds.updata_sqlite_data()
        except Exception:
            messagebox.showerror("錯誤",'網路不正常\n將關閉應用程式\n請稍後再試')
            self.destroy()
        

        #---------建立介面------------------------
        #print(ds.lastest_datetime_data())
        topFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1)
        tk.Label(topFrame,text="台北市youbike及時資料",font=("arial", 24), bg="#333333", fg='#ffffff',padx=10,pady=10).pack(padx=10,pady=20)
        topFrame.pack(pady=20)
        #---------------------------------------

    #--↓↓--↓↓--↓↓--↓↓--↓↓--參考內容--↓↓--↓↓--↓↓--↓↓--↓↓--↓↓--↓↓--#
        #新增notebook(分頁)
        notebook = ttk.Notebook(self)
        notebook.pack(pady=0, expand=True)

        #新增frames
        MapFrame = ttk.Frame(notebook, width=800, height=50)
        self.KeywordFrame = ttk.Frame(notebook, width=800, height=50)
        
        MapFrame.pack(fill='both', expand=True)
        
        #將frames放到notebook
        notebook.add(MapFrame, text='以行政區分類地圖顯示定位')

        
        #bottomFrame.pack(fill='both', expand=True)
        #notebook.add(bottomFrame, text='各站點清單附帶搜尋功能')
        #------區域時段搜尋框架--------
        #放選單的框架
        mainFrame = tk.Frame(MapFrame,width=1000,height=200)
        mainFrame.pack()

        #建立關鍵字的label
#        TKLable(mainFrame, text="以下可擇一搜尋，搜尋到的結果雙擊兩下可以到地圖區看到位置",bd=3).grid(row=0,column=0,columnspan=4)

        #建立Combo的Label
#        TKLable(mainFrame, text="請選擇行政區",bd=3).grid(row=1,column=0)
        #抓取台北行政區
#        self.TaipeiArea_dict=ds.Get_TaipeiArea()
        #台北市行政區下拉選單
#        self.TaipeiAreaValue = tk.StringVar()
#        self.TaipeiArea_Combo = ttk.Combobox(mainFrame,values=list(self.TaipeiArea_dict.keys()),justify="center",textvariable=self.TaipeiAreaValue)
#        self.TaipeiArea_Combo.grid(row=1,column=1)  
#        self.TaipeiArea_Combo.current(0)
    #--↑↑--↑↑--↑↑--↑↑--↑↑--參考內容--↑↑--↑↑--↑↑--↑↑--↑↑--↑↑--↑↑--#

        #----------建立搜尋------------------------
        middleFrame = ttk.LabelFrame(self,text='')
        tk.Label(middleFrame,text='站點名稱搜尋:').pack(side='left')
        search_entry = tk.Entry(middleFrame)
        search_entry.bind("<KeyRelease>", self.OnEntryClick)
        search_entry.pack(side='left')
        middleFrame.pack(fill='x',padx=20)
        #----------------------------------------

        #---------------建立treeView---------------
        bottomFrame = tk.Frame(self)
        
        self.youbikeTreeView = YoubikeTreeView(bottomFrame,show="headings",
                                               columns=('sno','sna','sarea','mday','ar','tot','sbi','bemp'),
                                               height=20)
        self.youbikeTreeView.pack(side='left')
        vsb = ttk.Scrollbar(bottomFrame, orient="vertical", command=self.youbikeTreeView.yview)
        vsb.pack(side='left',fill='y')
        self.youbikeTreeView.configure(yscrollcommand=vsb.set)
        bottomFrame.pack(pady=(0,30))
        #-------------------------------------------

        
        bottomFrame.pack(fill='both', expand=True)
        notebook.add(bottomFrame, text='各站點清單附帶搜尋功能')
    
    def OnEntryClick(self,event):
        searchEntry = event.widget
        #使用者輸入的文字
        input_word = searchEntry.get()
        if input_word == "":
            lastest_data = ds.lastest_datetime_data()
            self.youbikeTreeView.update_content(lastest_data)
        else:
            search_data = ds.search_sitename(word=input_word)
            self.youbikeTreeView.update_content(search_data)

def main():    
    def update_data(w:Window)->None:
        ds.updata_sqlite_data()
        #-----------更新treeView資料---------------
        lastest_data = ds.lastest_datetime_data()
        w.youbikeTreeView.update_content(lastest_data)

        w.after(10*60*1000,update_data,w) #每隔10分鐘

    window = Window()
    window.title('台北市youbike2.0')
    #window.geometry('600x300')
    #window.resizable(width=False,height=False)
    update_data(window)
    window.configure(background='#ffffff')
    window.mainloop()

if __name__ == '__main__':
    main()