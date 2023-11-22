import tkinter as tk
import dataSource
from message import MapDialog

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        titleFrame = tk.Frame(self, bg="#333333",borderwidth=2,relief=tk.SUNKEN,padx=50,pady=50)
        tk.Label(titleFrame,text="台北市 YouBike 2.0 站點即時資訊地圖",bg="#333333",fg="#cccccc",font=('arial',20)).pack()
        updateButton = tk.Button(titleFrame,text="立即更新",bg="#dbdbdb",fg="#333333",font=('arial',16),command=lambda :dataSource.download())
        updateButton.pack(pady=(20,0))
        titleFrame.pack(pady=20)

        col = 5
        for i in range(len(dataSource.AREA)):
            if  i % col == 0:
                topFrame = tk.Frame(self, bg="#cccccc", borderwidth=2, relief="raised")
                topFrame.pack(padx=20, pady=20)
            areaName = dataSource.AREA[i]
            btn1 = tk.Button(topFrame, text=areaName, padx=20, pady=20)
            btn1.bind('<Button-1>',self.areaClick)
            btn1.pack(side=tk.LEFT, padx=20, pady=20)

    def areaClick(self,even):
        areaName = even.widget["text"]
        areaList = []
        for site in dataSource.DATA:
            if areaName == site['sarea']:
                areaList.append(site)

        self.map_widget = MapDialog(self,title=areaName,info=areaList)


if __name__ == "__main__":
    root = Window()
    root.title("台北市 YouBike 2.0 站點即時資訊地圖")
    root.iconbitmap(default='youbikemap\images\Bike_blue41x35.ico') # 檔名字首要大寫。小寫會出錯。
    root.mainloop()