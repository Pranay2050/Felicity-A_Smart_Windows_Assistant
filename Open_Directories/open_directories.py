import win32gui, time
from win32con import PAGE_READWRITE, MEM_COMMIT, MEM_RESERVE, MEM_RELEASE, PROCESS_ALL_ACCESS, WM_GETTEXTLENGTH, WM_GETTEXT
from commctrl import LVS_OWNERDATA, LVM_GETITEMCOUNT, LVM_GETNEXTITEM, LVNI_SELECTED
import os
import struct
import ctypes
import win32api
import datetime
import win32com.client as win32
import win32ui
#import psutil
import subprocess
import time
import urllib.parse
import math
import re
import math
from collections import Counter


clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}' 

def getEditText(hwnd):
    # api returns 16 bit characters so buffer needs 1 more char for null and twice the num of chars
    buf_size = (win32gui.SendMessage(hwnd, WM_GETTEXTLENGTH, 0, 0) +1 ) * 2
    target_buff = ctypes.create_string_buffer(buf_size)
    win32gui.SendMessage(hwnd, WM_GETTEXT, buf_size, ctypes.addressof(target_buff))
    return target_buff.raw.decode('utf16')[:-1]# remove the null char on the end

def _normaliseText(controlText):
    '''Remove '&' characters, and lower case.
    Useful for matching control text.'''
    return controlText.lower().replace('&', '')

def _windowEnumerationHandler(hwnd, resultList):
    '''Pass to win32gui.EnumWindows() to generate list of window handle,
    window text, window class tuples.'''
    resultList.append((hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd)))

def searchChildWindows(currentHwnd,
               wantedText=None,
               wantedClass=None,
               selectionFunction=None):
    results = []
    childWindows = []
    try:
        win32gui.EnumChildWindows(currentHwnd,
                      _windowEnumerationHandler,
                      childWindows)
    except win32gui.error:
        # This seems to mean that the control *cannot* have child windows,
        # i.e. not a container.
        return
    for childHwnd, windowText, windowClass in childWindows:
        descendentMatchingHwnds = searchChildWindows(childHwnd)
        if descendentMatchingHwnds:
            results += descendentMatchingHwnds

        if wantedText and \
            not _normaliseText(wantedText) in _normaliseText(windowText):
                continue
        if wantedClass and \
            not windowClass == wantedClass:
                continue
        if selectionFunction and \
            not selectionFunction(childHwnd):
                continue
        results.append(childHwnd)
    return results


def explorer_fileselection():
    global clsid
    address_1=""
    files = []
    shellwindows = win32.Dispatch(clsid)
    w=win32gui
    window = w.GetForegroundWindow()
    #print("window: %s" % window)
    if (window != 0):
        if (w.GetClassName(window) == 'CabinetWClass'): # the main explorer window
            #print("class: %s" % w.GetClassName(window))
            #print("text: %s " %w.GetWindowText(window))
            children = list(set(searchChildWindows(window)))
            addr_edit = None
            file_view = None
            for child in children:
                if (w.GetClassName(child) == 'WorkerW'): # the address bar
                    addr_children = list(set(searchChildWindows(child)))
                    for addr_child in addr_children:
                        if (w.GetClassName(addr_child) == 'ReBarWindow32'):
                            addr_edit = addr_child
                            addr_children = list(set(searchChildWindows(child)))
                            for addr_child in addr_children:
                                if (w.GetClassName(addr_child) == 'Address Band Root'):
                                    addr_edit = addr_child
                                    addr_children = list(set(searchChildWindows(child)))
                                    for addr_child in addr_children:
                                        if (w.GetClassName(addr_child) == 'msctls_progress32'):
                                            addr_edit = addr_child
                                            addr_children = list(set(searchChildWindows(child)))
                                            for addr_child in addr_children:
                                                if (w.GetClassName(addr_child) == 'Breadcrumb Parent'):
                                                    addr_edit = addr_child
                                                    addr_children = list(set(searchChildWindows(child)))
                                                    for addr_child in addr_children:
                                                        if (w.GetClassName(addr_child) == 'ToolbarWindow32'):
                                                            text=getEditText(addr_child)
                                                            if "\\" in text:
                                                                address_1=getEditText(addr_child)[text.index(" ")+1:]
                                                                print("Address --> "+address_1)

    for window in range(shellwindows.Count):
        window_URL = urllib.parse.unquote(shellwindows[window].LocationURL,encoding='ISO 8859-1')
        window_dir = window_URL.split("///")[1].replace("/", "\\")
        return(window_dir)

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
    
def get_children():
    
    children_dict = {}
    
    if explorer_fileselection() == None:
        children_paths= [ f.path for f in os.scandir("C:\\Users\\ponki\\OneDrive\\Desktop") ]
    else:
        children_paths = [ f.path for f in os.scandir(explorer_fileselection()) ]
        
    children_names = [x.split("\\")[-1] for x in children_paths]
    
    for i in range(len(children_names)):
        if children_names[i][-3:] != "ini":
            if children_names[i] not in children_dict.keys():
                children_dict[children_names[i]] = children_paths[i]
                
    return children_dict

def open_child(string):
    children_dict = get_children()

    #string = "movielens"
    children_names = list(children_dict.keys())
    cosines = [get_cosine(string.lower(),i.lower()) for i in children_names]

    path = children_dict[children_names[cosines.index(max(cosines))]]
    os.startfile(path)