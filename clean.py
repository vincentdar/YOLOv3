# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2021-12-16 14:49:48
# @Last Modified by:   Your name
# @Last Modified time: 2021-12-16 18:17:43
from os import listdir, remove
from os.path import join, isfile, getctime
from datetime import datetime
import time
import threading 

class Cleaner():
    def __init__(self):
        pass
        
    def start(self):
        print("Cleaner started")
        self.start = True
        self.t = threading.Thread(target=self.periodic_cleaning)
        self.t.start()

    def stop(self):
        self.set_start(False)
        self.t.join()
        print("Cleaner Stopped")

    def cleanDirectory(self, path, now):
        
        file = [( join(path, f), datetime.fromtimestamp(getctime(join(path, f))).strftime('%Y-%m-%d %H:%M:%S')) for f in listdir(path) if isfile(join(path, f))]
        

        mark_delete_file = [f for f in file if (datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - datetime.strptime(f[1], '%Y-%m-%d %H:%M:%S')).total_seconds() > 3600]

        if len(mark_delete_file) > 0:
            for i in range(len(mark_delete_file)):
                remove(mark_delete_file[i][0])
    
    def periodic_cleaning(self):
        while(True):
            if self.start == False:
                break
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cleanDirectory("Uploads", now)
            self.cleanDirectory("result", now)
            time.sleep(1)

    def set_start(self, is_start):
        self.start = is_start
        


# if __name__ == '__main__':
#     cleaner = Cleaner()
#     cleaner.start()
#     time.sleep(5)
#     cleaner.stop()
      

    
