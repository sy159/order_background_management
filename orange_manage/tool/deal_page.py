__author__ = 'zzq'
class Page(object):
    #输入所有数据长度，每页要显示的数据，分页显示几页，当前页面位置
    def __init__(self,data_len,page_data_num,show_page_num,pid):
        self.data_len=data_len
        self.page_data_num=page_data_num
        self.show_page_num=show_page_num
        self.pid=pid
    @property
    def start_page(self):
        num=int((self.show_page_num-1)/2)
        start_page=self.pid-num
        return start_page
    @property
    def end_page(self):
        num=int((self.show_page_num-1)/2)
        end_page=self.pid+num
        return end_page
    #在页面遍历出所有数据显示在页面
    def data(self):
        start=(self.pid - 1) * self.page_data_num
        end=(self.pid)*self.page_data_num
        # data=[start,end]
        return start,end
    #显示下面的分页效果跟连接
    def main(self):
        start_page=self.start_page
        end_page=self.end_page
        all_page,remainder=divmod(self.data_len,self.page_data_num)
        if remainder:
            all_page+=1
        if all_page<=self.show_page_num:
            start_page=1
            end_page=all_page
        else:
            if start_page<1:
                start_page=1
                end_page=self.show_page_num
            if end_page>all_page:
                start_page=all_page-self.show_page_num+1
                end_page=all_page
        list=[]
        if self.pid==1:
            data = '<a href="#"><input type="submit" value="上一页"/></a>'
            list.append(data)
        else:
            data = '<a href="/test/p=%s"><input type="submit" value="上一页"/></a>'%(self.pid-1)
            list.append(data)
        for i in range(start_page,end_page+1):
            data = '<a href="/test/p=%s">%s</a>' % (i, i)
            list.append(data)
        if self.pid == end_page:
            data = '<a href="#"><input type="submit" value="下一页"/></a>'
            list.append(data)
        else:
            data = '<a href="/test/p=%s"><input type="submit" value="下一页"/></a>' % (self.pid + 1)
            list.append(data)
        return list