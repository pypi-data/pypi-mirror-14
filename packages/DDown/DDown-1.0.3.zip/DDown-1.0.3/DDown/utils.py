'''
    Created by Tracy on 2016/3/9
    Mail tracyliubai@gmail.com

'''
from multiprocessing import Pool
from urllib.parse import quote
import threading
import urllib.request
import socket, os

socket.setdefaulttimeout(150.0)


class download():
    def __init__(self, url_list, folder='', path='', down_type=0, pool_num=150):
        '''
        :param url_list:    list type
        :param folder:      storage  path
        :param path:        absolute path like:
                            win     D:/Document/test
                            unix    /root/document
        :param down_type:
                            0: multi_pool
                            1: multi_thread
        :param pool_num:    pool number
        :return:
        '''
        self.url_list = url_list
        self.down_type = down_type
        self.pool_num = pool_num
        self.store_folder = ''
        self.flag = False
        if path:
            self.store_folder = path
            self.mkdir()
            if folder:
                self.store_folder += '/' + folder
                self.mkdir()
            else:
                self.flag = True
        else:
            if folder:
                self.store_folder = folder
                self.mkdir()

    def mkdir(self):
        if (os.path.exists(self.store_folder)):
            print('Folder exists')
        else:
            os.makedirs(self.store_folder)
            print('Mkdir folder')

    def start(self):
        fun = self.url_retrieve
        if self.down_type == 0:
            self.multi_pool(function=fun)
        elif self.down_type == 1:
            self.multi_thread(function=fun)

    def multi_thread(self, function):
        threads_task = []
        for file in self.url_list:
            t = threading.Thread(target=function, args=[file])
            threads_task.append(t)
        for task in threads_task:
            task.start()
        for task in threads_task:
            task.join()

    def multi_pool(self, function):
        pool = Pool(processes=self.pool_num)
        pool.map(function, self.url_list)

    def url_open(self, url):
        try:
            conn = urllib.request.urlopen(url, timeout=60)
            file_name = url.split('/')[-1]
            f = open(self.store_folder + '/' + file_name, 'wb')
            f.write(conn.read())
            f.close()
        except Exception as e:
            print(e)

    def url_retrieve(self, url):
        f = url.split('/')[-1]
        url = quote(url).replace('%3A', ':')

        if self.store_folder == '':
            self.store_folder = f.split('.')[-1]
            self.mkdir()
        if self.flag:
            self.store_folder += '/' + f.split('.')[-1]
            self.mkdir()

        file_name = self.store_folder + '/' + f
        try:
            r = urllib.request.urlretrieve(url, file_name)
        except Exception as e:
            print(e)
            print(url)
