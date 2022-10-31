#!/usr/bin/env python
# -*- coding:utf-8 -*-
### autor:   liangjinfeng ###
### version:   2.0        ###


#nginx_process.py-----excel

import os
import sys
import pandas as pd

import threading
#import openpyxl
#from pandas import Series,DataFrame
import os
import sys,argparse
from pathlib import Path



def process_excel(outputfile):
    
    df=pd.read_excel('%s.xlsx' %outputfile ,engine='openpyxl',sheet_name='Sheet1')
    #max_row = df.shape[0] + 1
    df1 = pd.DataFrame((x.split('|') for x in df['IP_link']),
                  columns=['IP_link','IP_status', 'IP'])
    
    df2 = pd.DataFrame(df, columns=['IP_count'])
    result = pd.concat([df1, df2], axis=1)
    result.to_excel('%s.xlsx' %outputfile ,sheet_name='nginx日志分析情况', index=False)






if __name__ == "__main__":

    parser=argparse.ArgumentParser(description='nginx python ',usage='%(prog)s [options] -i inputfile -o outfile')
    parser.add_argument('-i','--input',nargs='?',required=True,dest='inputfile',default='inputfile',help='输入文件路径')
    parser.add_argument('-o','--output',nargs='?',required=True,dest='outputfile',default='outputfile',help='输出excel文件名称')
    

    if len(sys.argv)==1 :
        parser.print_help()

    else:
        args=parser.parse_args()
        inputfile=args.inputfile
        outputfile=args.outputfile
        
        #print(dest_filename)
        max_threads=200
        pool_sema = threading.BoundedSemaphore(max_threads)
        threads = []
        log_name=os.getcwd()
        logfile_format=os.path.join(log_name,"%s-log.txt" %outputfile)


        try:
            my_abs_path = Path(inputfile).resolve()
            with open(inputfile) as f:

                accessDict = {}
                for oneAccess in f:
                    oneAccessList = oneAccess.split(' ')
                    #accessDictKey = (oneAccessList[10][::-1].split('?', 1)[-1][::-1],oneAccessList[12],oneAccessList[0])
                    with open(logfile_format, 'a') as fw:
                        fw.write(oneAccessList[10][::-1].split('?', 1)[-1][::-1])
                        fw.write('|')
                        fw.write('\t')
                        fw.write(oneAccessList[12])
                        fw.write('|')
                        fw.write('\t')
                        fw.write(oneAccessList[0])
                        fw.write('\n')


                    ##写入数据
                reader=pd.read_table(logfile_format,sep='\n',engine='python',names=["IP_link"] ,header=None,iterator=True)
                loop=True
                chunksize=100000
                chunks=[]
                while loop:
                    try:
                        chunk=reader.get_chunk(chunksize)
                        chunks.append(chunk)
                            
                    except StopIteration:
                        loop=False
                        print ("Iteration is stopped.")

                df=pd.concat(chunks)
                df_groupd=df.groupby('IP_link')
                df_groupd_size= df_groupd.size()
                df_ana=pd.concat([df_groupd_size],axis=1,keys=["IP_count"])
                df_ana.to_excel("%s.xlsx" %outputfile)

                process_excel(outputfile)
                #删除日志存放临时目录
                remove_file = os.remove(logfile_format)

        except FileNotFoundError:
            print("FileNotFoundError")
            exit(0)

    


