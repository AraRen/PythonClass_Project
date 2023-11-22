from tkinter.simpledialog import Dialog
import tkintermapview 
import tkinter as tk
from tkinter import ttk,messagebox

class CustomFrame(tk.Frame):
    def __init__(self,parent,data=None,map_widget=None,**kwargs):#這裡的self是定義
        super().__init__(parent,**kwargs)

class MapDialog(Dialog):
    def __init__(self, parent, title = None,info=None):
        self.info = info
        super().__init__(parent,title=title)


    def getCenter(self):
        lat_l,lat_s,lng_l,lng_s = -10000,100000,-100000,100000
        for site in self.info:
            if lat_l < site["lat"]:
                lat_l = site["lat"]
            if lat_s > site["lat"]:
                lat_s = site["lat"]
            if lng_l < site["lng"]:
                lng_l = site["lng"]
            if lng_s > site["lng"]:
                lng_s = site["lng"]

        lat_cen = lat_s + ((lat_l - lat_s) / 2)
        lng_cen = lng_s + ((lng_l - lng_s) / 2)
        print(lat_cen)
        print(lng_cen)
        return lat_cen, lng_cen

    def MapSearch(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_bar.get()
            self.search_marker = self.map_widget.set_address(address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False

    def MapClear(self):
        self.search_bar.delete(0, last=tk.END)
        self.map_widget.delete(self.search_marker)

    def body(self, master):
        self.marker_list = []
        self.marker_path = None
        self.search_marker = None
        self.search_in_progress = False
        searchFrame = tk.Frame(master,width=800,height=500)
        searchFrame.pack()

        self.search_bar = tk.Entry(searchFrame, width=50)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        self.search_bar_button = tk.Button(master=searchFrame, width=8, text="搜尋", command=self.MapSearch)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_bar_clear = tk.Button(master=searchFrame, width=8, text="清除", command=self.MapClear)
        self.search_bar_clear.grid(row=0, column=2, pady=10, padx=10)


        self.map_widget = tkintermapview.TkinterMapView(master,width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        # map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.set_position(25.1150128,121.5361573)  # 設置初始座標(台北職能學院)
        self.map_widget.set_zoom(14)

        #建立marker
        for site in self.info:
            marker = self.map_widget.set_marker(site['lat'],site['lng'],marker_color_outside='white',font=('arial',10),text=f"{site['sna']}\n可借:{site['sbi']}\n可還:{site['bemp']}",command=self.click1)
            marker.data = site
            

    def click1(self,marker):
        '''
        marker.text = marker.data['sna']
        marker.marker_color_outside='black'
        self.map_widget.set_position(marker.data['lat'], marker.data['lng'])
        '''
        '''
        Update marker text and color, and center the map on the marker's location.
        '''
        marker.text = marker.data['sna']
        marker.marker_color_outside = 'black'

        # Center the map on the marker's location
        lat, lng = marker.data['lat'], marker.data['lng']
        self.map_widget.set_position(lat, lng)
        self.map_widget.set_zoom(19)


    def center_map(self):
        lat_sum = 0
        lng_sum = 0
        num_markers = len(self.marker_list)

        for marker in self.marker_list:
            lat_sum += marker.lat
            lng_sum += marker.lng

        lat_avg = lat_sum / num_markers
        lng_avg = lng_sum / num_markers

        self.map_widget.set_position(lat_avg, lng_avg)


    def buttonbox(self):
        #super().buttonbox()
        #自訂按鈕區
        #'relief='邊框樣式，可以設定 flat[扁平]、sunken[凹陷]、raised[浮凸]、groove[邊框]、ridge、solid，預設 flat。 https://steam.oxxostudio.tw/category/python/tkinter/button.html#a3
        bottomFrame = tk.Frame(self)
        tk.Button(bottomFrame,text="關閉"+self.title()+"地圖",command=self.ok,padx=10,pady=10,activeforeground='#FFF',bg='#FFF',relief='raised').pack(padx=10,pady=20)
        bottomFrame.pack()


    def ok(self, event=None):
        super().ok()