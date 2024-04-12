import requests
import json
import time
import threading
c=time.time()
class Count_Replies:
    def __init__(self):
        self.data=self.get_data()

    def get_max_id(self):
        w=requests.get("https://api.codemao.cn/web/work-shops/search?limit=1&sort=-created_at")
        data=json.loads(w.text)
        return data["items"][0]["id"]

    def get_data(self):
        n=self.get_max_id()
        lst=[]
        num = min(200,n)
        link_range_list = [(int(i * (n) / num), -1+int((1 + i) * (n) / num)) for i in range(num)]
        # print(link_range_list)

        thread_list = []
        for i in range(1, num + 1):
            thread = myThread("Thread-" + str(i), link_range_list[i - 1])
            thread.start()
            thread_list.append(thread)
        # print(len(thread_list))
        for i in thread_list:
            i.join()
        flag=all([i.flag for i in thread_list])
        while not flag:
            flag = all([i.flag for i in thread_list])
        for i in thread_list:
            lst+=i.lst
        # print(lst)
        # print(len(lst))
        return lst
    def show_list(self):
        lst=[[i["all"],i["name"],i["id"]] for i in self.data]
        lst.sort()
        lst=lst[::-1]
        return lst
class myThread(threading.Thread):
    def __init__(self, name, link_range):
        threading.Thread.__init__(self)
        self.name = name
        self.link_range = link_range
        self.lst = []
        self.flag=False

    def run(self):
        # print("Starting" + self.name)
        self.crawler(self.name, self.link_range)
        # print("Exiting" + self.name)

    def crawler(self, link_num, link_range):
        self.lst=[]
        for i in range(link_range[0],link_range[1]+1):
            # if link_num=="Thread-1":
                # print(i/len(link_range))
            l={}
            try:
                w = requests.get(f"https://api.codemao.cn/web/shops/{i}")
                l["name"] = json.loads(w.text)["name"]
            except:
                continue
            w=requests.get(f"https://api.codemao.cn/web/discussions/{i}/comments?source=WORK_SHOP&limit=5&offset=0")
            data = json.loads(w.text)
            l["reply"]=data["total"]#评论
            l["all"]=data["totalReply"]+data["total"]#总数，包括评论回复
            l["id"]=i
            self.lst.append(l)
        self.flag=True

if __name__=="__main__":
    count=Count_Replies()

    print(count.show_list())#[数量,名称,工作室id]

    print(time.time()-c)
