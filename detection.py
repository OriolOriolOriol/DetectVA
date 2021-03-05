import os,glob,time,sys
import colorama 
import shutil
colorama.init()
from colorama import Fore, Style, Back
from platform import system
import zipfile
from read_code_smali import Read_code_smali
from valutazione_finale import IntentTraceback
from pathlib import Path

def is_tool(name):
    from shutil import which

    return which(name) is not None


def extractCode(newname,APKpath,APP_code,nome_apk):
    lista_dex=[]
    file_code_txt= APP_code + nome_apk + ".txt"
    with zipfile.ZipFile(newname,"r") as zip_ref:
        zip_ref.extractall(APKpath)
    
    #append all file dex in a list
    for file_dex in glob.glob(f"{APKpath}*.dex"):
        lista_dex.append(file_dex)
    
    if len(lista_dex) > 0:
        count=0
        for i in lista_dex:
            if count == 0:
                if system() == 'Linux':
                    answer=is_tool("dexdump")
                    if answer == "False":
                        command000=f"sudo apt install dexdump"
                        os.system(command000)
                        command0 = f"dexdump -d   {i}   >  {file_code_txt}"
                    else:
                        command0 = f"dexdump -d   {i}   >  {file_code_txt}"
                else:
                    command0 = f"dexdump.exe -d   {i}   >  {file_code_txt}"

                result0 = os.popen(command0)
                time.sleep(20)
            else:
                if system() == 'Linux':
                    answer=is_tool("dexdump")
                    if answer == "False":
                        command000=f"sudo apt install dexdump"
                        os.system(command000)
                        command1 = f"dexdump -d   {i}   >>  {file_code_txt}"
                    else:
                        command1 = f"dexdump -d   {i}   >>  {file_code_txt}"
                else:
                    command1 = f"dexdump.exe -d   {i}   >>  {file_code_txt}"
                
                result1 = os.popen(command1)
                time.sleep(20)
            
            count = count + 1
        
        if os.stat(file_code_txt).st_size != 0:
            return 0
        else:
            print(Fore.RED + "Unable to extract smali code from dex file..!!")
            print(Fore.WHITE)
            return 1
    else:
        return 1

    

def delete_junk():
    path = os.getcwd()

    if system() == 'Linux':
        path1=path + "/Manifest_component_file/*"
        path2=path + "/APP_code/*"
        path3=path + "/APKs/*"

    else:
        path1=path + "\\Manifest_component_file\\*"
        path2=path + "\\APP_code\\*"
        path3=path + "\\APKs\\*"
    lista_pattern=[path1,path2,path3]
    for single in lista_pattern:
        fileNames = glob.glob(single)
        for filename in fileNames:
            try:
                os.remove(filename)
            except:
                shutil.rmtree(filename)

       
