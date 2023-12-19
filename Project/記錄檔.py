        
#在main.py的
#--↓↓--↓↓--↓↓--↓↓--↓↓--參考內容--↓↓--↓↓--↓↓--↓↓--↓↓--↓↓--↓↓--#正下方


        #bottomFrame.pack(fill='both', expand=True)
        #notebook.add(bottomFrame, text='各站點清單附帶搜尋功能')
        #------區域時段搜尋框架--------
        #放選單的框架
        #mainFrame = tk.Frame(MapFrame,width=1000,height=200)
        #mainFrame.pack()

        ##建立關鍵字的label
        #TKLable(mainFrame, text="以下可擇一搜尋，搜尋到的結果雙擊兩下可以到地圖區看到位置",bd=3).grid(row=0,column=0,columnspan=4)

        ##建立Combo的Label
        #TKLable(mainFrame, text="請選擇行政區",bd=3).grid(row=1,column=0)
        ##抓取台北行政區
        #self.TaipeiArea_dict=ds.Get_TaipeiArea()
        ##台北市行政區下拉選單
        #self.TaipeiAreaValue = tk.StringVar()
        #self.TaipeiArea_Combo = ttk.Combobox(mainFrame,values=list(self.TaipeiArea_dict.keys()),justify="center",textvariable=self.TaipeiAreaValue)
        #self.TaipeiArea_Combo.grid(row=1,column=1)  
        #self.TaipeiArea_Combo.current(0)
    #--↑↑--↑↑--↑↑--↑↑--↑↑--參考內容--↑↑--↑↑--↑↑--↑↑--↑↑--↑↑--↑↑--#