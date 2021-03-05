# encoding: utf-8
import os

#Determinazione delle funzioni di manipolazione di Intent
def IntentSubstitute(file_intentfunc):
    type = ""
    with open(file_intentfunc, "r") as f: #legge il file che è stato lavorato dopo la lettura del code smali
        lines = f.readlines()
        lines_length = len(lines)
        i = 0

        VirtualMethod = []
        count = 0
        list0 = []
        list1 = []
        list2 = []
        satlist = []

        while i <= lines_length - 1:
            ClassNametmp = lines[i].split(" ")[0]
            VirtualMethodtmp = lines[i].split(" ")[1]
            targetIntenttmp = lines[i].split(" ")[2]
            otherOperationstmp = lines[i].split(" ")[3]
            finalIntenttmp = lines[i].split(" ")[4]
            relatedFunctmp = lines[i].split(" ")[5].replace("\n","")

            if VirtualMethodtmp not in VirtualMethod:
                count = 0
                Comptmp = ""
                Typetmp = ""
                list0 = []
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                list6 = []
                list7 = []
                list8 = []
                VirtualMethod.append(VirtualMethodtmp)
            else:
                count = count + 1
            
           

            #mi mette nella lista 0 tutte le righe del file dove compare la funzione, getComponent
            if relatedFunctmp.find("getComponent") != -1:
                Comptmp = finalIntenttmp
                list0.append(ClassNametmp)
                list0.append(VirtualMethodtmp)
                list0.append(targetIntenttmp)
                list0.append(otherOperationstmp)
                list0.append(finalIntenttmp)
                list0.append(relatedFunctmp)


            #mi mette nella lista 1 tutte le righe del file dove compare la funzione, setType
            elif relatedFunctmp.find("setType") != -1:
                Typetmp = otherOperationstmp
                list1.append(ClassNametmp)
                list1.append(VirtualMethodtmp)
                list1.append(targetIntenttmp)
                list1.append(otherOperationstmp)
                list1.append(finalIntenttmp)
                list1.append(relatedFunctmp)

            #mi mette nella lista 2 tutte le righe del file dove compare la funzione, setClassName
            elif relatedFunctmp.find("setClassName") != -1:
                list2.append(ClassNametmp)
                list2.append(VirtualMethodtmp)
                list2.append(targetIntenttmp)
                list2.append(otherOperationstmp)
                list2.append(finalIntenttmp)
                list2.append(relatedFunctmp)

            #mi mette nella lista 3 tutte le righe del file dove compare la funzione, setComponent   
            elif relatedFunctmp.find("setComponent") != -1:
                setComptmplist = [] #Queste liste sono sotto-liste :[['android.support.v4.app.NavUtils', 'getParentActivityIntent', 'v4', 'v3', 'null', 'setComponent,java.util.ArrayList;get']] ,[['com.morgoo.droidplugin.stub.ServcesManager', 'stopServiceToken', 'v1', 'v7', 'null', 'setComponent,#int-1']]
                setComptmplist.append(ClassNametmp)
                setComptmplist.append(VirtualMethodtmp)
                setComptmplist.append(targetIntenttmp)
                setComptmplist.append(otherOperationstmp)
                setComptmplist.append(finalIntenttmp)
                setComptmplist.append(relatedFunctmp)
                list3.append(setComptmplist)


            #mi mette nella lista 4 tutte le righe del file dove compare la funzione, putExtra    
            elif relatedFunctmp.find("putExtra") != -1:
                putExtratmplist = []
                putExtratmplist.append(ClassNametmp)
                putExtratmplist.append(VirtualMethodtmp)
                putExtratmplist.append(targetIntenttmp)
                putExtratmplist.append(otherOperationstmp)
                putExtratmplist.append(finalIntenttmp)
                putExtratmplist.append(relatedFunctmp)
                list4.append(putExtratmplist)

            #mi mette nella lista 5 tutte le righe del file dove compare la funzione, addFlags       
            elif relatedFunctmp.find("addFlags") != -1:
                list5.append(ClassNametmp)
                list5.append(VirtualMethodtmp)
                list5.append(targetIntenttmp)
                list5.append(otherOperationstmp)
                list5.append(finalIntenttmp)
                list5.append(relatedFunctmp)

            
            #mi mette nella lista 6 tutte le righe del file dove compare la funzione, access$
            elif relatedFunctmp.find("access$") != -1:
                accesstmplist = []
                accesstmplist.append(ClassNametmp)
                accesstmplist.append(VirtualMethodtmp)
                accesstmplist.append(targetIntenttmp)
                accesstmplist.append(otherOperationstmp)
                accesstmplist.append(finalIntenttmp)
                accesstmplist.append(relatedFunctmp)
                list6.append(accesstmplist)


            #mi mette nella lista 7 tutte le righe del file dove compare la funzione, startActivity   
            elif relatedFunctmp.find("startActivity") != -1:
                list7.append(ClassNametmp)
                list7.append(VirtualMethodtmp)
                list7.append(targetIntenttmp)
                list7.append(otherOperationstmp)
                list7.append(finalIntenttmp)
                list7.append(relatedFunctmp)
            
            #Tutto il resto me lo mette nella lista 8
            else:
                otherstmplist = []
                otherstmplist.append(ClassNametmp)
                otherstmplist.append(VirtualMethodtmp)
                otherstmplist.append(targetIntenttmp)
                otherstmplist.append(otherOperationstmp)
                otherstmplist.append(finalIntenttmp)
                otherstmplist.append(relatedFunctmp)
                list8.append(otherstmplist)


            #Qui capiscono che tipo di framework c'è

            # VirtualApp
            if len(list0) != 0 and len(list1) != 0 and len(list2) != 0: #liste non vuote per getcomponent,setType,setClassName


                if (list0[4] == list1[3] and list0[1] == list1[1] and list1[1] == list2[1] and list2[2] == list1[2] and list0[2] != list1[2]):
                    type = "Virtualapp"
                    if list2 not in satlist:
                        satlist.append(list2)

            
            
            # DroidPlugin
            if len(list3) == 1 and len(list4) != 0 and len(list5) != 0:  #liste non vuote per setComponent putExtra e addFlags

                #cicliamo gli elementi presenti nella lista che raccoglie gli elementi con chiave putExtra
                for extra in list4:
                    #print(f"\n{extra[3]} ---> {list5[3]}")
                    #Le prime due condizioni confronti le librerie com.morgoo ecc. Le due successive condizioni controlli le funzioni. infine nell'ultima condizione
                    # Se dentro il terzo elemento di extra trovi 1 registro v8,v9 ---> v8
                    if extra[0]== list3[0][0] and extra[0]== list5[0] and extra[1]== list3[0][1] and extra[1]== list5[1] and extra[3].find(list5[3])>=0:
                        #print(extra)#Entrato qui hai eliminato un po' di elementi. Come vedi vi sono android.support e com.morgoo.
                        '''
                        ['android.support.v7.widget.SearchView', 'createIntent', 'v0', 'v1,v2', 'null', 'putExtra,"user_query",#int0']
                        ['android.support.v7.widget.SearchView', 'createIntent', 'v0', 'v1,v7', 'null', 'putExtra,"query",android.support.v7.widget.SearchView$SearchAutoComplete;getDropDownBackground']
                        ['android.support.v7.widget.SearchView', 'createIntent', 'v0', 'v1,v6', 'null', 'putExtra,"intent_extra_data_key",#int1']
                        ['android.support.v7.widget.SearchView', 'createIntent', 'v0', 'v1,v2', 'null', 'putExtra,"app_data",#int0']
                        ['android.support.v7.widget.SearchView', 'createIntent', 'v0', 'v1,v8', 'null', 'putExtra,"action_key",#int1']
                        ['android.support.v7.widget.SearchView', 'createIntent', 'v0', 'v1,v9', 'null', 'putExtra,"action_msg","web_search"']
                        ['com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivities', 'beforeInvoke', 'v8', 'v7,v5', 'null', 'putExtra,java.util.List;iterator,#int0']
                        ['com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivities', 'beforeInvoke', 'v8', 'v7,v5', 'null', 'putExtra,java.util.List;iterator,#int0']
                        ['com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivities', 'beforeInvoke', 'v8', 'v7,v5', 'null', 'putExtra,java.util.List;iterator,#int0']
                        ['com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity', 'doReplaceIntentForStartActivityAPIHigh', 'v4', 'v6,v8', 'null', 'putExtra,com.morgoo.droidplugin.pm.PluginManager;getProcessNameByPid,"com.morgoo.droidplugin.OldIntent"']
                        ['com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity', 'doReplaceIntentForStartActivityAPILow', 'v2', 'v4,v5', 'null', 'putExtra,#int1,"com.morgoo.droidplugin.OldIntent"']
                        ['com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity', 'doReplaceIntentForStartActivityAPILow', 'v2', 'v4,v5', 'null', 'putExtra,#int1,"com.morgoo.droidplugin.OldIntent"']
                        ['com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity', 'doReplaceIntentForStartActivityAPILow', 'v2', 'v4,v5', 'null', 'putExtra,#int1,"com.morgoo.droidplugin.OldIntent"']
                        '''
                        
                        
                        if list5[5].find("#int268435456") >=0 and extra[5].find("OldIntent\"")>=0:#Con questo if prendi solo quelli gli ultimi 4.
                            #print(list5[5]) 
                            '''
                            addFlags,#int268435456
                            addFlags,#int268435456
                            addFlags,#int268435456
                            addFlags,#int268435456

                            Con list5[0]--> mi vengono fuori gli ultimi 4 della lista
                            com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity
                            com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity
                            com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity
                            com.morgoo.droidplugin.hook.handle.IActivityManagerHookHandle$startActivity
                            '''
                            type = "Droidplugin" #con la seconda condizione prendi e vedi che è Droidplugin

                            #qui dentro ne inserisce solo due perchè negli ultimi 4 ci sono duplicati
                            if list5 not in satlist:
                                satlist.append(list5)
                            break
                        

            i = i + 1#ciclo while

    return satlist,type
