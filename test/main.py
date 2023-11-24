import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
from youbikeTreeView import YoubikeTreeView
from threading import Timer
import datasource as ds
from message import MapDialog

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
        tk.Label(topFrame,text="台北市youbike及時資料",font=("arial", 24), bg="#333333", fg='#ffffff',padx=10,pady=10).pack(padx=10,pady=10)
        updateButton = tk.Button(topFrame,text="立即更新",bg="#dbdbdb",fg="#333333",font=('arial',16),command=lambda :ds.download())
        updateButton.pack(pady=(0,5))
        topFrame.pack(pady=10)
        #---------------------------------------

        col = 5
        for i in range(len(ds.AREA)):
            if  i % col == 0:
                topFrame = tk.Frame(self, bg="#cccccc", borderwidth=2, relief="raised")
                topFrame.pack(padx=20, pady=20)
            areaName = ds.AREA[i]
            btn1 = tk.Button(topFrame, text=areaName, padx=20, pady=20)
            btn1.bind('<Button-1>',self.areaClick)
            btn1.pack(side=tk.LEFT, padx=20, pady=20)

    def areaClick(self,even):
        areaName = even.widget["text"]
        areaList = []
        for site in ds.DATA:
            if areaName == site['sarea']:
                areaList.append(site)

        MapDialog(self,title=areaName,info=areaList)
        
        #----------建立搜尋------------------------
        middleFrame = ttk.LabelFrame(self,text='')
        tk.Label(middleFrame,text='站點名稱搜尋:').pack(side='left')
        search_entry = tk.Entry(middleFrame)
        search_entry.bind("<KeyRelease>", self.OnEntryClick)
        search_entry.pack(side='left')
        middleFrame.pack(fill='x',padx=20)
        #----------------------------------------
    
    #--↓↓--↓↓--↓↓--↓↓--↓↓--參考內容--↓↓--↓↓--↓↓--↓↓--↓↓--↓↓--↓↓--#
        #新增notebook(分頁)
        notebook = ttk.Notebook(self)
        notebook.pack(pady=0, expand=True)

        #新增frames
        #地圖的待新增內容--
        MapFrame = ttk.Frame(notebook, width=800, height=50)
        MapFrame.pack(fill='both', expand=True)
        notebook.add(MapFrame, text='以行政區分類地圖顯示定位')
        
        #---------------建立treeView---------------
        bottomFrame = tk.Frame(self)
        
        self.youbikeTreeView = YoubikeTreeView(bottomFrame,show="headings",
                                               columns=('sno','sna','sarea','mday','ar','tot','sbi','bemp'),
                                               height=20)
        self.youbikeTreeView.pack(side='left')
        vsb = ttk.Scrollbar(bottomFrame, orient="vertical", command=self.youbikeTreeView.yview)
        vsb.pack(side='left',fill='y')
        self.youbikeTreeView.configure(yscrollcommand=vsb.set)
        #-------------------------------------------

        #將frames放到notebook
        bottomFrame.pack(pady=(0,30),fill='both', expand=True)
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
    def update_data(Window)->None:
        ds.updata_sqlite_data()
        #-----------更新treeView資料---------------
        #lastest_data = ds.lastest_datetime_data()
        #Window.youbikeTreeView.update_content(lastest_data)

        #Window.after(10*60*10000,update_data,w) #每隔10分鐘持續七天

    window = Window()
    window.title('台北市youbike2.0')
    window.iconbitmap(default='test\images\YouBike2.0_white.ico') # 檔名字首要大寫。小寫會出錯。
    #window.geometry('600x300')
    #window.resizable(width=False,height=False)
    update_data(window)
    window.configure(background='#ffffff')
    window.mainloop()

if __name__ == '__main__':
    main()