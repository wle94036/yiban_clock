#!/usr/bin/python3
import sys
import datetime
# from YiBan import YiBan
from YB import YiBan
def main(username):
        username = str(username)
        p=YiBan(username)
        p.con()
        p.get_valid_code()
        p.login()
        r = p.clock()
        r=str(datetime.datetime.now())+r
        print(r)
        log_path=username+'.log'
        with open(log_path,'a') as f:
                f.write(r)
                f.close()
if __name__=="__main__":
        main(sys.argv[1])
