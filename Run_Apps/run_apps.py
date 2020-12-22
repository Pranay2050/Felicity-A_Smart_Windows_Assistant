import os
import math
import re
from collections import Counter

def list_files_path(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:    
                #if(file == "Uplay.lnk"):
                 #   os.startfile(subdir + "\\" + file)
                r.append(file)                                                                         
    return r 

def text_to_vector(text):
    WORD = re.compile(r"\w+")
    words = WORD.findall(text)
    return Counter(words)

def get_cosine(text1, text2):
    
    vec1 = text_to_vector(text1)
    vec2 = text_to_vector(text2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def initialize_app_dict():
    app_dict = {}

    apps = list_files("C:\\ProgramData\\Microsoft\\Windows\\Start Menu") + list_files("C:\\Users\\ponki\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu")
    apps_path = list_files_path("C:\\ProgramData\\Microsoft\\Windows\\Start Menu") + list_files_path("C:\\Users\\ponki\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu")

    for i in range(len(apps)):
        if apps[i][-3:] != "ini":
            if apps[i][:-4] not in app_dict.keys():
                app_dict[apps[i][:-4]] = apps_path[i]
                
    return app_dict

def run_app(app_name, app_dict):
    string = "steam"
    apps = list(app_dict.keys())
    cosines = [get_cosine(string.lower(),i.lower()) for i in apps]

    path = app_dict[apps[cosines.index(max(cosines))]]
    os.startfile(path)