def detection():
    rootPath = os.getcwd()
    if system() == 'Linux':
        APKpath = rootPath + "/APKs/"
        APPCode= rootPath + "/APP_code/"
        temp=rootPath + "/StoreAPK/"
        manifest= rootPath + "/Manifest_component_file/"
    else:
        APKpath = rootPath + "\\APKs\\"
        APPCode= rootPath + "\\APP_code\\"
        temp=rootPath + "\\StoreAPK\\"
        manifest= rootPath + "\\Manifest_component_file\\"
   
   
    lunghezza=len([name for name in os.listdir(temp) if os.path.isfile(os.path.join(temp, name))])
    print (f"\nNumber of apk to analyze --> {str(lunghezza)}\n")
    count=1
    for root, dirs, files in os.walk(temp):
        for apk in files:

            if system() == 'Linux':
                os.system(f"cp {temp}{apk} {APKpath} ")
            else:
                os.system(f"copy {temp}{apk} {APKpath} ")

            nome_apk=apk
            print(Fore.LIGHTBLUE_EX + f"\n{count}) Starting with {nome_apk}\n")
            print(Fore.WHITE)
            apk=APKpath+nome_apk
            nome_file_aapt= manifest + nome_apk + ".txt"
            #Generate the APK-manifest file
            print(Fore.RED + "\n1-MANIFEST EXTRACTION & COMPONENT INFORMATION FROM APK FILE...")
            print(Fore.WHITE)
            if system() == 'Linux':
                answer=is_tool("aapt")
                if answer == "False":
                    command000=f"sudo apt install aapt"
                    os.system(command000)
                    command = f"aapt l -a  {apk} >   {nome_file_aapt}"

                else:
                    command = f"aapt l -a  {apk} >   {nome_file_aapt}"
            else:
                command = f"aapt.exe l -a  {apk} >   {nome_file_aapt}"
            
            result = os.popen(command)
            time.sleep(35)
            if os.stat(nome_file_aapt).st_size != 0:
                print(Fore.GREEN + "The Manifest extraction worked!!!\n")
                print(Fore.WHITE)
                split_manifest_component(nome_file_aapt,nome_apk,manifest)

                portion = os.path.splitext(nome_apk)  #  Separate file names and suffixes
                if portion[1] == ".apk":  # Edit according to suffix, if there is no suffix then blank
                    newname = APKpath + portion[0] + ".zip"  # The new suffix to change
                    os.rename(apk, newname)
                    print ("Rename successfully!!!: " + newname)
                    print(Fore.RED + "\n2-CODE SMALI EXTRACTION...\n")
                    print(Fore.WHITE)
                    time.sleep(1)
                    flag=extractCode(newname,APKpath,APPCode,nome_apk)
                    if flag==0:
                        print (Fore.GREEN + "Extracting the code file successfully！")
                        print(Fore.WHITE)
                        path_file_dex= APPCode + nome_apk +".txt"
                        print(Fore.RED + "\n3-READING CODE SMALI...\n")
                        time.sleep(2)
                        print(Fore.WHITE)
                        path_dir_smali,path_code_smali=Read_code_smali(path_file_dex,nome_apk)
                        print(Fore.RED + "4-FINAL EVALUATION...\n")
                        time.sleep(2)
                        print("\n"+ Fore.WHITE)
                        tipo,res= IntentTraceback(nome_apk,path_dir_smali,path_code_smali,path_file_dex)

                        if res == 0:
                            print (Fore.RED + "FINAL ANSWER: Failure - Cycle")
                            print("\n"+ Fore.WHITE)
                        elif res == 2:
                            print (Fore.GREEN + "FINAL ANSWER: APK without VA")
                            print("\n"+ Fore.WHITE)
                        elif (res != 0) and (res != 2):
                            print (Fore.RED + f"FINAL ANSWER: APK WITH VA --> {tipo}")
                            print("\n"+ Fore.WHITE)
                        
                        
                    
                        delete_junk()


                    else:
                        print(Fore.RED +"Error: No classes.dex found..\n")
                        print(Fore.WHITE)
                        delete_junk()
                        sys.exit(0)

        

            else:
                print(Fore.RED + "Manifest file extraction failed!!!\n")
                print(Fore.WHITE)
                delete_junk()
                sys.exit(0)
            
            count= count + 1 

    
# Function to convert  list to string 
def listToString(s):  
    str1 = " " 
    return (str1.join(s))   

#split the info of manifest and the component of apk file
def split_manifest_component(manifest,nome_apk,path):
    rootPath = os.getcwd()
    if system() == 'Linux':
        outcome=f"{rootPath}/Outcome/{nome_apk}/"
    else:
        outcome=f"{rootPath}\\Outcome\\{nome_apk}\\"
    Path(outcome).mkdir(parents=True, exist_ok=True)
    trovato=False
    with open(manifest,"r") as file1:
        for num, line in enumerate(file1, 1):
            if "Android manifest:" in line:
                trovato=True
                linea=num

    if trovato == True:  
        with open(manifest,"r") as file1:
            dati=file1.readlines()[linea-1:]
            dati_finali=listToString(dati)
        manifest1=path + nome_apk + "_manifest.txt"
        with open(manifest1,"w") as file3:
            file3.write(dati_finali)
        
        if system() == 'Linux':
            os.system(f"cp {manifest1} {outcome} ")
        else:
            os.system(f"copy {manifest1} {outcome} ")
        
        with open(manifest,"r") as file2:
            dati2=file2.readlines()[:linea-1]
            dati_finali2=listToString(dati2)
        components=path + nome_apk + "_components.txt"
        with open(components,"w") as file4:
            file4.write(dati_finali2)
        
        if system() == 'Linux':
            os.system(f"cp {components} {outcome} ")
        else:
            os.system(f"copy {components} {outcome} ")
    else:
        print("It Didn't find any manifest key in the file")





detection()