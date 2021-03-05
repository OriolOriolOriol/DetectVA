import os
from platform import system

def Read_code_smali(path_file_dex,nome_apk):
    rootPath = os.getcwd()
    if system() == 'Linux':
        path_outcome=f"{rootPath}/Outcome/{nome_apk}/"
    else:
        path_outcome=f"{rootPath}\\Outcome\\{nome_apk}\\"
        
    path_outcome1= path_outcome + f"{nome_apk}_afterCODESMALI.txt"
    intentfunc = open(path_outcome1, "w")
    with open(path_file_dex, "rU",encoding="latin1") as f:
        lines = f.readlines()
        lines_length = len(lines)
        i = 0
        new_intent = []
        param_intent = []
        new_intent0 = ""
        class_count = 0
        writelist = []
        param1 = []
        intent = []
        paramlist = []
        paramlists = []
        class_name = ""
        VirtualMethod = ""
        VirtualMethodNum = ""
        item = ""
        var = "null"
        res = "null"
        intentcount = 0

        while i <= lines_length - 3:
            func_name = []
            vmflag = 0
            newintentinVirtualMethod = []

            #A) Con questo while io sto tirando fuori tutte le class descriptor(le librerie usate)
            while lines[i].startswith("Class #"):
                class_name1 = lines[i + 1].split("'")[1]
                class_name = class_name1.strip("L").replace(';', '').replace('/', '.')
                class_count = class_count + 1
                i = i + 1
                '''
                ....
                com.morgoo.droidplugin.hook.handle.ITelephonyHookHandle$MyBaseHandler
                com.morgoo.droidplugin.hook.handle.ITelephonyRegistryHookHandle$MyBaseHandler
                com.morgoo.droidplugin.hook.handle.IWifiManagerHookHandle$getBatchedScanResults
                com.morgoo.droidplugin.hook.handle.IWifiManagerHookHandle$getScanResults
                com.morgoo.droidplugin.hook.handle.IWindowSessionInvokeHandle$add
                ....

                '''
            
            #B) Con questo while tiro fuori i metodi usati
            while lines[i].startswith("    #") and lines[i + 1].startswith("      name"):
                vmflag = i 
                VirtualMethod = lines[i + 1].split("'")[1]
                paramlist = []
                paramlists = []
                newintentinVirtualMethod = []
                intentcount = 0
                i = i + 1
                '''
                getScrollIndicators
                offsetLeftAndRight
                offsetTopAndBottom
                setScrollIndicators
                setScrollIndicators
                '''

            #C) con questo while cerco new-instance,check-cast,invoke-virtual(lavora sopratutto su quest'ultimo) (Dalvik bytecode) e mi salvi i registri dove questi agiscono
            while lines[i].find("new-instance") >= 0 and lines[i].find("Landroid/content/Intent") >= 0 and i <= lines_length - 3\
                    or lines[i].find("check-cast") >= 0 and lines[i].find("Landroid/content/Intent") >= 0 and i <= lines_length - 3 \
                    or lines[i].find("invoke-virtual") >= 0 and lines[i].find(":(") >= 0:

                if lines[i].find("new-instance") >= 0 :
                    new_intent0 = lines[i].split("new-instance ")[1].split(",")[0]
                    new_intent = []
                    #La new_intent contiene tutti i nuovi reg di intenti creati in un VirtualMethod e i loro numeri di linea, come [[v1,100],[v5,123]] {v1 è il registro e 100 è linea del file in cui si trova}
                    new_intent.append(new_intent0)  # new intent reg
                    new_intent.append(i)  # row number
                    newintentinVirtualMethod.append(new_intent)
                    intentcount = intentcount + 1
                    i = i + 1

                elif lines[i].find("check-cast") >= 0 :
                    new_intent0 = lines[i].split("check-cast ")[1].split(",")[0]
                    new_intent = []
                    new_intent.append(new_intent0)  # new intent reg
                    new_intent.append(i)  # row number
                    newintentinVirtualMethod.append(new_intent)
                    intentcount = intentcount + 1
                    i = i + 1

                elif lines[i].find("invoke-virtual") >= 0 and lines[i].find(":(") >= 0:
                    params = lines[i].split(":(")[1].split(")")[0]
                    if params.find("Landroid/content/Intent") >= 0:
                        params_type = params.split("Landroid/content/Intent")[0]
                        semicount = params_type.count(';')
                        #trova i vari parametri
                        if lines[i].find("{")>=0 and lines[i].find("}")>=0:
                            params_var = lines[i].split("{")[1].split("}")[0]
                            param_intent = params_var.split(", ")[semicount+1]
                            new_intent = []
                            new_intent.append(param_intent)  # nuovo registro degli intenti
                            new_intent.append(i)  # row number
                            flag = 0
                            for ni in newintentinVirtualMethod:
                                #print(ni[0]) #v1,v1,v3
                                if param_intent == ni[0]:
                                    flag = 1
                            if flag == 0:
                                newintentinVirtualMethod.append(new_intent)
                                intentcount = intentcount + 1
                    i = i + 1

            #D)check la lista newintentVirtualMethod(contenente i vari parametri(registri)) da cui tiro fuori i metodi dei metodi principali(esempio putExtra è un sottometodo di intent) e creazione del file dove ogni linea contiene tutte le info trovate e le metto dentro al file.txt 
            if newintentinVirtualMethod: #[['v1', 40339]],[['v1', 40360]]... (c'è il registro e a fianco il numero della riga)
                for niv in newintentinVirtualMethod:
                    ni = niv[0]         # ni è il registro degli intenti (v1,v2)
                    j = niv[1]          # numero riga in cui si trova il registro degli intenti
                    # new_intent seguito da "," o "}" per distinguere tra esempi come v1 e v12
                    ni1 = ni + ","
                    ni2 = ni + "}"
                    var = "null"
                    res = "null"
                    # Per ogni nuovo intento, in quel modulo VirtualMethod, iterare attraverso la linea da cui è stato creato, cercando i regs pertinenti
                    while not lines[j].startswith("    #") and not lines[j + 1].startswith("      name") and j <= lines_length - 4:
                        while lines[j].find(ni1) >= 0 and lines[j].find("invoke-") >= 0 or lines[j].find(ni2) >= 0 and lines[j].find("invoke-") >= 0:
                            paramlist = []
                            func_name = []
                            func_name_tmp = lines[j].split(".")[1].split(":")[0]
                            if func_name_tmp not in func_name:
                                func_name.append(func_name_tmp)#mi salva le funzioni dentro la lista func_name (getScrollIndicators, etc..)

                            param = lines[j].split("{")[1].split("}")[0]  
                            paramlen = 0
                            #Se dentro param c'è una virgola che significa (v0,v1,v2..) allora conta quanti sono questi parametri
                            if param.find(",") >= 0:  
                                paramlen = len(param.split(","))
                            for p in range(0, paramlen):
                                # La paramlist contiene i nomi di altre variabili associate al registro di questo intento regs. Esempio 1) [['v1', 40339]] ---> ['v0', 'v2'] 2) [['v1', 40360]] ---> ['v0', 'v2', 'v3']
                                ip = param.split(",")[p].replace(" ", "")
                                if ip not in paramlist and ip != ni:
                                    paramlist.append(ip)

                            var = "null"
                            res = "null"
                            #Controlla che tra i nomi di funzioni ci sia getComponent
                            if func_name_tmp == "getComponent":
                                if lines[j + 1].find("move-result-object ") >= 0:
                                    var_tmp = lines[j + 1].split("move-result-object ")[1]
                                    res = var_tmp.replace("\n", "")
                            #controlla che non ci sia <init> tra in nomi di funzione
                            elif func_name_tmp != "<init>":
                                var = ','.join(paramlist)
                                for pp in paramlist:#0c7cd8: 6e30 5401 1002 |0000: invoke-virtual {v0, v1, v2}, Landroid/content/Context;.startActivity:(Landroid/content/Intent;Landroid/os/Bundle;)V // method@0154 <-- Riga 40339(quando printo pp mi stampa v1 e v2 che sono collegati a v0)
                                    pp1 = pp + ","
                                    pp2 = pp + "}"
                                    if lines[j].find(pp1) >= 0 or lines[j].find(pp2) >= 0:
                                        q = j-1
                                        while q > vmflag:
                                            if lines[q].find("move-result-object " + pp) >= 0:
                                                if lines[q - 1].find(".") >= 0:
                                                    func_tmp = lines[q - 1].split(".")[1] #getReferrer:()Landroid/net/Uri; // method@0030
                                                    func_tmp1 = func_tmp.split(":")[0]
                                                    class_tmp = lines[q - 1].split(".")[0]#0c7be4: 6e10 3000 0100                         |0000: invoke-virtual {v1}, Landroid/app/Activity;
                                                    if class_tmp.find(", L") >= 0:
                                                        class_tmp1 = class_tmp.split(", L")[1].replace("/", ".")#android/app/Activity
                                                    else:
                                                        if class_tmp.find(", [")>=0:
                                                            class_tmp1 = class_tmp.split(", [")[1]
                                                    if func_name_tmp == "setType":
                                                        var_tmp = lines[q - 1].split("{")[1]
                                                        var = var_tmp.split("}")[0].replace(" ", "")
                                                    if class_tmp1 + func_tmp1 not in func_name:
                                                        if func_tmp1 != "getString" and func_tmp1 != "toString" and func_tmp1 != "append":
                                                            func_name.append(class_tmp1 + func_tmp1)
                                                            break
                                            elif lines[q].find("const") >= 0 and lines[q].find(
                                                    pp + ",") >= 0 and q < j:
                                                value = lines[q].split(pp + ", ")[1]
                                                if lines[q].find("//") >= 0:
                                                    value = value.split(" //")[0].replace(" ", "")
                                                    func_name.append(value)
                                                    break
                                            q = q - 1

                            j = j + 1#while interno

                            #Scrivo tutto quello che ho trvato dentro al file  Esempio: android.support.v4.app.ActivityCompatJB startActivity v1 v0,v2 null startActivity,android.app.Activity;getReferrer,android.app.Activity;getPackageManager
                            if func_name and func_name_tmp != "<init>" and func_name_tmp != "append" and func_name_tmp != "toString":
                                item = class_name + " " + VirtualMethod + " " + ni + " " + var + " " + res
                                sep = ','
                                writecontent = item + " " + sep.join(func_name) + "\n"
                                if writecontent not in writelist:
                                    try:
                                        writelist.append(writecontent)
                                        intentfunc.write(writecontent)
                                    except UnicodeEncodeError:
                                        pass

                        j = j + 1#while esterno

                    if paramlist and paramlist not in paramlists:
                        paramlists.append(paramlist)


            i = i + 1

    print("\nStop read the code smali and creation file completed..\n")
    return path_outcome,path_outcome1