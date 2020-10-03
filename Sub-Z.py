import requests
import re
import subprocess
from subprocess import Popen, PIPE
import os
import os.path
from os import path
from termcolor import colored
import terminal_banner
import socket
import argparse
import subprocess
import shutil
import itertools
import time



parser = argparse.ArgumentParser(description='\u001b[36mSubZ - A Subdomain Enumeration Tool \u001b[0m')
parser.add_argument('-d','--domain' , help = 'Domain name of the taget [ex : bugcrowd.com]' , required=True)
parser.add_argument('-ip', help='To get the IP address of the Subdomains',action='store_true')
parser.add_argument('-live', help='To find only live subdomains',action='store_true')

args = parser.parse_args()

banner = ("""\u001b[36m
                  ███████╗██╗   ██╗██████╗      ███████╗
                  ██╔════╝██║   ██║██╔══██╗     ╚══███╔╝
                  ███████╗██║   ██║██████╔╝█████╗ ███╔╝ 
                  ╚════██║██║   ██║██╔══██╗╚════╝███╔╝  
                  ███████║╚██████╔╝██████╔╝     ███████╗
                  ╚══════╝ ╚═════╝ ╚═════╝      ╚══════╝          \u001b[0m  
                                
                                Made with \u001b[31m❤️\u001b[0m 
                    For the Community, By the Community   
                    ###################################
                        Developed by \u001b[36mJitesh Kumar\u001b[0m 
                Intagram  - \u001b[36mhttps://instagram.com/jitesh.haxx\u001b[0m 
                   linkedin  - \u001b[36mhttps://linkedin.com/j1t3sh\u001b[0m 
                     Github - \u001b[36mhttps://github.com/j1t3sh\u001b[0m 
                                            
            ( DONT COPY THE CODE. CONTRIBUTIONS ARE MOST WELCOME \u001b[31m❤️\u001b[0m ) 
                                                                                
""")

print(banner)



def subez():
    spinner=itertools.cycle(['|','/','-','\\'])
    process=subprocess.Popen(".\wassetfinder.exe --subs-only " + args.domain + " | .\httprobe > " + args.domain +".txt",shell=True)
    while process.poll() is None:
        time.sleep(0.5)
        cols=" "*(shutil.get_terminal_size((80, 20))[0]-65)
        count = len(open(args.domain+".txt").read().split('\n')) - 1
        print("\r[+]Searching Subdomains "+next(spinner)+ cols+ "\u001b[32mFound: "+str(count),end=''+"\u001b[0m ")
    list_sub = []
    new_list=[]
    file1 = open(args.domain + '.txt','r')
    count = 0
    while True:
        count +=1
        line = file1.readline()

        if not line:
            break
        list_sub.append(line)
    print("\n")
    for i in range(len(list_sub)):
        z = str(list_sub[i])
        z = re.sub("\\n$","",z)
        new_list.append(z)
    
    for q in new_list:
        def ip():
            if "https" in q:
                ipaddr = q.replace("https://","")
                return ipaddr
            else:
                ipaddr = q.replace("http://","")
                return ipaddr
    
    if args.ip:
        args.ip =  socket.gethostbyname(ip())
    else:
        args.ip = ""

    if args.live:
        print("[+]Scanning for only Live Subdomains....\n")
        for m in new_list:
            try:
                response = requests.get(m)
                if response.status_code == 200:
                    print("\u001b[32m"+m + " - " +args.ip+" :",response.status_code,response.reason+"\u001b[0m ")
            except:
                    continue
    else:
        print("[+]Scanning for the Services....\n")
        for m in new_list:
            try:
                response = requests.get(m)
                
                if response.status_code == 200:
                    print("\u001b[32m"+m + " - " +args.ip+" :",response.status_code,response.reason+"\u001b[0m ")
                elif(400<response.status_code<500):
                    print("\u001b[31m"+m+ " - " +args.ip+" :",response.status_code,response.reason+"\u001b[0m")
                else:
                    print("\u001b[36m"+m+ " - " +args.ip+" :",response.status_code,response.reason+"\u001b[0m")
            except:
                continue   
    file1.close() 

            
try:
    subez()
except:
    print("Check your Internet Connection or Try Again Later")
