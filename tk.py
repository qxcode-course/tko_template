#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations


from typing import List, Dict, Tuple, Optional, Any, Callable, Union, Set
import argparse
import sys
import json
import os
from urllib.request import urlopen
import urllib
import curses
import datetime
import random
import tempfile
import subprocess
import enum
import urllib.request
import urllib.error
import shutil
import re
import math
import configparser
from subprocess import PIPE
import unicodedata
__version__ = "0.24.6"


class CheckVersion:

    link = "https://raw.githubusercontent.com/senapk/tko/master/src/tko/__init__.py"

    def __init__(self):
        self.version: str = __version__
        self.latest_version: Optional[str] = self.get_latest_version()

    def version_check(self):
        if self.latest_version is None:
            return
        if self.version != self.latest_version:
            major, minor, patch = [int(x) for x in self.version.split(".")]
            latest_major, latest_minor, latest_patch = [int(x) for x in self.latest_version.split(".")]
            if major < latest_major or (major == latest_major and minor < latest_minor):
                print(f"Sua versão do  TKO ({self.version}) está desatualizada.")
                print(f"A última versão é a {self.latest_version}.")

    def get_latest_version(self):
        try:
            with urlopen(self.link) as f:
                for line in f:
                    if b"__version__" in line:
                        return line.decode().split('"')[1]
        except:
            return None
class Colors:
    def __init__(self):
        self.focused_item = "B"
        self.task_text_done = "g"
        self.task_text_todo = "y"
        self.button_flag_on = "G"
        self.button_flag_off = "Y"
        self.progress_skill_done = "C"
        self.progress_skill_todo = "M"
        self.main_bar_done = "G"
        self.main_bar_todo = "R"
        self.task_skills = "c"
        self.task_new = "g"
        self.mark_nothing = "m"
        self.mark_started = "r"
        self.mark_required = "y"
        self.mark_complete = "g"
    
    def to_dict(self):
        return self.__dict__
    
    def from_dict(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self


def random_get(dic: dict, str_key: str, mode:str = "static"):
    if mode == "static":
        count = sum([ord(c) for c in str_key])
        keys = list(dic.keys())
        return dic[keys[count % len(keys)]]
    else:
        keys = list(dic.keys())
        return dic[random.choice(keys)]

opening: Dict[str, str] = {}

opening["parrot"] = r"""
                           .    
                          | \/| 
                          ) )|/|
                    _----. /.'.'
.-._________..      .' @ _\  .' 
'.._______.   '.   /    (_| .') 
  '._____.  /   '-/      | _.'  
   '.______ (         ) ) \     
     '..____ '._       )  )     
        .' __.--\  , ,  // ((   
        '.'     |  \/   (_.'(   
                '   \ .'        
                 \   (          
                  \   '.        
                   \ \ '.)      
                    '-'-'       
"""

opening["estuda"] = r"""
 ,`````.          __||||___       
' Estuda`,       /_  ___   \      
'carniça!`.     /@ \/@  \   \     
 ` , . , '  `.. \__/\___/   /     
                 \_\/______/      
                 /     /\\\\\     
                |     |\\\\\\     
                 \      \\\\\\    
                  \______/\\\\    
            _______ ||_||_______  
           (______(((_(((______(@)
"""


opening["alien3"] = r"""
           \.   \.      __,-"-.__      ./   ./
       \.   \`.  \`.-'"" _,="=._ ""`-.'/  .'/   ./
        \`.  \_`-''      _,="=._      ``-'_/  .'/
         \ `-',-._   _.  _,="=._  ,_   _.-,`-' /
      \. /`,-',-._ ""  \ _,="=._ /   ""_.-,`-,'\ ./
       \`-'  /    `-._  "       "  _.-'    \  `-'/
       /)   (   BOM   \    ,-.    / ESTUDO  )   (\
    ,-'"     `-.       \  /   \  /       .-'     "`-,
  ,'_._         `-.____/ /  _  \ \____.-'         _._`,
 /,'   `.                \_/ \_/                .'   `,\
/'       )                  _                  (       `\
        /   _,-'"`-.  ,++|T|||T|++.  .-'"`-,_   \
       / ,-'        \/|`|`|`|'|'|'|\/        `-, \
      /,'             | | | | | | |             `,\
     /'               ` | | | | | '               `\
"""

opening["alien4"] = r"""
            ______              ______
           /___   \___\ || /___/   ___\
          //\]/\ ___  \\||//  ___ /\[/\\
          \\/[\//  _)   \/   (_  \\/]\//
           \___/ _/   o    o   \_ \___/
               _/                \_
              //'VvvvvvvvvvvvvvvV'\\
             ( \.'^^^^^^^^^^^^^^'./ )
              \____   . .. .   ____/
   ________        \ . .''. . /        ________
  /______  \________)________(________/ _______\
 /|       \ \  Estuda seu miserável  / /       |\
(\|____   / /                        \ \   ____|/)
"""

opening["alien5"] = r"""
                   ⢀⡀⠤⠤⠤⠄ ⠒⠢⣄    
                ⡠⠐⢈⠄        ⢸⠓⠄  
              ⠐⠈⠠⠊         ⡠⠊ ⠈⢂ 
            ⢀⠊ ⡐⠁        ⢠⢊⠔⠈   ⠆
           ⣠⡃ ⢰    ⢀⡠⠄⠐⠒ ⢸⢜⠄     
          ⡐⣁⡑ ⠘  ⢀⠔⢁⣀⣤⣤⣤⣒⣤ ⠈    ⡄
          ⢫⣿⢧ ⢸  ⣡⣶⣯⠭⢄⣀⣼⡏⠁⢀⡤   ⢐⠁
          ⢠⢿⣾⣧⠈ ⢠⣿⣿⣗⢢⣤⣿⡿⢋ ⡏    ⡌ 
   Gosto  ⠘⠳⠙⠻  ⠰⠿⠟⠛⠻⢍⠫⠒⠁⡰   ⢀⠜  
    de    ⠘⢄          ⢀⠠⢊ ⡇⢠⠒⠁   
   comer    ⠈⢦⠂    ⢠⠊⠁ ⢀⠄ ⡇⢸     
 cérebros    ⠘⢄⡄⢤⢄ ⠘⡄  ⡀⠄⢊⡅⡆⢆    
    de         ⢊   ⠈⢁⠴⠅⣀⣀⠘⢣⠠⠈⠢⢀  
  alunos       ⠈⠢⢄⣀⡠⠊  ⠈⢣ ⠈⠃⠡  ⠉⠐
preguiçosos             ⠰⠇  ⠐⡑⠤⢀ 
"""

intro: Dict[str, str] = {}
# intro["shark"] = r"""
#   _________         .    . r -> Roda sem testar             
#  (..       \_    ,  |\  /| ↲ -> Testa usando casos de teste 
#   \       O  \  /|  \ \/ / f -> FIXA a execução para        
#    \______    \/ |   \  /       um único caso de teste      
#       vvvv\    \ |   /  |  TAB  Muda o arquivo PRINCIPAL    
#       \^^^^  ==   \_/   |       para problemas de múltiplos 
#        `\_   ===    \.  |       arquivos de código fonte    
#        / /\_   \ /      |  m -> muda o MODO diff de vertical
#        |/   \_  \|      /       para modo diff horizontal   
#               \________/   t -> define o limite de TEMPO    
#                            setas -> muda o teste            
# """

# intro["cat"] = r"""
#  ,_     _          r -> Roda sem testar             
#  |\\_,-~/          ↲ -> Testa usando casos de teste 
#  / _  _ |    ,--.  f -> FIXA a execução para        
# (  @  @ )   / ,-'       um único caso de teste      
#  \  _T_/-._( (     TAB  Muda o arquivo PRINCIPAL    
#  /         `. \         para problemas de múltiplos 
# |         _  \ |        arquivos de código fonte    
#  \ \ ,  /      |   m -> muda o MODO diff de vertical
#   || |-_\__   /         para modo diff horizontal   
#  ((_/`(____,-'     t -> define o limite de TEMPO    
#                    setas -> muda o teste            
# """

intro["elephant"] = r"""
        ⣀⣀                r -> Roda sem testar             
      ⣰⣿⣿⣿⣿⣦⣀⣀⣀           ↲ -> Testa usando casos de teste 
      ⢿⣿⠟⠋⠉    ⠉⠑⠢⣄⡀      f -> FIXA a execução para        
     ⢠⠞⠁           ⠙⢿⣿⣿⣦⡀      um único caso de teste      
 ⣀  ⢀⡏ ⢀⣴⣶⣶⡄         ⢻⣿⣿⠇ TAB  Muda o arquivo PRINCIPAL    
⣾⣿⣿⣦⣼⡀ ⢺⣿⣿⡿⠃    ⣠⣤⣄  ⠈⡿⠋       para problemas de múltiplos 
⢿⣿⣿⣿⣿⣇ ⠤⠌⠁ ⡀⢲⡶⠄⢸⣏⣿⣿   ⡇        arquivos de código fonte    
⠈⢿⣿⣿⣿⣿⣷⣄⡀  ⠈⠉⠓⠂ ⠙⠛⠛⠠ ⡸⠁   m -> muda o MODO diff de vertical
  ⠻⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀    ⠑ ⣠⠞⠁         para modo diff horizontal   
   ⢸⡏⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⡄      t -> define o limite de TEMPO    
   ⠸        ⠈⠉⠛⢿⣿⣿⣿⣿⡄     setas -> muda o teste            
"""

compilling: Dict[str, str] = {}

# compilling["bloody"] = r"""
#  ▄████▄   ▒█████   ███▄ ▄███▓ ██▓███   ██▓ ██▓    ▄▄▄       ███▄    █ ▓█████▄  ▒█████  
# ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓██░  ██▒▓██▒▓██▒   ▒████▄     ██ ▀█   █ ▒██▀ ██▌▒██▒  ██▒
# ▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▓██░ ██▓▒▒██▒▒██░   ▒██  ▀█▄  ▓██  ▀█ ██▒░██   █▌▒██░  ██▒
# ▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒██▄█▓▒ ▒░██░▒██░   ░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█▄   ▌▒██   ██░
# ▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒▒██▒ ░  ░░██░░██████▒▓█   ▓██▒▒██░   ▓██░░▒████▓ ░ ████▓▒░
# ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░▒▓▒░ ░  ░░▓  ░ ▒░▓  ░▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ 
#   ░  ▒     ░ ▒ ▒░ ░  ░      ░░▒ ░      ▒ ░░ ░ ▒  ░ ▒   ▒▒ ░░ ░░   ░ ▒░ ░ ▒  ▒   ░ ▒ ▒░ 
# ░        ░ ░ ░ ▒  ░      ░   ░░        ▒ ░  ░ ░    ░   ▒      ░   ░ ░  ░ ░  ░ ░ ░ ░ ▒  
# ░ ░          ░ ░         ░             ░      ░  ░     ░  ░         ░    ░        ░ ░  
# ░                                                                      ░               
# """


numbers = r"""
  __    __     _   ____  ____   ___   ___   ___  ____  ____  ___  
 /  \  /  \   / ) (___ \( __ \ / _ \ / __) / __)(__  )/ _  \/ _ \ 
(  0 )(_/ /  / /   / __/ (__ ((__  ((___ \(  _ \  / / ) _  (\__  )
 \__/  (__) (_/   (____)(____/  (__/(____/ \___/ (_/  \____/(___/ 
"""


executing: str = r"""
███████╗██╗  ██╗███████╗ ██████╗██╗   ██╗████████╗ █████╗ ███╗   ██╗██████╗  ██████╗ 
██╔════╝╚██╗██╔╝██╔════╝██╔════╝██║   ██║╚══██╔══╝██╔══██╗████╗  ██║██╔══██╗██╔═══██╗
█████╗   ╚███╔╝ █████╗  ██║     ██║   ██║   ██║   ███████║██╔██╗ ██║██║  ██║██║   ██║
██╔══╝   ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║   ██╔══██║██║╚██╗██║██║  ██║██║   ██║
███████╗██╔╝ ██╗███████╗╚██████╗╚██████╔╝   ██║   ██║  ██║██║ ╚████║██████╔╝╚██████╔╝
╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ 
"""

compilling["computer"] = r"""
 ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗██╗      █████╗ ███╗   ██╗██████╗  ██████╗ 
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║██║     ██╔══██╗████╗  ██║██╔══██╗██╔═══██╗
██║     ██║   ██║██╔████╔██║██████╔╝██║██║     ███████║██╔██╗ ██║██║  ██║██║   ██║
██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║██║     ██╔══██║██║╚██╗██║██║  ██║██║   ██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║███████╗██║  ██║██║ ╚████║██████╔╝╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ 
"""

# compilling["edge]"] = r"""
# ▄█▄    ████▄ █▀▄▀█ █ ▄▄  ▄█ █    ██      ▄   ██▄   ████▄
# █▀ ▀▄  █   █ █ █ █ █   █ ██ █    █ █      █  █  █  █   █
# █   ▀  █   █ █ ▄ █ █▀▀▀  ██ █    █▄▄█ ██   █ █   █ █   █
# █▄  ▄▀ ▀████ █   █ █     ▐█ ███▄ █  █ █ █  █ █  █  ▀████
# ▀███▀           █   █     ▐     ▀   █ █  █ █ ███▀       
#                ▀     ▀             █  █   ██            
#                                   ▀                     
# """

success: Dict[str, str] = {}


success["success"] = r"""
███████╗██╗   ██╗ ██████╗███████╗███████╗███████╗ ██████╗ 
██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔═══██╗
███████╗██║   ██║██║     █████╗  ███████╗███████╗██║   ██║
╚════██║██║   ██║██║     ██╔══╝  ╚════██║╚════██║██║   ██║
███████║╚██████╔╝╚██████╗███████╗███████║███████║╚██████╔╝
╚══════╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚══════╝ ╚═════╝ 
"""

# success["success3"] = r"""
#   ██████  █    ██  ▄████▄  ▓█████   ██████   ██████  ▒█████  
# ▒██    ▒  ██  ▓██▒▒██▀ ▀█  ▓█   ▀ ▒██    ▒ ▒██    ▒ ▒██▒  ██▒
# ░ ▓██▄   ▓██  ▒██░▒▓█    ▄ ▒███   ░ ▓██▄   ░ ▓██▄   ▒██░  ██▒
#   ▒   ██▒▓▓█  ░██░▒▓▓▄ ▄██▒▒▓█  ▄   ▒   ██▒  ▒   ██▒▒██   ██░
# ▒██████▒▒▒▒█████▓ ▒ ▓███▀ ░░▒████▒▒██████▒▒▒██████▒▒░ ████▓▒░
# ▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ 
# ░ ░▒  ░ ░░░▒░ ░ ░   ░  ▒    ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░  ░ ▒ ▒░ 
# ░  ░  ░   ░░░ ░ ░ ░           ░   ░  ░  ░  ░  ░  ░  ░ ░ ░ ▒  
#       ░     ░     ░ ░         ░  ░      ░        ░      ░ ░  
#                   ░                                          
# """

# success["success4"] = r"""
#   █████████                                                       
#  ███░░░░░███                                                      
# ░███    ░░░  █████ ████  ██████   ██████   █████   █████   ██████ 
# ░░█████████ ░░███ ░███  ███░░███ ███░░███ ███░░   ███░░   ███░░███
#  ░░░░░░░░███ ░███ ░███ ░███ ░░░ ░███████ ░░█████ ░░█████ ░███ ░███
#  ███    ░███ ░███ ░███ ░███  ███░███░░░   ░░░░███ ░░░░███░███ ░███
# ░░█████████  ░░████████░░██████ ░░██████  ██████  ██████ ░░██████ 
#  ░░░░░░░░░    ░░░░░░░░  ░░░░░░   ░░░░░░  ░░░░░░  ░░░░░░   ░░░░░░  
# """

# success["success5"] = r"""
# .▄▄ · ▄• ▄▌ ▄▄· ▄▄▄ ..▄▄ · .▄▄ ·       
# ▐█ ▀. █▪██▌▐█ ▌▪▀▄.▀·▐█ ▀. ▐█ ▀. ▪     
# ▄▀▀▀█▄█▌▐█▌██ ▄▄▐▀▀▪▄▄▀▀▀█▄▄▀▀▀█▄ ▄█▀▄ 
# ▐█▄▪▐█▐█▄█▌▐███▌▐█▄▄▌▐█▄▪▐█▐█▄▪▐█▐█▌.▐▌
#  ▀▀▀▀  ▀▀▀ ·▀▀▀  ▀▀▀  ▀▀▀▀  ▀▀▀▀  ▀█▄▀▪
# """

# success["success6"] = r"""
#    ▄▄▄▄▄   ▄   ▄█▄    ▄███▄     ▄▄▄▄▄    ▄▄▄▄▄   ████▄
#   █     ▀▄  █  █▀ ▀▄  █▀   ▀   █     ▀▄ █     ▀▄ █   █
# ▄  ▀▀▀▀▄ █   █ █   ▀  ██▄▄   ▄  ▀▀▀▀▄ ▄  ▀▀▀▀▄   █   █
#  ▀▄▄▄▄▀  █   █ █▄  ▄▀ █▄   ▄▀ ▀▄▄▄▄▀   ▀▄▄▄▄▀    ▀████
#          █▄ ▄█ ▀███▀  ▀███▀                           
#           ▀▀▀                                         
# """

# --------------------------------------------------------------

images: Dict[str, str] = {}

images["pink"] = r"""
Programando assim, você vai dominar o mundo!
                 /`.    /`.                       
                f   \  ,f  \                      
                |    \/-`\  \                     
                i.  _\';.,X j                     
                 `:_\ (  \ \',-.                  
                   .'"`\ a\eY' )               _,.
                   `._"\`-' `-/            .-;'  |
                     /;-`._.-';\.        ,',"    |
                   .'/   "'   | `\.-'""-/ /      j
                 ,/ /         i,-"        (  ,/  /
              .-' .f         .'            `"/  / 
             / ,,/ffj\      /          .-"`.'-.'  
            / /_\`--//)     \ ,--._ .-'_,-'; /    
           f  ".-"-._;'      `._ _.,-i; /_; /     
           `.,'   |; \          \`\_,/-'  \'      
            .'    l \ `.        /"\ _ \`  j       
            f      : `-'        `._;."/`-'        
"""

images["batman"] = r"""
Não é o que sou por dentro, é o que eu faço que me define.
                     .  .          
                     |\_|\         
                     | a_a\        
                     | | "]        
                 ____| '-\___      
                /.----.___.-'\     
               //        _    \    
              //   .-. (~v~) /|    
             |'|  /\:  .--  / \    
            // |-/  \_/____/\/~|   
           |/  \ |  []_|_|_] \ |   
           | \  | \ |___   _\ ]_}  
           | |  '-' /   '.'  |     
           | |     /    /|:  |     
           | |     |   / |:  /\    
           | |     /  /  |  /  \   
           | |    |  /  /  |    \  
           \ |    |/\/  |/|/\    \ 
            \|\ |\|  |  | / /\/\__\
             \ \| | /   | |__      
                  / |   |____)     
                  |_/              
"""


images["vegeta"] = r"""
O miserável é um gênio!
    ⢨⠊ ⢀⢀   ⠈⠺⡵⡱   ⢠⠃ ⡀         ⡘⢰⡁⠉⠊⠙⢎⣆    ⢩⢀⠜   
   ⢠⠃  ⢸⢸⡀    ⠘⢷⡡  ⠎ ⢰⣧  ⠈⡆       ⠈⣐⢤⣀⣀⢙⠦    ⡇    
  ⢀⠃   ⡌⢸⠃   ⢀  ⠑⢧⡸ ⢀⣿⢻⡀  ⣻     ⣠⡴⠛⠉   ⠑⢝⣦   ⢰⠠⠁  
  ⠌   ⡘⣖⣄⢃   ⠈⢦⡀ ⡜⡇ ⣼⠃⠈⢷⣶⢿⠟   ⢠⠞⠁ ⣀⠄⠂⣶⣶⣦⠆⠋⠓ ⢀⣀⡇   
⠡⡀⡇ ⢰⣧⢱⠊⠘⡈⠄  ⡀⠘⣿⢦⣡⢡⢰⡇⢀⠤⠊⡡⠃  ⢀⡴⠁⢀⠔⠊  ⢠⣿⠟⠁ ⢀ ⢀⠾⣤⣀  ⡠
⡀⠱⡇ ⡆⢃   ⠃   ⣧⣀⣹⡄⠙⡾⡏ ⡌⣠⡾⠁  ⣠⠊⢠⠔⠁    ⣸⡏   ⢨⣪⡄⢻⣥⠫⡳⢊⣴
  ⢡⢠ ⢸⡆ ⣀    ⠈⣛⢛⣁⣀⠘⣧⣀⢱⡿  ⢀⡔⢁⢔⠕⠉⠐⣄⣠⠤⠶⠛⠁⢀⣀  ⠉⠁⠈⠷⣞⠔⡕⣿
⢄⡀⠘⢸ ⣘⠇        ⠉⠐⠤⡑⢎⡉⢨⠁ ⣠⢏⠔⠁⠘⣤⠴⢊⣡⣤⠴⠖⠒⠻⠧⣐⠓    ⠈ ⡜ ⠇
⠤⡈⠑⠇⠡⣻⢠⠊⠉⠉⠉⠑⠒⠤⣀   ⠈⣾⣄⢘⣫⣜⠮⢿⣆⡴⢊⢥⡪⠛⠉    ⢀⠄⠂⠁      ⢧⡀⠈
⠁⠈⠑⠼⣀⣁⣇ ⣴⡉⠉⠉ ⠒⡢⠌⣐⡂⠶⣘⢾⡾⠿⢅ ⣠⣶⡿⠓⠁⢠⠖⣦⡄   ⠊         ⠈⢎⢳
    ⠉⣇⣿⢜⠙⢷⡄   ⣄⣠⠼⢶⡛⣡⢴ ⢀⠛⠱⡀    ⢀⠎ ⠁            ⢠⡋⠮⡈
  ⢀⣖⠂⢽⡈ ⠈⠑⠻⡦⠖⢋⣁⡴⠴⠊⣉⡠⢻⡖⠪⢄⡀⢈⠆  ⢠⠊⢠             ⢀⠤⡵⢤⣃
  ⠸⢠⡯⣖⢵⡀  ⣠⣤⠮⠋⠁     ⠸⣌⢆⢱⡾⠃⢀⠠⠔⠁⣀⢸     ⡄       ⡸⠚⡸⠈⠁
⠤⢀⣀⢇⢡⠸⡗⢔⡄⠸⠊           ⠉⡩⠔⢉⡠⠔⠂⠉⢀⠆            ⢠⢁⠎⢀⡠⠔
   ⠘⡌⢦⡃⣎⠘⡄        ⠠⡟⠠⡐⣋⠤ ⣀⠤⠐⠂⠉⠁             ⡸⢉⠉⠁  
⠤   ⠰⡀⠈⠻⡤⠚⢄  ⢠       ⠈⠂⠒⠉                  ⢠⠃⢸ ⢀⠤⠊
⣀    ⠘⠢⡑⢽⡬⢽⢆ ⠈           ⣠⣤⡶⠟⣉⣉⢢          ⢀⠇ ⠈⡖⠓⠒⠂
 ⢈⣑⣒⡤⠄ ⠈⠑⠥⣈⠙⠧           ⢰⣁⠔⠊⠁        ⡜   ⣠⡻   ⠇⠐⡔⣡
⠉⠉⠁ ⠒⠒⠒⠒ ⠤⠤⠍⣒⡗⢄⡀        ⠈           ⡸  ⢠⡞⢡⠃   ⢸ ⠸⣡
            ⢠  ⠈⣶⢄⡀                ⡰⠁⣠⡔⠉ ⡎    ⢸  ⠃
         ⢠⠇⣀⢼   ⢉⡄⠈⠐⠤⣀         ⢀⡀ ⡜⡡⣾⠃  ⠸      ⡧⢄⡈
       ⣀⠤⠚⠉ ⡆   ⠈⡵⢄⡀  ⠙⠂⠄⣀⡀⠤⠊⠉⢀⣀⣠⡴⢿⣟⠞  ⢀⠇      ⡗⠢⢌
    ⡠⠔⠉  ⢀⡠⡤⠇  ⢀ ⠰⣣⠈⠐⠤⡀ ⡀⠈⠙⢍⠉⣉⠤⠒⠉⣠⣟⢮⠂⡄ ⣼⠁ ⡆    ⢡⣀ 
⣿⡷⠖⠉  ⡠⠔⣪⣿⠟⣫   ⢸  ⢩⢆  ⠈⠑⢳⠤⠄⠠⠭⠤⠐⠂⢉⣾⢮⠃⢠⠃⢰⡹ ⢰     ⢸⡉⣳
⠉ ⢀⡠⠒⠉⣠⠾⠋⢁⠔⠹   ⡈⡇  ⢫⣆   ⠘⣆      ⣘⢾⠃⢀⠏⣠⡳⠁ ⣾      ⠈⠉
"""



images["esqueleto"] = r"""
Você venceu o desafio, mas não a guerra!
Espero você no próximo nível!
                              _.--""-._                     
  .                         ."         ".                   
 / \    ,^.         /(     Y             |      )\          
/   `---. |--'\    (  \__..'--   -   -- -'""-.-'  )         
|        :|    `>   '.     l_..-------.._l      .'          
|      __l;__ .'      "-.__.||_.-'v'-._||`"----"            
 \  .-' | |  `              l._       _.'                   
  \/    | |                   l`^^'^^'j                     
        | |                _   \_____/     _                
        j |               l `--__)-'(__.--' |               
        | |               | /`---``-----'"1 |  ,-----.      
        | |               )/  `--' '---'   \'-'  ___  `-.   
        | |              //  `-'  '`----'  /  ,-'   I`.  \  
      _ L |_            //  `-.-.'`-----' /  /  |   |  `. \ 
     '._' / \         _/(   `/   )- ---' ;  /__.J   L.__.\ :
      `._;/7(-.......'  /        ) (     |  |            | |
      `._;l _'--------_/        )-'/     :  |___.    _._./ ;
        | |                 .__ )-'\  __  \  \  I   1   / / 
        `-'                /   `-\-(-'   \ \  `.|   | ,' /  
                           \__  `-'    __/  `-. `---'',-'   
                              )-._.-- (        `-----'      
                             )(  l\ o ('..-.                
                       _..--' _'-' '--'.-. |                
                __,,-'' _,,-''            \ \               

"""

images["coiote"] = r"""
Você fez essa questão muito rápido, da próxima vez
vou aumentar a dificuldade!
                      _                                   
                     : \                                  
                     ;\ \_                   _            
                     ;@: ~:              _,-;@)           
                     ;@: ;~:          _,' _,'@;           
                     ;@;  ;~;      ,-'  _,@@@,'           
                    |@(     ;      ) ,-'@@@-;             
                    ;@;   |~~(   _/ /@@@@@@/              
                    \@\   ; _/ _/ /@@@@@@;~               
                     \@\   /  / ,'@@@,-'~                 
                       \\  (  ) :@@(~                     
                    ___ )-'~~~~`--/ ___                   
                   (   `--_    _,--'   )                  
                  (~`- ___ \  / ___ -'~)                  
                 __~\_(   \_~~_/   )_/~__                 
 /\ /\ /\     ,-'~~~~~`-._ 0\/0 _,-'~~~~~`-.              
| |:  ::|    ;     ______ `----'  ______    :             
| `'  `'|    ;    {      \   ~   /      }   |             
 \_   _/     `-._      ,-,' ~~  `.-.      _,'        |\   
   \ /_          `----' ,'       `, `----'           : \  
   |_( )                `-._/#\_,-'                  :  ) 
 ,-'  ~)           _,--./  (###)__                   :  : 
 (~~~~_)          /       ; `-'   `--,               |  ; 
 (~~~' )         ;       /@@@@@@.    `.              | /  
 `.HH~;        ,-'  ,-   |@@@ @@@@.   `.             .')  
  `HH `.      ,'   /     |@@@@@ @@@@.  `.           / /(~)
   HH   \_   ,'  _/`.    |@@@@@ @@@@@;  `.          ; (~~)
   ~~`.   \_,'  /   ;   .@@@@@ @@@@@@;\_  \___      ; H~\)
"""

images["piupiu"] = r"""
Eu acho que eu vi um programador!
                 $                
              $  $   $$           
              $ $$ $$             
         $$$$      $$$$$$         
       $$                $$       
     $$        $$          $$     
   $$                        $$   
  $$                          $$  
  $                           $ $ 
 $                $             $ 
 $             $$$$              $
 $            $$ $           $   $
 $          $$$$$$       $$$$    $
 $         $$$$$$$      $$  $    $
  $        $$$$$ $     $$$$$$   $ 
  $$       $     $    $$$$$$   $$ 
   $$      $    $    $$$$     $   
    $      $   $     $       $    
    $      $$$$         $  $$     
    $$               $$$  $       
     $$$       $$$$$      $       
        $$$     $$       $$       
            $$     $$$$$$         
          $$      $$ $            
       $$$$        $ $$           
         $  $$     $   $          
    $$$$$$ $       $  $           
  $$   $$$$ $      $   $$$$$$$    
  $$      $$$$     $ $$     $$    
  $          $$$$$$$$         $   
   $$         $   $          $    
    $$$$$$$$$$$   $$$$$$$$$$$ ~*  
"""

images["saitama"] = r"""
Se garantiu
        ⣠⣴⣶⡋⠉⠙⠒⢤⡀     ⢠⠖⠉⠉⠙⠢⡄ 
      ⢀⣼⣟⡒⠒     ⠙⣆   ⢠⠃     ⠹⡄
      ⣼⠷⠖        ⠘⡆  ⡇       ⢷
      ⣷⡒  ⢐⣒⣒⡒ ⣐⣒⣒⣧  ⡇ ⢠⢤⢠⡠  ⢸
     ⢰⣛⣟⣂ ⠘⠤⠬⠃⠰⠑⠥⠊⣿ ⢴⠃ ⠘⠚⠘⠑⠐ ⢸
     ⢸⣿⡿⠤     ⢀⡆  ⣿  ⡇       ⣸
     ⠈⠿⣯⡭    ⢀⣀   ⡟  ⢸      ⢠⠏
       ⠈⢯⡥⠄      ⡼⠁   ⠳⢄⣀⣀⣀⡴⠃ 
         ⢱⡦⣄⣀⣀⣀⣠⠞⠁      ⠈⠉    
       ⢀⣤⣾⠛⠃   ⢹⠳⡶⣤⡤⣄         
    ⣠⢴⣿⣿⣿⡟⡷⢄⣀⣀⣀⡼⠳⡹⣿⣷⠞⣳        
   ⢰⡯⠭⠹⡟⠿⠧⠷⣄⣀⣟⠛⣦⠔⠋⠛⠛⠋⠙⡆       
  ⢸⣿⠭⠉ ⢠⣤   ⠘⡷⣵⢻    ⣼ ⣇       
  ⡇⣿⠍⠁ ⢸⣗⠂   ⣧⣿⣼    ⣯ ⢸  
"""

images["cool"] = r"""
Essa foi show de bola!
       ⢀⣠⣤⣴⡾⠻⢶⣤⡀ 
     ⢀⣶⠟⠉⠉    ⠉⢷⡄
   ⠉⢿⣿⣿⣿⠏⠈⢿⣿⣿⣿⡿⢟⣿
    ⢸⡏ ⢠⣀ ⢀⡤   ⢨⣿
    ⠸⣿⡀ ⠉⠉⠉  ⢀⣠⡾⠃
     ⠈⠻⠷⠶⣶⡶⠾⠿⠛⠉  
 ⢀⡀     ⢀⣿       
⠿⢿⣧⡀    ⣸⣟       
  ⠘⢿⡄ ⣠⡾⢻⣿⣄      
    ⢿⣴⡟ ⢸⡏⠹⣧     
    ⠈⠛  ⢸⣟ ⠹⣧    
"""

images["among"] = r"""
Sossegue, você não é um importor
           ⣠⣤⣤⣤⣤⣤⣶⣦⣤⣄⡀         
        ⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣿⣷⣤⡀      
        ⣼⣿⠋       ⢀⣀⣀⠈⢻⣿⣿⡄     
       ⣸⣿⡏   ⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄    
       ⣿⣿⠁  ⢰⣿⣿⣯⠁       ⠈⠙⢿⣷⡄  
  ⣀⣤⣴⣶⣶⣿⡟   ⢸⣿⣿⣿⣆          ⣿⣷  
 ⢰⣿⡟⠋⠉⣹⣿⡇   ⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿  
 ⢸⣿⡇  ⣿⣿⡇    ⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃  
 ⣸⣿⡇  ⣿⣿⡇     ⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⡇   
 ⣿⣿⠁  ⣿⣿⡇                ⢸⣿⣧   
 ⣿⣿   ⣿⣿⡇                ⢸⣿⣿   
 ⣿⣿   ⣿⣿⡇                ⢸⣿⣿   
 ⢿⣿⡆  ⣿⣿⡇                ⢸⣿⡇   
 ⠸⣿⣧⡀ ⣿⣿⡇                ⣿⣿⠃   
  ⠛⢿⣿⣿⣿⣿⣇     ⣰⣿⣿⣷⣶⣶⣶⣶⠶ ⢠⣿⣿    
       ⣿⣿     ⣿⣿⡇ ⣽⣿⡏⠁  ⢸⣿⡇    
       ⣿⣿     ⣿⣿⡇ ⢹⣿⡆   ⣸⣿⠇    
       ⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁ ⠈⠻⣿⣿⣿⣿⡿⠏     
       ⠈⠛⠻⠿⠿⠿⠿⠋⠁               
"""

images["heart"] = r"""
O código ficou lindo dessa vez!
     ⣀⣀⣀⡀          ⣀⣠⣠⣴⣦⣤⣤⣄⣀   
  ⣰⣼⣿⣯⢭⣿⣿⣿⣻⣶⣤⡀  ⢀⣠⣾⣿⣿⣾⣿⣿⣿⣽⣿⣿⣻⣦⡀
 ⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢀⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⠊⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠎⠠⠐⡉⢉⠁⠘⣭⣿⣿⣿⣿⣿⣿⣿⡿ 
⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠈⠄⡁⠂⢀⠂⡬⣾⣿⣿⣿⣿⣿⣿⣿⣿⠁ 
 ⠈⢿⣿⣿⣿⣿⣿⣶⣤⣖⡂⠌⠐⠠⠐⢨⢀⠄⠘⢜⢿⣿⣿⣿⣿⣿⣿⠃  
   ⠹⣿⣿⣿⣿⣿⣿⣿⣿⠆⠁⢂⠅⣒⡈⠤⠈⡈ ⠻⣿⣿⣿⡿⠃   
    ⠙⢿⣿⣿⣿⣿⣿⣿⣄⡦⣠⣾⣿⣿⣿⣷⣾⣤⣗⣹⣿⡟     
      ⠘⠿⣿⣿⣿⣿⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏      
        ⠻⢿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏       
          ⠘⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁        
             ⠙⠿⢿⣿⣿⣿⡿⠋          
"""

images["pikachu"] = r"""
        Picapi!          
⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿    ⣠⣤⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿   ⢰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
⣿⣿⣿⣿⣿⣿   ⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁ ⣿
⣿⣿⣿⣿⣿⣿⣧⡀    ⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉     ⣸⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄ ⡀               ⢀⣴⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏              ⠠⣴⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟  ⢰⣹⡆      ⣭⣷   ⠸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃  ⠈⠉  ⠤⠄   ⠉⠁    ⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷    ⡠⠤⢄   ⠠⣿⣿⣷ ⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉     ⢄ ⢀    ⠉⠉⠁  ⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧       ⠈          ⢹⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃                 ⢸⣿⣿
"""

images["yoda"] = r"""
Que a força esteja com você
 ⢀⣠⣄⣀⣀⣀               ⣀⣤⣴⣶⡾⠿⠿⠿⠿⢷⣶⣦⣤⣀⡀                     
⢰⣿⡟⠛⠛⠛⠻⠿⠿⢿⣶⣶⣦⣤⣤⣀⣀⡀⣀⣴⣾⡿⠟⠋⠉        ⠉⠙⠻⢿⣷⣦⣀         ⢀⣀⣀⣀⣀⣀⣀⣀⡀
 ⠻⣿⣦⡀ ⠉⠓⠶⢦⣄⣀⠉⠉⠛⠛⠻⠿⠟⠋⠁   ⣤⡀  ⢠   ⣠    ⠈⠙⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠛⢻⣿
  ⠈⠻⣿⣦    ⠈⠙⠻⢷⣶⣤⡀    ⢀⣀⡀ ⠙⢷⡀⠸⡇ ⣰⠇ ⢀⣀⣀      ⣀⣠⣤⣤⣶⡶⠶⠶⠒⠂  ⣠⣾⠟
    ⠈⢿⣷⡀      ⠈⢻⣿⡄⣠⣴⣿⣯⣭⣽⣷⣆ ⠁    ⢠⣾⣿⣿⣿⣿⣦⡀ ⣠⣾⠟⠋⠁       ⣠⣾⡟⠁ 
     ⠈⢻⣷⣄       ⣿⡗⢻⣿⣧⣽⣿⣿⣿⣧  ⣀⣀ ⢠⣿⣧⣼⣿⣿⣿⣿⠗⠰⣿⠃        ⣠⣾⡿⠋   
       ⠙⢿⣶⣄⡀    ⠸⠃⠈⠻⣿⣿⣿⣿⣿⡿⠃⠾⣥⡬⠗⠸⣿⣿⣿⣿⣿⡿⠛ ⢀⡟      ⣀⣠⣾⡿⠋     
         ⠉⠛⠿⣷⣶⣤⣤⣄⣰⣄  ⠉⠉⠉⠁ ⢀⣀⣠⣄⣀⡀ ⠉⠉⠉  ⢀⣠⣾⣥⣤⣤⣤⣶⣶⡿⠿⠛⠉       
             ⠈⠉⢻⣿⠛⢿⣷⣦⣤⣴⣶⣶⣦⣤⣤⣤⣤⣬⣥⡴⠶⠾⠿⠿⠿⠿⠛⢛⣿⣿⣿⣯⡉⠁           
               ⠈⣿⣧⡀⠈⠉ ⠈⠁⣾⠛⠉⠉          ⣀⣴⣿⠟⠉⣹⣿⣇            
               ⢀⣸⣿⣿⣦⣀   ⢻⡀       ⢀⣠⣤⣶⣿⠋⣿⠛⠃ ⣈⣿⣿            
               ⣿⡿⢿⡀⠈⢹⡿⠶⣶⣼⡇ ⢀⣀⣀⣤⣴⣾⠟⠋⣡⣿⡟ ⢻⣶⠶⣿⣿⠛⠋            
              ⠘⣿⣷⡈⢿⣦⣸⠇⢀⡿⠿⠿⡿⠿⠿⣿⠛⠋⠁ ⣴⠟⣿⣧⡀⠈⢁⣰⣿⠏              
               ⢸⣿⢻⣦⣈⣽⣀⣾⠃ ⢸⡇ ⢸⡇ ⢀⣠⡾⠋⢰⣿⣿⣿⣿⡿⠟⠋               
               ⠘⠿⢿⣿⣿⡟⠛⠃  ⣾  ⢸⡇⠐⠿⠋  ⣿⢻⣿⣿                   
                  ⢸⣿⠁⢀⡴⠋ ⣿  ⢸⠇     ⠁⢸⣿⣿                   
                 ⢀⣿⡿⠟⠋   ⣿  ⣸       ⢸⣿⣿                   
                 ⢸⣿⣁⣀    ⣿⡀ ⣿      ⢀⣈⣿⣿                   
                 ⠘⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠋                   
"""

images["vader"] = r"""
Sua falta de fé é perturbadora.
                 ⢀⣀⡀   ⢀⣀               
            ⣠⣤⣶⣾⣿⡉⢤⣍⡓⢶⣶⣦⣤⣉⠒⠤⡀           
         ⢀⣴⣿⣿⣿⣿⣿⣿⣷⡀⠙⣿⣷⣌⠻⣿⣿⣿⣶⣌⢳⡀         
        ⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠈⢿⣿⡆⠹⣿⣿⣿⣿⣷⣿⡀        
       ⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠹⣿⡄⢻⣿⣿⣿⣿⣿⣧        
      ⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣷⣽⣷⢸⣿⡿⣿⡿⠿⠿⣆       
      ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄   ⠐⠾⢭⣭⡼⠟⠃⣤⡆⠘⢟⢺⣦⡀     
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣥⣶⠾⠿⠛⠳⠶⢬⡁  ⠘⣃⠤⠤⠤⢍⠻⡄    
      ⣿⣿⣿⣿⣿⣿⣿⡿⣫⣾⡿⢋⣥⣶⣿⠿⢿⣿⣿⣿⠩⠭⢽⣷⡾⢿⣿⣦⢱⡹⡀   
      ⣿⣿⣿⣿⣿⣿⡟⠈⠛⠏⠰⢿⣿⣿⣧⣤⣼⣿⣿⣿⡏⠩⠽⣿⣀⣼⣿⣿⢻⣷⢡   
     ⢰⣿⣿⣿⣿⣿⣿⢁⣿⣷⣦⡀ ⠉⠙⠛⠛⠛⠋⠁⠙⢻⡆ ⢌⣉⠉⠉ ⠸⣿⣇⠆  
    ⢀⣾⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⠷⣄⢠⣶⣾⣿⣿⣿⣿⣿⠁  ⢿⣿⣿⣿⣷⠈⣿⠸⡀ 
    ⣼⣿⣿⣿⣿⣿⣿ ⣌⡛⠿⣿⣿ ⠈⢧⢿⣿⡿⠟⠋⠉⣠⣤⣤⣤⣄⠙⢿⣿⠏⣰⣿⡇⢇ 
   ⣼⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣶⣤⣙⠣⢀⠈⠘⠏  ⢀⣴⢹⡏⢻⡏⣿⣷⣄⠉⢸⣿⣿⣷⠸⡄
  ⣸⣿⣿⣿⣿⣿⣿⣿⠁⣾⣟⣛⠛⠛⠻⠿⠶⠬⠔ ⣠⡶⠋⠿⠈⠷⠸⠇⠻⠏⠻⠆⣀⢿⣿⣿⡄⢇
 ⢰⣿⣿⣿⣿⠿⠿⠛⠋⣰⣿⣿⣿⣿⠿⠿⠿⠒⠒⠂ ⢨⡤⢶⣶⣶⣶⣶⣶⣶⣶⣶⠆⠃⣀⣿⣿⡇⣸
⢀⣿⣿⠿⠋⣡⣤⣶⣾⣿⣿⣿⡟⠁ ⣠⣤⣴⣶⣶⣾⣿⣿⣷⡈⢿⣿⣿⣿⣿⠿⠛⣡⣴⣿⣿⣿⣿⠟⠁
⣼⠋⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⠻⠟⠋⣠⣴⣿⣿⣿⣿⠿⠋⠁  
⢿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣴ ⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣠⣾⣿⠿⠿⠟⠋⠁     
 ⠉⠛⠛⠿⠿⠿⢿⣿⣿⣿⣵⣾⣿⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏           
                  ⠉⠉⠉⠉⠉⠉⠉⠁              
"""

images["mario"] = r"""
Vamos lá. Nossa grande aventura começa agora!
                      ⢀⣀⣠⣤⣤⣤⣄⣀            
                   ⣠⣴⡾⣻⣿⣿⣿⣿⣯⣍⠛⠻⢷⣦⣀        
                ⢀⣴⣿⠟⢁⣾⠟⠋⣁⣀⣤⡉⠻⣷⡀ ⠙⢿⣷⣄      
       ⢀⡀      ⣰⣿⠏  ⢸⣿ ⠼⢋⣉⣈⡳⢀⣿⠃   ⠙⣿⣦⡀    
      ⢰⡿⠿⣷⡀   ⣼⣿⠃  ⣀⣤⡿⠟⠛⠋⠉⠉⠙⢛⣻⠶⣦⣄⡀ ⠘⣿⣷⡀   
⢠⣾⠟⠳⣦⣄⢸⡇ ⠈⣷⡀ ⣼⣿⡏⢀⣤⡾⢋⣵⠿⠻⢿⠋⠉⠉⢻⠟⠛⠻⣦⣝⠻⣷⣄⠸⣿⣿   
⠘⣧   ⠙⢿⣿  ⢸⣷ ⣿⣿⣧⣾⣏⡴⠛⢡⠖⢛⣲⣅  ⣴⣋⡉⠳⡄⠈⠳⢬⣿⣿⣿⡿   
 ⠘⠷⣤⣀⣀⣀⣽⡶⠛⠛⠛⢷⣿⣿⣿⣿⣏  ⡏⢰⡿⢿⣿  ⣿⠻⣿ ⡷ ⣠⣾⣿⡿⠛⠷⣦  
  ⢀⣾⠟⠉⠙⣿⣤⣄ ⢀⣾⠉ ⢹⣿⣿⣷ ⠹⡘⣷⠾⠛⠋⠉⠛⠻⢿⡴⢃⣄⣻⣿⣿⣷  ⢹⡇ 
  ⢸⡇⠈⠉⠛⢦⣿⡏ ⢸⣧ ⠈⠻⣿⡿⢣⣾⣦⣽⠃       ⣷⣾⣿⡇⠉⢿⡇ ⢀⣼⠇ 
  ⠘⣷⡠⣄⣀⣼⠇   ⠻⣷⣤⣀⣸⡇ ⠹⣿⣿⣦⣀    ⢀⣴⣿⣿⡟  ⢸⣷⣾⡿⠃  
   ⠈⠻⢦⣍⣀⣀⣀⡄ ⣰⣿⡿⠿⢿⣇  ⠉⠛⠻⣿⣿⡷⠾⣿⣿⡿⠉⠁  ⢀⣾⠋⠁    
      ⠈⠉⠉⠙⠿⢿⣿⣇  ⠈⢿⣧⣄   ⢹⣷⣶⣶⣾⣿⡇  ⣀⣴⡿⣧⣄⡀    
            ⠙⢿⣷⡀  ⠙⢿⣿⣶⣤⡀⠻⢤⣀⡤⠞⢀⣴⣿⣿⠟⢷⡀⠙⠻⣦⣄  
              ⠈⢻⣦ ⢠⡟⠁⠙⢻⣿⠷⠶⣶⠶⠾⠛⠙⣿⠇  ⢻⡄  ⠙⢷⡀
               ⣸⣿⡀⣿⠁⣤⣤⡄⢻⡶⠶⠛⠛⠛⠛⠛⣿⢠⣾⣷⣆⢻⡀  ⠈⣷
               ⣿⣿⣿⣿⢸⣿⣿⣿⡈⢿⡀     ⡿⢸⣿⣿⣿⢸⡇   ⡟
               ⠈⠉⠉⠉⠈⠉⠉⠉⠁⠈⠁    ⠈⠁⠈⠉⠉⠉ ⠁  ⠈⠁
"""

images["mandalorian"] = r"""
Como deve ser
                     ⢀⣀⣀⣀⣀                        
                 ⢀⣠⠴⠚⣹⠁⣶⢲⢈⠉⠓⠶⢤⡀                   
               ⣠⠞⠉ ⢀⣾⢻ ⣿⡈⢸    ⠉⠳⢄⡀                
             ⢠⠞    ⣈⣿⣾⣾⣿⡇⢸       ⠙⢄               
           ⢀⡴⠃ ⢀⡀ ⣴⣿⡏⣿⣿⣿⡇⣼⡇       ⠈⠳⣄⡀            
       ⣠⡴⠶⠟⠋  ⡄⢸⡇⢸⣿⣼⣧⣿⣿⣿⣁⣿⣤⣄⣀⣀ ⢀    ⠈⠙⠛⠒⠦⠄        
            ⣠⣦⣷⣾⡿⠿⢿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣓⣲⠲⠦⢤⣀              
          ⢀⣴⣿⣫⣭⣼⣶⣿⠿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣟⢻⣶⣌⢻⣶            
         ⢀⣿⡿⡿⢿⠓⠒⣛⠻⣿⣟⣿⣿⣿⣿⣿⣿⡏⠙⠋⠛    ⠈⠉⣿⢹⡆           
         ⠸⣿⡇⢀⣀  ⣿⢀ ⠸⣿⣿⣿⣿⣿⣿⠁     ⣠⣴⣶⣦⣼⣿⣇           
         ⠈⣿⡇⣿⣿⣿⣦⡹⣆  ⣿⣿⣿⣿⣿⣿   ⣴⣿⣾⣿⣿⢿⣿⣿⣿⠛           
          ⢘⣿⣿⣿⣿⣿⣿⡝⣧ ⢹⣿⣿⣿⣿⣿ ⢀⣼⣿⣿⣿⣿⣿⣿⠃⣿⣿            
          ⠈⢻⣿⢸⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⡗⠈⣼⣿⢿⣿⡿⠿⢿⣯ ⠿⣿            
           ⢸⣿⣸⡇⠈⠙⢿⣷⢿⡘⣿⣿⣿⣿⠃⢠⣿⣿⡿⠉   ⢻⡀⢀⣿            
           ⢸⣿⣿   ⠈⢻⡟⣇⣇⣿⣿⣿ ⢸⣿⡿⠁     ⢷⣄⢻            
           ⢸⣿⡏     ⣿⢿⣿⣿⣿⣿ ⣾⣿⠃      ⠘⣿⡟            
           ⠘⠻⠧⣄⡀   ⢸⣾⣿⣿⣿⣿ ⣿⡟    ⣀⣠⣥⣶⣿⣦⣄⡀          
               ⠉⠙⠲⣦⣄⣿⣿⣿⣿⣿⣷⣿⣧⣴⣶⡾⣛⣯⣭⣷⠤⠶⠤⢬⣭⢽⣆⡀⢠⣶⣶⣶⠶⠶⢤
               ⣀⣀⡤⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣟⢿⠏⣉⣡⣤⣶⣾⠿⣿⣿⣿⣿⠛⢸⣾⡿⠛⠛⠛⠶
           ⣀⣠⣤⣿⣛⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣷⣿⣿⡿⢟⣿⡟⣰⣾⠋     
       ⣠⣴⡶⣫⣽⢿⣯⣽⣿⣿⣿⣿⠿⠛⠁⢈⣹⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⣤⣴⣿⠛⢰⣿⠇      
      ⣰⣿⣿⣼⣟⣽⣼⣿⣿⣿⣿⣯⣷⢍⣣⣶⣿⣿⣿⣿⣿⣿⣿⠟⠁     ⢸⣿⣿⡟ ⣧⣿ ⡀     
"""


images["minion"] = r"""
Bananaaaa!
              ⣀ ⠤⠤⠤ ⣀       
           ⡠⠐⢉⠴⣚⠉⣙⠢⢄⡤⢞⡂⢀⣐⢄  
          ⡔⡤⣞⢁⠊⢀⣀⠐⢿⡄⠰⢁⡀⠈⠺⣦⢡ 
         ⢰⣿⣗⣟⡸ ⠻⡿⠃⢸⣇⢃⠿⠿  ⣽⢸ 
         ⠁ ⠈⠙⢷⣴⡀ ⠠⣪⣾⣷⡄⡀⠠⣐⢕⠁ 
 ⢰⡦      ⡇    ⠙⠲⡖⠓⠉⠁⠈⠉⠒ ⠈⢸  
⢶⣿⣷⣤⢀⣀⡀  ⣏⡑⠢⢄   ⠈⠐ ⠐     ⡸⡀ 
⠛⠛⠛⠟ ⠤⠤⠌⢉ ⠈⠓⢬⣿⣦⡤⣤⣤⠤⠤⣤⣤⣤⣤⣚⣔⣄ 
         ⡇  ⡤⠂  ⢀⠤⠤⢄⡨⠔⠒⢍⠉⢁⣯⡆
         ⡗⢤⡤⣬   ⢇   ⠁  ⡸⢰⣿⣿⡿
         ⠘⢌⡿⣽⡀  ⠈⠒⢄⡀ ⢀⠔⠁⠈⠙⡋ 
           ⠑⠳⢧⣠⣤⣄⣠⣀⣈⣱⡥⠤⠴⠦⠴⠃ 
              ⢹⣿⣿ ⣿⣿⣿⣄      
              ⠙⠉⠉ ⠈⠉⠉⠉      
"""

images["minions2"] = r"""
Banana banana bananáaaaaa!
            ⣀⢀⣠⣤⣄⡀⢀⣀          
         ⣠⡶⠛⢉⠤⣀⠤⡠⢫⠵⠶⢩⡢        
 ⣀      ⢰⠋ ⣠⢡⠋⠉⠙⣆⢂⣤⡄⠈⡇⡇  ⣀⣶⣄⢤ 
⢠⢇⠓⠒⣂⡤⡀ ⡆ ⡜⣿⣜⢄⣿⢆⠜⣤⣝⣓⣢⠜ ⡠⢛⠧⠬⠭⠸⠇
⠈⠒⠓⠂⠙⠓⢌⠢⢷⡫⠐⠉⠛⠴⠶⠖⠊ ⠉⠉ ⢸⠌⡰⠁     
       ⠑⡀⠙⢕⢦  ⠠⣲⣒⠲⢲⠎⢻⢈⣷       
        ⠸⡀ ⢣⡑⡄ ⠑⠠⠄⠘⠴⠂⣸⣹       
         ⠃  ⢹⣼⡶⣄    ⡴⢿⢻       
         ⢀   ⡝⠁ ⠙⠒⠒⠋ ⢸⢸       
         ⢸⢄⣀⣀⡇  ⡖⢦⣴⠊⡆⢸⣸       
         ⢰ ⠉⢸⠁ ⠸⡇⣞⣯⡷⡇⢨⢹       
         ⣸⡀⠔⠃   ⠑⠬⠭⠝ ⣈⡾⡄      
        ⡴⢣⠑⢄⣀⣀⣀⣀⣀ ⠤⣐⢞⣿⡡⠃      
        ⠈⠁⠉⠉       ⠈⠫⠙        
"""

images["slayer"] = r"""
Não há atalhos, apenas trabalho duro.
Treine duro e seja paciente. Vai valer a pena.
⠏⠁⠈⠙⠛⢿⣿⣿⣿⣿⣿⣿⣿⡟ ⠈⠻⣿⣿⣿⣿⣿⠟⢡⡿⢿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⢀⣎⣏⡏⣟⠛⠿⠿⡟⢁⣀⣀⣠⡼⠟⠛⠉  ⠉⠐⠋  ⠛⠋⠭⠾⢿⣿⣿⠟⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣦⣶⡀   ⠉⠛⣿⣿⣷⣿⣇⣠⠟⠋⠁  ⢀⡄       ⣀⣠⡤⠴⠒⠋⠁⣰⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣷  ⡀   ⠉⠉⡿⠋⠁⡠⢀⠄⡠⠔⠋⢀⣀⠔ ⢀⡤⠚⣽⡟⠋   ⢀⡜⢱⠃⠉⣩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣦⡀⢹   ⢀⡞⠁⡰⠛⣡⢃⣾⠁⠤⡾⢋⣀⡀⠠⠊ ⢾⣏⡾ ⢀⣠⡴⠿⠙⣿⠃ ⠙⠛⢉⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⡄  ⡜ ⠐⡅⡜⡇⢠⠃⡠⠊⠐⠝⠋    ⠈⠙⢁⠔⣯⡝⢁⡶⢾⣿⠇   ⠐⠺⠿⢻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡀⣠⡇ ⣠⡇⡸ ⢣⠎⢀⣀⣤⣴⣶⠟⠛      ⣭⣷⣤⡴⠋        ⠙⣽⡿⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢿⡇⢀⡟⠃⣡⡿⠃⣰⣾⡯⠚⠉⣀⣠⣄⣤            ⢀ ⢀⡈⠁   ⣠⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⢸⣷⠸⠁⢲⡏⢀⣾⣿⠏⣠⠞⠁ ⢾⣿⣽⡆⡀ ⣠        ⣀⡠⠄   ⢀⡾⢧⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣟⣳⣿⣿⣆ ⢸⠁⠸⣿⠏⣰⣿ ⡀  ⢁⣻⣧⣷⣿⡽⠃      ⠉    ⢠⣶⠯⣄⣠⡽⠿⢿⣿
⣿⣿⣿⣿⣿⣿⣟⡁⢈⠟⣁    ⠋⢰⣿⡿⣧⣌⣒⣒⣿⣞⣿⣿⠋           ⢀⣸⣯⠽⠋⠁     
⣿⣿⣿⠿⣿⣿⡿⠟⠁⠊⠱⣣⣶⡀  ⢘⡛⠓⠚⣛⣋⣛⣸⠭⠞⠁          ⣀⡠⣞⡋⠁        
⣿⣿⡃ ⠘⣿⢤⡀   ⣹⣿⡟ ⢀⡎⢱ ⡀                ⣉⡥⠖⠉          
⣿⣟⢿ ⢆⠘⢦⡈⢦⡠⡺⠋⠉⠠⢊⡝ ⢰⣧⡈⠓⢤⣀             ⣽⠶⠄           
⣿⣿⣼⣷⠈⢳⣄⠙⠲⣧  ⣠⠖⠋⠙⠢⠼⠁⠙⠶ ⠈⠉⠛⠤         ⣀⠉⠉            
⣿⣿⣷⣍  ⠻⠷⠄⢘⣧⣞⣡⣶⣏⠉⣳ ⣠⣤⣀ ⢤⣠⡐⠦⣄⡀    ⢀⡐⠒⠉              
⣿⣿⣿⣿⣿⣷⣶⣄⣀⣸⣿⣿⣿⣿⣿⣶⣿⣆⣻⣿⣿⣷⣶⢭⣿⣦⣶⠿⠾⣗⢒⠿ ⠁                
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⠁⠙⠂⢀⡉⣁⡠⠴⠛⠉⠁                  
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀  ⠈ ⣄              ⣠⣤⣶⠶⠖⣶⠁ 
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⡦ ⣀⣨⠟⠲⠤⠤⠬⣷⣀          ⣠⣴⠟⢁⡀ ⣼⠇  
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣶⣬⣿⣿⣡⣵⣖⣤⣀⣤⣈⣙⣶⣦⣤⣀⣀⣠⡤⠶⠟⠋⠁  ⠉⢷⠉   
"""

images["jujutsu"] = r"""
Não sei como vou me sentir quando estiver morto, 
mas não quero me arrepender da maneira como vivi.
   ⣀                      
⢠⣀⡀⡏⠳⣄   ⢀⡀ ⢠             
⡤⠵ ⢀⡶⠛⠁⢢⢄⡜⠱⡾⠍⠧⠲⡇⣀⡄        
⠈⢶⣤⠛⠁⣀⡹⠉        ⠰⠥⣤       
  ⠁ ⠠⣿⢃⢀⣤⣤⡴⣰⢰⣠⢠  ⢨⣷⡆      
     ⠝⢿⠙⢯⣟ ⣱⡿⠌⡷⣿⣾⣿⡿⠙⢦     
      ⣸ ⠼   ⠃⣠⠄⠘⡟⢘⣄ ⠈⢷    
     ⠘⡏⠉ ⡐⢢ ⢀⡀ ⢰⠖⡩⠊ ⣠⠋    
      ⢈⣷⢄⡑⠚⢀⡠⠤⣒⠡⠊⢀⣠⣾⣿⣦    
    ⢀⣴⣿⣿⣿⣍⠫⠇⠐⠉⢒⣠⣴⣿⣿⣿⣿⣿⡆   
  ⡤⢐⠚⣿⣿⣿⣿⣿⣶⣶⣶⣶⣾⣿⣛⠟⠛⣿⣿⣿⡇   
 ⢸⠐⠠⢌⣺⣿⠿⠛⠻⣿⣿⣿⣿⣿⣿ ⠄ ⠈⣿⣿⣷   
  ⠣⢌⡹⠋⠁ ⢀⣠⣿⣿⣿⣿⣿⣿⣯⣭⣀⣴⣿⣿⣿⠇  
     ⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍   
   ⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇  
  ⢀⣾⣿⣿⣿⣿⣿⡿⠏⠁ ⠈⠉⠙⢿⣿⣿⣿⣿⣿⣿⣿⣇ 
  ⣼⣿⣿⣿⣿⡿⠋⠁       ⠙⢿⣿⣿⣿⣿⣿⣿⡆
 ⠘⠛⣿⡿⠛⠋              ⢿⣿⣏⠉⠉
⢀⠤⣾⠛⣿                ⠾⣐⣚⣦ 
⠉⠉⠉⠉⠁                     
"""


images["gollum"] = r"""
Meu precioso!
        ⣀⣠⣴⣶⡿⠟⠋⠁              
     ⢀⣴⣾⣿⣿⣿⠋      ⠈           
   ⢀⣼⡿⠛⠻⣿⣿⠃⢀            ⢀     
  ⢠⣿⣿⠃⢰⣆⠘⢿⡦⠈            ⠸     
 ⢠⣿⣿⣿ ⠙⢿⡆⠈⠁                 ⡀ 
⢀⣿⣿⣿⣿⢀⠐⢿⠃                  ⢀⣷ 
⠈⠉⠉⠙⠛⠃⣷⣮⠃ ⢀⣀⣀⡀             ⢸⣿⡇
      ⠘⣿⡄⠐⠚⢆⠁⠙⢻⣶⣦⣄⡀⡀       ⠘⠋⠁
  ⢀⣶⡀⠐⣠⣿⣷⣤⡀⠐⠙⠶⠶⠿⠿⠛⠿⣿⣿⣿⣤⣴⣀  ⣴⢎ 
  ⠈⣿⣿⣾⣿⣿⣿⣿⣇⣠⠴⠖⠲⡂   ⠹⣿⣟⡛⠹⠛⠂⠘⣡⡿ 
   ⢻⣿⣿⣿⣿⣿⡇⢹⣧   ⠱⢀⣀⡠⠲⣄⣹⣿⡏ ⣠⣾⣿⠃ 
   ⠸⣿⣿⣿⣿⣿⡇ ⠁⠙⣢⣄⣀    ⢹⣿⣿⣫⣾⣿⡿⠃  
    ⠙⢩⢻⣿⣿⣷⡀  ⢈⡙⠛⠿⠓⠐⠉ ⢸⣿⣿⣿⠟⠁   
       ⠽⢀⣤⡀ ⢠⣤⡈⠉⠁⠠⠤  ⠘⠿⠋⠁     
         ⠉⠛⠿⠶⢾⣭⢤⡾ ⠠⠒          
"""

class GuiActions:
    tab = "↔TAB"
    sair   = "Sair"
    editar = "Editar"
    rodar  = " Rodar"
    principal = "Principal"
    fixar  = "Fixar"
    tempo = "Tempo"
    hud = "HUD"
    github = "Github"
    ajuda = "Ajuda"
    baixar = "Baixar"
    ativar = "Ativar"
    navegar = "←↓→"
    marcar = "Marcar"
    desmarcar = "Desmarcar"
    colapsar = "Colapsar"
    pesquisar = "Buscar"


class GuiKeys:
    left = "a"
    right = "d"
    down = "s"
    up = "w"

    hud = "h"
    images = "I"
    down_task = "b"
    activate = "\n"
    key_help = "?"
    expand = ">"
    expand2 = "."
    collapse = "<"
    collapse2 = ","
    inc_grade = "+"
    inc_grade2 = "="
    dec_grade = "-"
    dec_grade2 = "_"
    set_root_dir = "D"
    set_lang = "L"
    github_open = "g"
    key_quit = "q"
    edit= "e"
    colors = "C"
    borders = "B"
    pesquisar = "/"
    graph = "G"
    diff = "m"
    rodar = "r"
    testar = "\n"
    principal = "\t"
    sair   = "q"
    editar = "e"
    travar = "f"
    tempo  = "t"
    border = "B"

class InputManager:
    backspace1 = 127
    backspace2 = 263
    left = 260
    right = 261
    a = 97
    d = 100
    tab = 9
    special_double_key = 195
    cedilha = 167
    esc = 27

    def __init__(self):
        # stores a function than can return another function
        self.calls: Dict[int, Callable[[], Optional[Callable[[], None]]]] = {}

    def add_int(self, _key: int, fn: Callable[[], None]):
        if _key in self.calls.keys():
            raise ValueError(f"Chave duplicada {chr(_key)}")
        self.calls[_key] = fn

    def add_str(self, str_key: str, fn: Callable[[], None]):
        if str_key != "":
            self.add_int(ord(str_key), fn)

    def has_str_key(self, key: str) -> bool:
        return ord(key) in self.calls
    
    def has_int_key(self, key: int) -> bool:
        return key in self.calls
    
    def exec_call(self, key: int):
        return self.calls[key]()

    @staticmethod
    def fix_esc_delay():
        if hasattr(curses, "set_escdelay"):
            curses.set_escdelay(25)
        else:
            os.environ.setdefault('ESCDELAY', '25')

    @staticmethod
    def fix_cedilha(scr, value: int) -> int:
        if value == InputManager.special_double_key:
            value = scr.getch()
            if value == InputManager.cedilha: #ç
                value = ord("c")
        return value
tko_guide = """
       ╔════ TKO GUIA COMPACTO ════╗
╔══════╩═════ BAIXAR PROBLEMA ═════╩═══════╗
║        tko down <curso> <label>          ║
║ exemplo poo  : tko down poo carro        ║
║ exemplo fup  : tko down fup opala        ║
╟─────────── EXECUTAR SEM TESTAR ──────────╢
║          tko run <cod, cod...>           ║
║exemplo ts  : tko run solver.ts           ║
║exemplo cpp : tko run main.cpp lib.cpp    ║
╟──────── ABRIR O MODO INTERATIVO ─────────╢
║              tko play <curso>            ║
║exemplo:      tko play fup                ║
╟──────────── RODAR OS TESTES ─────────────╢
║   tko run cases.tio <cod, ...> [-i ind]  ║
║ exemplo: tko run cases.tio main.ts       ║
╟── DEFINIR EXTENSÃO PADRÃO DOS RASCUNHOS ─╢
║           tko config -l <ext>            ║
║     exemplo c : tko config -l c          ║
║  exemplo java : tko config -l java       ║
╟─────────── MUDAR VISUALIZAÇÃO ───────────╢
║             tko config <--opcao>         ║
║DiffMode: tko config [--side  | --down ]  ║
║Cores   : tko config [--mono  | --color  ]║
║Encoding: tko config [--ascii | --unicode]║
╚══════════════════════════════════════════╝
"""

bash_guide = """
       ╔═══ BASH  GUIA COMPACTO ════╗
╔══════╩════ MOSTRAR E NAVEGAR ═════╩══════╗
║Mostrar arquivos  : ls                    ║
║Mostrar ocultos   : ls -la                ║
║Mudar de pasta    : cd _nome_da_pasta     ║
║Subir um nível    : cd ..                 ║
╟─────────────── CRIAR ────────────────────╢
║Criar um arquivo  : touch _nome_do_arquivo║
║Criar uma pasta   : mkdir _nome_da_pasta  ║
╟─────────────── REMOVER ──────────────────╢
║Apagar um arquivo : rm _nome_do_arquivo   ║
║Apagar uma pasta  : rm -r _nome_da_pasta  ║
║Renomear ou mover : mv _antigo _novo      ║
╟─────────────── CONTROLAR ────────────────╢
║Últimos comandos  : SETA PRA CIMA         ║
║Limpar console    : Control L             ║
║Cancelar execução : Control C             ║
║Finalizar entrada : Control D             ║
╚══════════════════════════════════════════╝
"""



def get_md_link(title: str) -> str:
    if title is None:
        return ""
    title = title.lower()
    out = ""
    for c in title:
        if c == " " or c == "-":
            out += "-"
        elif c == "_":
            out += "_"
        elif c.isalnum():
            out += c
    return out

class Title:
    @staticmethod
    def extract_title(readme_file):
        title = open(readme_file).read().split("\n")[0]
        parts = title.split(" ")
        if parts[0].count("#") == len(parts[0]):
            del parts[0]
        title = " ".join(parts)
        return title

class RemoteCfg:
    def __init__(self, url: Optional[str] = None):
        self.user = ""
        self.repo = ""
        self.branch = ""
        self.folder = ""
        self.file = ""
        if url is not None:
            self.from_url(url)

    def from_url(self, url: str):
        if url.startswith("https://raw.githubusercontent.com/"):
            url = url.replace("https://raw.githubusercontent.com/", "")
            parts = url.split("/")
            self.user = parts[0]
            self.repo = parts[1]
            self.branch = parts[2]
            self.folder = "/".join(parts[3:-1])
            self.file = parts[-1]
        elif url.startswith("https://github.com/"):
            url = url.replace("https://github.com/", "")
            parts = url.split("/")
            self.user = parts[0]
            self.repo = parts[1]
            self.branch = parts[3]
            self.folder = "/".join(parts[4:-1])
            self.file = parts[-1]
        else:
            raise Exception("Invalid URL")

    def get_raw_url(self):
        return "https://raw.githubusercontent.com/" + self.user + "/" + self.repo + "/" + self.branch + "/" + self.folder + "/" + self.file

    def download_absolute(self, filename: str):
        [tempfile, __content] = urllib.request.urlretrieve(self.get_raw_url(), filename)
        content = ""
        try:
            content = open(tempfile, encoding="utf-8").read()
        except:
            content = open(tempfile).read()
        with open(filename, "w", encoding="utf-8") as f:
            absolute = Absolute.relative_to_absolute(content, self)
            f.write(absolute.encode("utf-8").decode("utf-8"))
        return

    def __str__(self):
        return f"user: ({self.user}), repo: ({self.repo}), branch: ({self.branch}), folder: ({self.folder}), file: ({self.file})"

    def read(self, cfg_path: str):
        if not os.path.isfile(cfg_path):
            print("no remote.cfg found")

        config = configparser.ConfigParser()
        config.read(cfg_path)

        self.user   = config["DEFAULT"]["user"]
        self.repo   = config["DEFAULT"]["rep"]
        self.branch = config["DEFAULT"]["branch"]
        self.folder = config["DEFAULT"]["base"]
        self.tag    = config["DEFAULT"]["tag"]

    @staticmethod
    def search_cfg_path(source_dir) -> Optional[str]:
        # look for the remote.cfg file in the current folder
        # if not found, look for it in the parent folder
        # if not found, look for it in the parent's parent folder ...

        path = os.path.abspath(source_dir)
        while path != "/":
            cfg_path = os.path.join(path, "remote.cfg")
            if os.path.isfile(cfg_path):
                return cfg_path
            path = os.path.dirname(path)
        return None

class Absolute:

    # processa o conteúdo trocando os links locais para links absolutos utilizando a url remota
    @staticmethod
    def __replace_remote(content: str, remote_raw: str, remote_view: str, remote_folder: str) -> str:
        if content is None or content == "":
            return ""
        if not remote_raw.endswith("/"):
            remote_raw += "/"
        if not remote_view.endswith("/"):
            remote_view += "/"
        if not remote_folder.endswith("/"):
            remote_folder += "/"

        #trocando todas as imagens com link local
        regex = r"!\[(.*?)\]\((\s*?)([^#:\s]*?)(\s*?)\)"
        subst = r"![\1](" + remote_raw + r"\3)"
        result = re.sub(regex, subst, content, 0)


        regex = r"\[(.+?)\]\((\s*?)([^#:\s]*?)(\s*?/)\)"
        subst = r"[\1](" + remote_folder + r"\3)"
        result = re.sub(regex, subst, result, 0)

        #trocando todos os links locais cujo conteudo nao seja vazio
        regex = r"\[(.+?)\]\((\s*?)([^#:\s]*?)(\s*?)\)"
        subst = r"[\1](" + remote_view + r"\3)"
        result = re.sub(regex, subst, result, 0)

        return result

    @staticmethod
    def relative_to_absolute(content: str, cfg: RemoteCfg):
        user_repo = cfg.user + "/" + cfg.repo
        raw = "https://raw.githubusercontent.com"
        github = "https://github.com"
        remote_raw    = f"{raw}/{user_repo}/{cfg.branch}/{cfg.folder}"
        remote_view    = f"{github}/{user_repo}/blob/{cfg.branch}/{cfg.folder}"
        remote_folder = f"{github}/{user_repo}/tree/{cfg.branch}/{cfg.folder}"
        return Absolute.__replace_remote(content, remote_raw, remote_view, remote_folder)

    @staticmethod
    def from_file(source_file, output_file, cfg: RemoteCfg, hook):
        content = open(source_file, encoding="utf-8").read()
        content = Absolute.relative_to_absolute(content, cfg)
        open(output_file, "w").write(content)
        
class RemoteMd:

    # @staticmethod
    # def insert_preamble(lines: List[str], online: str, tkodown: str) -> List[str]:

    #     text = "\n- Veja a versão online: [aqui.](" + online + ")\n"
    #     text += "- Para programar na sua máquina (local/virtual) use:\n"
    #     text += "  - `" + tkodown + "`\n"
    #     text += "- Se não tem o `tko`, instale pelo [LINK](https://github.com/senapk/tko#tko).\n\n---"

    #     lines.insert(1, text)

    #     return lines

    # @staticmethod
    # def insert_qxcode_preamble(cfg: RemoteCfg, content: str, hook) -> str:
    #     base_hook = os.path.join(cfg.base, hook)

    #     lines = content.split("\n")
    #     online_readme_link = os.path.join("https://github.com", cfg.user, cfg.repo, "blob", cfg.branch, base_hook, "Readme.md")
    #     tkodown = "tko down " + cfg.tag + " " + hook
    #     lines = RemoteMd.insert_preamble(lines, online_readme_link, tkodown)
    #     return "\n".join(lines)

    @staticmethod
    def run(remote_cfg: RemoteCfg, source: str, target: str, hook) -> bool:    
        content = open(source).read()
        content = Absolute.relative_to_absolute(content, remote_cfg)
        open(target, "w").write(content)
        return True


languages_avaliable = ["c", "cpp", "py", "ts", "js", "java", "go"]

class RepSource:
    def __init__(self, file: str = "", url: str = ""):
        self.file: str = ""
        if file != "":
            self.file = os.path.abspath(file)
        self.url: str = url

    def set_file(self, file: str):
        self.file = os.path.abspath(file)
        return self

    def set_url(self, url: str):
        self.url = url
        return self

    def get_file_or_cache(self, rep_dir: str) -> str:
        # arquivo existe e é local
        if self.file != "" and os.path.exists(self.file) and self.url == "":
            return self.file

        # arquivo não existe e é remoto
        if self.url != "" and (self.file == "" or not os.path.exists(self.file)):
            cache_file = os.path.join(rep_dir, ".cache.md")
            os.makedirs(rep_dir, exist_ok=True)
            cfg = RemoteCfg(self.url)
            try:
                cfg.download_absolute(cache_file)
            except urllib.error.URLError:
                print("fail: Não foi possível baixar o arquivo do repositório")
                if os.path.exists(cache_file):
                    print("Usando arquivo do cache")
                else:
                    raise Warning("fail: Arquivo do cache não encontrado")
            return cache_file

        raise ValueError("fail: arquivo não encontrado ou configurações inválidas para o repositório")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "url": self.url
        }

    def from_dict(self, data: Dict[str, Any]):
        self.file = data.get("file", "")
        self.url = data.get("url", "")
        return self    

class RepData:

    def __init__(self, rootdir: str, alias: str, json_file: str = ""):
        self.json_file: str = json_file
        self.data: Dict[str, Any] = {}
        self.rootdir = rootdir
        self.alias = alias

    def get_rootdir(self) -> str:
        return self.rootdir

    def get_rep_dir(self) -> str:
        return os.path.join(self.rootdir, self.alias)

    __expanded = "expanded"
    __new_items = "new_items"
    __tasks = "tasks"
    __flags = "flags"
    __lang = "lang"
    __index = "index"

    defaults = {
        __expanded: [],
        __tasks: {},
        __flags: {},
        __new_items: [],
        __lang: "",
        __index: 0
    }

    def get_index(self) -> int:
        return self.__get(RepData.__index)

    def get_expanded(self) -> List[str]:
        return self.__get(RepData.__expanded)

    def get_new_items(self) -> List[str]:
        return self.__get(RepData.__new_items)
    
    def get_tasks(self) -> Dict[str, Any]:
        return self.__get(RepData.__tasks)
    
    def get_flags(self) -> Dict[str, Any]:
        return self.__get(RepData.__flags)
    
    def get_lang(self) -> str:
        return self.__get(RepData.__lang)

    def set_expanded(self, value: List[str]):
        return self.__set(RepData.__expanded, value)
    
    def set_new_items(self, value: List[str]):
        return self.__set(RepData.__new_items, value)
    
    def set_tasks(self, value: Dict[str, str]):
        return self.__set(RepData.__tasks, value)
    
    def set_flags(self, value: Dict[str, Any]):
        return self.__set(RepData.__flags, value)
    
    def set_lang(self, value: str):
        return self.__set(RepData.__lang, value)
    
    def set_index(self, value: int):
        return self.__set(RepData.__index, value)

    def __get(self, key: str) -> Any:
        if key not in self.defaults:
            raise ValueError(f"Key {key} not found in RepSettings")
        value = self.data.get(key, RepData.defaults[key])
        if type(value) != type(RepData.defaults[key]):
            return RepData.defaults[key]
        return value

    def __set(self, key: str, value: Any):
        self.data[key] = value
        return self

    def load_defaults(self):
        for key in RepData.defaults:
            self.data[key] = RepData.defaults[key]
        return self

    def load_data_from_json(self):
        with open(self.json_file, encoding="utf-8") as f:
            self.data = json.load(f)
        return self


    def save_data_to_json(self):
        if not os.path.exists(os.path.dirname(self.json_file)):
            os.makedirs(os.path.dirname(self.json_file))
        # filter keys that are not in defaults
        for key in list(self.data.keys()):
            if key not in RepData.defaults:
                del self.data[key]

        with open(self.json_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, indent=4))
        return self

    def __str__(self) -> str:
        return (
            f"data: {self.data}\n"
        )



class FileSource:
    def __init__(self, label, input_file, output_file):
        self.label = label
        self.input_file = input_file
        self.output_file = output_file

    def __eq__(self, other):
        return self.label == other.label and self.input_file == other.input_file and \
                self.output_file == other.output_file


class PatternLoader:
    pattern: str = ""

    def __init__(self):
        parts = PatternLoader.pattern.split(" ")
        self.input_pattern = parts[0]
        self.output_pattern = parts[1] if len(parts) > 1 else ""
        self._check_pattern()

    def _check_pattern(self):
        self.__check_double_wildcard()
        self.__check_missing_wildcard()

    def __check_double_wildcard(self):
        if self.input_pattern.count("@") > 1 or self.output_pattern.count("@") > 1:
            raise ValueError("  fail: the wildcard @ should be used only once per pattern")

    def __check_missing_wildcard(self):
        if "@" in self.input_pattern and "@" not in self.output_pattern:
            raise ValueError("  fail: is input_pattern has the wildcard @, the input_patter should have too")
        if "@" not in self.input_pattern and "@" in self.output_pattern:
            raise ValueError("  fail: is output_pattern has the wildcard @, the input_pattern should have too")

    def make_file_source(self, label):
        return FileSource(label, self.input_pattern.replace("@", label), self.output_pattern.replace("@", label))

    def get_file_sources(self, filename_list: List[str]) -> List[FileSource]:
        input_re = self.input_pattern.replace(".", "\\.")
        input_re = input_re.replace("@", "(.*)")
        file_source_list = []
        for filename in filename_list:
            match = re.findall(input_re, filename)
            if not match:
                continue
            label = match[0]
            file_source = self.make_file_source(label)
            if file_source.output_file not in filename_list:
                print("fail: file " + file_source.output_file + " not found")
            else:
                file_source_list.append(file_source)
        return file_source_list

    def get_odd_files(self, filename_list) -> List[str]:
        matched = []
        sources = self.get_file_sources(filename_list)
        for source in sources:
            matched.append(source.input_file)
            matched.append(source.output_file)
        unmatched = [file for file in filename_list if file not in matched]
        return unmatched


class Token:
    def __init__(self, text: str = "", fmt: str = "", ):
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        self.text = text
        self.fmt = fmt

    def __eq__(self, other: Any):
        if not isinstance(other, Token):
            return False
        return self.text == other.text and self.fmt == other.fmt

    def __len__(self):
        return len(self.text)
    
    def __add__(self, other: Any):
        return Sentence().add(self).add(other)

    def __str__(self):
        return f"('{self.text}', '{self.fmt}')"

def RToken(fmt: str, text: str) -> Token:
    return Token(text, fmt)

class Sentence:
    def __init__(self, value: Union[str, Tuple[str, str]] = ""):
        self.data: List[Token] = []
        self.add(value)
    
    def clone(self):
        other = Sentence()
        other.data = [v for v in self.data]
        return other

    def setup(self, data: List[Token]):
        self.data = []
        for d in data:
            for c in d.text:
                self.data.append(Token(c, d.fmt))
        return self

    def __getitem__(self, index: int) -> Token:
        if index < 0 or index >= len(self):
            raise IndexError("index out of range")
        return self.data[index]

    def __len__(self):
        return self.len()
    
    def __add__(self, other: Any):
        return Sentence().add(self).add(other)

    def __eq__(self, other: Any):
        if len(self.data) != len(other.data):
            return False
        for i in range(len(self.data)):
            if self.data[i] != other.data[i]:
                return False
        return True


    def __str__(self):
        return "".join([str(d) for d in self.resume()])
    
    def resume(self) -> List[Token]:
        if len(self.data) == 0:
            return []
        
        new_data: List[Token] = [Token("", self.data[0].fmt)]
        for d in self.data:
            if d.fmt == new_data[-1].fmt:
                new_data[-1].text += d.text
            else:
                new_data.append(Token())
                new_data[-1].text = d.text
                new_data[-1].fmt = d.fmt
        return new_data
    
    def resume_val_fmt(self) -> Tuple[str, str]:
        fmt = []
        val = []
        for d in self.data:
            fmt.append(" " if d.fmt == "" else d.fmt[0])
            val.append(d.text)
        return "".join(val), "".join(fmt)


    # search for a value inside the tokens and replace it with a new value and fmt
    def replace(self, old: str, token: Token):
        old_list: List[str] = [c for c in old]
        new_list = [c for c in token.text]
        new_list.reverse()

        index = 0
        while index < len(self.data) - len(old_list) + 1:
            found = True
            for i in range(len(old_list)):
                if self.data[index + i].text != old_list[i]:
                    found = False
                    break
            if found:
                for _ in range(len(old_list)):
                    del self.data[index]
                for c in new_list:
                    self.data.insert(index, Token(c, token.fmt))
                index += len(new_list)
            else:
                index += 1
        return self

    def plus(self, qtd: int) -> Sentence:
        output = Sentence()
        for i in range(qtd):
            output.add(self)
        return output

    def add(self, value: Union[str, Token, Tuple[str, str], Sentence]):
        if isinstance(value, str):
            if value != "":
                for c in value:
                    self.data.append(Token(c))
        elif isinstance(value, Token):
            if value.text != "":
                for c in value.text:
                    self.data.append(Token(c, value.fmt))
        elif isinstance(value, Sentence):
            self.data += value.data
        else:
            raise TypeError("unsupported type '{}'".format(type(value)))
        return self
    
    def addf(self, fmt: str, text: Any):
        if not isinstance(text, str):
            raise TypeError("fmt must be a string")
        self.add(Token(text, fmt))
        return self

    def ljust(self, width: int, filler: Token = Token(" ")):
        total = self.len()
        char = " " if filler.text == "" else filler.text[0]
        fmt = filler.fmt
        if total < width:
            suffix = [Token(char, fmt) for _ in range(width - total)]
            self.data = self.data + suffix
        return self
    
    def rjust(self, width: int, filler: Token = Token(" ")):
        total = self.len()
        char = " " if filler.text == "" else filler.text[0]
        fmt = filler.fmt
        if total < width:
            prefix = [Token(char, fmt) for _ in range(width - total)]
            self.data = prefix + self.data
        return self
    
    def center(self, width: int, filler: Token = Token(" ")):
        total = self.len()
        char = " " if filler.text == "" else filler.text[0]
        fmt = filler.fmt
        if total < width:
            left = (width - total) // 2
            right = width - total - left
            prefix = [Token(char, fmt) for _ in range(left)]
            suffix = [Token(char, fmt) for _ in range(right)]
            self.data = prefix + self.data + suffix
        return self
    
    def len(self):
        return len(self.data)
    
    def get_data(self):
        return self.data
    
    def get_text(self) -> str:
        return "".join([t.text for t in self.data])

    def trim_alfa(self, limit: int):
        i = len(self.data) - 1
        size = len(self.data)
        locked = False
        while i >= 0 and size > limit:
            if self.data[i].text == "[":
                locked = False
                i -= 1
            elif self.data[i].text == "]":
                locked = True
                i -= 1
            elif not locked and self.data[i].text != " ":
                del self.data[i]
                size -= 1
                i -= 1
            else:
                i -= 1

    def cut_begin(self, qtd: int):
        if qtd > len(self.data):
            self.data = []
        else:
            self.data = self.data[qtd:]
        return self

    def trim_spaces(self, limit: int):
        return self

    def trim_end(self, width: int):
        if self.len() > width:
            self.data = self.data[:width]
        return self

    def join(self, array: List[Sentence]):
        out = Sentence()
        for i, a in enumerate(array):
            if i != 0:
                out.add(self)
            out.add(a)
        return out
            


class Flag:
    def __init__(self):
        self._name: str = ""
        self._text: str = ""  # description
        self._char: str = ""
        self._values: List[str] = ["0", "1"]
        self._index: int = 0
        self._location: str = ""
        self._bool = True  # many options

    def set_name(self, _name):
        self._name = _name
        return self

    def set_description(self, _text):
        self._text = _text
        return self

    def set_keycode(self, _key):
        self._char = _key
        return self

    def set_values(self, _values: List[str]):
        self._values = _values
        return self

    def index(self, _index):
        self._index = _index
        return self

    def location(self, value: str):
        self._location = value
        return self

    def get_values(self):
        return self._values

    def toggle(self):
        self._index = (self._index + 1) % len(self._values)
        return self
    
    def set_bool(self):
        self._bool = True
        return self
    
    def is_bool(self):
        return self._bool

    def get_location(self) -> str:
        return self._location

    def get_value(self) -> str:
        return self._values[self._index % len(self._values)]
    
    def set_value(self, value: Any):
        for i, v in enumerate(self._values):
            if v == value:
                self._index = i
                break

    def is_true(self):
        return self.get_value() == "1"

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._text

    def get_keycode(self) -> str:
        return self._char

    def get_index(self) -> int:
        return self._index
    

class Flags:
    minimum = Flag().set_name("Mínimo").set_keycode("M").set_values(["0", "1"])    .set_description("Mostra os requisitos para completar a missão").location("left")
    reward = Flag().set_name("Recompensa").set_keycode("R").set_values(["0", "1"]) .set_description("Mostra a experiência obtida nas tarefas     ").location("left")
    percent = Flag().set_name("Percentual").set_keycode("P").set_values(["1", "0"]).set_description("Mostra todos os valores em porcentagem      ").location("left")
    admin = Flag().set_name("Admin").set_keycode("A").set_values(["0", "1"])       .set_description("Habilitas todas as missões e tarefas        ").location("left")
    config    = Flag().set_name("Config").set_keycode("c").set_values(["0", "1"]).set_description("Mostra a barra de flags").location("top")
    skills = Flag().set_name("Skills").set_keycode("i").set_values(["0", "1"]).set_description("Mostra a barra de skills").location("top")

class FlagsMan:
    def __init__(self, data: Dict[str, int]):
        self.flags: Dict[str, Flag] = {}
        self.top: List[Flag] = []
        self.left: List[Flag] = []
        self.others: List[Flag] = []

        for varname, flag in Flags.__dict__.items():
            if isinstance(flag, Flag):
                self.flags[varname] = flag
                if flag.get_location() == "top":
                    self.top.append(flag)
                elif flag.get_location() == "left":
                    self.left.append(flag)
                else:
                    self.others.append(flag)

        for key, _index in data.items():
            if key in self.flags:
                self.flags[key].index(_index)

    def get_data(self) -> Dict[str, int]:
        data = {}
        for name, flag in self.flags.items():
            if flag.get_location() == "geral":
                continue
            if len(flag.get_values()) > 1:
                data[name] = flag.get_index()
        return data


class FlagFunctor:
    def __init__(self, flag: Flag):
        self.flag = flag

    def __call__(self):
        self.flag.toggle()

class GradeFunctor:
    def __init__(self, grade: int, fn):
        self.grade = grade
        self.fn = fn

    def __call__(self):
        self.fn(self.grade)


class Fmt:
    __scr = None
    # Definindo constantes para as cores
    color_pairs: Dict[str, int] = {}

    COLOR_MAP = {
        'k': curses.COLOR_BLACK,
        'r': curses.COLOR_RED,
        'g': curses.COLOR_GREEN,
        'y': curses.COLOR_YELLOW,
        'b': curses.COLOR_BLUE,
        'm': curses.COLOR_MAGENTA,
        'c': curses.COLOR_CYAN,
        'w': curses.COLOR_WHITE,
    }
    @staticmethod
    def set_scr(scr):
        Fmt.__scr = scr
        Fmt.init_colors()

    @staticmethod
    def init_colors():
        pair_number = 1
        curses.start_color()
        curses.use_default_colors()
        for fk, fg in Fmt.COLOR_MAP.items():
            curses.init_pair(pair_number, fg, -1)
            Fmt.color_pairs[fk] = pair_number
            pair_number += 1

        for fk, fg in Fmt.COLOR_MAP.items():
            for bk, bg in Fmt.COLOR_MAP.items():
                curses.init_pair(pair_number, fg, bg)
                Fmt.color_pairs[fk + bk.upper()] = pair_number
                pair_number += 1

    @staticmethod
    def stroke(y: int, x: int, fmt: str, text: str):
        if Fmt.__scr is None:
            raise Exception("Fmt.__scr não foi inicializado")
        stdscr = Fmt.__scr
        italic = False
        underline = False
        source_fmt = fmt
        if "/" in fmt:
            italic = True
            fmt = fmt.replace("/", "")
        if "_" in fmt:
            underline = True
            fmt = fmt.replace("_", "")

        fg_list = [c for c in fmt if c.islower()]
        bg_list = [c for c in fmt if c.isupper()]
        bg = "" if len(bg_list) == 0 else bg_list[0]
        fg = "" if len(fg_list) == 0 else fg_list[0]

        if bg != "" and fg == "":
            fg = "k"
        if fg == "" and bg == "":
            pair_number = -1
        else:
            try:
                pair_number = Fmt.color_pairs[fg + bg]
            except KeyError:
                # print("Cor não encontrada: " + fg + bg)
                raise(Exception("Cor não encontrada: " + source_fmt))
                exit(1)
        if italic:
            stdscr.attron(curses.A_ITALIC)
        if underline:
            stdscr.attron(curses.A_UNDERLINE)
        # Exibir o texto com a combinação de cores escolhida
        if pair_number != -1:
            stdscr.attron(curses.color_pair(pair_number))
        try:
            stdscr.addstr(y, x, text)
        except curses.error as _e:
            lines, cols = Fmt.get_size()
            if y == lines - 1:
                if x + len(text) <= cols:
                    pass
            # lines, cols = stdscr.getmaxyx()
            # stdscr.addstr(10, 10, f"y:{y}, x:{x}, fmt:{fmt}, len:{len(text)} lines:{lines}, cols:{cols}")
            # stdscr.addstr(1, 0, text)
            # raise Exception(f"y:{y}, x:{x}, fmt:{fmt}, len:{len(text)} lines:{lines}, cols:{cols}\n{text}")
        if pair_number != -1:
            stdscr.attroff(curses.color_pair(pair_number))
        if italic:
            stdscr.attroff(curses.A_ITALIC)
        if underline:
            stdscr.attroff(curses.A_UNDERLINE)

    @staticmethod
    def write(y: int, x: int, sentence: Sentence):

        # Escreve um texto na tela com cores diferentes
        lines, cols = Fmt.get_size()
        if y < 0 or y >= lines:
            return
        for token in sentence.resume():
            fmt = token.fmt
            text = token.text
            if x < 0:
                if x + len(text) >= 0:
                    text = text[-x:]
                    x = 0
            if x < cols:
                if x + len(text) >= cols:
                    text = text[:cols - x]
                Fmt.stroke(y, x, fmt, text)
            x += len(text)  # Move a posição x para a direita após o texto

    @staticmethod
    def write_text(y: int, x: int, text: str):
        Fmt.write(y, x, Sentence().add(text))

    @staticmethod
    def debug(y, x, text: Sentence):
        Fmt.write(y, x, text)
        Fmt.getch()


    # @staticmethod
    # def get_user_input(stdscr, prompt: str) -> str:
    #     lines, cols = stdscr.getmaxyx()
    #     curses.echo()  # Ativa a exibição dos caracteres digitados
    #     curses.curs_set(1)  # Ativa o cursor
    #     stdscr.addstr(0, 0, cols * " ")
    #     stdscr.addstr(0, 0, prompt)
    #     stdscr.refresh()
    #     input_str = stdscr.getstr(0, len(prompt), 20).decode('utf-8')  # Captura o input do usuário
    #     curses.noecho()  # Desativa a exibição dos caracteres digitados
    #     curses.curs_set(0)
    #     return input_str

    @staticmethod
    def get_percent(value, pad = 0) -> Sentence:
        text = f"{str(value)}%".rjust(pad)
        if value == 100:
            return Sentence().addf(Colors.mark_complete, "100%")
        if value >= 70:
            return Sentence().addf(Colors.mark_required, text)
        if value == 0:
            return Sentence().addf(Colors.mark_nothing, text)
        return Sentence().addf(Colors.mark_started, text)
    
    @staticmethod
    def getch():
        if Fmt.__scr is None:
            raise Exception("Fmt.__scr não foi inicializado")
        return Fmt.__scr.getch()

    @staticmethod
    def clear():
        if Fmt.__scr is None:
            raise Exception("Fmt.__scr não foi inicializado")
        Fmt.__scr.erase()

    @staticmethod
    def refresh():
        if Fmt.__scr is None:
            raise Exception("Fmt.__scr não foi inicializado")
        Fmt.__scr.refresh()

    @staticmethod
    def get_size() -> Tuple[int, int]:
        if Fmt.__scr is None:
            raise Exception("Fmt.__scr não foi inicializado")
        return Fmt.__scr.getmaxyx()
        



class Frame:
    def __init__(self, y: int = 0, x: int = 0):
        self._x = x
        self._y = y
        self._inner_dx = 0
        self._inner_dy = 0
        self._border = "rounded"
        self._filled = False
        self._header: Sentence = Sentence()
        self._halign = ""
        self._hprefix = ""
        self._hsuffix = ""
        self._footer: Sentence = Sentence()
        self._falign = ""
        self._fprefix = ""
        self._fsuffix = ""
        self._fill_char = " "
        self._wrap = False
        self._border_color = ""
        self._print_index = 0

    def set_border_color(self, color: str):
        self._border_color = color
        return self

    def get_dx(self):
        return self._inner_dx

    def get_dy(self):
        return self._inner_dy

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def __align_header_footer(self, data, symbol, prefix, suffix):
        dx = self._inner_dx
        color = self._border_color
        pad = dx - len(prefix) - len(suffix)
        hor = self.get_symbol("h")
        
        data.trim_end(pad)
        sent = Sentence().addf(color, prefix).add(data).addf(color, suffix)
        if symbol == "<":
            sent.ljust(dx, Token(hor, color))
        elif symbol == ">":
            sent.rjust(dx, Token(hor, color))
        else:
            sent.center(dx, Token(hor, color))
        return sent

    def get_header(self):
        return Sentence().add(self._hprefix).add(self._header).add(self._hsuffix)
    
    def get_footer(self):
        return Sentence().add(self._fprefix).add(self._footer).add(self._fsuffix)

    def get_full_header(self):
        return self.__align_header_footer(self._header, self._halign, self._hprefix, self._hsuffix)

    def get_full_footer(self):
        return self.__align_header_footer(self._footer, self._falign, self._fprefix, self._fsuffix)

    def set_pos(self, y: int, x: int):
        self._x = x
        self._y = y
        return self

    def set_size(self, size_y, size_x):
        self._inner_dx = size_x - 2
        self._inner_dy = size_y - 2
        return self

    def set_inner(self, inner_dy: int, inner_dx: int):
        self._inner_dy = inner_dy
        self._inner_dx = inner_dx
        return self

    def get_inner(self):
        return (self._inner_dy, self._inner_dx)

    def get_size(self):
        return self._inner_dy + 2, self._inner_dx + 2

    def set_end(self, y: int, x: int):
        self._inner_dx = x - self._x - 1
        self._inner_dy = y - self._y - 1
        return self

    def set_wrap(self):
        self._wrap = True
        return self

    def set_fill_char(self, char: str):
        self._fill_char = char
        return self

    def get_symbol(self, value: str):
        square = {"lu": "┌", "ru": "┐", "ld": "└", "rd": "┘", "h": "─", "v": "│"}
        rounded = {"lu": "╭", "ru": "╮", "ld": "╰", "rd": "╯", "h": "─", "v": "│"}
        bold = {"lu": "┏", "ru": "┓", "ld": "┗", "rd": "┛", "h": "━", "v": "┃"}

        if self._border == "square":
            return square[value]
        elif self._border == "rounded":
            return rounded[value]
        elif self._border == "bold":
            return bold[value]
        return " "

    def set_border_none(self):
        self._border = "none"
        return self

    def set_border_bold(self):
        self._border = "bold"
        return self

    def set_border_rounded(self):
        self._border = "rounded"
        return self

    def set_border_square(self):
        self._border = "square"
        return self

    def set_header(self, header: Sentence, align="<", prefix="", suffix=""):
        self._halign = align
        self._header = header
        self._hprefix = prefix
        self._hsuffix = suffix
        return self

    def set_footer(self, footer: Sentence, align=">", prefix="", suffix=""):
        self._falign = align
        self._footer = footer
        self._fprefix = prefix
        self._fsuffix = suffix
        return self

    def set_fill(self):
        self._filled = True
        return self

    def set_nofill(self):
        self._filled = False
        return self

    def print(self, x: int, sentence: Sentence):
        self.write(self._print_index, x, sentence)
        self._print_index += 1
        return self

    # return y, x of the last character
    def write(self, y: int, x: int, sentence: Sentence) -> bool:
        lines, cols = Fmt.get_size()

        x_min = max(-1, self._x)
        y_min = max(-1, self._y)
        x_max = min(cols, self._x + self._inner_dx)
        y_max = min(lines, self._y + self._inner_dy)

        x_abs = x + self._x + 1
        y_abs = y + self._y + 1

        if y_abs <= y_min or y_abs > y_max:
            return False
        count = 0
        for token in sentence.resume():
            fmt, text = token.fmt, token.text
            if x_abs - 1 < x_min:  # Se o texto começa fora do frame
                if x_abs + len(text) > x_min:  # mas ter parte dentro
                    text = text[x_min - x_abs + 1 :]
                    x_abs = x_min + 1
            if x_abs <= x_max:  # Se o texto começa dentro do frame
                if x_abs + len(text) >= x_max:
                    cut_point = x_max - x_abs + 1
                    text = text[:cut_point]

                Fmt.stroke(y_abs, x_abs, fmt, text)
                count += 1
            x_abs += len(text)
        return count != 0

    def draw(self):
        x = self._x
        y = self._y
        dx = self._inner_dx
        dy = self._inner_dy
        color = self._border_color
        up_left = self.get_symbol("lu")
        up_right = self.get_symbol("ru")
        down_left = self.get_symbol("ld")
        down_right = self.get_symbol("rd")
        hor = self.get_symbol("h")
        ver = self.get_symbol("v")

        header = self.get_full_header()
        footer = self.get_full_footer()

        above = Sentence().addf(color, up_left).add(header).addf(color, up_right)
        below = Sentence().addf(color, down_left).add(footer).addf(color, down_right)

        Fmt.write(y, x, above)
        if dy > 0:
            Fmt.write(y + dy + 1, x, below)
        if self._filled:
            for i in range(1, dy + 1):
                Fmt.write(
                    y + i,
                    x,
                    Sentence()
                    .addf(color, ver)
                    .add(dx * self._fill_char)
                    .addf(color, ver),
                )
        else:
            for i in range(1, dy + 1):
                Fmt.write(y + i, x, Sentence().addf(color, ver))
                Fmt.write(y + i, x + dx + 1, Sentence().addf(color, ver))
        return self



class Floating:
    def __init__(self, _align=""):
        self._frame = Frame(0, 0)
        self._content: List[Sentence] = []
        self._type = "warning"
        self._options = []
        self._options_index = 0
        self._fn_answer = None
        self._enable = True
        self._extra_exit: List[int] = []
        self._exit_fn = None
        self._exit_key = None
        self._centralize = True
        self._floating_align = _align

    def disable(self):
        self._enable = False

    def set_ljust_text(self):
        self._centralize = False
        return self

    def set_align(self, _align: str):
        self._floating_align = _align

    def set_header(self, text: str):
        self._frame.set_header(Sentence().addf("/", text), "")
        return self
    
    def set_header_sentence(self, sentence: Sentence):
        self._frame.set_header(sentence, "")
        return self
    
    def set_exit_key(self, key: str):
        self._exit_key = ord(key)
        return self

    def set_exit_fn(self, fn):
        self._exit_fn = fn
        return self

    def _set_xy(self, dy, dx):
        valid = "<>^v"
        for c in self._floating_align:
            if c not in valid:
                raise ValueError("Invalid align " + c)

        lines, cols = Fmt.get_size()

        x = (cols - dx) // 2
        if "<" in self._floating_align:
            x = 1
        elif ">" in self._floating_align:
            x = cols - dx - 3

        y = (lines - dy) // 2
        if "^" in self._floating_align:
            y = 1
        elif "v" in self._floating_align:
            y = lines - dy - 5

        self._frame.set_pos(y, x)
        return self
            
    def is_enable(self):
        return self._enable

    def __setup_frame(self):
        header_len = self._frame.get_header().len()
        footer_len = self._frame.get_footer().len()
        data = [x.len() for x in self._content] + [header_len, footer_len]
        max_dx = max(data)
        dx = max_dx
        dy = len(self._content)
        self._frame.set_inner(dy, dx)
        self._set_xy(dy, dx)
        self._frame.set_fill()
        
        if self._type == "answer":
            footer = Sentence().add(" ")
            for i, option in enumerate(self._options):
                fmt = "kG" if i == self._options_index else ""
                footer.addf(fmt, option).add(" ")
            self._frame.set_footer(footer, "^")

    def put_text(self, text: str):
        lines = text.split("\n")
        for line in lines:
            self._content.append(Sentence().add(line))
        return self

    def put_sentence(self, sentence: Sentence):
        self._content.append(sentence)
        return self
    
    def set_content(self, content: List[str]):
        self._content = [Sentence().add(x) for x in content]
        return self

    def _set_default_footer(self):
        if self._frame.get_footer().len() == 0:
            label = Sentence().addf("/", " Pressione espaço ")
            self._frame.set_footer(label, "", "─", "─")
        return self

    def _set_default_header(self):
        if self._frame.get_header().len() == 0:
            if self._type == "warning":
                self.set_header(" Aviso ")
            elif self._type == "error":
                self.set_header(" Erro ")
            elif self._type == "answer":
                self.set_header(" Pergunta ")

    def warning(self):
        self._type = "warning"
        self._frame.set_border_color("y")
        return self
    
    def error(self):
        self._type = "warning"
        self._frame.set_border_color("r")
        return self
    
    def answer(self, fn_answer):
        self._type = "answer"
        self._frame.set_border_color("g")
        self._fn_answer = fn_answer
        return self

    def set_options(self, options: List[str]):
        self._options = options
        return self

    def draw(self):
        self._set_default_header()
        self._set_default_footer()
        self.__setup_frame()
        self._frame.draw()
        y = 0

        for line in self._content:
            x = 0
            if self._centralize:
                x = (self._frame.get_dx() - line.len()) // 2
            self._frame.write(y, x, line)
            y += 1
        return self

    def get_input(self) -> int:
        self.draw()
        key: int = Fmt.getch()
        if self._type == "warning" or self._type == "error":
            if key < 300:
                self._enable = False
                if self._exit_fn is not None:
                    self._exit_fn()
                if self._exit_key is not None:
                    return self._exit_key
                if key == ord(" ") or key == 27:
                    return -1
                return key
        if self._type == "answer":
            if key == curses.KEY_LEFT:
                self._options_index = (self._options_index - 1) % len(self._options)
            elif key == curses.KEY_RIGHT:
                self._options_index = (self._options_index + 1) % len(self._options)
            elif key == 27:
                self._enable = False
            elif key == ord('\n'):
                self._enable = False
                if self._fn_answer is not None:
                    self._fn_answer(self._options[self._options_index])
                if self._exit_fn is not None:
                    self._exit_fn()
                if self._exit_key is not None:
                    return self._exit_key
                return -1
        return -1
        


class FloatingManager:
    def __init__(self):
        self.input_layer: List[Floating] = []

    def add_input(self, floating: Floating):
        self.input_layer.append(floating)

    def draw_warnings(self):
        if len(self.input_layer) > 0 and self.input_layer[0].is_enable():
            self.input_layer[0].draw()

    def has_floating(self) -> bool:
        while len(self.input_layer) > 0 and not self.input_layer[0].is_enable():
            self.input_layer = self.input_layer[1:]
        return len(self.input_layer) > 0 and self.input_layer[0].is_enable()

    def get_input(self) -> int:
        return self.input_layer[0].get_input()


class __Symbols:

    def __init__(self):
        self.downloaded = Token("▼")
        self.to_download = Token("▽")
        self.cant_download = Token("◉")
        self.opening = Token("=> ")
        self.neutral = Token("»")
        self.success = Token("✓")
        self.failure = Token("✗")
        self.wrong = Token("ω")
        self.compilation = Token("ϲ")
        self.execution = Token("ϵ")
        self.unequal = Token("├")
        self.equalbar = Token("│")
        self.hbar = Token("─")
        self.vbar = Token("│")

        self.whitespace = Token("·")
        # self.whitespace = Token("␣")
        
        # self.newline = Token("¶")
        self.newline = Token("↲")
        # self.newline = Token("⏎")

        self.cfill = Token("_")
        self.tab = Token("    ")
        self.arrow_up = Token("↑")

        self.check = Token("✓")
        self.uncheck = Token("✗")
        # self.opcheck = Token("ⴲ")
        # self.opuncheck = Token("ⵔ")
        self.infinity = Token("∞")
        self.locked_free = Token("⇉")
        self.locked_locked = Token("⇟")
        self.left_toggle = Token("━─")
        self.right_toggle = Token("─━")


    def set_colors(self):
        self.opening.fmt = "b"
        self.neutral.fmt = "b"
        self.success.fmt = "g"
        self.failure.fmt = "r"
        self.wrong.fmt = "r"
        self.compilation.fmt = "y"
        self.execution.fmt = "y"
        self.unequal.fmt = "r"
        self.equalbar.fmt = "g"

symbols = __Symbols()


class Task:

    def __init__(self):
        self.line_number = 0
        self.line = ""
        self.key = ""

        self.grade: int = 0 #valor de 0 a 10
        self.test_progress: int = 0 #valor de 0 a 100
        self.main_index: int = 0

        self.qskills: Dict[str, int] = {} # default quest skills
        self.skills: Dict[str, int] = {} # local skills
        self.xp: int = 0
        
        self.opt: bool = False
        self.title = ""
        self.link = ""

        self.default_min_value = 7 # default min grade to complete task

    def load_from_db(self, value: str):
        if ":" not in value:
            self.grade = int(value)
        else:
            v = value.split(":")
            if len(v) == 3:
                self.grade = int(v[0])
                self.main_index = int(v[1])
                self.test_progress = int(v[2])

    def save_to_db(self) -> str:
        return f"{self.grade}:{self.main_index}:{self.test_progress}"
    
    def is_db_empty(self) -> bool:
        return self.grade == 0 and self.main_index == 0 and self.test_progress == 0

    def get_grade_color(self, min_value: Optional[int] = None) -> str:
        if min_value is None:
            min_value = self.default_min_value
        if self.grade == 0:
            return "m"
        if self.grade < min_value:
            return "r"
        if self.grade < 10:
            return "y"
        if self.grade == 10:
            return "g"
        return "w"  

    def get_grade_symbol(self, min_value: Optional[int] = None) -> Sentence:
        
        if min_value is None:
            min_value = self.default_min_value
        color = self.get_grade_color(min_value)
        if self.grade == 0:
            return Sentence().addf(color, symbols.uncheck.text)
        if self.grade < min_value:
            return Sentence().addf(color, str(self.grade))
        if self.grade < 10:
            return Sentence().addf(color, str(self.grade))
        if self.grade == 10:
            return Sentence().addf(color, symbols.check.text)
        return Sentence().add("0")

    def get_percent(self):
        if self.grade == 0:
            return 0
        if self.grade == 10:
            return 100
        return self.grade * 10
    
    def is_complete(self):
        return self.grade == 10

    def not_started(self):
        return self.grade == 0
    
    def in_progress(self):
        return self.grade > 0 and self.grade < 10

    def set_grade(self, grade: int):
        grade = int(grade)
        if grade >= 0 and grade <= 10:
            self.grade = grade
        else:
            print(f"Grade inválida: {grade}")
    
    def process_link(self, base_file):
        if self.link.startswith("http"):
            return
        if self.link.startswith("./"):
            self.link = self.link[2:]
        # todo trocar / por \\ se windows
        self.link = base_file + self.link

    def __str__(self):
        line = str(self.line_number).rjust(3)
        key = "" if self.key == self.title else self.key + " "
        return f"{line}    {self.grade} {key}{self.title} {self.skills} {self.link}"
    
    def is_downloadable(self):
        return f"@{self.key}" in self.title
    
    def is_downloaded_for_lang(self, rep_dir: str, lang: str) -> bool:
        folder = os.path.join(rep_dir, self.key)
        if not os.path.isfile(os.path.join(folder, "Readme.md")):
            return False
        files = os.listdir(folder)
        if not any([f.endswith("." + lang) for f in files]):
            return False
        return True

class TaskParser:

    @staticmethod
    def load_html_tags(task: Task):                   
        pattern = r"<!--\s*(.*?)\s*-->"
        match = re.search(pattern, task.line)
        if not match:
            return

        tags_raw = match.group(1).strip()
        tags = [tag.strip() for tag in tags_raw.split(" ")]
        task.opt = "opt" in tags
        for t in tags:
            if t.startswith("+"):
                key, value = t[1:].split(":")
                task.skills[key] = int(value)
            elif t.startswith("@"):
                task.key = t[1:]

    @staticmethod
    def parse_item_with_link(line) -> Tuple[bool, str, str]:
        pattern = r"\ *-.*\[(.*?)\]\((.+?)\)"
        match = re.match(pattern, line)
        if match:
            return True, match.group(1), match.group(2)
        return False, "", ""
    
    @staticmethod
    def parse_task_with_link(line) -> Tuple[bool, str, str]:
        pattern = r"\ *- \[ \].*\[(.*?)\]\((.+?)\)"
        match = re.match(pattern, line)
        if match:
            return True, match.group(1), match.group(2)
        return False, "", ""

    @staticmethod
    def parse_arroba_from_title_link(titulo, link) -> Tuple[bool, str]:
        pattern = r'@\w+'
        match = re.search(pattern, titulo)
        if not match:
            return False, ""
        key = match.group(0)[1:]
        if not (key + "/Readme.md") in link:
            return False, ""
        return True, key

    # - [Titulo com @palavra em algum lugar](link/@palavra/Readme.md) <!-- tag1 tag2 tag3 -->
    @staticmethod
    def __parse_coding_task(line, line_num) -> Optional[Task]:
        if line == "":
            return None
        line = line.lstrip()

        found, titulo, link = TaskParser.parse_item_with_link(line)
        if not found:
            return None
        found, key = TaskParser.parse_arroba_from_title_link(titulo, link)
        if not found:
            return None

        task = Task()

        task.line = line
        task.line_number = line_num
        task.key = key
        task.title = titulo
        task.link = link
        TaskParser.load_html_tags(task)

        return task

    # se com - [ ], não precisa das tags dentro do html, o key será dado pelo título
    # se tiver as tags dentro do html, se alguma começar com @, o key será dado por ela
    # - [ ] [Título](link)
    # - [ ] [Título](link) <!-- tag1 tag2 tag3 -->
    # - [Título](link) <!-- tag1 tag2 tag3 -->
    @staticmethod
    def __parse_reading_task(line, line_num) -> Optional[Task]:
        if line == "":
            return None
        line = line.lstrip()

        found, titulo, link = TaskParser.parse_task_with_link(line)

        if found:
            task = Task()
            task.key = link
            task.title = titulo
            task.link = link
            task.line = line
            task.line_number = line_num
            TaskParser.load_html_tags(task)
            return task
        
        task = Task()
        found, titulo, link = TaskParser.parse_item_with_link(line)
        task.key = ""
        if found:
            task.link = link
            task.line = line
            task.line_number = line_num
            TaskParser.load_html_tags(task)
            if task.key == "": # item with links needs a key
                return None
            task.title = titulo
            return task

        return None

    @staticmethod
    def parse_line(line, line_num) -> Optional[Task]:
        task = TaskParser.__parse_coding_task(line, line_num)
        
        if task is not None:
            return task
        task = TaskParser.__parse_reading_task(line, line_num)
        if task is not None:
            return task
        return None



class Quest:
    def __init__(self):
        self.line_number = 0
        self.line = ""
        self.key = ""
        self.title = ""
        self.__tasks: List[Task] = []
        self.skills: Dict[str, int] = {}  # s:skill
        self.cluster = ""
        self.requires = []  # r:quest_key
        self.requires_ptr = []
        self.opt = False  # opt
        self.qmin: Optional[int] = None  # q:  minimo de 50 porcento da pontuação total para completar
        self.tmin: Optional[int] = None  # t: ou ter no mínimo esse valor de todas as tarefas
        self.filename = ""
        self.__is_reachable: bool = False
        
    def is_reachable(self)-> bool:
        return self.__is_reachable

    def set_reachable(self, value: bool):
        self.__is_reachable = value

    def __str__(self):
        line = str(self.line_number).rjust(3)
        tasks_size = str(len(self.__tasks)).rjust(2, "0")
        key = "" if self.key == self.title else self.key + " "
        output = f"{line} {tasks_size} {key}{self.title} {self.skills} {self.requires}"
        return output

    def get_resume_by_percent(self) -> Sentence:
        value = self.get_percent()
        return Sentence().addf(self.get_grade_color(), (str(value) + "%").rjust(4))
    
    def get_requirement(self) -> Sentence:
        if self.qmin is not None:
            return Sentence().addf("y", f"[{self.qmin}%]")
        if self.tmin is not None:
            return Sentence().addf("y", f"[t>{self.tmin - 1}]")
        return Sentence()

    def get_resume_by_tasks(self) -> Sentence:
        tmin = self.tmin if self.tmin is not None else 7
        total = len([t for t in self.__tasks if not t.opt])
        plus = len([t for t in self.__tasks if t.opt])
        count = len([t for t in self.__tasks if t.grade >= tmin])
        output = f"{count}/{total}"
        if plus > 0:
            output += f"+{plus}"
        return Sentence().addf(self.get_grade_color(), "(" + output + ")")

    def get_grade_color(self) -> str:
        if self.not_started():
            return "m"
        if not self.is_complete():
            return "r"
        if self.get_percent() == 100:
            return "g"
        return "y"

    def is_complete(self):
        if self.qmin is not None:
            return self.get_percent() >= self.qmin
        # task complete mode
        if self.tmin is not None:
            for t in self.__tasks:
                if not t.opt and t.grade < self.tmin:
                    return False
        return True

    def add_task(self, task: Task, filename: str):
        if self.qmin is not None:
            if task.opt:
                print(f"Quests com requerimento de porcentagem não deve ter Tasks opcionais")
                print(f"{filename}:{task.line_number} {task.key}")
                exit(1)
        task.qskills = self.skills

        task.xp = 0
        for s in task.skills:
            task.xp += task.skills[s]

        for s in task.qskills:
            task.xp += task.qskills[s]
        
        self.__tasks.append(task)

    def get_tasks(self):
        return self.__tasks

    def get_xp(self) -> Tuple[int, int]:
        total = 0
        obtained = 0
        for t in self.__tasks:
            total += t.xp
            if t.grade > 0:
                obtained += t.xp * t.grade // 10

        return obtained, total
        
    def get_percent(self):
        obtained, total = self.get_xp()
        if total == 0:
            return 0
        return obtained * 100 // total

    def in_progress(self):
        if self.is_complete():
            return False
        for t in self.__tasks:
            if t.grade != 0:
                return True
        return False

    def not_started(self):
        if self.is_complete():
            return False
        if self.in_progress():
            return False
        return True




class QuestParser:
    quest: Quest

    def __init__(self):
        self.quest = Quest()
        self.line = ""
        self.line_num = 0
        self.default_qmin_requirement = 50
        self.default_task_xp = 10
        self.filename = ""

    def finish_quest(self) -> Quest:

        if self.quest.key == "":
            self.quest.key = get_md_link(self.quest.title)

        if len(self.quest.skills) == 0:
            self.quest.skills["xp"] = self.default_task_xp
        
        if self.quest.qmin is None and self.quest.tmin is None:
            self.quest.qmin = self.default_qmin_requirement

        return self.quest

    def match_full_pattern(self):
        fullpattern = r"^#+\s*(.*?)<!--\s*(.*?)\s*-->.*$"
        match = re.match(fullpattern, self.line)

        if not match:
            return False
        self.quest.title = match.group(1).strip()
        tags_raw = match.group(2).strip()
        tags = [tag.strip() for tag in tags_raw.split()]

        # key
        keys = [t[1:] for t in tags if t.startswith("@")]
        if len(keys) > 0:
            self.quest.key = keys[0]

        # skills
        skills = [t[1:] for t in tags if t.startswith("+")]
        if len(skills) > 0:
            self.quest.skills = {}
            for s in skills:
                k, v = s.split(":")
                self.quest.skills[k] = int(v)
        # requires
        self.quest.requires = [t[2:] for t in tags if t.startswith("r:")]

        self.quest.opt = "opt" in tags
        # type
        # try:
        #     self.quest.type = [t[1:] for t in tags if t.startswith("#")][0]
        # except:
        #     self.quest.type = "main"
        
        # quest percent
        qmin = [t[2:] for t in tags if t.startswith("q:")]
        
        if len(qmin) > 0:
            self.quest.qmin = int(qmin[0])

        # task min value requirement
        tmin = [t[2:] for t in tags if t.startswith("t:")]
        if len(tmin) > 0:
            self.quest.tmin = int(tmin[0])
            if self.quest.tmin > 10:
                print("fail: tmin > 10")
                exit(1)
        return True

    def __match_minimal_pattern(self):
        minipattern = r"^#+\s*(.*?)\s*$"
        match = re.match(minipattern, self.line)
        if match:
            self.quest.title = match.group(1).strip()
            return True
        return False

    def parse_quest(self, filename, line, line_num) -> Optional[Quest]:
        self.line = line
        self.line_num = line_num
        self.filename = filename

        self.quest.line = self.line
        self.quest.line_number = self.line_num
        self.quest.cluster = ""

        if self.match_full_pattern():
            return self.finish_quest()
        
        if self.__match_minimal_pattern():
            return self.finish_quest()
        
        return None



class Cluster:
    def __init__(self, line_number: int = 0, title: str = "", key: str = "", color: Optional[str] = None):
        self.line_number = line_number
        self.title: str = title
        self.key: str = key
        self.quests: List[Quest] = []
        self.color: Optional[str] = color
        self.__is_reachable = False

    def is_reachable(self):
        return self.__is_reachable
    
    def set_reachable(self, value: bool):
        self.__is_reachable = value
        return self

    def __str__(self):
        line = str(self.line_number).rjust(3)
        quests_size = str(len(self.quests)).rjust(2, "0")
        key = "" if self.key == self.title else self.key + " "
        return f"{line} {quests_size} {key}{self.title}"
    
    def get_grade_color(self) -> str:
        perc = self.get_percent()
        if perc == 0:
            return "m"
        if perc < 50:
            return "r"
        if perc < 100:
            return "y"
        return "g"

    def get_percent(self):
        total = 0
        for q in self.quests:
            total += q.get_percent()
        return total // len(self.quests)

    def get_resume_by_percent(self) -> Sentence:
        return Sentence().addf(self.get_grade_color(), f"{self.get_percent()}%".rjust(4))

    def get_resume_by_quests(self):
        total = len(self.quests)
        count = len([q for q in self.quests if q.is_complete()])
        return Sentence().addf(self.get_grade_color(), f"({count}/{total})")
        

class LabelFactory:
    def __init__(self):
        self._label = ""
        self._index = -1

    def index(self, value: int):
        try:
            self._index = int(value)
        except ValueError:
            raise ValueError("Index on label must be a integer")
        return self

    def label(self, value: str):
        self._label = value
        return self

    def generate(self):
        label = LabelFactory.trim_spaces(self._label)
        label = LabelFactory.remove_old_index(label)
        if self._index != -1:
            index = str(self._index).zfill(2)
            if label != "":
                return index + " " + label
            else:
                return index
        return label

    @staticmethod
    def trim_spaces(text):
        parts = text.split(" ")
        parts = [word for word in parts if word != '']
        return " ".join(parts)

    @staticmethod
    def remove_old_index(label):
        split_label = label.split(" ")
        if len(split_label) > 0:
            try:
                int(split_label[0])
                return " ".join(split_label[1:])
            except ValueError:
                return label


class TermColor:
    enabled = True
    terminal_styles = {
        '.': '\033[0m', # Reset
        '*': '\033[1m', # Bold
        '/': '\033[3m', # Italic
        '_': '\033[4m', # Underline
        
        'k': '\033[30m', # Black
        'r': '\033[31m', # Red
        'g': '\033[32m', # Green
        'y': '\033[33m', # Yellow
        'b': '\033[34m', # Blue
        'm': '\033[35m', # Magenta
        'c': '\033[36m', # Cyan
        'w': '\033[37m', # White


        'K': '\033[40m', # Background black
        'W': '\033[47m', # Background white
    }

def _colour(modifiers: str, text: str) -> str:
    if not TermColor.enabled:
        return text
    output = ''
    for m in modifiers:
        val = TermColor.terminal_styles.get(m, '')
        if val != '':
            output += val
    output += text + TermColor.terminal_styles.get('.', "")
    return output

def term_colour(ftext: Sentence) -> str:
    output = ""
    for token in ftext.data:
        output += _colour(token.fmt, token.text)
    return output

def term_print(ftext: Union[str, Sentence], **kwargs):
    if isinstance(ftext, str):
        print(ftext, **kwargs)
    else:
        print(term_colour(ftext), **kwargs)


class Report:
    __term_width: Optional[int] = None

    def __init__(self):
        pass

    @staticmethod
    def __get_terminal_size() -> int:
        term_width = shutil.get_terminal_size().columns
        if term_width % 2 == 0:
            term_width -= 1
        return term_width

    @staticmethod
    def get_terminal_size():
        if Report.__term_width is None:
            return Report.__get_terminal_size()
        return Report.__term_width

    @staticmethod
    def set_terminal_size(value: int):
        if value % 2 == 0:
            value -= 1
        Report.__term_width = value

    @staticmethod
    def centralize(
        ftext: Union[Sentence, str],
        sep: Optional[Union[str, Token]] = Token(" "),
        left_border: Optional[Union[str, Token]] = None,
        right_border: Optional[Union[str, Token]] = None,
    ) -> Sentence:

        if isinstance(ftext, str) or isinstance(ftext, Token):
            ftext = Sentence() + ftext
        if sep is None:
            sep = Token(" ")
        elif isinstance(sep, str):
            sep = Token(sep)
        if left_border is None:
            left_border = sep
        if right_border is None:
            right_border = sep
        term_width = Report.get_terminal_size()

        size = len(ftext)
        pad = sep if size % 2 == 0 else Token("")
        tw = term_width - 2
        filler = Token(sep.text * (int(tw / 2 - size / 2)), sep.fmt)
        return Sentence() + left_border + pad + filler + ftext + filler + right_border


class Runner:
    def __init__(self):
        pass

    @staticmethod
    def subprocess_run(cmd: str, input_data: str = "", timeout:Optional[float] = None) -> Tuple[int, str, str]:
        try:
            answer = subprocess.run(cmd, shell=True, input=input_data, stdout=PIPE, stderr=PIPE, text=True, timeout=timeout)
            err = ""
            if answer.returncode != 0:
                err = answer.stderr + Runner.decode_code(answer.returncode)
            # if running on windows
            if os.name == "nt":
                return answer.returncode, answer.stdout.encode("cp1252").decode("utf-8"), err
            return answer.returncode, answer.stdout, err
        except subprocess.TimeoutExpired:
            err = "fail: processo abortado depois de {} segundos".format(timeout)
            return 1, "", err



    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def decode_code(return_code: int) -> str:
        code = 128 - return_code
        if code == 127:
            return ""
        if code == 139:
            return "fail: segmentation fault"
        if code == 134:
            return "fail: runtime exception"
        return "fail: execution error code " + str(code)

# class Runner:

#     def __init__(self):
#         pass

#     @staticmethod
#     def subprocess_run(cmd_list: List[str], input_data: str = "") -> Tuple[int, Any, Any]:
#         try:
#             p = subprocess.Popen(cmd_list, stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
#             stdout, stderr = p.communicate(input=input_data)
#             return p.returncode, stdout, stderr
#         except FileNotFoundError:
#             print("\n\nCommand not found: " + " ".join(cmd_list))
#             exit(1)




class CompileError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class SolverBuilder:
    def __init__(self, solver_list: List[str]):
        self.path_list: List[str] = [os.path.normpath(SolverBuilder.__add_dot_bar(path)) for path in solver_list]
        
        self.temp_dir = tempfile.mkdtemp()
        self.error_msg: str = ""
        self.__executable: str = ""
        self.compile_error: bool = False

    def check_tool(self, name):
        if shutil.which(name) is None:
            self.compile_error = True
            raise CompileError("fail: comando '" + name + "' não foi encontrado")

    def set_main(self, main: str):
        list_main: List[str] = []
        list_other: List[str] = []

        for path in self.path_list:
            if os.path.basename(path) == main:
                list_main.append(path)
            else:
                list_other.append(path)
        
        self.path_list = list_main + list_other
        return self

    def set_executable(self, executable: str):
        self.__executable = executable
        return self

    def reset(self):
        self.__executable = ""
        self.compile_error = False
        self.error_msg = ""

    def not_compiled(self):
        return self.__executable == "" and not self.compile_error

    def get_executable(self, force_rebuild=False) -> str:
        if (len(self.path_list) > 0 and self.not_compiled()) or force_rebuild:
            self.prepare_exec()
        return self.__executable

    def prepare_exec(self, free_run_mode: bool = False) -> None:
        self.__executable = ""
        path = self.path_list[0]
        self.compile_error = False

        if path.endswith(".py"):
            self.__executable = "python " + path
        elif path.endswith(".js"):
            self.__prepare_js()
        elif path.endswith(".ts"):
            self.__prepare_ts(free_run_mode)
        elif path.endswith(".java"):
            self.__prepare_java()
        elif path.endswith(".c"):
            self.__prepare_c()
        elif path.endswith(".cpp"):
            self.__prepare_cpp()
        elif path.endswith(".go"):
            self.__prepare_go()
        elif path.endswith(".sql"):
            self.__prepare_sql()
        else:
            self.__executable = path

    def __prepare_java(self):
        self.check_tool("javac")

        solver = self.path_list[0]

        filename = os.path.basename(solver)
        # tempdir = os.path.dirname(self.path_list[0])

        cmd = ["javac"] + self.path_list + ['-d', self.temp_dir]
        cmdt = " ".join(cmd)
        return_code, stdout, stderr = Runner.subprocess_run(cmdt)
        if return_code != 0:
            self.error_msg = stdout + stderr
            self.compile_error = True
        else:
            self.__executable = "java -cp " + self.temp_dir + " " + filename[:-5]  # removing the .java

    def __prepare_js(self):
        self.check_tool("node")
        solver = self.path_list[0]
        self.__executable = "node " + solver

    def __prepare_go(self):
        self.check_tool("go")
        solver = self.path_list[0]
        self.__executable = "go run " + solver

    def __prepare_sql(self):
        self.check_tool("sqlite3")
        self.__executable = "cat " + " ".join(self.path_list) + " | sqlite3"

    def __prepare_ts(self, free_run_mode: bool):
        if free_run_mode:
            self.check_tool("ts-node")
            self.__executable = "ts-node -O '{\"module\": \"commonjs\"}' " + " ".join(self.path_list)
            return
        
        transpiler = "esbuild"
        if os.name == "nt":
            transpiler += ".cmd"

        self.check_tool(transpiler)
        self.check_tool("node")

        solver = self.path_list[0]

        filename = os.path.basename(solver)
        source_list = self.path_list
        cmd = [transpiler] + source_list + ["--outdir=" + self.temp_dir, "--format=cjs", "--log-level=error"]
        return_code, stdout, stderr = Runner.subprocess_run(" ".join(cmd))
        if return_code != 0:
            self.error_msg = stdout + stderr
            self.compile_error = True
        else:
            jsfile = os.path.join(self.temp_dir, filename[:-3] + ".js")
            self.__executable = "node " + jsfile  # renaming solver to main
    
    def __prepare_c_cpp(self, pre_args: List[str], pos_args: List[str]):
        # solver = self.path_list[0]
        tempdir = self.temp_dir
        source_list = self.path_list
        # print("Using the following source files: " + str([os.path.basename(x) for x in source_list]))
        
        exec_path = os.path.join(tempdir, ".a.out")
        cmd = pre_args + source_list + ["-o", exec_path] + pos_args
        return_code, stdout, stderr = Runner.subprocess_run(" ".join(cmd))
        if return_code != 0:
            self.error_msg = stdout + stderr
            self.compile_error = True
        else:
            self.__executable = exec_path

    def __prepare_c(self):
        self.check_tool("gcc")
        pre = ["gcc", "-Wall"]
        pos = ["-lm"]
        self.__prepare_c_cpp(pre, pos)

    def __prepare_cpp(self):
        self.check_tool("g++")
        pre = ["g++", "-std=c++17", "-Wall", "-Wextra", "-Werror"]
        pos: List[str] = []
        self.__prepare_c_cpp(pre, pos)

    @staticmethod
    def __add_dot_bar(solver: str) -> str:
        if os.sep not in solver and os.path.isfile("." + os.sep + solver):
            solver = "." + os.sep + solver
        return solver
    

class Free:
    @staticmethod
    def free_run(solver: SolverBuilder, show_compilling:bool=True, to_clear: bool=True, wait_input:bool=True) -> bool:

        if to_clear:
            Runner.clear_screen()
        if show_compilling:
            image = random.choice(list(compilling.keys()))
            for line in compilling[image].split("\n"):
                term_print(Report.centralize(Sentence().addf("y", line), Token(" ")))

        if show_compilling:
            Runner.clear_screen()
        solver.prepare_exec(free_run_mode=True)
        if solver.compile_error:
            print(solver.error_msg)
        else:
            cmd = solver.get_executable()
            # term_print(Report.centralize(Sentence() + " " + cmd + " ", "─"))
            if cmd.startswith("node"):
                if os.name == "nt":
                    term_print(Report.centralize(Sentence() + " Use Control-Z Enter caso precise finalizar a entrada ", "─"))
                else:
                    term_print(Report.centralize(Sentence() + " Use Control-D caso precise finalizar a entrada ", "─"))
                
            answer = subprocess.run(cmd, shell=True, text=True)
            if answer.returncode != 0 and answer.returncode != 1:
                print(Runner.decode_code(answer.returncode))
        to_run_again = False
        if wait_input:
            term_print(Report.centralize("", "─"))
            term_print(Sentence().addf("y", "Deseja compilar e executar novamente? (").addf("c", "s").addf("y", "/n): "), end="")
            valor = input()
            if valor != "n" and valor != "q":
                if to_clear:
                    Runner.clear_screen()
                to_run_again = True
        if to_clear:
            Runner.clear_screen()

        return to_run_again

def uni_to_asc(input_str: str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

class SearchAsc:
    def __init__(self, pattern: str):
        self.pattern = uni_to_asc(pattern.lower())

    def find(self, title: str) -> int:
        return uni_to_asc(title.lower()).find(self.pattern)
    
    def inside(self, title: str) -> bool:
        return self.find(title) != -1


def load_html_tags(task: str) -> Optional[str]:
    pattern = r"<!--\s*(.*?)\s*-->"
    match = re.search(pattern, task)
    if not match:
        return None
    return match.group(1).strip()


class Game:
    def __init__(self, file: Optional[str] = None):
        self.ordered_clusters: List[str] = [] # ordered clusters
        self.clusters: Dict[str, Cluster] = {} 
        self.quests: Dict[str, Quest] = {}  # quests indexed by quest key
        self.tasks: Dict[str, Task] = {}  # tasks indexed by task key

        self.available_quests: List[str] = []
        self.available_clusters: List[str] = []

        self.token_level_one = "level_one"
        self.token_level_mult = "level_mult"
        self.level_one = 100
        self.level_mult = 1.5

        self.filename = None
        if file is not None:
            self.filename = file
            self.parse_file(file)

    def parse_xp(self, line: str):
        values = load_html_tags(line)
        if values is not None:
            tags = values.split(" ")
            for t in tags:
                if t.startswith(self.token_level_one):
                    self.level_one = int(t.split(":")[1])
                if t.startswith(self.token_level_mult):
                    self.level_mult = float(t.split(":")[1])

    def get_task(self, key: str) -> Task:
        if key in self.tasks:
            return self.tasks[key]
        raise Warning(f"fail: tarefa '{key}' não encontrada no curso")

    # se existir um cluster nessa linha, insere na lista de clusters e 
    # retorno o objeto cluster inserido
    def load_cluster(self, line: str, line_num: int) -> Optional[Cluster]:
        pattern = r"^#+\s*(.*?)<!--\s*(.*?)\s*-->\s*$"
        match = re.match(pattern, line)
        if not match:
            return None
        titulo = match.group(1)
        tags_raw = match.group(2).strip()
        tags = [tag.strip() for tag in tags_raw.split(" ")]
        if "group" not in tags:
            return None
        
        keys = [tag[1:] for tag in tags if tag.startswith("@")]
        key = uni_to_asc(get_md_link(titulo))
        try:
            color = [tag[2:] for tag in tags if tag.startswith("c:")][0]
        except IndexError as _e:
            color = None
        if len(keys) > 0:
            key = keys[0]
        
        cluster = Cluster(line_num, titulo, key, color)

        if key in self.clusters.keys():
            c = self.clusters[key]
            print(f"Cluster {key} já existe")
            print(f"{self.filename}:{line_num}")
            print(f"{self.filename}:{c.line_number}")
            print("  " + str(c))
            print("  " + str(cluster))
            exit(1)
                
        self.clusters[key] = cluster
        self.ordered_clusters.append(key)
        return cluster
                
    def load_quest(self, line, line_num) -> Optional[Quest]:
        quest = QuestParser().parse_quest(self.filename, line, line_num + 1)
        if quest is None:
            return None
        if quest.key in self.quests:
            print(f"Quest {quest.key} já existe")
            print(f"{self.filename}:{quest.line_number}")
            print(f"{self.filename}:{self.quests[quest.key].line_number}")
            print("  " + str(quest))
            print("  " + str(self.quests[quest.key]))
            exit(1)
        self.quests[quest.key] = quest
        return quest

    def load_task(self, line, line_num) -> Optional[Task]:
        if line == "":
            return None
        task = TaskParser.parse_line(line, line_num + 1)
        if task is None:
            return None
        
        if task.key in self.tasks:
            print(f"Task {task.key} já existe")
            print(f"{self.filename}:{task.line_number}")
            print(f"{self.filename}:{self.tasks[task.key].line_number}")
            print("  " + str(task))
            print("  " + str(self.tasks[task.key]))
            exit(1)
        self.tasks[task.key] = task
        return task

    def get_xp_resume(self):
        total = 0
        obtained = 0
        for q in self.quests.values():
            o, t = q.get_xp()
            total += t
            obtained += o
        return obtained, total

    def get_skills_resume(self, avaliable_quests: List[Quest]) -> Tuple[Dict[str, int], Dict[str, int]]:
        total: Dict[str, int] = {}
        obtained: Dict[str, int] = {}
        avaliable_keys = [q.key for q in avaliable_quests]
        for q in self.quests.values():
            reachable = q.key in avaliable_keys
            for t in q.get_tasks():
                for s in t.skills:
                    if s in total:
                        total[s] += t.skills[s]
                        if reachable:
                            obtained[s] += int(t.skills[s] * t.grade/10)
                        else:
                            obtained[s] += 0
                    else:
                        total[s] = t.skills[s]
                        if reachable:
                            obtained[s] = int(t.skills[s] * t.grade/10)
                        else:
                            obtained[s] = 0
                for s in t.qskills:
                    if s in total:
                        total[s] += t.qskills[s]
                        if reachable:
                            obtained[s] += int(t.qskills[s] * t.grade/10)
                        else:
                            obtained[s] += 0
                    else:
                        total[s] = t.qskills[s]
                        if reachable:
                            obtained[s] = int(t.qskills[s] * t.grade/10)
                        else:
                            obtained[s] = 0
        return total, obtained

    # Verificar se todas as quests requeridas existem e adiciona o ponteiro
    # Verifica se todas as quests tem tarefas
    def validate_requirements(self):

        # verify is there are keys repeated between quests, tasks and groups

        keys = [c.key for c in self.clusters.values()] +\
               [k for k in self.quests.keys()] +\
               [k for k in self.tasks.keys()]

        # print chaves repetidas
        for k in keys:
            if keys.count(k) > 1:
                print(f"Chave repetida: {k}")
                exit(1)

        # remove all quests without tasks
        valid_quests = {}
        for k, q in self.quests.items():
            if len(q.get_tasks()) > 0:
                valid_quests[k] = q

        # trim titles
        for q in self.quests.values():
            q.title = q.title.strip()
        for c in self.clusters.values():
            c.title = c.title.strip()

        self.quests = valid_quests

        # verificar se todas as quests requeridas existem e adicionar o ponteiro
        for q in self.quests.values():
            for r in q.requires:
                if r in self.quests:
                    q.requires_ptr.append(self.quests[r])
                else:
                    # print(f"keys: {self.quests.keys()}")
                    print(f"Quest\n{self.filename}:{q.line_number}\n{str(q)}\nrequer {r} que não existe")
                    exit(1)

    def check_cycle(self):
        def dfs(qx, visitedx):
            if len(visitedx) > 0:
                if visitedx[0] == qx.key:
                    print(f"Cycle detected: {visitedx}")
                    exit(1)
            if q.key in visitedx:
                return
            visitedx.append(q.key)
            for r in q.requires_ptr:
                dfs(r, visitedx)

        for q in self.quests.values():
            visited: List[str] = []
            dfs(q, visited)

    def parse_file(self, file):
        self.filename = file
        lines = open(file, encoding="utf-8").read().split("\n")
        active_quest = None
        active_cluster = None

        if len(lines) > 0:
            self.parse_xp(lines[0])

        for line_num, line in enumerate(lines):
            cluster = self.load_cluster(line, line_num)
            if cluster is not None:
                active_cluster = cluster
                continue
            
            quest = self.load_quest(line, line_num)
            if quest is not None:
                active_quest = quest
                if active_cluster is None:
                    key = "Sem Grupo"
                    cluster = Cluster(0, key, key)
                    self.clusters[key] = cluster
                    self.ordered_clusters.append(key)
                    active_cluster = cluster
                quest.cluster = active_cluster.key
                active_cluster.quests.append(quest)
                continue

            task = self.load_task(line, line_num)
            if task is not None:
                
                if active_quest is None:
                    print(f"Task {task.key} não está dentro de uma quest")
                    print(f"{file}:{task.line_number}")
                    print(f"  {task}")
                    exit(1)
                if self.filename is not None:
                    active_quest.add_task(task, self.filename)

        self.clear_empty()

        self.validate_requirements()
        for t in self.tasks.values():
            t.process_link(os.path.dirname(file) + "/")

    def clear_empty(self):

        # apagando quests vazias da lista de quests
        for k in list(self.quests.keys()):
            if len(self.quests[k].get_tasks()) == 0:
                del self.quests[k]

        # apagando quests vazias dos clusters e clusters vazios
        ordered_clusters: List[str] = []
        clusters: Dict[str, Cluster] = {}
        for key in self.ordered_clusters:
            cluster = self.clusters[key]
            quests = [q for q in cluster.quests if len(q.get_tasks()) > 0]
            if len(quests) > 0:
                cluster.quests = quests
                clusters[cluster.key] = cluster
                ordered_clusters.append(cluster.key)

        self.ordered_clusters = ordered_clusters
        self.clusters = clusters

    @staticmethod
    def __is_reachable_quest(q: Quest, cache: Dict[str, bool]):
        if q.key in cache:
            return cache[q.key]

        if len(q.requires_ptr) == 0:
            cache[q.key] = True
            return True
        cache[q.key] = all([r.is_complete() and Game.__is_reachable_quest(r, cache) for r in q.requires_ptr])
        return cache[q.key]

    # def __get_reachable_quests(self):
    #     # cache needs to be reseted before each call
    #     cache: Dict[str, bool] = {}
    #     return [q for q in self.quests.values() if Game.__is_reachable_quest(q, cache)]

    def update_reachable_and_available(self, admin_mode: bool):
        for q in self.quests.values():
            q.set_reachable(False)
        for c in self.clusters.values():
            c.set_reachable(False)

        cache: Dict[str, bool] = {}
        for c in self.clusters.values():
            for q in c.quests:
                if Game.__is_reachable_quest(q, cache):
                    q.set_reachable(True)
                    c.set_reachable(True)

        self.available_quests = []
        self.available_clusters = []
        if admin_mode:
            self.available_quests = [key for key in self.quests.keys()]
            self.available_clusters = [key for key in self.clusters.keys()]
        else:
            self.available_quests = [q.key for q in self.quests.values() if q.is_reachable()]
            self.available_clusters = [c.key for c in self.clusters.values() if c.is_reachable()]


    def __str__(self):
        output = []
        for c in self.clusters.values():
            output.append(str(c))
            for q in c.quests:
                output.append(str(q))
                for t in q.get_tasks():
                    output.append(str(t))
        return "\n".join(output)



class Graph:

    colorlist: List[Tuple[str, str]] = [
            ("aquamarine3", "aquamarine4"),
            ("bisque3", "bisque4"),
            ("brown3", "brown4"),
            ("chartreuse3", "chartreuse4"),
            ("coral3", "coral4"),
            ("cyan3", "cyan4"),
            ("darkgoldenrod3", "darkgoldenrod4"),
            ("darkolivegreen3", "darkolivegreen4"),
            ("darkorchid3", "darkorchid4"),
            ("darkseagreen3", "darkseagreen4"),
            ("darkslategray3", "darkslategray4"),
            ("deeppink3", "deeppink4"),
            ("deepskyblue3", "deepskyblue4"),
            ("dodgerblue3", "dodgerblue4"),
            ("firebrick3", "firebrick4"),
            ("gold3", "gold4"),
            ("green3", "green4"),
            ("hotpink3", "hotpink4"),
            ("indianred3", "indianred4"),
            ("khaki3", "khaki4"),
            ("lightblue3", "lightblue4"),
            ("lightcoral", "lightcoral"),
            ("lightcyan3", "lightcyan4"),
            ("lightgoldenrod3", "lightgoldenrod4"),
            ("lightgreen", "lightgreen"),
            ("lightpink3", "lightpink4"),
            ("lightsalmon3", "lightsalmon4"),
            ("lightseagreen", "lightseagreen"),
            ("lightskyblue3", "lightskyblue4"),
            ("lightsteelblue3", "lightsteelblue4"),
            ("lightyellow3", "lightyellow4"),
            ("magenta3", "magenta4"),
            ("maroon3", "maroon4"),
            ("mediumorchid3", "mediumorchid4"),
            ("mediumpurple3", "mediumpurple4"),
            ("mediumspringgreen", "mediumspringgreen"),
            ("mediumturquoise", "mediumturquoise"),
            ("mediumvioletred", "mediumvioletred"),
            ("mistyrose3", "mistyrose4"),
            ("navajowhite3", "navajowhite4"),
            ("olivedrab3", "olivedrab4"),
            ("orange3", "orange4"),
            ("orangered3", "orangered4"),
            ("orchid3", "orchid4"),
            ("palegreen3", "palegreen4"),
            ("paleturquoise3", "paleturquoise4"),
            ("palevioletred3", "palevioletred4")
            ]

    def __init__(self, game: Game):
        self.game = game
        self.path = "graph.png"
        self.opt = False
        self.reachable = [q.key for q in self.game.quests.values() if q.is_reachable()]
        # self.reachable = [key for key in self.game.quests.keys()]

        self.counts: Dict[str, str] = {}
        for q in self.game.quests.values():
            done = len([t for t in q.get_tasks() if t.is_complete()])
            init = len([t for t in q.get_tasks() if t.in_progress()])
            todo = len([t for t in q.get_tasks() if t.not_started()])
            self.counts[q.key] = f"{done} / {done + init + todo}"

    def set_path(self, path: str):
        self.path = path
        return self

    def set_opt(self, opt: bool):
        self.opt = opt
        return self

    def set_counts(self, counts: Dict[str, str]):
        self.counts = counts
        return self
    
    def set_output(self, output: str):
        self.output = output
        return self

    def info(self, qx: Quest):
        text = f'{qx.title.strip()}'
        if self.reachable is None or self.counts is None:
            return f'"{text}"'
        return f'"{text}\\n{self.counts[qx.key]}"'

    def is_reachable_or_next(self, q: Quest):
        if self.reachable is None:
            return True
        if q.key in self.reachable:
            return True
        for r in q.requires_ptr:
            if r.key in self.reachable:
                return True
        return False

    def generate(self):
        saida = ["digraph diag {", '  node [penwidth=1, style="rounded,filled", shape=box]']

        targets = [q for q in self.game.quests.values()]
        for q in targets:
            token = "->"
            if len(q.requires_ptr) > 0:
                for r in q.requires_ptr:
                    extra = ""
                    if self.reachable is not None:
                        if q.key not in self.reachable and not r.is_complete():
                            extra = "[style=dotted]"
                    saida.append(f"  {self.info(r)} {token} {self.info(q)} {extra}")
            else:
                v = '  "Início"'
                saida.append(f"{v} {token} {self.info(q)}")

        for i, c in enumerate(self.game.clusters.values()):
            # cluster_targets = [q for q in c.quests if self.is_reachable_or_next(q)]
            cluster_targets = [q for q in c.quests]
            for q in cluster_targets:
                if self.opt:
                    if q.opt:
                        fillcolor = "pink"
                    else:
                        fillcolor = "lime"
                else:
                    if c.color is not None:
                        fillcolor = c.color
                    else:
                        fillcolor = self.colorlist[i][0]

                    if q.opt:
                        fillcolor = f'"{fillcolor};0.9:orange"'
                    else:
                        fillcolor = f'"{fillcolor};0.9:lime"'
                shape = "ellipse"
                color = "black"
                width = 1
                if self.reachable is not None:
                    if q.key not in self.reachable:
                        color = "white"
                    else:
                        width = 3
                        color = q.get_grade_color()
                        if color == "g":
                            color = "green"
                        elif color == "r":
                            color = "red"
                        elif color == "y":
                            color = "yellow"
                        elif color == "m":
                            color = "magenta"
                saida.append(f"  {self.info(q)} [shape={shape} color={color} penwidth={width} fillcolor={fillcolor} ]")

        saida.append("}")
        # saida.append("@enduml")
        saida.append("")

        dot_file = os.path.join(os.path.dirname(self.path) + "graph.dot")
        out_file = self.path
        open(dot_file, "w").write("\n".join(saida))

        # if self.graph_ext == ".png":
        subprocess.run(["dot", "-Tpng", dot_file, "-o", out_file])
        # elif self.graph_ext == ".svg":
        #     subprocess.run(["dot", "-Tsvg", dot_file, "-o", out_file])
        # else:
        #     print("Formato de imagem não suportado")


class XP:
    token_level_one = "level_one"
    token_level_mult = "level_mult"
    level_one: int = 100
    level_mult: float = 1.5
    
    def __init__(self, game: Game):
        self.game = game
        self.obtained = 0
        self.avaliable = 0
        self.update()
        self.level = self.get_level()
    
    def update(self):
        self.obtained, self.avaliable = self.game.get_xp_resume()

    def get_level(self) -> int:
        return self.calc_level(self.obtained)

    def get_xp_level_current(self) -> int:
        xp_prev = self.calc_xp(self.level)
        atual = self.obtained - xp_prev
        return atual

    def get_xp_level_needed(self) -> int:
        xp_next = self.calc_xp(self.level + 1)
        xp_prev = self.calc_xp(self.level)
        return xp_next - xp_prev

    def get_xp_total_obtained(self) -> int:
        return self.obtained

    def get_xp_total_available(self) -> int:
        return self.avaliable

    def calc_level(self, xp) -> int:
        level = 1
        while self.calc_xp(level) <= xp:
            level += 1
        return level - 1
    
    def calc_xp(self, level: int) -> int:
        total = 0
        for i in range(level - 1):
            total += self.game.level_one * (int(self.game.level_mult) ** i)
        return int(total)







class ExecutionResult(enum.Enum):
    UNTESTED          = "não_verificado_"
    SUCCESS           = "saída_correta__"
    WRONG_OUTPUT      = "saída_incorreta"
    COMPILATION_ERROR = "erro_compilação"
    EXECUTION_ERROR   = "erro_execução__"

    @staticmethod
    def get_symbol(result) -> Token:
        if result == ExecutionResult.UNTESTED:
            return symbols.neutral
        elif result == ExecutionResult.SUCCESS:
            return symbols.success
        elif result == ExecutionResult.WRONG_OUTPUT:
            return symbols.wrong
        elif result == ExecutionResult.COMPILATION_ERROR:
            return symbols.compilation
        elif result == ExecutionResult.EXECUTION_ERROR:
            return symbols.execution
        else:
            raise ValueError("Invalid result type")

    def __str__(self):
        return self.value

class DiffMode(enum.Enum): # não mude os valores pois são utilizados no json
    SIDE = "side"
    DOWN = "down"

class DiffCount(enum.Enum):
    FIRST = "MODO: APENAS PRIMEIRO ERRO"
    ALL   = "MODO: TODOS OS ERROS"
    QUIET = "MODO: SILENCIOSO"


class IdentifierType(enum.Enum):
    OBI = "OBI"
    MD = "MD"
    TIO = "TIO"
    VPL = "VPL"
    SOLVER = "SOLVER"

class Success(enum.Enum):
    RANDOM = "RANDOM"
    FIXED = "FIXED"


class AppSettings:

    def __init__(self):
        self._rootdir = ""
        self._diff_mode = str(DiffMode.SIDE)
        self._lang_default = ""
        self._last_rep = ""
        self._full_hud = True
        self._use_images = False
        self._use_borders = False
        self._editor = "code"
        self._timeout = 1

    def to_dict(self):
        return self.__dict__
    
    def from_dict(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) and type(getattr(self, key)) == type(value):
                setattr(self, key, value)
        return self
    
    def toggle_hud(self):
        self._full_hud = not self._full_hud

    def has_full_hud(self):
        return self._full_hud
    
    def set_full_hud(self, value: bool):
        self._full_hud = value
        return self

    def toggle_diff(self):
        if self._diff_mode == DiffMode.SIDE.value:
            self._diff_mode = DiffMode.DOWN.value
        else:
            self._diff_mode = DiffMode.SIDE.value

    def toggle_borders(self):
        self._use_borders = not self._use_borders
    
    def toggle_images(self):
        self._use_images = not self._use_images

    def set_rootdir(self, rootdir: str):
        self._rootdir = rootdir
        return self

    def set_diff_mode(self, diff_mode: DiffMode):
        self._diff_mode = str(diff_mode)
        return self

    def set_side_size_min(self, side_size_min: int):
        self._side_size_min = side_size_min
        return self

    def set_lang_default(self, lang_default: str):
        self._lang_default = lang_default
        return self

    def set_last_rep(self, last_rep: str):
        self._last_rep = last_rep
        return self

    def set_borders(self, borders: bool):
        self._use_borders = borders
        return self

    def set_editor(self, editor: str):
        self._editor = editor
        return self

    def set_timeout(self, timeout: int):
        self._timeout = timeout
        return self

    def get_rootdir(self) -> str:
        return self._rootdir

    def get_diff_mode(self) -> DiffMode:
        if self._diff_mode == DiffMode.SIDE.value:
            return DiffMode.SIDE
        return DiffMode.DOWN

    def get_lang_default(self) -> str:
        return self._lang_default

    def get_last_rep(self) -> str:
        return self._last_rep

    def has_images(self) -> bool:
        return self._use_images

    def has_borders(self) -> bool:
        return self._use_borders

    def get_editor(self) -> str:
        return self._editor

    def get_timeout(self) -> int:
        return self._timeout

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Settings:
    def __init__(self):
        self.reps: Dict[str, RepSource] = {}
        self.app = AppSettings()
        self.colors = Colors()

        self.settings_file = ""

    def set_settings_file(self, path: str):
        self.settings_file = path
        return self

    def get_settings_file(self) -> str:
        if self.settings_file is None or self.settings_file == "":
            self.package_name = "tko"
            default_filename = "settings.json"
            self.settings_file = os.path.abspath(default_filename)  # backup for replit, dont remove
        
        if not os.path.exists(self.settings_file):
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        return self.settings_file

    def reset(self):
        self.reps = {}
        self.reps["fup"] = RepSource(url = "https://github.com/qxcodefup/arcade/blob/master/Readme.md")
        self.reps["ed"] = RepSource(url = "https://github.com/qxcodeed/arcade/blob/master/Readme.md")
        self.reps["poo"] = RepSource(url = "https://github.com/qxcodepoo/arcade/blob/master/Readme.md")

        # for key in self.reps:
        #     repdata = self.get_rep_data(key)
        #     repdata.save_data_to_json()

        self.app = AppSettings()
        self.colors = Colors()
        return self

    def __get_old_rep_file_path(self, course: str) -> str:
        return os.path.join(self.app.get_rootdir(), course, ".rep.json")

    def __get_new_rep_file_path(self, course: str) -> str:
        return os.path.join(self.app.get_rootdir(), course, "rep.json")

    def get_rep_source(self, course: str) -> RepSource:
        if course in self.reps:
            return self.reps[course]
        raise Warning(f"Curso {course} não encontrado")

    def get_rep_data(self, course: str) -> RepData:
        old_cfg_file = self.__get_old_rep_file_path(course)
        new_cfg_file = self.__get_new_rep_file_path(course)
        if os.path.exists(old_cfg_file):
            os.rename(old_cfg_file, new_cfg_file)
        
        rep_data = RepData(self.app.get_rootdir(), course, new_cfg_file)
        if os.path.exists(new_cfg_file):
            return rep_data.load_data_from_json()
        return rep_data.load_defaults()
  
    # def to_dict(self) -> Dict[str, Any]:
    #     return {
    #         "reps": {k: v.to_dict() for k, v in self.reps.items()},
    #         "geral": self.app.to_dict()
    #     }
    
    def load_settings(self):
        try:
            settings_file = self.get_settings_file() # assure right loading if value == ""
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.reps = {k: RepSource().from_dict(v) for k, v in data.get("reps", {}).items()}
                self.app = AppSettings().from_dict(data.get("geral", {}))
                self.colors = Colors().from_dict(data.get("colors", {}))
        except (FileNotFoundError, json.decoder.JSONDecodeError) as _e:
            self.reset()
            self.save_settings()
        return self

    # def from_dict(self, data: Dict[str, Any]):
    #     self.reps = {k: RepSource().from_dict(v) for k, v in data.get("reps", {}).items()}
    #     self.app = AppSettings().from_dict(data.get("geral", {}))
    #     return self

    def check_rootdir(self):
        if self.app._rootdir != "":
            return
        term_print(Sentence().add("Pasta padrão para download de arquivos ").addf("r", "precisa").add(" ser definida."))
        here_cwd = os.getcwd()
        qxcode = os.path.join(os.path.expanduser("~"), "qxcode")

        while True:
            term_print(Sentence().addf("r", "1").add(" - ").add(here_cwd))
            term_print(Sentence().addf("r", "2").add(" - ").add(qxcode))
            term_print(Sentence().addf("r", "3").add(" - ").add("Outra pasta"))
            term_print(Sentence().add("Default ").addf("r", "1").add(": "), end="")
            op = input()
            if op == "":
                op = "1"
            if op == "1":
                home_qxcode = here_cwd
                break
            if op == "2":
                home_qxcode = qxcode
                break
            if op == "3":
                term_print(Sentence().addf("y", "Navegue até o diretório desejado e execute o tko novamente."))
                exit(1)

        if not os.path.exists(home_qxcode):
            os.makedirs(home_qxcode)
        term_print("Pasta padrão para download de arquivos foi definida em: " + home_qxcode)
        term_print(Report.centralize("", "-"))
        self.app._rootdir = home_qxcode
        self.save_settings();
        return self
    
    def check_rep_alias(self, rep_alias: str):
        if rep_alias == "__ask":
            last = self.app.get_last_rep()
            if last != "" and last in self.reps:
                rep_alias = last
            else:
                print("Escolha um dos repositórios para abrir:")
                options: Dict[int, str] = {}
                for i, alias in enumerate(self.reps, start=1):
                    term_print(Sentence().addf("r", str(i)).add(f" - {alias}"))
                    options[i] = alias
                while True:
                    try:
                        print("Digite o número do repositório desejado: ", end="")
                        index = int(input())
                        if index in options:
                            rep_alias = options[index]
                            self.app.set_last_rep(rep_alias)
                            self.save_settings()
                            break
                    except ValueError:
                        pass
                    print("Digite um número válido")
        return rep_alias
    
    def save_settings(self):
        file = self.get_settings_file()
        value = {
            "reps": {k: v.to_dict() for k, v in self.reps.items()},
            "geral": self.app.to_dict(),
            "colors": self.colors.to_dict()
        }
        with open(file, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=4)
        return self

    def __str__(self):
        output = ["Repositories:"]
        maxlen = max([len(key) for key in self.reps])
        for key in self.reps:
            prefix = f"- {key.ljust(maxlen)}"
            if self.reps[key].file and self.reps[key].url:
                output.append(f"{prefix} : dual   : {self.reps[key].url} ; {self.reps[key].file}")
            elif self.reps[key].url:
                output.append(f"{prefix} : remote : {self.reps[key].url}")
            else:
                output.append(f"{prefix} : local  : {self.reps[key].file}")
        return "\n".join(output)


class Border:
    def __init__(self, app: AppSettings):
        self.app = app

    def has_borders(self):
        return self.app.has_borders()

    def border(self, color: str, data: str):
        return Sentence().add(self.roundL(color)).addf(color, data).add(self.roundR(color))

    def border_sharp(self, color: str, data: str):
        return Sentence().add(self.sharpL(color)).addf(color, data).add(self.sharpR(color))

    def roundL(self, color: str) -> Token:
        return Token("", color.lower()) if self.has_borders() else Token(" ", color)

    def roundR(self, color: str) -> Token:
        return Token("", color.lower()) if self.has_borders() else Token(" ", color)

    def sharpL(self, color: str) -> Token:
        return Token("", color.lower()) if self.has_borders() else Token(" ", color)

    def sharpR(self, color: str):
        return Token("", color.lower()) if self.has_borders() else Token(" ", color)

    def build_bar(self, text: str, percent: float, length: int, fmt_true: str = "/kC",
                  fmt_false: str = "/kY", round=True) -> Sentence:
        if round and (len(text) >= length - 2):
            text = " " + text

        if length > len(text):
            prefix = (length - len(text)) // 2
            suffix = length - len(text) - prefix
            text = " " * prefix + text + " " * suffix
        elif length < len(text):
            text = text[:length]
        
        full_line = text
        done_len = int(percent * length)
        xp_bar = Token(full_line[:done_len], fmt_true) + Token(full_line[done_len:], fmt_false)
            
        if round:
            xp_bar.data[0] = self.roundL(xp_bar.data[0].fmt)
            xp_bar.data[-1] = self.roundR(xp_bar.data[-1].fmt)
        return xp_bar

    def get_flag_sentence(self, flag: Flag, pad: int = 0, button_mode: bool = True) -> Sentence:
        char = flag.get_keycode()
        text = flag.get_name()
        color = "M" 
        symbol = symbols.neutral
        if len(flag.get_values()) > 0:
            color = "G" if flag.is_true() else "Y"
            symbol = symbols.success if flag.is_true() else symbols.failure
        if not button_mode:
            color = color.lower()
        extra = Sentence()
        filler = " "
        if pad > 2:
            extra.addf(color, (pad - 2 - len(text)) * filler)

        mid = Sentence().addf(color, symbol.text).addf(color, " ").addf(color, text).add(extra).addf(color, f"[{char}]")
        if button_mode:
            middle = Sentence().add(self.roundL(color)).add(mid).add(self.roundR(color))
        else:
            middle = Sentence().add(" ").add(mid).add(" ")
        return middle





class Entry:
    def __init__(self, obj: Union[Task, Quest, Cluster], sentence: Sentence):
        self.obj = obj
        self.sentence = sentence

    def get(self):
        return self.sentence

class TaskTree:

    def __init__(self, settings: Settings, game: Game, rep: RepData):
        self.settings = settings
        self.app = settings.app
        self.game = game
        self.rep = rep
        self.style = Border(settings.app)
        self.colors = settings.colors
        self.items: List[Entry] = []
        self.index_selected = 0
        self.index_begin = 0
        self.max_title = 0
        self.search_text = ""
        self.in_focus = True
        self.load_from_rep()
        self.update_tree(admin_mode=Flags.admin.is_true(), first_loop=True)
        self.reload_sentences()

    def set_focus(self, focus: bool):
        self.in_focus = focus

    def load_from_rep(self):
        self.new_items: List[str] = [v for v in self.rep.get_new_items()]
        self.expanded: List[str] = [v for v in self.rep.get_expanded()]
        self.index_selected = self.rep.get_index()

        tasks = self.rep.get_tasks()
        for key, serial in tasks.items():
            if key in self.game.tasks:
                self.game.tasks[key].load_from_db(serial)

    def save_on_rep(self):
        self.rep.set_expanded(self.expanded)
        self.rep.set_new_items([x for x in set(self.new_items)])
        self.rep.set_index(self.index_selected)
        tasks = {}
        for t in self.game.tasks.values():
            if not t.is_db_empty():
                tasks[t.key] = t.save_to_db()
        self.rep.set_tasks(tasks)


    def update_tree(self, admin_mode: bool, first_loop: bool = False):
        if not admin_mode:
            old_reachable = self.game.available_clusters + self.game.available_quests

        self.game.update_reachable_and_available(admin_mode)
            
        if not admin_mode:
            available_keys = self.game.available_quests + self.game.available_clusters
            for key in self.expanded:
                if key not in available_keys:
                    self.expanded.remove(key)
            if not first_loop:
                for key in available_keys:
                    if key not in old_reachable and key not in self.new_items:
                        self.new_items.append(key)

        # remove expanded items from new
        self.new_items = [item for item in self.new_items if item not in self.expanded]

    def update_max_title(self):
        min_value = 20
        items = []
        for c in self.game.clusters.values():
            if c.key in self.game.available_clusters:
                items.append(len(c.title))
                if c.key in self.expanded:
                    for q in [q for q in c.quests if q.key in self.game.available_quests]:
                        items.append(len(q.title) + 2)
                        if q.key in self.expanded:
                            for t in q.get_tasks():
                                items.append(len(t.title) + 6)
        self.max_title = max(items)
        if self.max_title < min_value:
            self.max_title = min_value

    def str_task(self, focus_color: str, t: Task, lig_cluster: str, lig_quest: str, quest_reachable: bool, min_value=1) -> Sentence:
        # downloadable_in_focus = False
        rootdir = self.app._rootdir
        down_symbol = Token(" ")
        in_focus = focus_color != ""
        down_symbol = symbols.cant_download
        rep_dir = os.path.join(self.app.get_rootdir(), self.rep.alias)
        if t.is_downloadable() and rootdir != "":
            if t.is_downloaded_for_lang(rep_dir, self.rep.get_lang()):
                down_symbol = symbols.downloaded
                # if in_focus:
                #     downloadable_in_focus = True
            else:
                down_symbol = symbols.to_download

        color_aval = "" if quest_reachable else "r"

        output = Sentence()
        output.add(" ").addf(color_aval, lig_cluster)
        output.add(" ")
        output.addf(color_aval, lig_quest)
        output.add(down_symbol)
        output.add(" ")
        output.add(t.get_grade_symbol(min_value))

        if in_focus:
            output.add(self.style.roundL(focus_color))
        else:
            output.add(" ")

        color = ""
        if in_focus:
            color = "k" + focus_color

        done = color + "g"
        todo = color
        perc = t.test_progress
        output.add(self.style.build_bar(t.title, perc / 100, len(t.title), done, todo, round=False))
        # output.addf(color, t.title)

        if in_focus:
            output.add(self.style.roundR(focus_color))
        else:
            output.add(" ")


        if Flags.reward.is_true():
            xp = ""
            for s, v in t.skills.items():
                xp += f" +{s}:{v}"
            output.addf(self.colors.task_skills, xp)
            
        return output

    def str_quest(self, has_kids: bool, focus_color: str, q: Quest, lig: str) -> Sentence:
        con = "━─"
        if q.key in self.expanded and has_kids:
            con = "─┯"

        color_reachable = "" if q.is_reachable() else "r"
        output: Sentence = Sentence().addf(color_reachable, " " + lig + con)

        in_focus = focus_color != ""
        if in_focus:
            output.add(self.style.roundL(focus_color))
        else:
            output.add(" ")

        color = ""
        if in_focus:
            color = "k" + focus_color

        title = q.title
        title = title.ljust(self.max_title - 2, ".")

        done = color + self.colors.task_text_done
        todo = color + self.colors.task_text_todo
        output.add(self.style.build_bar(title, q.get_percent() / 100, len(title), done, todo, round=False))

        if in_focus:
            output.add(self.style.roundR(focus_color))
        else:
            output.add(" ")

        if Flags.percent.is_true():
            output.add(" ").add(q.get_resume_by_percent())
        else:
            output.add(" ").add(q.get_resume_by_tasks())

        if Flags.minimum.is_true():
            output.add(" ").add(q.get_requirement())

        if Flags.reward.is_true():
            xp = ""
            for s, v in q.skills.items():
                xp += f" +{s}:{v}"
            output.addf(self.colors.task_skills, " " + xp)

        if q.key in self.new_items:
            output.addf(self.colors.task_new, " [new]")

        return output


    def str_cluster(self, has_kids: bool, focus_color: str, cluster: Cluster) -> Sentence:
        output: Sentence = Sentence()
        opening = "━─"
        if cluster.key in self.expanded and has_kids:
            opening = "─┯"
        color_reachable = "" if cluster.is_reachable() else "r"
        output.addf(color_reachable, opening)

        color = ""
        if focus_color != "":
            color = "k" + focus_color
        title = cluster.title

        title = cluster.title.ljust(self.max_title, ".")
        if focus_color != "":
            output.add(self.style.roundL(focus_color))
        else:
            output.add(" ")

        done = color + self.colors.task_text_done
        todo = color + self.colors.task_text_todo

        output.add(self.style.build_bar(title, cluster.get_percent() / 100, len(title), done, todo, round=False))

        if focus_color != "":
            output.add(self.style.roundR(focus_color))
        else:
            output.add(" ")


        if Flags.percent.is_true():
            output.add(" ").add(cluster.get_resume_by_percent())
        else:
            output.add(" ").add(cluster.get_resume_by_quests())
        if cluster.key in self.new_items:
            output.addf(self.colors.task_new, " [new]")

        return output


    # def add_in_search(self, item: Any, sentence: Sentence) -> bool:
    #     if self.search_text == "":
    #         self.items.append(Entry(item, sentence))
    #         return True
        
    #     matcher = SearchAsc(self.search_text)
    #     pos = matcher.find(sentence.get_text())
    #     found = pos != -1
    #     if found:
    #         for i in range(pos, pos + len(self.search_text)):
    #             sentence.data[i].fmt = "Y"

    #     if isinstance(item, Task):
    #         if found:
    #             self.items.append(Entry(item, sentence))
    #             return True
    #     elif isinstance(item, Quest):
    #         if found:
    #             self.items.append(Entry(item, sentence))
    #             return True
    #         for t in item.get_tasks():
    #             if matcher.inside(t.title):
    #                 self.items.append(Entry(item, sentence))
    #                 return True
    #     elif isinstance(item, Cluster):
    #         cluster: Cluster = item
    #         if matcher.inside(cluster.title):
    #             self.items.append(Entry(cluster, sentence))
    #             return True
    #         for q in cluster.quests:
    #             if matcher.inside(q.title):
    #                 self.items.append(Entry(item, sentence))
    #                 return True
    #             for t in q.get_tasks():
    #                 if matcher.inside(t.title):
    #                     self.items.append(Entry(item, sentence))
    #                     return True
    #     return False

    def get_focus_color(self, item: Union[Quest, Cluster], index: int) -> str:
        if index != self.index_selected or not self.in_focus:
            return ""
        if not item.is_reachable() and not Flags.admin.is_true():
            return "R"
        return self.colors.focused_item

    def filter_by_search(self) -> Set[str]:
        matches: Set[str] = set()
        search = SearchAsc(self.search_text)
        for cluster in self.game.clusters.values():
            if search.inside(cluster.title):
                matches.add(cluster.key)
            for quest in cluster.quests:
                if search.inside(quest.title):
                    matches.add(cluster.key)
                    matches.add(quest.key)
                for task in quest.get_tasks():
                    if search.inside(task.title):
                        matches.add(cluster.key)
                        matches.add(quest.key)
                        matches.add(task.key)
        return matches

    def try_add(self, filtered, matcher, item, sentence):
        if self.search_text == "":
            self.items.append(Entry(item, sentence))
            return True
        if item.key in filtered:
            pos = matcher.find(sentence.get_text())
            found = pos != -1
            if found:
                for i in range(pos, pos + len(self.search_text)):
                    sentence.data[i].fmt = "Y"
            self.items.append(Entry(item, sentence))
            return True
        return False

    def reload_sentences(self):
        self.update_max_title()
        index = 0
        self.items = []
        available_quests = self.game.available_quests
        available_clusters = self.game.available_clusters

        filtered = self.filter_by_search()
        matcher = SearchAsc(self.search_text)

        clusters = [self.game.clusters[key] for key in available_clusters if key in filtered]
        for cluster in clusters:
            quests = [q for q in cluster.quests if q.key in available_quests if q.key in filtered]
            focus_color = self.get_focus_color(cluster, index)
            sentence = self.str_cluster(len(quests) > 0, focus_color, cluster)

            if self.try_add(filtered, matcher, cluster, sentence):
                index += 1

            if cluster.key not in self.expanded:  # adicionou o cluster, mas não adicione as quests
                continue

            for q in quests:
                tasks =[t for t in q.get_tasks() if t.key in filtered]
                lig = "├" if q != quests[-1] else "╰"
                focus_color = self.get_focus_color(q, index)
                sentence = self.str_quest(len(tasks) > 0, focus_color, q, lig)

                # self.items.append(Entry(q, sentence))
                if self.try_add(filtered, matcher, q, sentence):
                    index += 1
                if q.key in self.expanded:
                    for t in tasks:
                        ligc = "│" if q != quests[-1] else " "
                        ligq = "├ " if t != tasks[-1] else "╰ "
                        min_value = 7 if q.tmin is None else q.tmin
                        focus_color = self.get_focus_color(q, index)
                        sentence = self.str_task(focus_color, t, ligc, ligq, q.is_reachable(), min_value)
                        if self.try_add(filtered, matcher, t, sentence):
                            index += 1

        if self.index_selected >= len(self.items):
            self.index_selected = len(self.items) - 1


    def process_collapse(self):
        if any([q in self.expanded for q in self.game.available_quests]):
            self.expanded = [key for key in self.expanded if key not in self.game.available_quests]
        else:
            self.expanded = []

    def process_expand(self):
        # if any cluster outside expanded
        expand_clusters = False
        for ckey in self.game.available_clusters:
            if ckey not in self.expanded:
                expand_clusters = True
        if expand_clusters:
            for ckey in self.game.available_clusters:
                if ckey not in self.expanded:
                    self.expanded.append(ckey)
        else:
            for qkey in self.game.available_quests:
                if qkey not in self.expanded:
                    self.expanded.append(qkey)


    def mass_mark(self):
        obj = self.items[self.index_selected].obj
        if isinstance(obj, Cluster):
            cluster: Cluster = obj
            if cluster.key not in self.expanded:
                self.expanded.append(cluster.key)
                return
            full_open = True
            for q in cluster.quests:
                if q.key in self.game.available_quests and q.key not in self.expanded:
                    self.expanded.append(q.key)
                    full_open = False
            if not full_open:
                return

            value = None
            for q in obj.quests:
                for t in q.get_tasks():
                    if value is not None:
                        t.set_grade(value)
                    else:
                        value = 10 if t.grade < 10 else 0
                        t.set_grade(value)
        elif isinstance(obj, Quest):
            if obj.key not in self.expanded:
                self.expanded.append(obj.key)
            else:
                value = None
                for t in obj.get_tasks():
                    if value is not None:
                        t.set_grade(value)
                    else:
                        value = 10 if t.grade < 10 else 0
                        t.set_grade(value)
        else:
            obj.set_grade(10 if obj.grade < 10 else 0)

    def set_grade(self, grade: int):
        obj = self.items[self.index_selected].obj
        if isinstance(obj, Task):
            obj.set_grade(grade)

    def inc_grade(self):
        obj = self.items[self.index_selected].obj
        if isinstance(obj, Task):
            grade = obj.grade + 1
            if grade == 11:
                grade = 10
            obj.set_grade(grade)
        else:
            self.unfold(obj)

    
    def dec_grade(self):
        obj = self.items[self.index_selected].obj
        if isinstance(obj, Task):
            grade = obj.grade - 1
            if grade == -1:
                grade = 0
            obj.set_grade(grade)
        else:
            self.fold(obj)

    def arrow_right(self):
        obj = self.items[self.index_selected].obj
        if isinstance(obj, Cluster):
            if not self.unfold(obj):
                self.index_selected += 1
        elif isinstance(obj, Quest):
            if not self.unfold(obj):
                while True:
                    self.index_selected += 1
                    obj = self.items[self.index_selected].obj
                    if isinstance(obj, Cluster) or isinstance(obj, Quest):
                        break
                    if self.index_selected == len(self.items) - 1:
                        break
        elif isinstance(obj, Task):
            while True:
                obj = self.items[self.index_selected].obj
                if isinstance(obj, Quest) or isinstance(obj, Cluster):
                    break
                if self.index_selected == len(self.items) - 1:
                    break
                self.index_selected += 1

    def arrow_left(self):
        obj = self.items[self.index_selected].obj
        if isinstance(obj, Quest):
            if not self.fold(obj):
                while True:
                    if self.index_selected == 0:
                        break
                    self.index_selected -= 1
                    obj = self.items[self.index_selected].obj
                    if isinstance(obj, Cluster) or isinstance(obj, Quest) and obj.key in self.expanded:
                        break
                    if self.index_selected == 0:
                        break
        elif isinstance(obj, Cluster):
            if obj.key in self.expanded:
                self.expanded.remove(obj.key)
                for q in obj.quests:
                    try:
                        self.expanded.remove(q.key)
                    except ValueError:
                        pass
            else:
                while True:
                    if self.index_selected == 0:
                        break
                    self.index_selected -= 1
                    obj = self.items[self.index_selected].obj
                    if isinstance(obj, Cluster) or isinstance(obj, Quest):
                        break
                    if self.index_selected == 0:
                        break
        elif isinstance(obj, Task):
            while True:
                obj = self.items[self.index_selected].obj
                if isinstance(obj, Quest):
                    break
                self.index_selected -= 1

    def unfold(self, obj: Union[Task, Quest, Cluster]) -> bool:
        if isinstance(obj, Quest) or isinstance(obj, Cluster):
            if obj.key not in self.expanded:
                self.expanded.append(obj.key)
                return True
        return False

    def fold(self, obj: Union[Task, Quest, Cluster]) -> bool:
        if isinstance(obj, Quest) or isinstance(obj, Cluster):
            if obj.key in self.expanded:
                self.expanded.remove(obj.key)
                return True
        return False

    def toggle(self, obj: Union[Quest, Cluster]):
            if not self.fold(obj):
                self.unfold(obj)

    def get_senteces(self, dy):
        if len(self.items) < dy:
            self.index_begin = 0
        else:
            if self.index_selected < self.index_begin:  # subiu na tela
                self.index_begin = self.index_selected
            elif self.index_selected >= dy + self.index_begin:  # desceu na tela
                self.index_begin = self.index_selected - dy + 1

        sentences: List[Sentence] = []
        for i in range(self.index_begin, len(self.items)):
            sentences.append(self.items[i].sentence)
        return sentences

    def get_selected(self):
        return self.items[self.index_selected].obj

    def move_up(self):
        self.index_selected = max(0, self.index_selected - 1)

    def move_down(self):
        self.index_selected = min(len(self.items) - 1, self.index_selected + 1)



class Search:
    def __init__(self, tree: TaskTree, fman: FloatingManager):
        self.tree = tree
        self.game = tree.game
        self.fman = fman
        self.search_mode: bool = False
        self.backup_expanded: List[str] = []
        self.backup_index_selected = 0
        self.backup_admin_mode = False

    def toggle_search(self):
        self.search_mode = not self.search_mode
        if self.search_mode:
            self.backup_expanded = [v for v in self.tree.expanded]
            self.backup_index_selected = self.tree.index_selected
            self.backup_admin_mode = Flags.admin.is_true()
            self.tree.update_tree(admin_mode=True)
            self.tree.process_expand()
            self.tree.process_expand()
            self.fman.add_input(Floating(">v").warning().put_text("Digite o texto\nVavegue até o elemnto desejado\ne aperte Enter"))
    
    def finish_search(self):
        self.search_mode = False
        unit = self.tree.get_selected()
        self.tree.index_selected = 0
        self.tree.search_text = ""
        if self.backup_admin_mode == False:
            self.tree.update_tree(admin_mode=False)
        self.tree.reload_sentences()
    
        found = False
        for i, item in enumerate(self.tree.items):
            if item.obj == unit:
                self.tree.index_selected = i
                found = True
                break

        if not found:
            self.fman.add_input(Floating(">v").warning().put_text("Elemento não acessível no modo normal.\nEntrando no modo Admin\npara habilitar acesso"))
            Flags.admin.toggle()
            self.tree.update_tree(True)
            self.tree.reload_sentences()
        
        self.tree.process_collapse()
        self.tree.process_collapse()

        if isinstance(unit, Task):
            for cluster_key in self.game.available_clusters:
                cluster = self.game.clusters[cluster_key]
                for quest in cluster.quests:
                    for task in quest.get_tasks():
                        if task == unit:
                            self.tree.expanded = [cluster.key, quest.key]
        elif isinstance(unit, Quest):
            for cluster_key in self.game.available_clusters:
                cluster = self.game.clusters[cluster_key]
                for quest in cluster.quests:
                    if quest == unit:
                        self.tree.expanded = [cluster.key]
        self.tree.reload_sentences()
        for i, item in enumerate(self.tree.items):
            if item.obj == unit:
                self.tree.index_selected = i
                break


    def process_search(self, key):
        if key == 27:
            self.search_mode = False
            self.tree.search_text = ""
            self.tree.expanded = [v for v in self.backup_expanded]
            self.tree.index_selected = self.backup_index_selected
        elif key == ord("\n"):
            self.finish_search()
    
        elif key == curses.KEY_UP:
            self.tree.move_up()
        elif key == curses.KEY_DOWN:
            self.tree.move_down()
        elif key == 127 or key == 263 or key == 330:
            self.tree.search_text = self.tree.search_text[:-1]
        elif key >= 32 and key < 127:
            self.tree.search_text += chr(key).lower()



class Opener:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.fman: Optional[FloatingManager] = None
        self.folders: List[str] = []
        self.language: str = ""

    def set_fman(self, fman: FloatingManager):
        self.fman = fman
        return self
    
    def set_target(self, folders: List[str]):
        self.folders = folders
        return self

    def set_language(self, language: str):
        self.language = language
        return self

    def open_files(self, files_to_open: List[str]):
        files_to_open = list(set(files_to_open))

        cmd = self.settings.app.get_editor()
        folder = os.path.dirname(os.path.abspath(files_to_open[0]));
        aviso = (Floating("v>")
                .warning()
                .put_sentence(Sentence().add("Pasta: ").addf("g", folder).add(" "))
                .put_text("Abrindo arquivos com o comando")
                )
        files = [os.path.basename(path) for path in files_to_open]
        aviso.put_sentence(Sentence().addf("g", f"{cmd}").add(" ").addf("g", " ".join(files)).add(" "))
        self.send_floating(aviso)
        fullcmd = "{} {}".format(cmd, " ".join(files_to_open))
        outfile = tempfile.NamedTemporaryFile(delete=False)
        subprocess.Popen(fullcmd, stdout=outfile, stderr=outfile, shell=True)

    def send_floating(self, Floating: Floating):
        if self.fman is not None:
            self.fman.add_input(Floating)

    def load_drafs(self, folder: str) -> List[str]:
        files = os.listdir(folder)
        files_to_open = []
        for f in files:
            allowed = [self.language]
            if self.language == "c" or self.language== "cpp":
                allowed.append("h")
                allowed.append("hpp")
            if not f.endswith(tuple(allowed)):
                continue
            files_to_open.append(os.path.join(folder, f))
        return files_to_open

    @staticmethod
    def try_add(files_to_open: List[str], folder: str, file: str):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            files_to_open.append(path)

    def load_folder(self, folder: str):
        files_to_open: List[str] = []
        Opener.try_add(files_to_open, folder, "Readme.md")
        # Opener.try_add(files_to_open, folder, "cases.tio")
        files_to_open += self.load_drafs(folder)
        return files_to_open

    def load_folders_and_open(self):
        files_to_open: List[str] = []
        for folder in self.folders:
            files_to_open += self.load_folder(folder)
        if len(files_to_open) != 0:
            self.open_files(files_to_open)

    def __call__(self):
        self.load_folders_and_open()

def empty_fn():
    pass

class ConfigItem:
    def __init__(self, flag: Flag, fn: Callable[[], None], sentence: Sentence = Sentence() ):
        self.flag = flag
        self.fn: Callable[[], None] = fn
        self.sentence = sentence


class Config:
    def __init__(self, settings: Settings, rep: RepData, flagsman: FlagsMan, fman: FloatingManager):
        self.index: int = 0
        self.flagsman = flagsman
        self.border = Border(settings.app)
        self.gen_graph: bool = False
        self.app = settings.app
        self.colors = settings.colors
        self.fman = fman
        self.rep = rep
        self.enabled = False
        self.size = len(self.get_elements())

    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False

    def activate_selected(self):
        elements = self.get_elements()
        chosen = elements[self.index]
        chosen.fn()

    def move_down(self):
        self.index += 1
        if self.index == self.size:
            self.index = 0

    def move_up(self):
        self.index -= 1
        if self.index == -1:
            self.index = self.size - 1

    def mark_focused(self, index, elem: Flag) -> Sentence:
        pad = 14 if index == self.index else 14
        sentence = self.border.get_flag_sentence(elem, pad)

        if index == self.index and self.enabled:
            focus = self.colors.focused_item
            return sentence
        return Sentence("    ").add(sentence)

    def graph_toggle(self):
        self.gen_graph = not self.gen_graph

    def get_elements(self) -> List[ConfigItem]:
        elements: List[ConfigItem] = []
        for flag in self.flagsman.left:
            item = ConfigItem(flag, FlagFunctor(flag))
            elements.append(item)
        border_values = ["1" if self.app.has_borders() else "0"]
        graph_values = ["1" if self.gen_graph else "0"]
        images_values = ["1" if self.app.has_images() else "0"]
        bordas = Flag().set_name("Bordas").set_keycode("B").set_values(border_values).set_description("Ativa as bordas se a fonte tiver suporte    ").set_bool()
        elements.append(ConfigItem(bordas, self.app.toggle_borders))
        grafo = Flag().set_name("Grafo").set_keycode("G").set_values(graph_values)   .set_description("Ativa a geração do grafo do repositório     ").set_bool()
        elements.append(ConfigItem(grafo, self.graph_toggle))
        images = Flag().set_name("Imagens").set_keycode("I").set_values(images_values)    .set_description("Mostra imagens de abertura e sucesso        ").location("left")
        elements.append(ConfigItem(images, self.app.toggle_images))
       
        language = Flag().set_name("Linguagem").set_values([]).set_keycode("L")      .set_description("Muda a linguagem de download dos rascunhos  ")
        elements.append(ConfigItem(language, lambda: self.set_language(False)))

        if Flags.config.is_true():
            for i in range(len(elements)):
                elements[i].sentence = self.mark_focused(i, elements[i].flag)
        return elements

    def set_language(self, only_if_empty=True):
        if only_if_empty and self.rep.get_lang() != "":
            return

        def back(value):
            self.rep.set_lang(value)
            self.rep.save_data_to_json()
            self.fman.add_input(
                Floating()
                .put_text("")
                .put_text("Linguagem alterada para " + value)
                .put_text("")
                .warning()
            )

        self.fman.add_input(
            Floating()
            .put_text("")
            .put_text("Escolha a extensão default para os rascunhos")
            .put_text("")
            .put_text("Selecione e tecle Enter.")
            .put_text("")
            .set_options(languages_avaliable)
            .answer(back)
        )



class Gui:

    def __init__(self, tree: TaskTree, flagsman: FlagsMan, fman: FloatingManager):
        self.rep = tree.rep
        self.game = tree.game
        self.tree = tree
        self.flagsman = flagsman
        self.fman = fman
        self.settings = tree.settings
        self.search = Search(tree=self.tree, fman=self.fman)
        self.style: Border = Border(self.settings.app)
        self.config = Config(self.settings, self.rep, self.flagsman, self.fman)
        self.colors = self.settings.colors

        self.app = Settings().app
        self.wrap_size = Sentence(" ").join(self.build_bottom_array()).len()

    def get_help_others_after(self):
        color = "Y" if self.tree.in_focus else "W"
        help_others_after: List[Sentence] = [
            Sentence() + RToken(color, f"{GuiActions.baixar} [{GuiKeys.down_task}]"),
            Sentence() + RToken("Y", f"{GuiActions.navegar} [wasd]")
        ]
        return help_others_after

    def get_help_basic(self):
        color = "Y" if self.tree.in_focus else "W"
        help_basic: List[Sentence] = [
            Sentence() + RToken(color, f"{GuiActions.pesquisar}[{GuiKeys.pesquisar}]"),
            Sentence() + RToken(color, f"{GuiActions.marcar} {GuiKeys.inc_grade}{GuiKeys.dec_grade}"),
        ]
        return help_basic

    def get_help_fixed(self):
        color = "C" if self.tree.in_focus else "W"
        help_fixed: List[Sentence] = [
            Sentence() + RToken("C", f" {GuiActions.sair}  [{GuiKeys.key_quit}]"),
            Sentence() + RToken(color, f"{GuiActions.editar} [{GuiKeys.edit}]"),
            Sentence() + RToken("G", f"{GuiActions.ativar} [↲]"),
        ]
        return help_fixed

    def get_help_others_before(self):
        color = "Y" if self.tree.in_focus else "W"
        help_others_before: List[Sentence] = [
            Sentence() + RToken("Y", f" {GuiActions.ajuda} [{GuiKeys.key_help}]"),
            Sentence() + RToken(color, f"{GuiActions.github} [{GuiKeys.github_open}]"),
        ]
        return help_others_before

    @staticmethod
    def disable_on_resize():
        _, cols = Fmt.get_size()
        if cols < 50 and Flags.skills.is_true() and Flags.config.is_true():
            Flags.skills.toggle()
        elif cols < 30 and Flags.skills.is_true():
            Flags.skills.toggle()
        elif cols < 35 and Flags.config.is_true():
            Flags.config.toggle()


    def show_main_bar(self, frame: Frame):
        top = Sentence()
        if self.two_column_mode() and self.app.has_full_hud() and not Flags.config.is_true():
            top.add(self.style.get_flag_sentence(Flags.config)).add(" ")

        alias_color = "R"
        top.add(self.style.border(alias_color, self.rep.alias.upper()))
        if Flags.admin.is_true():
            color = "W" if Flags.admin.is_true() else "K"
            top.add(self.style.border(color, "ADMIN"))
        top.add(self.style.border("G", self.rep.get_lang().upper()))

        if self.two_column_mode() and self.app.has_full_hud() and not Flags.config.is_true():
            top.add(" ").add(self.style.get_flag_sentence(Flags.skills))
        half = top.len() // 2
        x = frame.get_x()
        dy, dx = Fmt.get_size()
        full = Sentence().add("─" * ((dx//2) - x - 2 - half)).add(top)
        frame.set_header(full, "<")
        
        if self.two_column_mode() and not Flags.config.is_true():
            elems = self.build_bottom_array()
            line_up = Sentence(" ").join(elems[0 : 2] + elems[-2:])
            half = line_up.len() // 2
            _, adx = Fmt.get_size()
            if adx % 2 == 1:
                adx += 1 
            x = frame.get_x()
            full = Sentence().add("─" * ((adx//2) - x - 2 - half)).add(line_up)
            frame.set_footer(full, "<")
        frame.draw()

        dy, dx = frame.get_inner()
        for y, sentence in enumerate(self.tree.get_senteces(dy)):
            if sentence.len() > dx:
                sentence.trim_end(dx - 3)
                sentence.addf("r", "...")
            frame.write(y, 0, sentence)

    def show_skills_bar(self, frame_xp):
        dy, dx = frame_xp.get_inner()
        xp = XP(self.game)
        total_perc = int(
            100 * (xp.get_xp_total_obtained() / xp.get_xp_total_available())
        )
        if Flags.percent.is_true():
            text = f" XPTotal:{total_perc}%"
        else:
            text = f" XPTotal:{xp.get_xp_total_obtained()}"

        done = self.colors.main_bar_done + "/"
        todo = self.colors.main_bar_todo + "/"
        total_bar = self.style.build_bar(text, total_perc / 100, dx - 2, done, todo)
        frame_xp.set_header(Sentence().addf("/", "Skills"), "^", "{", "}")
        frame_xp.set_footer(Sentence().add(" ").add(self.app._rootdir).add(" "), "^")
        frame_xp.draw()

        total, obt = self.game.get_skills_resume([self.game.quests[key] for key in self.game.available_quests])
        elements: List[Sentence] = []
        for skill, value in total.items():
            if Flags.percent.is_true():
                text = f"{skill}:{int(100 * obt[skill] / value)}%"
            else:
                text = f"{skill}:{obt[skill]}/{value}"
            perc = obt[skill] / value
            done = self.colors.progress_skill_done + "/"
            todo = self.colors.progress_skill_todo + "/"
            skill_bar = self.style.build_bar(text, perc, dx - 2, done, todo)
            elements.append(skill_bar)
            
        elements.append(total_bar)

        line_breaks = dy - len(elements)
        for skill_bar in elements:
            frame_xp.print(1, skill_bar)
            if line_breaks > 0:
                line_breaks -= 1
                frame_xp.print(1, Sentence())

    def show_config_bar(self, frame: Frame):
        frame.set_header(Sentence().addf("/", "Config"), "^", "{", "}")
        frame.draw()
        elements = self.config.get_elements()
        dy, dx = frame.get_inner()
        y = frame.get_y()
        lines, cols = Fmt.get_size()
        
        index = 0
        delta = 0
        if len(elements) > dy and self.config.index > dy - 2:
            delta = self.config.index - dy + 2
        elements = elements[delta:]
        target = self.config.index - delta

        while index < len(elements):
            item = elements[index]
            frame.print(0, item.sentence)
            if index == target and self.config.enabled:
                text = item.flag.get_description()
                focus = self.colors.focused_item
                Fmt.write(y + index + 1, cols - dx - len(text) - 4, Sentence().addf(focus, f" {text} ").add(self.style.sharpR(focus)))
            index += 1
            # if line_breaks > 0:
            #     line_breaks -= 1
            #     frame.print(0, Sentence())
            #     delta += 1

    def two_column_mode(self):
        _, cols = Fmt.get_size()
        return cols < self.wrap_size + 2 and self.app.has_full_hud()

    def build_list_sentence(self, items: List[Sentence]) -> List[Sentence]:
        out: List[Sentence] = []
        for x in items:
            color_ini = x.data[0].fmt
            color_end = x.data[-1].fmt
            left = self.style.roundL(color_ini)
            right = self.style.roundR(color_end)
            middle = x.clone()
            if x.data[0].text == "!":
                left = self.style.sharpL(color_ini)
                right = self.style.sharpR(color_end)
                middle.data = x.data[1:]
            out.append(Sentence().add(left).add(middle).add(right))
        return out

    def build_bottom_array(self):
        array: List[Sentence] = []
        array += self.get_help_others_before()
        array += self.get_help_fixed()
        color = "G" if self.app.has_full_hud() else "Y"
        symbol = symbols.success if self.app.has_full_hud() else symbols.failure
        array.append(Sentence() + RToken(color, f" {symbol.text} {GuiActions.hud} [{GuiKeys.hud}]"))
        array += self.get_help_others_after()

        return self.build_list_sentence(array)

    def show_bottom_bar(self):
        lines, cols = Fmt.get_size()
        elems = self.build_bottom_array()
        if self.two_column_mode():
            line_down = Sentence(" ").join(elems[2:-2])
            Fmt.write(lines - 1, 0, line_down.center(cols))
        else:
            if self.app.has_full_hud():
                line_all = Sentence(" ").join(elems)
                Fmt.write(lines - 1, 0, line_all.center(cols))
            else:
                line_main = Sentence(" ").join(elems[2: -2]) # alignment adjust
                Fmt.write(lines - 1, 0, line_main.center(cols))   

    def make_xp_button(self, size):
        if self.search.search_mode:
            text = " Busca: " + self.tree.search_text + "┊"
            percent = 0.0
            done = "W"
            todo = "W"
            text = text.ljust(size)
        else:
            text, percent = self.build_xp_bar()
            done = self.colors.main_bar_done
            todo = self.colors.main_bar_todo
            text = text.center(size)
        xpbar = self.style.build_bar(text, percent, len(text), done, todo)
        return xpbar

    def show_top_bar(self, frame: Frame):
        help = self.build_list_sentence(self.get_help_basic())
        pesquisar = help[0]
        marcar = help[1]
        config = self.style.get_flag_sentence(Flags.config)
        skills = self.style.get_flag_sentence(Flags.skills)
        others = self.app.has_full_hud()

        pre: List[Sentence] = []
        pre.append(marcar)
        if others and not self.two_column_mode():
            pre.append(config)

        pos: List[Sentence] = []
        if others and not self.two_column_mode():
            pos.append(skills)
        pos.append(pesquisar)

        limit = self.wrap_size
        if frame.get_dx() < self.wrap_size:
            limit = frame.get_dx()
        size = limit - Sentence(" ").join(pre + pos).len() - 2
        main_label = self.make_xp_button(size)
        info = Sentence(" ").join(pre + [main_label] + pos)
        frame.write(0, 0, info.center(frame.get_dx()))


    def show_help_config(self):
        _help: Floating = Floating("v>").warning().set_ljust_text().set_header(" Configurações ")
        self.fman.add_input(_help)
        _help.put_sentence(Sentence() + f"      Mínimo " + RToken("r", f"[{Flags.minimum.get_keycode()}]") + " - Mostrar os requisitos mínimos para completar a missão")
        _help.put_sentence(Sentence() + f"  Recompensa " + RToken("r", f"[{Flags.reward.get_keycode()}]") + " - Mostrar quanto de experiência cada atividade fornece")
        _help.put_sentence(Sentence() + f"  Percentual " + RToken("r", f"[{Flags.percent.get_keycode()}]") + " - Mostrar os valores em percentual")
        _help.put_sentence(Sentence() + f"  ModoAdmin " + RToken("r", f"Shift + [A]") + " - Liberar acesso a todas as missões" )
        _help.put_sentence(Sentence() + f"  PastaRaiz " + RToken("r", f"Shift + [{GuiKeys.set_root_dir}]") + " - Mudar a pasta padrão de download do tko" )
        _help.put_sentence(Sentence() + f"  Linguagem " + RToken("r", f"Shift + [{GuiKeys.set_lang}]") + " - Mudar a linguagem de download dos rascunhos" )


    def show_help(self):
        # def empty(value):
        #     pass
        _help: Floating = Floating("v>").set_ljust_text()
        self.fman.add_input(_help)

        _help.set_header_sentence(Sentence().add(" Ajuda "))
        # _help.put_text(" Movimentação ".center(dx, symbols.hbar.text))
        _help.put_sentence(Sentence("    Ajuda ").addf("r", GuiKeys.key_help).add("  Abre essa tela de ajuda")
        )

        _help.put_sentence(Sentence("  ").addf("r", "Shift + B")
                           .add("  Habilita ").addf("r", "").addf("R", "ícones").addf("r", "").add(" se seu ambiente suportar"))
        _help.put_sentence(Sentence() + "" + RToken("g", "setas") + ", " + RToken("g", "wasd")  + "  Para navegar entre os elementos")
        _help.put_sentence(Sentence() + f"{GuiActions.github} " + RToken("r", f"{GuiKeys.github_open}") + "  Abre tarefa em uma aba do browser")
        _help.put_sentence(Sentence() + f"   {GuiActions.baixar} " + RToken("r", f"{GuiKeys.down_task}") + "  Baixa tarefa de código para seu dispositivo")
        _help.put_sentence(Sentence() + f"   {GuiActions.editar} " + RToken("r", f"{GuiKeys.edit}") + "  Abre os arquivos no editor de código")
        _help.put_sentence(Sentence() + f"   {GuiActions.ativar} " + RToken("r", "↲") + "  Interage com o elemento")
        _help.put_sentence(Sentence() + f"   {GuiActions.marcar} " + RToken("r", f"{GuiKeys.inc_grade}") + RToken("r", f"{GuiKeys.dec_grade}") + " Muda a pontuação da tarefa")
        _help.put_sentence(Sentence())
        _help.put_sentence(Sentence() + "Você pode mudar o editor padrão com o comando")
        _help.put_sentence(Sentence() + RToken("g", "             tko config --editor <comando>"))


    def build_xp_bar(self) -> Tuple[str, float]:
        xp = XP(self.game)
        if xp.get_xp_total_obtained() == xp.get_xp_total_available():
            text = "Você atingiu o máximo de xp!"
            percent = 100.0
        else:
            # lang = self.rep.get_lang().upper()
            level = xp.get_level()
            percent = float(xp.get_xp_level_current()) / float(xp.get_xp_level_needed())
            if Flags.percent.is_true():
                xpobt = int(100 * xp.get_xp_level_current() / xp.get_xp_level_needed())
                text = "Level:{} XP:{}%".format(level, xpobt)
            else:
                xpobt1 = xp.get_xp_level_current()
                xpobt2 = xp.get_xp_level_needed()
                text = "Level:{} XP:{}/{}".format(level, xpobt1, xpobt2)

        return text, percent

    def show_opening(self):
        if Fmt.get_size()[1] < 100:
            return
        if not self.app.has_images():
            return
        _, cols = Fmt.get_size()
        
        now = datetime.datetime.now()
        parrot = random_get(opening, str(now.hour))
        parrot_lines = parrot.split("\n")
        max_len = max([len(line) for line in parrot_lines])
        yinit = 1
        for y, line in enumerate(parrot_lines):
            Fmt.write(yinit + y, cols - max_len - 2, Sentence().addf("g", line))

    def show_items(self):
        border_color = "r" if Flags.admin.is_true() else ""
        Fmt.clear()
        self.tree.set_focus(not self.config.enabled)
        self.tree.reload_sentences()
        lines, cols = Fmt.get_size()
        main_sx = cols  # tamanho em x livre
        main_sy = lines  # size em y avaliable

        top_y = -1
        top_dy = 1  #quantas linhas o topo usa
        bottom_dy = 1 # quantas linhas o fundo usa
        mid_y = top_dy # onde o meio começa
        mid_sy = main_sy - top_dy - bottom_dy # tamanho do meio
        left_size = 25
        skills_sx = 0
        flags_sx = 0
        if Flags.skills.is_true():
            skills_sx = left_size #max(20, main_sx // 4)
        elif Flags.config.is_true():
            flags_sx = left_size
        else:
            self.show_opening()
        
        task_sx = main_sx - flags_sx - skills_sx

        frame_top = Frame(top_y, 0).set_size(top_dy + 2, cols)
        self.show_top_bar(frame_top)

        # frame_bottom = Frame(lines - bottom_dy - 1, -1).set_size(bottom_dy + 2, cols + 2)
        self.show_bottom_bar()
        if task_sx > 5: 
            frame_main = Frame(mid_y, 0).set_size(mid_sy, task_sx).set_border_color(border_color)
            self.show_main_bar(frame_main)

        if Flags.config.is_true():
            frame_flags = Frame(mid_y, cols - flags_sx).set_size(mid_sy, flags_sx).set_border_color(border_color)
            self.show_config_bar(frame_flags)
            Fmt.write(1, cols - left_size - 3, Sentence().addf("r", f" {GuiActions.tab} "))

        if Flags.skills.is_true():
            frame_skills = Frame(mid_y, cols - skills_sx).set_size(mid_sy, skills_sx).set_border_color(border_color)
            self.show_skills_bar(frame_skills)



class ConfigParams:
    def __init__(self):
        self.side = False
        self.down = False
        self.lang = None
        self.ask = False
        self.root = None
        self.editor = None

    def __str__(self):
        return f"side: {self.side}, down: {self.down}, lang: {self.lang}, ask: {self.ask}, root: {self.root}, editor: {self.editor}"

class CmdConfig:
        
    @staticmethod
    def execute(settings: Settings, param: ConfigParams):
        action = False

        if param.side:
            action = True
            settings.app.set_diff_mode(DiffMode.SIDE)
            print("Diff mode now is: SIDE_BY_SIDE")
        if param.down:
            action = True
            settings.app.set_diff_mode(DiffMode.DOWN)
            print("Diff mode now is: UP_DOWN")
        if param.lang:
            action = True
            settings.app._lang_default = param.lang
            print("Default language extension now is:", param.lang)
        if param.ask:
            action = True
            settings.app._lang_default = ""
            print("Language extension will be asked always.")

        if param.root:
            action = True
            path = os.path.abspath(param.root)
            settings.app._rootdir = path
            print("Root directory now is: " + path)
        
        if param.editor:
            action = True
            settings.app._editor = param.editor
            print(f"Novo comando para abrir arquivos de código: {param.editor}")

        if not action:
            action = True
            print(settings.get_settings_file())
            print("Rootdir: {}".format(settings.app.get_rootdir()))
            print("Diff   : {}".format(str(settings.app.get_diff_mode())))
            print("Editor : {}".format(settings.app.get_editor()))
            print("Bordas : {}".format(settings.app.has_borders()))
            print("Images : {}".format(settings.app.has_images()))
            value = settings.app.get_lang_default()
            print("Linguagem default: {}".format("Não definido" if value == "" else value))

        settings.save_settings()


class CmdRep:
    @staticmethod
    def list(_args):
        settings = Settings()
        print(f"SettingsFile\n- {settings.settings_file}")
        print(str(settings))

    @staticmethod
    def add(args):
        settings = Settings()
        rep = RepSource()
        if args.url:
            rep.set_url(args.url)
        elif args.file:
            rep.set_file(args.file)
        settings.reps[args.alias] = rep
        settings.save_settings()

    @staticmethod
    def rm(args):
        sp = Settings()
        if args.alias in sp.reps:
            sp.reps.pop(args.alias)
            sp.save_settings()
        else:
            print("Repository not found.")

    @staticmethod
    def reset(_):
        sp = Settings().reset()
        print(sp.settings_file)
        print(sp.app._rootdir)
        sp.save_settings()

    @staticmethod
    def graph(args):
        settings = Settings()
        rep_source:RepSource = settings.get_rep_source(args.alias)
        file = rep_source.get_file_or_cache(os.path.join(settings.app._rootdir, args.alias))
        game = Game()
        game.parse_file(file)
        game.check_cycle()
        Graph(game).generate()

class Unit:
    def __init__(self, case: str = "", inp: str = "", outp: str = "", grade: Optional[int] = None, source: str = ""):
        self.source = source  # stores the source file of the unit
        self.source_pad = 0  # stores the pad to justify the source file
        self.case = case  # name
        self.case_pad = 0  # stores the pad to justify the case name
        self.input = inp  # input
        self.output = outp  # expected output
        self.user: Optional[str] = None  # solver generated answer
        self.grade: Optional[int] = grade  # None represents proportional gr, 100 represents all
        self.grade_reduction: int = 0  # if grade is None, this atribute should be filled with the right grade reduction
        self.index = 0
        self.repeated: Optional[int] = None

        self.result: ExecutionResult = ExecutionResult.UNTESTED

    def str(self, pad: bool = True) -> Sentence:
        index = str(self.index).zfill(2)
        grade = str(self.grade_reduction).zfill(3)
        rep = "" if self.repeated is None else " [" + str(self.repeated) + "]"
        op = Sentence() + ExecutionResult.get_symbol(self.result) + " " + self.result.value
        source = os.path.basename(self.source)
        if pad:
            source = self.source.ljust(self.source_pad)
        case = self.case
        if pad:
            case = self.case.ljust(self.case_pad)
        return Sentence() + "(" + op + ")" + f"[{index}] GR:{grade} {source} ({case}){rep}"



class DiffBuilder:

    vinput    = " INSERIDO "
    vexpected = " ESPERADO "
    vreceived = " RECEBIDO "
    vunequal  = " DESIGUAL "

    @staticmethod
    def make_line_arrow_up(a: str, b: str) -> Sentence:
        hdiff = Sentence()
        first = True
        i = 0
        lim = max(len(a), len(b))
        while i < lim:
            if i >= len(a) or i >= len(b) or a[i] != b[i]:
                if first:
                    first = False
                    hdiff += symbols.arrow_up
                    return hdiff
            else:
                hdiff += " "
            i += 1
        while len(hdiff) < lim:
            hdiff += " "
        return hdiff

    @staticmethod
    def render_white(text: Sentence, color: str = "") -> Optional[Sentence]:
        out = Sentence().add(text).replace(' ', Token(symbols.whitespace.text, color)).replace('\n', Token(symbols.newline.text, color))

        return out

    # create a string with both ta and tb side by side with a vertical bar in the middle
    @staticmethod
    def side_by_side(ta: List[Sentence], tb: List[Sentence], unequal: Token = symbols.unequal) -> List[Sentence]:
        cut = (Report.get_terminal_size() - 6) // 2
        upper = max(len(ta), len(tb))
        data: List[Sentence] = []

        for i in range(upper):
            a = ta[i] if i < len(ta) else Sentence("###############")
            b = tb[i] if i < len(tb) else Sentence("###############")
            if len(a) < cut:
                a = a.ljust(cut, Token(" "))
            # if len(a) > cut:
            #     a = a[:cut]
            if i >= len(ta) or i >= len(tb) or ta[i] != tb[i]:
                data.append(Sentence() + unequal + " " + a + " " + unequal + " " + b)
            else:
                data.append(Sentence() + symbols.vbar + " " + a + " " + symbols.vbar + " " + b)

        return data

    # a_text -> clean full received
    # b_text -> clean full expected
    # first_failure -> index of the first line unmatched 
    @staticmethod
    def first_failure_diff(a_text: str, b_text: str, first_failure: int) -> List[Sentence]:
        def get(vet, index):
            if index < len(vet):
                return DiffBuilder.render_white(vet[index])
            return ""

        a_render = a_text.splitlines(True)
        b_render = b_text.splitlines(True)

        first_a = get(a_render, first_failure)
        first_b = get(b_render, first_failure)
        # greater = max(len(first_a), len(first_b))

        # if first_failure > 0:
        #     lbefore = get(a_render, first_failure - 1)
        #     greater = max(greater, len(lbefore))

        out_a, out_b = DiffBuilder.colorize_2_lines_diff(Sentence(first_a), Sentence(first_b))
        greater = max(len(out_a), len(out_b))
        output: List[Sentence] = []

        output.append(Sentence().add(symbols.vbar).add(" ").add(out_a.ljust(greater)).addf("g", " (esperado)"))
        output.append(Sentence().add(symbols.vbar).add(" ").add(out_b.ljust(greater)).addf("r", " (recebido)"))
        diff = DiffBuilder.make_line_arrow_up(first_a, first_b)
        output.append(Sentence().add(symbols.vbar).add(" ").add(diff.ljust(greater)).addf("b", " (primeiro)"))
        return output

    @staticmethod
    def find_first_mismatch(line_a: Sentence, line_b: Sentence) -> int: 
        i = 0
        while i < len(line_a) and i < len(line_b):
            if line_a[i] != line_b[i]:
                return i
            i += 1
        return i
    
    @staticmethod
    def colorize_2_lines_diff(la: Sentence, lb: Sentence, neut: str = "", exp: str = "g", rec: str = "r") -> Tuple[Sentence, Sentence]:
        pos = DiffBuilder.find_first_mismatch(la, lb)
        lat = la.get_text()
        lbt = lb.get_text()
        a_out = Sentence().addf(neut, lat[0:pos]).addf(exp, lat[pos:])
        b_out = Sentence().addf(neut, lbt[0:pos]).addf(rec, lbt[pos:])
        return a_out, b_out

    # return a tuple of two strings with the diff and the index of the  first mismatch line
    @staticmethod
    def render_diff(a_text: str, b_text: str, pad: Optional[bool] = None) -> Tuple[List[Sentence], List[Sentence], int]:
        a_lines = a_text.splitlines()
        b_lines = b_text.splitlines()

        a_output: List[Sentence] = []
        b_output: List[Sentence] = []

        a_size = len(a_lines)
        b_size = len(b_lines)
        
        first_failure = -1

        cut: int = 0
        if pad is True:
            cut = (Report.get_terminal_size() - 6) // 2

        max_size = max(a_size, b_size)

        # lambda function to return element in index i or empty if out of bounds
        def get(vet, index):
            out = ""
            if index < len(vet):
                out = vet[index]
            if pad is None:
                return out
            return out[:cut].ljust(cut)

        # get = lambda vet, i: vet[i] if i < len(vet) else ""
        expected_color = "g"
        received_color = "r" if a_text != "" else ""
        for i in range(max_size):
            a_data = Sentence(get(a_lines, i))
            b_data = Sentence(get(b_lines, i))
            
            if i >= a_size or i >= b_size or a_lines[i] != b_lines[i]:
                if first_failure == -1:
                    first_failure = i
                a_out, b_out = DiffBuilder.colorize_2_lines_diff(a_data, b_data, "y", expected_color, received_color)
                a_output.append(a_out)
                b_output.append(b_out)
            else:
                a_output.append(a_data)
                b_output.append(b_data)

        return a_output, b_output, first_failure

    @staticmethod
    def mount_up_down_diff(unit: Unit, curses=False) -> List[Sentence]:
        output: List[Sentence] = []

        string_input = unit.input
        string_expected = unit.output
        string_received = unit.user

        no_diff_mode = string_input == "" and string_expected == ""

        if string_received is None:
            string_received = ""
        expected_lines, received_lines, first_failure = DiffBuilder.render_diff(string_expected, string_received)
        string_input_list = [Sentence().add(symbols.vbar.text).add(" ").add(line) for line in string_input.split("\n")][:-1]
        unequal = symbols.unequal
        if unit.result == ExecutionResult.EXECUTION_ERROR or unit.result == ExecutionResult.COMPILATION_ERROR or string_expected == "":
            unequal = symbols.vbar
        expected_lines, received_lines = DiffBuilder.put_left_equal(expected_lines, received_lines, unequal)

        color = "b" if string_expected != string_received else "g"
        if not curses:
            output.append(Report.centralize("", symbols.hbar, "╭"))
            output.append(Report.centralize(unit.str(), " ", symbols.vbar))
            output.append(Report.centralize(Sentence().addf(color, DiffBuilder.vinput), symbols.hbar, "├"))
        else:
            if no_diff_mode:
                output.append(Report.centralize(Sentence().addf(color, DiffBuilder.vreceived), symbols.hbar, "╭"))
            else:
                output.append(Report.centralize(Sentence().addf(color, DiffBuilder.vinput), symbols.hbar, "╭"))


        output += string_input_list
            
        if string_expected != "":
            output.append(Report.centralize(Sentence().addf("g", DiffBuilder.vexpected), symbols.hbar, "├"))
            output += expected_lines
        # output.append("\n".join(expected_lines))
        rcolor = "r" if (string_expected != "" and string_expected != string_received) else "g"
        if no_diff_mode == False:
            output.append(Report.centralize(Sentence().addf(rcolor, DiffBuilder.vreceived), symbols.hbar, "├"))
        output +=  received_lines

        include_rendering = False
        if string_expected != string_received and string_expected != "":
            include_rendering = True
        if unit.result == ExecutionResult.EXECUTION_ERROR or unit.result == ExecutionResult.COMPILATION_ERROR:
            include_rendering = False

        if include_rendering:
            output.append(Report.centralize(Sentence().addf("b", DiffBuilder.vunequal),  symbols.hbar, "├"))
            output += DiffBuilder.first_failure_diff(string_expected, string_received, first_failure)
        output.append(Report.centralize("",  symbols.hbar, "╰"))

        return output

    @staticmethod
    def put_left_equal(exp_lines: List[Sentence], rec_lines: List[Sentence], unequal: Token = symbols.unequal):

        max_size = max(len(exp_lines), len(rec_lines))

        for i in range(max_size):
            if i >= len(exp_lines) or i >= len(rec_lines) or (exp_lines[i] != rec_lines[i]):
                exp_lines[i] = Sentence() + unequal + " " + exp_lines[i]
                rec_lines[i] = Sentence() + unequal + " " + rec_lines[i]
            else:
                exp_lines[i] = Sentence() + symbols.vbar + " " + exp_lines[i]
                rec_lines[i] = Sentence() + symbols.vbar + " " + rec_lines[i]
        
        return exp_lines, rec_lines
            
    @staticmethod
    def title_side_by_side(left: Sentence, right: Sentence, filler: Token = Token(" "), middle: Token = Token(" "), prefix: Token = Token()) -> Sentence:
        half = int((Report.get_terminal_size() - len(middle)) / 2)
        line = Sentence()
        a = left
        a = a.center(half, filler)
        if len(a) > half:
            a = a.trim_end(half)
        line += a
        line += middle
        b = right
        b = b.center(half, filler)
        if len(b) > half:
            b = b.trim_end(half)
        line += b
        if prefix != "":
            line.data[0].text = line.data[0].text[1:]
            line = Sentence() + prefix + line
        return line

    @staticmethod
    def mount_side_by_side_diff(unit: Unit, curses=False) -> List[Sentence]:

        output: List[Sentence] = []

        string_input = unit.input
        string_expected = unit.output
        string_received = unit.user
        if string_received is None:
            string_received = ""
        # dotted = "-"
        # vertical_separator = symbols.vbar
        hbar = symbols.hbar

        expected_lines, received_lines, first_failure = DiffBuilder.render_diff(string_expected, string_received, True)
        if not curses:
            output.append(Report.centralize("", hbar, "╭"))
            output.append(Report.centralize(unit.str(), " ", "│"))
        input_color = "b" if string_expected != string_received else "g"
        input_headera = Sentence().addf(input_color, DiffBuilder.vinput)
        input_headerb = Sentence().addf(input_color, DiffBuilder.vinput)
        if not curses:
            output.append(DiffBuilder.title_side_by_side(input_headera, input_headerb, hbar, Token("┬"), Token("├")))
        else:
            output.append(Report.centralize(Sentence().addf(input_color, DiffBuilder.vinput),  symbols.hbar, "╭"))
            # output.append(Diff.title_side_by_side(input_headera, input_headerb, hbar, TK("┬"), TK("╭")))

        if string_input != "":
            lines = [Sentence(x) for x in string_input.split("\n")[:-1]]
            output += DiffBuilder.side_by_side(lines, lines)
        expected_header = Sentence().addf("g", DiffBuilder.vexpected)
        rcolor = "r" if string_expected != string_received else "g"
        received_header = Sentence().addf(rcolor, DiffBuilder.vreceived)
        output.append(DiffBuilder.title_side_by_side(expected_header, received_header, hbar, Token("┼"), Token("├")))
        unequal = symbols.unequal
        if unit.result == ExecutionResult.EXECUTION_ERROR or unit.result == ExecutionResult.COMPILATION_ERROR:
            unequal = symbols.vbar
        output += DiffBuilder.side_by_side(expected_lines, received_lines, unequal)
        if unit.result != ExecutionResult.EXECUTION_ERROR and unit.result != ExecutionResult.COMPILATION_ERROR and string_expected != string_received:
            output.append(Report.centralize(Sentence().addf("b", DiffBuilder.vunequal),  symbols.hbar, "├"))
            output += DiffBuilder.first_failure_diff(string_expected, string_received, first_failure)
            output.append(Report.centralize("",  symbols.hbar, "╰"))
        else:
            output.append(Report.centralize("┴",  symbols.hbar, "╰"))

        return output




class VplParser:
    @staticmethod
    def finish(text):
        return text if text.endswith("\n") else text + "\n"

    @staticmethod
    def unwrap(text):
        while text.endswith("\n"):
            text = text[:-1]
        if text.startswith("\"") and text.endswith("\""):
            text = text[1:-1]
        return VplParser.finish(text)

    @staticmethod
    class CaseData:
        def __init__(self, case="", inp="", outp="", grade: Optional[int] = None):
            self.case: str = case
            self.input: str = VplParser.finish(inp)
            self.output: str = VplParser.unwrap(VplParser.finish(outp))
            self.grade: Optional[int] = grade

        def __str__(self):
            return "case=" + self.case + '\n' \
                   + "input=" + self.input \
                   + "output=" + self.output \
                   + "gr=" + str(self.grade)

    regex_vpl_basic = r"case= *([ \S]*) *\n *input *=(.*?)^ *output *=(.*)"
    regex_vpl_extended = r"case= *([ \S]*) *\n *input *=(.*?)^ *output *=(.*?)^ *grade *reduction *= *(\S*)% *\n?"

    @staticmethod
    def filter_quotes(x):
        return x[1:-2] if x.startswith('"') else x

    @staticmethod
    def split_cases(text: str) -> List[str]:
        regex = r"^ *[Cc]ase *="
        subst = "case="
        text = re.sub(regex, subst, text, 0, re.MULTILINE | re.DOTALL)
        return ["case=" + t for t in text.split("case=")][1:]

    @staticmethod
    def extract_extended(text) -> Optional[CaseData]:
        f = re.match(VplParser.regex_vpl_extended, text, re.MULTILINE | re.DOTALL)
        if f is None:
            return None
        try:
            gr = int(f.group(4))
        except ValueError:
            gr = None
        return VplParser.CaseData(f.group(1), f.group(2), f.group(3), gr)

    @staticmethod
    def extract_basic(text) -> Optional[CaseData]:
        m = re.match(VplParser.regex_vpl_basic, text, re.MULTILINE | re.DOTALL)
        if m is None:
            return None
        return VplParser.CaseData(m.group(1), m.group(2), m.group(3), None)

    @staticmethod
    def parse_vpl(content: str) -> List[CaseData]:
        text_cases = VplParser.split_cases(content)
        seq: List[VplParser.CaseData] = []

        for text in text_cases:
            case = VplParser.extract_extended(text)
            if case is not None:
                seq.append(case)
                continue
            case = VplParser.extract_basic(text)
            if case is not None:
                seq.append(case)
                continue
            print("invalid case: " + text)
            exit(1)
        return seq

    @staticmethod
    def to_vpl(unit: CaseData):
        text = "case=" + unit.case + "\n"
        text += "input=" + unit.input
        text += "output=\"" + unit.output + "\"\n"
        if unit.grade is not None:
            text += "grade reduction=" + str(unit.grade) + "%\n"
        return text


class Loader:
    regex_tio = r"^ *>>>>>>>> *(.*?)\n(.*?)^ *======== *\n(.*?)^ *<<<<<<<< *\n?"

    def __init__(self):
        pass

    @staticmethod
    def parse_cio(text, source):
        unit_list = []
        text = "\n" + text

        pattern = r'```.*?\n(.*?)```'  # get only inside code blocks
        code = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
        # join all code blocks found
        text = "\n" + "\n".join(code)

        pieces = []  # header, input, output

        open_case = False
        for line in text.split("\n"):
            if line.startswith("#__case") or line.startswith("#TEST_CASE"):
                pieces.append({"header": line, "input": [], "output": []})
                open_case = True
            elif open_case:
                pieces[-1]["output"].append(line)
                if line.startswith("$end"):
                    open_case = False

        # concatenando testes contínuos e finalizando testes sem $end
        for i in range(len(pieces)):
            output = pieces[i]["output"]
            if output[-1] != "$end" and i < len(pieces) - 1:
                pieces[i + 1]["output"] = output + pieces[i + 1]["output"]
                output.append("$end")

        # removendo linhas vazias e criando input das linhas com $
        for piece in pieces:
            piece["input"] = [line[1:] for line in piece["output"] if line.startswith("$")]
            piece["output"] = [line for line in piece["output"] if line != "" and not line.startswith("#")]

        for piece in pieces:
            case = " ".join(piece["header"].split(" ")[1:])
            inp = "\n".join(piece["input"]) + "\n"
            output = "\n".join(piece["output"]) + "\n"
            unit_list.append(Unit(case, inp, output, None, source))

        return unit_list

    @staticmethod
    def parse_tio(text: str, source: str = "") -> List[Unit]:

        # identifica se tem grade e retorna case name e grade
        def parse_case_grade(value: str) -> Tuple[str, Optional[int]]:
            if value.endswith("%"):
                words = value.split(" ")
                last = value.split(" ")[-1]
                _case = " ".join(words[:-1])
                grade_str = last[:-1]           # ultima palavra sem %
                try:
                    _grade = int(grade_str)
                    return _case, _grade
                except ValueError:
                    pass
            return value, None

        matches = re.findall(Loader.regex_tio, text, re.MULTILINE | re.DOTALL)
        unit_list = []
        for m in matches:
            case, grade = parse_case_grade(m[0])
            unit_list.append(Unit(case, m[1], m[2], grade, source))
        return unit_list

    @staticmethod
    def parse_vpl(text: str, source: str = "") -> List[Unit]:
        data_list = VplParser.parse_vpl(text)
        output: List[Unit] = []
        for m in data_list:
            output.append(Unit(m.case, m.input, m.output, m.grade, source))
        return output

    @staticmethod
    def parse_dir(folder) -> List[Unit]:
        pattern_loader = PatternLoader()
        files = sorted(os.listdir(folder))
        matches = pattern_loader.get_file_sources(files)

        unit_list: List[Unit] = []
        try:
            for m in matches:
                unit = Unit()
                unit.source = os.path.join(folder, m.label)
                unit.grade = 100
                with open(os.path.join(folder, m.input_file)) as f:
                    value = f.read()
                    unit.input = value + ("" if value.endswith("\n") else "\n")
                with open(os.path.join(folder, m.output_file)) as f:
                    value = f.read()
                    unit.output = value + ("" if value.endswith("\n") else "\n")
                unit_list.append(unit)
        except FileNotFoundError as e:
            print(str(e))
        return unit_list

    @staticmethod
    def parse_source(source: str) -> List[Unit]:
        if os.path.isdir(source):
            return Loader.parse_dir(source)
        if os.path.isfile(source):
            #  if PreScript.exists():
            #      source = PreScript.process_source(source)
            with open(source, encoding="utf-8") as f:
                content = f.read()
            if source.endswith(".vpl"):
                return Loader.parse_vpl(content, source)
            elif source.endswith(".tio"):
                return Loader.parse_tio(content, source)
            elif source.endswith(".md"):
                tests = Loader.parse_tio(content, source)
                tests += Loader.parse_cio(content, source)
                return tests
            else:
                print("warning: target format do not supported: " + source)  # make this a raise
        else:
            raise FileNotFoundError('warning: unable to find: ' + source)
        return []



class UnitRunner:

    def __init__(self):
        pass

    # run a unit using a solver and return if the result is correct
    @staticmethod
    def run_unit(solver: SolverBuilder, unit: Unit, timeout: Optional[float]=None) -> ExecutionResult:
        if solver.compile_error:
            unit.user = solver.error_msg
            return ExecutionResult.COMPILATION_ERROR
        cmd = solver.get_executable()
        if timeout == 0:
            timeout = None
        return_code, stdout, stderr = Runner.subprocess_run(cmd, unit.input, timeout)
        unit.user = stdout + stderr
        if return_code != 0:
            return ExecutionResult.EXECUTION_ERROR
        if unit.user == unit.output:
            return ExecutionResult.SUCCESS
        return ExecutionResult.WRONG_OUTPUT

class Param:

    def __init__(self):
        pass

    class Basic:
        def __init__(self):
            self.index: Optional[int] = None
            self.label_pattern: Optional[str] = None
            self.diff_mode = DiffMode.SIDE
            self.diff_count = DiffCount.FIRST
            self.filter: bool = False
            self.compact: bool = False

        def set_index(self, value: Optional[int]):
            self.index= value
            return self

        def set_label_pattern(self, label_pattern: Optional[str]):
            self.label_pattern = label_pattern
            return self
        
        def set_compact(self, value: bool):
            self.compact = value
            return self

        def set_diff_mode(self, value: DiffMode):
            self.diff_mode = value
            return self
    
        def set_filter(self, value: bool):
            self.filter = value
            return self

        def set_diff_count(self, value: DiffCount):
            self.diff_count = value
            return self

    class Manip:
        def __init__(self):
            self.unlabel: bool = False
            self.to_sort: bool = False
            self.to_number: bool = False
        
        def set_unlabel(self, value: bool):
            self.unlabel = value
            return self
        
        def set_to_sort(self, value: bool):
            self.to_sort = value
            return self
        
        def set_to_number(self, value: bool):
            self.to_number = value
            return self



class Identifier:
    def __init__(self):
        pass

    @staticmethod
    def get_type(target: str) -> IdentifierType:
        if os.path.isdir(target):
            return IdentifierType.OBI
        elif target.endswith(".md"):
            return IdentifierType.MD
        elif target.endswith(".tio"):
            return IdentifierType.TIO
        elif target.endswith(".vpl"):
            return IdentifierType.VPL
        else:
            return IdentifierType.SOLVER



class Wdir:
    def __init__(self):
        self.__autoload = False
        self.__autoload_folder = ""
        self.__solver: Optional[SolverBuilder] = None
        self.__source_list: List[str] = []
        self.__pack_list: List[List[Unit]] = []
        self.__unit_list: List[Unit] = []
        self.__curses = False
        self.__lang = ""

    def has_solver(self) -> bool:
        return not self.__solver is None

    def has_tests(self) -> bool:
        return len(self.__unit_list) != 0

    def get_solver(self) -> SolverBuilder:
        if self.__solver is None:
            raise Warning("fail: Não foi encontrado arquivo de código")
        return self.__solver
    
    def get_unit_list(self) -> List[Unit]:
        return self.__unit_list

    def get_unit(self, index: int) -> Unit:
        return self.__unit_list[index]
    
    def get_source_list(self) -> List[str]:
        return self.__source_list

    def set_curses(self, value: bool):
        self.__curses = value
        return self

    def set_lang(self, lang: str):
        self.__lang = lang
        return self
    
    def is_curses(self) -> bool:
        return self.__curses

    def is_autoload(self) -> bool:
        return self.__autoload

    def get_autoload_folder(self) -> str:
        return self.__autoload_folder

    def set_solver(self, solver_list: List[str]):
        if len(solver_list) > 0:
            self.__solver = SolverBuilder(solver_list)
        return self

    def set_sources(self, source_list: List[str]):
        self.__source_list = source_list
        return self

    def autoload(self):
        folder = self.__autoload_folder
        files = os.listdir(folder)
        files = [os.path.join(folder, f) for f in files]
        files = [f for f in files if os.path.isfile(f)]

        sources = [target for target in files if target.endswith(".tio")]
        if self.__lang != "":
            solvers = [target for target in files if target.endswith("." + self.__lang)]
        else:
            solvers = [target for target in files if any([target.endswith("." + lang) for lang in languages_avaliable])]

        solvers = sorted(solvers)

        # if not self.__curses:
        #     print("códigos encontrados: [" + ", ".join(solvers) + "]")
        #     print("testes  encontrados: [" + ", ".join(sources) + "]")
            # print("Para remover um arquivo da lista, renomeie para sua extensão para .txt")
        self.set_solver(solvers)
        self.set_sources(sources)
        self.__autoload = True
        return self

    def set_target_list(self, target_list: List[str]):
        target_list = [os.path.normpath(t) for t in target_list]
        if len(target_list) == 0:
            target_list.append(".")
        if len(target_list) == 1 and os.path.isdir(target_list[0]):
            self.__autoload_folder = target_list[0]
            return self.autoload()
            
        target_list = [t for t in target_list if t != ""]
        for target in target_list:
            if not os.path.exists(target):
                raise FileNotFoundError(f"fail: {target} não encontrado")

        solvers = [target for target in target_list if Identifier.get_type(target) == IdentifierType.SOLVER]
        sources = [target for target in target_list if Identifier.get_type(target) != IdentifierType.SOLVER]
        
        self.set_solver(solvers)
        self.set_sources(sources)
        return self

    def set_cmd(self, exec_cmd: Optional[str]):
        if exec_cmd is None:
            return self
        if self.__solver is not None:
            print("fail: if using --cmd, don't pass source files to target")
        self.__solver = SolverBuilder([])
        self.__solver.set_executable(exec_cmd)
        return self

    def build(self):
        loading_failures = 0
        self.__pack_list = []
        for source in self.__source_list:
            try:
                self.__pack_list.append(Loader.parse_source(source))
            except FileNotFoundError as e:
                print(str(e))
                loading_failures += 1
                pass
        if loading_failures > 0 and loading_failures == len(self.__source_list):
            raise FileNotFoundError("failure: nenhum arquivo de teste encontrado")
        self.__unit_list = sum(self.__pack_list, [])
        self.__number_and_mark_duplicated()
        self.__calculate_grade()
        self.__pad()
        return self

    def calc_grade(self) -> int:
        grade = 100
        for case in self.__unit_list:
            if not case.repeated and (case.user is None or case.output != case.user):
                grade -= case.grade_reduction
        return max(0, grade)

    # put all the labels with the same length
    def __pad(self):
        if len(self.__unit_list) == 0:
            return
        max_case = max([len(x.case) for x in self.__unit_list])
        max_source = max([len(x.source) for x in self.__unit_list])
        for unit in self.__unit_list:
            unit.case_pad = max_case
            unit.source_pad = max_source

    # select a single unit to execute exclusively
    def filter(self, param: Param.Basic):
        index = param.index
        if index is not None:
            if 0 <= index < len(self.__unit_list):
                self.__unit_list = [self.__unit_list[index]]
            else:
                raise ValueError("Índice fora dos limites: " + str(index))
        return self

    # calculate the grade reduction for the cases without grade
    # the grade is proportional to the number of unique cases
    def __calculate_grade(self):
        unique_count = len([x for x in self.__unit_list if not x.repeated])
        for unit in self.__unit_list:
            if unit.grade is None:
                unit.grade_reduction = math.floor(100 / unique_count)
            else:
                unit.grade_reduction = unit.grade

    # number the cases and mark the repeated
    def __number_and_mark_duplicated(self):
        new_list: List[Unit] = []
        index = 0
        for unit in self.__unit_list:
            unit.index = index
            index += 1
            search = [x for x in new_list if x.input == unit.input]
            if len(search) > 0:
                unit.repeated = search[0].index
            new_list.append(unit)
        self.__unit_list = new_list

    # sort, unlabel ou rename using the param received
    def manipulate(self, param: Param.Manip):
        # filtering marked repeated
        self.__unit_list = [unit for unit in self.__unit_list if unit.repeated is None]
        if param.to_sort:
            self.__unit_list.sort(key=lambda v: len(v.input))
        if param.unlabel:
            for unit in self.__unit_list:
                unit.case = ""
        if param.to_number:
            number = 00
            for unit in self.__unit_list:
                unit.case = LabelFactory().label(unit.case).index(number).generate()
                number += 1

    def unit_list_resume(self) -> List[Sentence]:
        return [unit.str() for unit in self.__unit_list]

    def sources_names(self) -> List[Tuple[str, int]]:
        out: List[Tuple[str, int]] = []
        if len(self.__pack_list) == 0:
            out.append((symbols.failure.text, 0))
        for i in range(len(self.__pack_list)):
            nome: str = self.__source_list[i].split(os.sep)[-1]
            out.append((nome, len(self.__pack_list[i])))
        return out

    def solvers_names(self) -> List[str]:
        path_list = [] if self.__solver is None else self.__solver.path_list
        if self.__solver is not None and len(path_list) == 0:  # free_cmd
            out = ["free cmd"]
        else:
            out = [os.path.basename(path) for path in path_list]
        return out

    def resume(self) -> Sentence:
        sources = ["{}({})".format(name, str(count).rjust(2, "0")) for name, count in self.sources_names()]
        __sources = Sentence().add("Testes:").add("[").addf("y", ", ".join(sources)).add("]")

        __solvers = Sentence().add("Códigos:").add("[").addf("g", ", ".join(self.solvers_names())).add("]")

        return Sentence().add(__solvers).add(" ").add(__sources)




class SeqMode(enum.Enum):
    intro = 0
    select = 1
    running = 2
    finished = 3

class Tester:
    def __init__(self, settings: Settings, wdir: Wdir):
        self.results: List[Tuple[ExecutionResult, int]] = []
        self.wdir = wdir
        self.unit_list = [unit for unit in wdir.get_unit_list()] # unit list to be consumed
        self.exit = False

        self.task = Task()
        self.init = 1000   # index of first line to show
        self.length = 1  # length of diff
        self.space = 0  # dy space for draw
        self.mode: SeqMode = SeqMode.intro

        self.settings = settings
        self.app = settings.app
        self.borders = Border(settings.app)

        self.locked_index: bool = False
        self.focused_index = 0
        self.resumes: List[str] = []

        self.fman = FloatingManager()
        self.opener: Optional[Opener] = None
        self.dummy_unit = Unit()


    def set_opener(self, opener: Opener):
        self.opener = opener
        self.opener.set_fman(self.fman)
        return self

    def set_autorun(self, value:bool):
        if value:
            self.mode = SeqMode.running
        return self
    
    def set_task(self, task: Task):
        self.task = task
        return self

    def set_exit(self):
        self.exit = True
        return self

    def print_centered_image(self, image: str, color: str, clear=False, align: str = "."):
        dy, dx = Fmt.get_size()
        lines = image.split("\n")[1:]
        init_y = 4
        if align == "v":
            init_y = dy - len(lines) - 1
        for i, line in enumerate(lines):
            info = Sentence().addf(color, line).center(dx - 2, Token(" ", " "))
            if clear:
                Fmt.write(i + init_y, 1, Sentence(" " * info.len()))
            else:
                Fmt.write(i + init_y, 1, Sentence().addf(color, line).center(dx - 2, Token(" ", " ")))

    def show_success(self):
        if self.settings.app.has_images():
            out = random_get(images, self.get_folder(), "static")
        else:
            out = random_get(success, self.get_folder(), "static")
        self.print_centered_image(out, "g")
        
    def show_compilling(self, clear=False):
        out = random_get(compilling, self.get_folder(), "random")
        self.print_centered_image(out, "y", clear)

    def show_executing(self, clear=False):
        out = executing
        self.print_centered_image(out, "y", clear, "v")

    def draw_scrollbar(self):
        y_init = 3
        # if len(self.results_fail) == 0:
        #     return
        tr = "╮"
        br = "╯"
        vbar = "│"
        bar = []

        if self.length > self.space:
            total = self.space
            _begin = False
            _end = False
            if self.init == 0:
                _begin = True
            if self.init == self.length - self.space:
                _end = True

            pre = int((self.init / self.length) * total)
            mid = int((self.space / self.length) * total)
            pos = (max(0, total - pre - mid))

            if _begin:
                pre -= 1
            if _end:
                pos -= 1

            if self.init > 0 and pre == 0:
                pre = 1
                pos -= 1

            if _begin:
                bar.append(tr)
            for _ in range(pre):
                bar.append(vbar)
            for _ in range(mid):
                bar.append("┃")
            for _ in range(pos):
                bar.append(vbar)
            if _end:
                bar.append(br)

        else:
            bar.append(tr)
            for i in range(self.length - 2):
                bar.append(vbar)
            bar.append(br)


        _, cols = Fmt.get_size()
        for i in range(len(bar)):
            Fmt.write(i + y_init, cols - 1, Sentence().add(bar[i]))

    def get_folder(self):
        source_list = self.wdir.get_source_list()
        if source_list:
            folder = os.path.abspath(source_list[0])
        else:
            folder = os.path.abspath(self.wdir.get_solver().path_list[0])
        return folder.split(os.sep)[-2]

    def get_focused_unit(self) -> Unit:
        if not self.wdir.has_tests():
            return self.dummy_unit
        if len(self.results) != 0:
            _, index = self.results[self.focused_index]
            unit = self.wdir.get_unit(index)
            return unit
        return self.wdir.get_unit(self.focused_index)

    def get_token(self, result: ExecutionResult) -> Token:
        if result == ExecutionResult.SUCCESS:
            return Token(ExecutionResult.get_symbol(ExecutionResult.SUCCESS).text, "G")
        elif result == ExecutionResult.WRONG_OUTPUT:
            return Token(ExecutionResult.get_symbol(ExecutionResult.WRONG_OUTPUT).text, "R")
        elif result == ExecutionResult.COMPILATION_ERROR:
            return Token(ExecutionResult.get_symbol(ExecutionResult.UNTESTED).text, "W")
        elif result == ExecutionResult.EXECUTION_ERROR:
            return Token(ExecutionResult.get_symbol(ExecutionResult.EXECUTION_ERROR).text, "Y")
        else:
            return Token(ExecutionResult.get_symbol(ExecutionResult.UNTESTED).text, "W")

    def process_one(self):

        if self.mode != SeqMode.running:
            return

        solver = self.wdir.get_solver()

        if solver.compile_error:
            self.mode = SeqMode.finished
            while len(self.unit_list) > 0:
                index = len(self.results)
                self.unit_list = self.unit_list[1:]
                self.results.append((ExecutionResult.COMPILATION_ERROR, index))
            return
        
        if self.locked_index or not self.wdir.has_tests():
            self.mode = SeqMode.finished
            unit = self.get_focused_unit()
            unit.result = UnitRunner.run_unit(solver, unit, self.settings.app._timeout)
            return

        if self.wdir.has_tests():
            index = len(self.results)
            unit = self.unit_list[0]
            self.unit_list = self.unit_list[1:]
            unit.result = UnitRunner.run_unit(solver, unit, self.settings.app._timeout)
            self.results.append((unit.result, index))
            success = [result for result, _ in self.results if result == ExecutionResult.SUCCESS]
            self.task.test_progress = (len(success) * 100) // len(self.wdir.get_unit_list())
            self.focused_index = index

        if len(self.unit_list) == 0:
            self.mode = SeqMode.finished
            self.focused_index = 0


            done_list: List[Tuple[ExecutionResult, int]] = []
            fail_list: List[Tuple[ExecutionResult, int]] = []
            for data in self.results:
                unit_result, _ = data
                if unit_result != ExecutionResult.SUCCESS:
                    fail_list.append(data)
                else:
                    done_list.append(data)
            self.results = fail_list + done_list


    def build_top_line_header(self, frame):
        activity_color = "C"
        solver_color = "W"
        sources_color = "Y"
        running_color = "R"

        # building activity
        activity = Sentence().add(self.borders.border(activity_color, self.get_folder()))

        # building solvers
        solvers = Sentence()
        if len(self.get_solver_names()) > 1:
            solvers.add(Sentence().add(self.borders.roundL("R")).addf("R", f"{GuiActions.tab}").add(self.borders.sharpR("R")))
        for i, solver in enumerate(self.get_solver_names()):
            if len(self.get_solver_names()) > 1:
                solvers.add(" ")
            color = solver_color
            if i == self.task.main_index:
                color = "G"
            solvers.add(self.borders.border(color, solver))
        
        # replacing with count if running
        done = len(self.results)
        full = len(self.wdir.get_unit_list())
        count_missing = Sentence().add(self.borders.border(running_color, f"({done}/{full})"))
        if self.mode == SeqMode.running:
            if  self.locked_index:
                solvers = Sentence().add(self.borders.border("R", "Executando atividade travada"))
            else:
                solvers = count_missing

        # building sources
        source_names = Sentence(", ").join([Sentence().addf(sources_color, f"{name[0]}({name[1]})") for name in self.wdir.sources_names()])
        sources = Sentence().add(self.borders.roundL(sources_color)).add(source_names).add(self.borders.roundR(sources_color))

        # merging activity, solvers and sources in header
        delta = frame.get_dx() - solvers.len()
        left = 1
        right = 1
        if delta > 0:
            delta_left = delta // 2
            left = max(1, delta_left - activity.len())
            delta_right = delta - delta_left
            right = max(1, delta_right - sources.len())

        return Sentence().add(activity).add("─" * left).add(solvers).add("─" * right).add(sources)

    def build_unit_list(self, frame: Frame) -> Sentence:
        done_list = self.results
        if len(done_list) > 0 and self.locked_index:
            _, index = done_list[self.focused_index]
            done_list[self.focused_index] = (self.get_focused_unit().result, index)
        todo_list: List[Tuple[ExecutionResult, int]] = []
        i = len(done_list)
        for _ in self.unit_list:
            if self.locked_index and i == self.focused_index:
                todo_list.append((self.wdir.get_unit(self.focused_index).result, i))
            else:
                todo_list.append((ExecutionResult.UNTESTED, i))
            i += 1

        i = 0
        show_focused_index = not self.wdir.get_solver().compile_error and not self.mode == SeqMode.intro and not self.is_all_right()
        
        output = Sentence()
        if self.wdir.has_tests():
            output.add(self.get_fixed_arrow())
        else:
            output.add(self.borders.border("R", "Nenhum teste encontrado"))

            

        for unit_result, index in done_list + todo_list:
            foco = i == self.focused_index
            token = self.get_token(unit_result)
            extrap = self.borders.roundL(token.fmt)
            extras = self.borders.roundR(token.fmt)
            if foco and show_focused_index:
                token.fmt = token.fmt.lower() + "C"
                extrap = self.borders.roundL("C")
                extras = self.borders.roundR("C")
            if self.locked_index and not foco:
                output.add("  ").addf(token.fmt.lower(), str(index).zfill(2)).addf(token.fmt.lower(), token.text).add(" ")
            else:
                output.add(" ").add(extrap).addf(token.fmt, str(index).zfill(2)).add(token).add(extras)
            i += 1

        size = 6
        to_remove = 0
        index = self.focused_index
        dx = frame.get_dx()
        while (index + 2) * size - to_remove >= dx:
            to_remove += size
        output.data = output.data[:6] + output.data[6 + to_remove:]
        return output

    def get_fixed_arrow(self) -> Sentence:
        free = symbols.locked_free.text
        locked = symbols.locked_locked.text
        symbol = locked if self.locked_index else free
        color = "R" if self.locked_index else "G"
        return Sentence().add(self.borders.roundL(color)).addf(color, f"{GuiKeys.travar} {symbol}").add(self.borders.sharpR(color))

    def draw_top_bar_content(self, frame):
        if not self.wdir.has_tests():
            return
        value = self.get_focused_unit()
        info = Sentence()
        if self.wdir.get_solver().compile_error:
            info = self.borders.border("R", "Erro de compilação")
        elif value is not None and not self.is_all_right() and not self.mode == SeqMode.intro:
            info = value.str(pad = False)
            # if self.locked_index:
            #     info = self.borders.border(focused_unit_color, info.get_text())
        frame.write(0, 0, Sentence().add(info).center(frame.get_dx()))

    def draw_top_bar(self):
        # construir mais uma solução
        _, cols = Fmt.get_size()
        frame = Frame(0, 0).set_size(3, cols)
        frame.set_header(self.build_top_line_header(frame))
        self.draw_top_bar_content(frame)
        frame.set_footer(self.build_unit_list(frame), "")
        frame.draw()
        
    def two_column_mode(self):
        _, cols = Fmt.get_size()
        return cols < Sentence(" ").join(self.make_bottom_line()).len() + 2

    def make_bottom_line(self) -> List[Sentence]:
        cmds: List[Sentence] = []
        if self.app.has_full_hud():
            # rodar
            cmds.append(self.borders.border("M", f"{GuiActions.rodar} [{GuiKeys.rodar}]"))
            # fixar
            color = "G" if self.locked_index else "M"
            symbol = symbols.success if self.locked_index else symbols.failure
            travar = f"{symbol.text} {GuiActions.fixar}[{GuiKeys.travar}]"
            cmds.append(self.borders.border(color, travar))
        # sair
        cmds.append(self.borders.border("C", f" {GuiActions.sair}  [{GuiKeys.sair}]"))
        # editar
        if self.opener is not None:
            cmds.append(self.borders.border("C", f"{GuiActions.editar} [{GuiKeys.editar}]"))
        # ativar
        cmds.append(self.borders.border("G", f"{GuiActions.ativar} [↲]"))
        
        # hud
        color = "G" if self.app.has_full_hud() else "Y"
        symbol = symbols.success if self.app.has_full_hud() else symbols.failure
        cmds.append(self.borders.border(color, f" {symbol.text} {GuiActions.hud} [{GuiKeys.hud}]"))

        if self.app.has_full_hud():
            # tempo
            value = str(self.settings.app.get_timeout())
            if value == "0":
                value = symbols.infinity.text
            cmds.append(
                Sentence()
                    .add(self.borders.roundL("M"))
                    .add(RToken("M", "{} {}[{}]".format(GuiActions.tempo, value, GuiKeys.tempo)))
                    .add(self.borders.roundR("M"))
            )
            # diff mode
            if self.settings.app.get_diff_mode() == DiffMode.DOWN:
                text = f"Diff ⇕ [{GuiKeys.diff}]"
            else:
                text = f"Diff ⇔ [{GuiKeys.diff}]"

            cmds.append(self.borders.border("M", text))
            
        return cmds

    def show_bottom_line(self):
        lines, cols = Fmt.get_size()
        if self.two_column_mode():
            line = self.make_bottom_line()
            one = line[0:2] + line[-2:]
            two = line[2:-2]
            Fmt.write(lines - 2, 0, Sentence(" ").join(one).center(cols, Token(" ")))
            Fmt.write(lines - 1, 0, Sentence(" ").join(two).center(cols, Token(" ")))
        else:
            out = Sentence(" ").join(self.make_bottom_line())
            # if Fmt.get_size()[1] % 2 == 0:
            #     out.add("-")
            Fmt.write(lines - 1, 0, out.center(cols, Token(" ")))
 
    def is_all_right(self):
        if self.locked_index or len(self.results) == 0:
            return False
        if not self.mode == SeqMode.finished:
            return False
        for result, _ in self.results:
            if result != ExecutionResult.SUCCESS:
                return False
        return True

    def draw_main(self):
        unit = self.get_focused_unit()
        lines, cols = Fmt.get_size()
        self.space = lines - 4
        if self.two_column_mode():
            self.space = lines - 5
        frame = Frame(2, -1).set_inner(self.space, cols - 1).set_border_square()

        if self.is_all_right():
            self.show_success()
            return
        Report.set_terminal_size(cols)
        
        if self.wdir.get_solver().compile_error:
            received = self.wdir.get_solver().error_msg
            line_list = [Sentence().add(line) for line in received.split("\n")]
        elif self.settings.app.get_diff_mode() == DiffMode.DOWN or not self.wdir.has_tests():
            line_list = DiffBuilder.mount_up_down_diff(unit, curses=True)
        else:
            line_list = DiffBuilder.mount_side_by_side_diff(unit, curses=True)

        self.length = max(1, len(line_list))

        if self.length - self.init < self.space:
            self.init = max(0, self.length - self.space)

        if self.init >= self.length:
            self.init = self.length - 1

        if self.init < self.length:
            line_list = line_list[self.init:]
        for i, line in enumerate(line_list):
            frame.write(i, 0, Sentence().add(line))

        self.draw_scrollbar()
        return

    def get_solver_names(self):
        return sorted(self.wdir.solvers_names())
    
    def main(self, scr):
        InputManager.fix_esc_delay()
        curses.curs_set(0)  # Esconde o cursor
        Fmt.init_colors()  # Inicializa as cores
        Fmt.set_scr(scr)  # Define o scr como global
        while not self.exit:

            Fmt.clear()
            if self.mode == SeqMode.running:
                if self.wdir.get_solver().not_compiled():
                    self.draw_top_bar()
                    self.show_bottom_line()
                    self.show_compilling()
                    Fmt.refresh()
                    try:
                        self.wdir.get_solver().prepare_exec()
                    except CompileError as e:
                        self.fman.add_input(Floating("v>").error().put_text(e.message))
                        self.mode = SeqMode.finished
                    Fmt.clear()
                    self.draw_top_bar()
                    self.show_bottom_line()
                    Fmt.refresh()
                self.process_one()
            self.draw_top_bar()

            if self.mode == SeqMode.intro:
                self.print_centered_image(random_get(intro, self.get_folder()), "y")
            else:
                self.draw_main()
            
            self.show_bottom_line()

            if self.fman.has_floating():
                self.fman.draw_warnings()

            if self.mode == SeqMode.running:
                Fmt.refresh()
                continue

            if self.fman.has_floating():
                key = self.fman.get_input()
            else:
                key = Fmt.getch()

            fn_exec = self.process_key(key)
            if fn_exec is not None:
                return fn_exec

    def run_exec_mode(self):
        self.mode = SeqMode.running
        if self.wdir.is_autoload():
            self.wdir.autoload()
            self.wdir.get_solver().set_main(self.get_solver_names()[self.task.main_index])
        self.mode = SeqMode.finished
        return lambda: Free.free_run(self.wdir.get_solver(), show_compilling=True, to_clear=True, wait_input=True)

    def run_test_mode(self):
        self.mode = SeqMode.running
        if self.wdir.is_autoload():
            self.wdir.autoload() # reload sources and solvers
        
        self.wdir.build() # reload cases

        Fmt.clear()
        self.wdir.get_solver().set_main(self.get_solver_names()[self.task.main_index]).reset() # clear old compilation
        
        if self.locked_index:
            for i in range(len(self.results)):
                _, index = self.results[i]
                self.results[i] = (ExecutionResult.UNTESTED, index)
        else:
            self.focused_index = 0
            self.results = []
            self.unit_list = [unit for unit in self.wdir.get_unit_list()]

    def send_char_not_found(self, key):
        self.fman.add_input(Floating("v>").error()
                    .put_text("Tecla")
                    .put_text(f"char {chr(key)}")
                    .put_text(f"code {key}")
                    .put_text("não reconhecida")
                    .put_text("")
                    )

    def go_left(self):
        if self.mode == SeqMode.intro:
            self.mode = SeqMode.select
        if self.mode == SeqMode.finished:
            self.mode = SeqMode.select
        if self.locked_index:
            self.fman.add_input(Floating("v>").warning().put_text("←\nAtividade travada\nAperte {} para destravar".format(GuiKeys.travar)))
            return
        if not self.wdir.get_solver().compile_error:
            self.focused_index = max(0, self.focused_index - 1)
            self.init = 1000

    def go_right(self):
        if self.mode == SeqMode.intro:
            self.mode = SeqMode.select
            self.focused_index = 0
            return
        if self.mode == SeqMode.finished:
            self.mode = SeqMode.select
        if self.locked_index:
            self.fman.add_input(Floating("v>").warning().put_text("→\nAtividade travada\nAperte {} para destravar".format(GuiKeys.travar)))
            return
        if not self.wdir.get_solver().compile_error:
            self.focused_index = min(len(self.wdir.get_unit_list()) - 1, self.focused_index + 1)
            self.init = 1000

    def go_down(self):
        if self.mode == SeqMode.intro:
            self.mode = SeqMode.select
        self.init += 1

    def go_up(self):
        if self.mode == SeqMode.intro:
            self.mode = SeqMode.select
        self.init = max(0, self.init - 1)

    def change_main(self):
        if len(self.get_solver_names()) == 1:
            self.fman.add_input(
                Floating("v>").warning()
                .put_text("Seu projeto só tem um arquivo de solução")
                .put_text("Essa funcionalidade troca qual dos arquivos")
                .put_text("de solução será o principal.")
            )
            return
        self.task.main_index = (self.task.main_index + 1) % len(self.get_solver_names())

    def lock_unit(self):
        self.locked_index = not self.locked_index
        if self.mode == SeqMode.intro:
            self.mode = SeqMode.select
        if self.locked_index:
            for i in range(len(self.results)):
                _, index = self.results[i]
                self.results[i] = (ExecutionResult.UNTESTED, index)
            self.fman.add_input(
                Floating("v>").warning()
                .put_text("Atividade travada")
                .put_sentence(Sentence("Aperte ").addf("g", GuiKeys.travar).add(" para destravar"))
                .put_sentence(Sentence("Use ").addf("g", "Enter").add(" para rodar os testes"))
            )

    def change_limit(self):
            valor = self.settings.app._timeout
            if valor == 0:
                valor = 1
            else:
                valor *= 2
            if valor >= 5:
                valor = 0
            self.settings.app.set_timeout(valor)
            self.settings.save_settings()
            nome = "∞" if valor == 0 else str(valor)
            self.fman.add_input(
                Floating("v>").warning()
                .put_text("Limite de tempo de execução alterado para")
                .put_text(f"{nome} segundos")
            )

    def process_key(self, key):
        if key == ord('q') or key == InputManager.backspace1 or key == InputManager.backspace2:
            self.set_exit()
        elif key == InputManager.esc:
            if self.locked_index:
                self.locked_index = False
            else:
                self.set_exit()
        elif key == curses.KEY_LEFT or key == ord(GuiKeys.left):
            self.go_left()
        elif key == curses.KEY_RIGHT or key == ord(GuiKeys.right):
            self.go_right()
        elif key == curses.KEY_DOWN or key == ord(GuiKeys.down):
            self.go_down()
        elif key == curses.KEY_UP or key == ord(GuiKeys.up):
            self.go_up()
        elif key == ord(GuiKeys.principal):
            self.change_main()
        elif key == ord(GuiKeys.rodar):
            return self.run_exec_mode()
        elif key == ord(GuiKeys.testar):
            self.run_test_mode()
        elif key == ord(GuiKeys.travar):
            self.lock_unit()
        elif key == ord(GuiKeys.editar):
            if self.opener is not None:
                self.opener.load_folders_and_open()
        elif key == ord(GuiKeys.tempo):
            self.change_limit()
        elif key == ord(GuiKeys.hud):
            self.settings.app.toggle_hud()
            self.settings.save_settings()
        elif key == ord(GuiKeys.diff):
            self.settings.app.toggle_diff()
            self.settings.save_settings()
        elif key == ord(GuiKeys.border):
            self.settings.app.toggle_borders()
            self.settings.save_settings()
        elif key == ord(GuiKeys.images):
            self.settings.app.toggle_images()
            self.settings.save_settings()
        elif key != -1 and key != curses.KEY_RESIZE:
            self.send_char_not_found(key)

    def run(self):
        while True:
            free_run_fn = curses.wrapper(self.main)
            if free_run_fn == None:
                break
            else:
                while(True):
                    try:
                        repeat = free_run_fn()
                        if repeat == False:
                            break
                    except CompileError as e:
                        self.mode = SeqMode.finished
                        print(e)
                        input("Pressione enter para continuar")
                        break





class Writer:

    def __init__(self):
        pass

    @staticmethod
    def to_vpl(unit: Unit):
        text = "case=" + unit.case + "\n"
        text += "input=" + unit.input
        text += "output=\"" + unit.output + "\"\n"
        if unit.grade is None:
            text += "\n"
        else:
            text += "grade reduction=" + str(unit.grade).zfill(3) + "%\n"
        return text

    @staticmethod
    def to_tio(unit: Unit):
        text = ">>>>>>>>"
        if unit.case != '':
            text += " " + unit.case
        if unit.grade is not None:
            text += " " + str(unit.grade) + "%"
        text += '\n' + unit.input
        text += "========\n"
        text += unit.output
        if unit.output != '' and unit.output[-1] != '\n':
            text += '\n'
        text += "<<<<<<<<\n"
        return text

    @staticmethod
    def save_dir_files(folder: str, pattern_loader: PatternLoader, label: str, unit: Unit) -> None:
        file_source = pattern_loader.make_file_source(label)
        with open(os.path.join(folder, file_source.input_file), "w") as f:
            f.write(unit.input)
        with open(os.path.join(folder, file_source.output_file), "w") as f:
            f.write(unit.output)

    @staticmethod
    def save_target(target: str, unit_list: List[Unit], force: bool = False):
        def ask_overwrite(file):
            print("file " + file + " found. Overwrite? (y/n):")
            resp = input()
            if resp.lower() == 'y':
                print("overwrite allowed")
                return True
            print("overwrite denied\n")
            return False

        def save_dir(_target: str, _unit_list):
            folder = _target
            pattern_loader = PatternLoader()
            number = 0
            for unit in _unit_list:
                Writer.save_dir_files(folder, pattern_loader, str(number).zfill(2), unit)
                number += 1

        def save_file(_target, _unit_list):
            if _target.endswith(".tio"):
                _new = "\n".join([Writer.to_tio(unit) for unit in _unit_list])
            else:
                _new = "\n".join([Writer.to_vpl(unit) for unit in _unit_list])

            file_exists = os.path.isfile(_target)

            if file_exists:
                _old = open(_target).read()
                if _old == _new:
                    print("no changes in test file")
                    return

            if not file_exists or (file_exists and (force or ask_overwrite(_target))):
                with open(_target, "w") as f:
                    f.write(_new)

                    if not force:
                        print("file " + _target + " wrote")

        target_type = Identifier.get_type(target)
        if target_type == IdentifierType.OBI:
            save_dir(target, unit_list)
        elif target_type == IdentifierType.TIO or target_type == IdentifierType.VPL:
            save_file(target, unit_list)
        else:
            print("fail: target " + target + " do not supported for build operation\n")





class FilterMode:
    @staticmethod
    def deep_copy_and_change_dir():
        # path to ~/.tko_filter
        filter_path = os.path.join(os.path.expanduser("~"), ".tko_filter")

        # verify if filter command is available
        if shutil.which("filter_code") is None:
            print("ERROR: comando de filtragem não encontrado")
            print("Instale o feno com 'pip install feno'")
            exit(1)

        subprocess.run(["filter_code", "-rf", ".", "-o", filter_path])

        os.chdir(filter_path)

class Run:

    def __init__(self, settings: Settings, target_list: List[str], exec_cmd: Optional[str], param: Optional[Param.Basic]):
        self.settings = settings
        self.target_list: List[str] = target_list
        self.exec_cmd: Optional[str] = exec_cmd
        if param is None:
            self.param = Param.Basic()
        else:
            self.param = param
        self.wdir: Wdir = Wdir()
        self.wdir_builded = False
        self.__curses_mode: bool = False
        self.__lang = ""
        self.__task: Optional[Task] = None
        self.__opener: Optional[Opener] = None
        self.__autorun: bool = True

    def set_curses(self, value:bool=True, success: Success=Success.RANDOM):
        self.__curses_mode = value
        return self
   
    def set_lang(self, lang:str):
        self.__lang = lang
        return self
    
    def set_opener(self, opener: Opener):
        self.__opener = opener
        return self

    def set_autorun(self, value:bool):
        self.__autorun = value

    def set_task(self, task: Task):
        self.__task = task
        return self

    def execute(self):
        if not self.wdir_builded:
            self.build_wdir()

        if self.__missing_target():
            return
        if self.__list_mode():
            return
        if self.__free_run():
            return
        self.__diff_mode()
        return

    def __remove_duplicates(self):
        # remove duplicates in target list keeping the order
        self.target_list = list(dict.fromkeys(self.target_list))

    def __change_targets_to_filter_mode(self):
        if self.param.filter:
            old_dir = os.getcwd()

            term_print(Report.centralize(" Entrando no modo de filtragem ", "═"))
            FilterMode.deep_copy_and_change_dir()  
            # search for target outside . dir and redirect target
            new_target_list = []
            for target in self.target_list:
                if ".." in target:
                    new_target_list.append(os.path.normpath(os.path.join(old_dir, target)))
                elif os.path.exists(target):
                    new_target_list.append(target)
            self.target_list = new_target_list

    def __print_top_line(self):
        if self.wdir is None:
            return

        term_print(Sentence().add(symbols.opening).add(self.wdir.resume()), end="")
        term_print(" [", end="")
        first = True
        for unit in self.wdir.get_unit_list():
            if first:
                first = False
            else:
                term_print(" ", end="")
            solver = self.wdir.get_solver()
            if solver is None:
                raise Warning("Solver vazio")
            unit.result = UnitRunner.run_unit(solver, unit)
            term_print(Sentence() + ExecutionResult.get_symbol(unit.result), end="")
        term_print("]")

    def __print_diff(self):
        if self.wdir is None or not self.wdir.has_solver():
            return
        
        if self.param.diff_count == DiffCount.QUIET:
            return
        
        if self.wdir.get_solver().compile_error:
            term_print(self.wdir.get_solver().error_msg)
            return
        
        results = [unit.result for unit in self.wdir.get_unit_list()]
        if ExecutionResult.EXECUTION_ERROR not in results and ExecutionResult.WRONG_OUTPUT not in results:
            return
        
        if not self.param.compact:
            for elem in self.wdir.unit_list_resume():
                term_print(elem)
        
        if self.param.diff_count == DiffCount.FIRST:
            # printing only the first wrong case
            wrong = [unit for unit in self.wdir.get_unit_list() if unit.result != ExecutionResult.SUCCESS][0]
            if self.param.diff_mode:
                for line in DiffBuilder.mount_up_down_diff(wrong):
                    term_print(line)
            else:
                for line in DiffBuilder.mount_side_by_side_diff(wrong):
                    term_print(line)
            return

        if self.param.diff_count == DiffCount.ALL:
            for unit in self.wdir.get_unit_list():
                if unit.result != ExecutionResult.SUCCESS:
                    if self.param.diff_mode:
                        for line in DiffBuilder.mount_up_down_diff(unit):
                            term_print(line)
                    else:
                        for line in DiffBuilder.mount_side_by_side_diff(unit):
                            term_print(line)

    def build_wdir(self):
        self.wdir_builded = True
        self.__remove_duplicates()
        self.__change_targets_to_filter_mode()
        try:
            self.wdir = Wdir().set_curses(self.__curses_mode).set_lang(self.__lang).set_target_list(self.target_list).set_cmd(self.exec_cmd).build().filter(self.param)
        except FileNotFoundError as e:
            if self.wdir.has_solver():
                self.wdir.get_solver().error_msg += str(e)
                self.wdir.get_solver().compile_error = True
        return self.wdir

    def __missing_target(self) -> bool:
        if self.wdir is None:
            return False
        if not self.wdir.has_solver() and not self.wdir.has_tests():
            term_print(Sentence().addf("", "fail: ") + "Nenhum arquivo de código ou de teste encontrado.")
            return True
        return False
    
    def __list_mode(self) -> bool:
        if self.wdir is None:
            return False

        # list mode
        if not self.wdir.has_solver() and self.wdir.has_tests():
            term_print(Report.centralize(" Nenhum arquivo de código encontrado. Listando casos de teste.", Token("╌")), flush=True)
            term_print(self.wdir.resume())
            for line in self.wdir.unit_list_resume():
                term_print(line)
            return True
        return False

    def __free_run(self) -> bool:
        if self.wdir is None:
            return False
        if self.wdir.has_solver() and (not self.wdir.has_tests()) and not self.__curses_mode:
            Free.free_run(self.wdir.get_solver(), show_compilling=False, to_clear=False, wait_input=False)
            return True
        return False

    def __create_opener_for_wdir(self) -> Opener:
        opener = Opener(self.settings)
        folders = []
        targets = ["."]
        if self.target_list:
            targets = self.target_list
        for f in targets:
            if os.path.isdir(f) and f not in folders:
                folders.append(f)
            else:
                folder = os.path.dirname(os.path.abspath(f))
                if folder not in folders:
                    folders.append(folder)
        opener.set_target(folders)
        solver_zero = self.wdir.get_solver().path_list[0]
        lang = solver_zero.split(".")[-1]
        opener.set_language(lang)
        return opener

    def __diff_mode(self):
        if self.wdir is None:
            return
        
        if self.__curses_mode:
            cdiff = Tester(self.settings, self.wdir)
            if self.__task is not None:
                cdiff.set_task(self.__task)
            if self.__opener is not None:
                cdiff.set_opener(self.__opener)
            else:
                cdiff.set_opener(self.__create_opener_for_wdir())
            cdiff.set_autorun(self.__autorun)
            cdiff.run()
        else:
            term_print(Report.centralize(" Testando o código com os casos de teste ", "═"))
            self.__print_top_line()
            self.__print_diff()



class CmdBuild:

    def __init__(self, target_out: str, source_list: List[str], param: Param.Manip, to_force: bool):
        self.target_out = target_out
        self.source_list = source_list
        self.param = param
        self.to_force = to_force

    def execute(self):
        try:
            wdir = Wdir().set_sources(self.source_list).build()
            wdir.manipulate(self.param)
            Writer.save_target(self.target_out, wdir.get_unit_list(), self.to_force)
        except FileNotFoundError as e:
            print(str(e))
            return False
        return True

class Drafts:
    ts_draft = r"""
let _cin_ : string[] = [];
try { _cin_ = require("fs").readFileSync(0).toString().split(/\r?\n/); } catch(e){}
let input = () : string => _cin_.length === 0 ? "" : _cin_.shift()!;
let write = (text: any, end:string="\n")=> process.stdout.write("" + text + end);
export {};

write("qxcode");
"""[1:]

    js_draft = r"""
let __lines = require("fs").readFileSync(0).toString().split("\n");
let input = () => __lines.length === 0 ? "" : __lines.shift();
let write = (text, end="\n") => process.stdout.write("" + text + end);

write("qxcode");
"""[1:]

    c_draft = r"""
#include <stdio.h>

int main() {
    puts("qxcode");
    return 0;
}

"""[1:]

    cpp_draft = r"""
#include <iostream>

int main() {
    std::cout << "qxcode\n";
}

"""[1:]

    java_draft = r"""
public class draft {
    public static void main(String args[]) {
        System.out.println("qxcode");
    }
}

"""[1:]

    go_draft = (
        r"package main""\n"
        r'import "fmt"'"\n"
        r"func main() {""\n"
        r'    fmt.Println("qxcode")''\n'
        r"}""\n"
    )


    drafts = {'c': c_draft, 'cpp': cpp_draft, 'ts': ts_draft, 'js': js_draft, 'java': java_draft, 'go': go_draft}




class DownProblem:
    fnprint: Callable[[str], None] = print

    @staticmethod
    def __create_file(content, path, label=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        DownProblem.fnprint("  " + path + " " + label)

    @staticmethod
    def unpack_json(loaded, destiny, lang: str):
        # extracting all files to folder
        for entry in loaded["upload"]:
            if entry["name"] == "vpl_evaluate.cases":
                DownProblem.__compare_and_save(entry["contents"], os.path.join(destiny, "cases.tio"))

        if "draft" in loaded:
            if lang in loaded["draft"]:
                for file in loaded["draft"][lang]:
                    path = os.path.join(destiny, file["name"])
                    DownProblem.__create_file(file["contents"], path, "(Draft)")

    @staticmethod
    def __compare_and_save(content, path):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.encode("utf-8").decode("utf-8"))
            DownProblem.fnprint("  " + path + " (Novo)")
        else:
            if open(path, encoding="utf-8").read() != content:
                DownProblem.fnprint(path + " (Atualizado)")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                DownProblem.fnprint("  " + path + " (Inalterado)")

    @staticmethod
    def down_problem_def(destiny, cache_url) -> Tuple[str, str]:
        # downloading Readme
        readme = os.path.join(destiny, "Readme.md")
        [tempfile, __content] = urllib.request.urlretrieve(cache_url + "Readme.md")

        # content = ""
        try:
            content = open(tempfile, encoding="utf-8").read()
        except FileNotFoundError:
            content = open(tempfile, encoding="utf-8").read()

        DownProblem.__compare_and_save(content, readme)

        # downloading mapi
        mapi = os.path.join(destiny, "mapi.json")
        urllib.request.urlretrieve(cache_url + "mapi.json", mapi)
        return readme, mapi

    @staticmethod
    def create_problem_folder(rootdir: str, activity: str) -> str:
        # create dir
        destiny: str = os.path.join(rootdir, activity)
        if not os.path.exists(destiny):
            os.makedirs(destiny, exist_ok=True)
        else:
            DownProblem.fnprint("  Pasta do problema "+ destiny + " encontrada, juntando conteúdo.")

        return destiny

    @staticmethod
    def download_drafts(loaded_json, destiny: str, language, cache_url, ask_ext):
        if len(loaded_json["required"]) == 1:  # you already have the students file
            return

        if "draft" in loaded_json and language in loaded_json["draft"]:
            pass
        else:
            try:
                draft_path = os.path.join(destiny, "draft." + language)
                urllib.request.urlretrieve(cache_url + "draft." + language, draft_path)
                DownProblem.fnprint("  " + draft_path + " (Rascunho) Renomeie antes de modificar")

            except urllib.error.HTTPError:  # draft not found
                filename = "draft."
                draft_path = os.path.join(destiny, filename + language)
                if not os.path.exists(draft_path):
                    with open(draft_path, "w", encoding="utf-8") as f:
                        if language in Drafts.drafts:
                            f.write(Drafts.drafts[language])
                        else:
                            f.write("")
                    DownProblem.fnprint("  " + draft_path + " (Vazio)")

        if ask_ext:
            print("\nVocê pode escolher a extensão padrão com o comando\n$ tko config -l <extension>")




class CmdDown:
    @staticmethod
    def execute(rep_alias: str, task_key: str, language: Optional[str], settings: Settings, fnprint: Callable[[str], None], game: Optional[Game] = None) -> bool:
        DownProblem.fnprint = fnprint
        rep_dir = os.path.join(settings.app.get_rootdir(), rep_alias)
        rep_source = settings.get_rep_source(rep_alias)
        rep_data = settings.get_rep_data(rep_alias)
        if game is None:
            try:
                file = rep_source.get_file_or_cache(rep_dir)
            except urllib.error.HTTPError:
                DownProblem.fnprint("falha: Verifique sua internet")
            game = Game(file)
        item = game.get_task(task_key)
        if not item.link.startswith("http"):
            DownProblem.fnprint("falha: link para atividade não é um link remoto")
            return False
        cfg = RemoteCfg(item.link)
        cache_url = os.path.dirname(cfg.get_raw_url()) + "/.cache/"

        destiny = DownProblem.create_problem_folder(rep_dir, task_key)
        destiny = os.path.abspath(destiny)
        try:
            [_readme_path, mapi_path] = DownProblem.down_problem_def(destiny, cache_url)
        except urllib.error.HTTPError:
            DownProblem.fnprint("  falha: atividade não encontrada no curso")
            # verifi if destiny folder is empty and remove it
            if len(os.listdir(destiny)) == 0:
                os.rmdir(destiny)
            return False
        except urllib.error.URLError:
            DownProblem.fnprint("  falha: não consegui baixar a atividade, verifique sua internet")
            return False


        with open(mapi_path, encoding="utf-8") as f:
            loaded_json = json.load(f)
        os.remove(mapi_path)

        language_def = rep_data.get_lang()
        if language_def == "":
            language_def = Settings().app.get_lang_default()
        ask_ext = False
        if language is None:
            if language_def != "":
                language = language_def
            else:
                print("  Escolha uma extensão para os rascunhos: [c, cpp, py, ts, js, java]: ", end="")
                language = input()
                ask_ext = True

        DownProblem.unpack_json(loaded_json, destiny, language)
        DownProblem.download_drafts(loaded_json, destiny, language, cache_url, ask_ext)
        return True








class PlayActions:

    def __init__(self, gui: Gui):
        self.app = Settings().app
        self.settings = Settings()
        self.fman = gui.fman
        self.rep = gui.rep
        self.tree = gui.tree
        self.game = gui.game
        self.graph_opened: bool = False
        self.gui = gui

    def gen_graph_path(self) -> str:
        return os.path.join(self.app._rootdir, self.rep.alias, "graph.png")
        

    def open_link_without_stdout_stderr(self, link: str):
        outfile = tempfile.NamedTemporaryFile(delete=False)
        subprocess.Popen("python3 -m webbrowser -t {}".format(link), stdout=outfile, stderr=outfile, shell=True)

    def open_code(self):
        obj = self.tree.get_selected()
        if isinstance(obj, Task):
            task: Task = obj
            folder = os.path.join(self.app._rootdir, self.rep.alias, task.key)
            if os.path.exists(folder):
                opener = Opener(self.settings).set_fman(self.fman)
                opener.set_target([folder]).set_language(self.rep.get_lang())
                opener.load_folders_and_open()
            else:
                self.fman.add_input(
                    Floating("v>")
                    .put_text("\nO arquivo de código não foi encontrado.\n")
                    .error()
                )
        else:
            self.fman.add_input(
                Floating("v>")
                .put_text("\nVocê só pode abrir o código")
                .put_text("de tarefas baixadas.\n")
                .error()
            )

    def open_link(self):
        obj = self.tree.get_selected()
        if isinstance(obj, Task):
            task: Task = obj
            if task.link.startswith("http"):
                try:
                    self.open_link_without_stdout_stderr(task.link)
                except Exception as _:
                    pass
            self.fman.add_input(
                Floating("v>")
                .set_header(" Abrindo link ")
                .put_text("\n " + task.link + " \n")
                .warning()
            )
        elif isinstance(obj, Quest):
            self.fman.add_input(
                Floating("v>")
                .put_text("\nEssa é uma missão.")
                .put_text("\nVocê só pode abrir o link")
                .put_text("de tarefas.\n")
                .error()
            )
        else:
            self.fman.add_input(
                Floating("v>")
                .put_text("\nEsse é um grupo.")
                .put_text("\nVocê só pode abrir o link")
                .put_text("de tarefas.\n")
                .error()
            )

    def generate_graph(self):
        try:
            Graph(self.game).set_path(self.gen_graph_path()).set_opt(False).generate()
            path = self.gen_graph_path()
            # self.fman.add_input(Floating().put_text(f"\nGrafo gerado em\n {path} \n"))
            if not self.graph_opened:
                opener = Opener(self.settings)
                opener.open_files([path])
                self.graph_opened = True
        except FileNotFoundError as _:
            self.gui.config.gen_graph = False
            self.fman.add_input(Floating().error()
                                .put_text("")
                                .put_sentence(Sentence().add("Instale o ").addf("r", "graphviz").add(" para poder gerar os grafos"))
                                .put_text("")
                                )

    def down_task(self):

        lang = self.rep.get_lang() 
        obj = self.tree.items[self.tree.index_selected].obj
        if isinstance(obj, Task) and obj.key in obj.title:
            task: Task = obj
            down_frame = (
                Floating("v>").warning().set_ljust_text().set_header(" Baixando tarefa ")
            )
            down_frame.put_text(f"\ntko down {self.rep.alias} {task.key} -l {lang}\n")
            self.fman.add_input(down_frame)

            def fnprint(text):
                down_frame.put_text(text)
                down_frame.draw()
                Fmt.refresh()
            CmdDown.execute(self.rep.alias, task.key, lang, self.settings, fnprint, self.game)
        else:
            if isinstance(obj, Quest):
                self.fman.add_input(
                    Floating("v>")
                    .put_text("\nEssa é uma missão.")
                    .put_text("\nVocê só pode baixar tarefas.\n")
                    .error()
                )
            elif isinstance(obj, Cluster):
                self.fman.add_input(
                    Floating("v>")
                    .put_text("\nEsse é um grupo.")
                    .put_text("\nVocê só pode baixar tarefas.\n")
                    .error()
                )
            else:
                self.fman.add_input(
                    Floating("v>").put_text("\nEssa não é uma tarefa de código.\n").error()
                )
    
    def select_task(self):
        rootdir = self.app._rootdir
        
        obj = self.tree.items[self.tree.index_selected].obj

        if isinstance(obj, Quest) or isinstance(obj, Cluster):
            self.tree.toggle(obj)
            return

        rep_dir = os.path.join(rootdir, self.rep.alias)
        task: Task = obj
        if not task.is_downloadable():
            self.open_link()
            return
        if not task.is_downloaded_for_lang(rep_dir, self.rep.get_lang()):
            self.down_task()
            return
        return self.run_selected_task(task, rep_dir)
        
    def run_selected_task(self, task: Task, rep_dir: str):
        folder = os.path.join(rep_dir, task.key)
        run = Run(self.settings, [folder], None, Param.Basic())
        run.set_lang(self.rep.get_lang())
        opener = Opener(self.settings).set_language(self.rep.get_lang()).set_target([folder])
        run.set_opener(opener)
        run.set_autorun(False)
        if self.app.has_images():
            run.set_curses(True, Success.RANDOM)
        else:
            run.set_curses(True, Success.FIXED)
        run.set_task(task)

        run.build_wdir()
        if not run.wdir.has_solver():
            msg = Floating("v>").error()
            msg.put_text("\nNenhum arquivo de código na linguagem {} encontrado.".format(self.rep.get_lang()))
            msg.put_text("Arquivos encontrados na pasta:\n")
            folder = run.wdir.get_autoload_folder()
            file_list = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
            for file in file_list:
                msg.put_text(file)
            msg.put_text("")
            self.fman.add_input(msg)
            return
        return run.execute




class Play:
    def __init__(self, settings: Settings, game: Game, rep: RepData):
        self.settings = settings
        self.app = settings.app
        self.rep = rep
        self.game: Game = game

        self.exit = False

        if self.rep.get_lang() == "":
            self.rep.set_lang(self.app._lang_default)
        self.flagsman = FlagsMan(self.rep.get_flags())
        self.fman = FloatingManager()
        self.tree = TaskTree(self.settings, game, rep)
        self.gui = Gui(tree=self.tree, flagsman=self.flagsman, fman=self.fman)

        if len(self.rep.get_tasks()) == 0:
            self.gui.show_help()

        self.first_loop = True
        self.graph_ext = ""

        self.actions = PlayActions(self.gui)



    def save_to_json(self):
        self.tree.save_on_rep()
        self.rep.set_flags(self.flagsman.get_data())
        self.settings.save_settings()
        self.rep.save_data_to_json()

    def send_quit_msg(self):
        def set_exit():
            self.exit = True

        self.fman.add_input(
            Floating().put_text("\nAté a próxima\n").set_exit_fn(set_exit).warning()
        ),

    def toggle_config(self):
        if Flags.config.is_true():
            Flags.config.toggle()
            self.gui.config.disable()
        else:
            Flags.config.toggle()
            self.gui.config.enable()
            if Flags.skills.is_true():
                Flags.skills.toggle()

    def toggle_skills(self):
        if Flags.skills.is_true():
            Flags.skills.toggle()
        else:
            Flags.skills.toggle()
            if Flags.config.is_true():
                Flags.config.toggle()
            
    def process_tab(self):
        if Flags.config.is_true():
            self.gui.config.enable()

    def make_callback(self) -> InputManager:
        cman = InputManager()

        cman.add_int(curses.KEY_RESIZE, self.gui.disable_on_resize)
        cman.add_str(GuiKeys.key_quit, self.send_quit_msg)
        cman.add_int(InputManager.esc, self.send_quit_msg)
        cman.add_int(curses.KEY_BACKSPACE, self.send_quit_msg)

        if Flags.config.is_true() and self.gui.config.enabled:
            cman.add_str(GuiKeys.up, self.gui.config.move_up)
            cman.add_int(curses.KEY_UP, self.gui.config.move_up)
            cman.add_str(GuiKeys.down, self.gui.config.move_down)
            cman.add_int(curses.KEY_DOWN, self.gui.config.move_down)
            cman.add_str(GuiKeys.activate, self.gui.config.activate_selected)
            cman.add_int(InputManager.tab, self.gui.config.disable)
    
        else:
            cman.add_str(GuiKeys.up, self.tree.move_up)
            cman.add_int(curses.KEY_UP, self.tree.move_up)
            cman.add_str(GuiKeys.down, self.tree.move_down)
            cman.add_int(curses.KEY_DOWN, self.tree.move_down)
            cman.add_str(GuiKeys.left, self.tree.arrow_left)
            cman.add_int(curses.KEY_LEFT, self.tree.arrow_left)
            cman.add_str(GuiKeys.right, self.tree.arrow_right)
            cman.add_int(curses.KEY_RIGHT, self.tree.arrow_right)
            cman.add_str(GuiKeys.activate, self.actions.select_task)
            cman.add_int(InputManager.tab, self.process_tab)
            cman.add_str(GuiKeys.expand, self.tree.process_expand)
            cman.add_str(GuiKeys.expand2, self.tree.process_expand)
            cman.add_str(GuiKeys.collapse, self.tree.process_collapse)
            cman.add_str(GuiKeys.collapse2, self.tree.process_collapse)
            cman.add_str(GuiKeys.github_open, self.actions.open_link)
            cman.add_str(GuiKeys.down_task, self.actions.down_task)
            cman.add_str(GuiKeys.inc_grade, self.tree.inc_grade)
            cman.add_str(GuiKeys.inc_grade2, self.tree.inc_grade)
            cman.add_str(GuiKeys.dec_grade, self.tree.dec_grade)
            cman.add_str(GuiKeys.dec_grade2, self.tree.dec_grade)
            cman.add_str(GuiKeys.edit, lambda: self.actions.open_code())
            for value in range(1, 10):
                cman.add_str(str(value), GradeFunctor(int(value), self.tree.set_grade))
            cman.add_str("'", GradeFunctor(0, self.tree.set_grade))
            cman.add_str("0", GradeFunctor(10, self.tree.set_grade))
        
        cman.add_str(GuiKeys.key_help, self.gui.show_help)
        
        for flag in self.flagsman.others:
            cman.add_str(flag.get_keycode(), FlagFunctor(flag))

        config_elements = self.gui.config.get_elements()
        for element in config_elements:
            key = element.flag.get_keycode()
            fn = element.fn
            cman.add_str(key, fn)

        cman.add_str(Flags.config.get_keycode(), self.toggle_config)
        cman.add_str(Flags.skills.get_keycode(), self.toggle_skills)
        cman.add_str(GuiKeys.hud, self.app.toggle_hud)
        cman.add_str("/", self.gui.search.toggle_search)

        return cman
        
    def send_char_not_found(self, key):
        exclude_str = [ord(v) for v in [" ", "a", "d", "\n"]]
        exclude_int = [ -1, InputManager.esc, InputManager.left, InputManager.right ]
        if key in exclude_int + exclude_str:
            return
        self.fman.add_input(
            Floating("v")
                .error()
                .put_text(f"Tecla char {chr(key)} code {key} não reconhecida")
        )

    def main(self, scr):
        InputManager.fix_esc_delay()
        curses.curs_set(0)  # Esconde o cursor
        Fmt.init_colors()  # Inicializa as cores
        Fmt.set_scr(scr)  # Define o scr como global

        while True:
            self.tree.update_tree(admin_mode=Flags.admin.is_true() or self.gui.search.search_mode)
            self.fman.draw_warnings()
            if self.gui.config.gen_graph:
                self.actions.generate_graph()
            cman = self.make_callback()
            self.gui.show_items()

            if self.fman.has_floating():
                value: int = self.fman.get_input()
            else:
                value = scr.getch()
                value = InputManager.fix_cedilha(scr, value)

            if self.exit:
                break

            if self.gui.search.search_mode:
                self.gui.search.process_search(value)
            elif cman.has_int_key(value):
                callback = cman.exec_call(value)
                if callback is not None:
                    return callback
            else:
                self.send_char_not_found(value)

            self.tree.reload_sentences()
            self.save_to_json()
            if self.first_loop:
                self.first_loop = False

    def check_lang_in_text_mode(self):
        lang = self.rep.get_lang()
        if lang == "":
            options = languages_avaliable
            print("\nLinguagem padrão ainda não foi definida.\n")
            while True:
                print("Escolha entre as opções a seguir ", end="")
                print("[" + ", ".join(options) + "]", ":", end=" ")
                lang = input()
                if lang in options:
                    break
            self.rep.set_lang(lang)

    def play(self):

        self.check_lang_in_text_mode()

        while True:
            output = curses.wrapper(self.main)
            if output is None:
                return
            else:
                output()


class CmdPlay:
    @staticmethod
    def execute(rep_alias: str, settings: Settings):
        while True:
            rep_alias = settings.check_rep_alias(rep_alias)
            rep_source: RepSource = settings.get_rep_source(rep_alias)
            rep = settings.get_rep_data(rep_alias)
            rep_dir = rep.get_rep_dir()
            file = rep_source.get_file_or_cache(rep_dir)
            game = Game()
            game.parse_file(file)

            # passing a lambda function to the play class to save the settings
            play = Play(settings=settings, game=game, rep=rep)
            print(f"Abrindo repositório de {rep_alias}")
            reload = play.play()
            if not reload:
                break










class Main:
    @staticmethod
    def go(args):
        PatternLoader.pattern = args.pattern
        param = Param.Basic().set_index(args.index)
        if args.quiet:
            param.set_diff_count(DiffCount.QUIET)
        elif args.all:
            param.set_diff_count(DiffCount.ALL)
        else:
            param.set_diff_count(DiffCount.FIRST)

        if args.filter:
            param.set_filter(True)
        if args.compact:
            param.set_compact(True)

        settings = Settings()
        # load default diff from settings if not specified
        if not args.side and not args.down:
            param.set_diff_mode(settings.app.get_diff_mode())
        elif args.side:
            param.set_diff_mode(DiffMode.SIDE)
        elif args.down:
            param.set_diff_mode(DiffMode.DOWN)
        cmd_run = Run(settings, args.target_list, args.cmd, param)
        cmd_run.execute()

    @staticmethod
    def run(args):
        PatternLoader.pattern = args.pattern
        param = Param.Basic().set_index(args.index)
        settings = Settings()
        param.set_diff_mode(settings.app.get_diff_mode())
        if args.filter:
            param.set_filter(True)
        cmd_run = Run(settings, args.target_list, args.cmd, param)
        cmd_run.set_curses()
        cmd_run.execute()

    @staticmethod
    def build(args):
        PatternLoader.pattern = args.pattern
        manip = Param.Manip().set_unlabel(args.unlabel).set_to_sort(args.sort).set_to_number(args.number)
        build = CmdBuild(args.target, args.target_list, manip, args.force)
        build.execute()

    @staticmethod
    def play(args):
        settings = Settings()
        settings.check_rootdir()
        CmdPlay.execute(args.repo, settings)
        CheckVersion().version_check()

    @staticmethod
    def down(args):
        settings = Settings().check_rootdir()
        CmdDown.execute(args.course, args.activity, args.language, settings, print)

    @staticmethod
    def config(args):
        settings = Settings()
        param = ConfigParams()
        param.side = args.side
        param.down = args.down
        param.lang = args.lang
        param.ask = args.ask
        param.root = args.root
        param.editor = args.editor

        CmdConfig.execute(settings, param)


class Parser:
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(prog='tko', description=f'tko version {__version__}')
        self.subparsers = self.parser.add_subparsers(title='subcommands', help='help for subcommand.')

        self.parent_manip = self.create_parent_manip()
        self.parent_basic = self.create_parent_basic()

        self.add_parser_global()
        self.create_parent_basic()
        self.create_parent_manip()
        self.add_parser_run()
        self.add_parser_go()
        self.add_parser_build()
        self.add_parser_down()
        self.add_parser_config()
        self.add_parser_repo()
        self.add_parser_play()

    def add_parser_global(self):
        self.parser.add_argument('-c', metavar='CONFIG_FILE', type=str, help='config json file.')
        self.parser.add_argument('-w', metavar='WIDTH', type=int, help="terminal width.")
        self.parser.add_argument('-v', action='store_true', help='show version.')
        self.parser.add_argument('-m', action='store_true', help='monochromatic debug.')

    def create_parent_basic(self):
        parent_basic = argparse.ArgumentParser(add_help=False)
        parent_basic.add_argument('--index', '-i', metavar="I", type=int, help='run a specific index.')
        parent_basic.add_argument('--pattern', '-p', metavar="P", type=str, default='@.in @.sol',
                                  help='pattern load/save a folder, default: "@.in @.sol"')
        return parent_basic

    def create_parent_manip(self):
        parent_manip = argparse.ArgumentParser(add_help=False)
        parent_manip.add_argument('--width', '-w', type=int, help="term width.")
        parent_manip.add_argument('--unlabel', '-u', action='store_true', help='remove all labels.')
        parent_manip.add_argument('--number', '-n', action='store_true', help='number labels.')
        parent_manip.add_argument('--sort', '-s', action='store_true', help="sort test cases by input size.")
        parent_manip.add_argument('--pattern', '-p', metavar="@.in @.out", type=str, default='@.in @.sol',
                                  help='pattern load/save a folder, default: "@.in @.sol"')
        return parent_manip

    def add_parser_run(self):
        parser_r = self.subparsers.add_parser('run', parents=[self.parent_basic], help='run with test cases using curses.')
        parser_r.add_argument('target_list', metavar='T', type=str, nargs='*', help='solvers, test cases or folders.')
        parser_r.add_argument('--filter', '-f', action='store_true', help='filter solver in temp dir before run')
        parser_r.add_argument("--cmd", type=str, help="bash command to run code")
        parser_r.set_defaults(func=Main.run)

    def add_parser_go(self):
        parser_r = self.subparsers.add_parser('go', parents=[self.parent_basic], help='run with test cases.')
        parser_r.add_argument('target_list', metavar='T', type=str, nargs='*', help='solvers, test cases or folders.')
        parser_r.add_argument('--filter', '-f', action='store_true', help='filter solver in temp dir before run')
        parser_r.add_argument('--compact', '-c', action='store_true', help='Do not show case descriptions in failures')
        parser_r.add_argument("--cmd", type=str, help="bash command to run code")

        group_n = parser_r.add_mutually_exclusive_group()
        group_n.add_argument('--quiet', '-q', action='store_true', help='quiet mode, do not show any failure.')
        group_n.add_argument('--all', '-a', action='store_true', help='show all failures.')

        # add an exclusive group for diff mode
        group = parser_r.add_mutually_exclusive_group()
        group.add_argument('--down', '-d', action='store_true', help="diff mode up-to-down.")
        group.add_argument('--side', '-s', action='store_true', help="diff mode side-by-side.")
        parser_r.set_defaults(func=Main.go)

    def add_parser_build(self):
        parser_b = self.subparsers.add_parser('build', parents=[self.parent_manip], help='build a test target.')
        parser_b.add_argument('target', metavar='T_OUT', type=str, help='target to be build.')
        parser_b.add_argument('target_list', metavar='T', type=str, nargs='+', help='input test targets.')
        parser_b.add_argument('--force', '-f', action='store_true', help='enable overwrite.')
        parser_b.set_defaults(func=Main.build)

    def add_parser_down(self):
        parser_d = self.subparsers.add_parser('down', help='download problem from repository.')
        parser_d.add_argument('course', type=str, nargs='?', help=" [ fup | ed | poo ].")
        parser_d.add_argument('activity', type=str, nargs='?', help="activity @label.")
        parser_d.add_argument('--language', '-l', type=str, nargs='?', help="[ c | cpp | js | ts | py | java ]")
        parser_d.set_defaults(func=Main.down)

    def add_parser_config(self):
        parser_s = self.subparsers.add_parser('config', help='settings tool.')

        g_diff = parser_s.add_mutually_exclusive_group()
        g_diff.add_argument('--side', action='store_true', help='set side_by_side diff mode.')
        g_diff.add_argument('--down', action='store_true', help='set up_to_down   diff mode.')

        g_lang = parser_s.add_mutually_exclusive_group()
        g_lang.add_argument("--lang", '-l', metavar='ext', type=str, help="set default language extension.")
        g_lang.add_argument("--ask", action='store_true', help='ask language extension every time.')

        parser_s.add_argument("--root", metavar="path", type=str, help='set root directory.')
        parser_s.add_argument("--editor", metavar="cmd", type=str, help='set editor command.')

        parser_s.set_defaults(func=Main.config)

    def add_parser_repo(self):
        parser_repo = self.subparsers.add_parser('rep', help='manipulate repositories.')
        subpar_repo = parser_repo.add_subparsers(title='subcommands', help='help for subcommand.')

        repo_list = subpar_repo.add_parser('list', help='list all repositories')
        repo_list.set_defaults(func=CmdRep.list)

        repo_add = subpar_repo.add_parser('add', help='add a repository.')
        repo_add.add_argument('alias', metavar='alias', type=str, help='alias of the repository to be added.')
        repo_add.add_argument('--url', '-u', type=str, help='add a repository url to the settings file.')
        repo_add.add_argument('--file', '-f', type=str, help='add a repository file to the settings file.')
        repo_add.set_defaults(func=CmdRep.add)

        repo_rm = subpar_repo.add_parser('rm', help='remove a repository.')
        repo_rm.add_argument('alias', metavar='alias', type=str, help='alias of the repository to be removed.')
        repo_rm.set_defaults(func=CmdRep.rm)

        repo_reset = subpar_repo.add_parser('reset', help='reset all repositories to factory default.')
        repo_reset.set_defaults(func=CmdRep.reset)

        repo_graph = subpar_repo.add_parser('graph', help='generate graph of the repository.')
        repo_graph.add_argument('alias', metavar='alias', type=str, help='alias of the repository to be graphed.')
        repo_graph.set_defaults(func=CmdRep.graph)

    def add_parser_play(self):
        parser_p = self.subparsers.add_parser('play', help='play a game.')
        parser_p.add_argument('repo', metavar='repo', type=str, nargs="?", default="__ask", help='repository to be played.')
        # parser_p.add_argument("--graph", "-g", action='store_true', help='generate graph of the game using graphviz.')
        # parser_p.add_argument("--svg", "-s", action='store_true', help='generate graph in svg instead png.')
        parser_p.set_defaults(func=Main.play)


def exec(parser: argparse.ArgumentParser, args):
    settings = Settings()
    if args.w is not None:
        Report.set_terminal_size(args.w)
    if args.c:
        settings.set_settings_file(args.c)
    settings.load_settings()

    if args.m:
        TermColor.enabled = False
    else:
        TermColor.enabled = True
        symbols.set_colors()

    if args.v:
        if args.v:
            print("tko version " + __version__)
    else:
        if "func" in args:
            args.func(args)
        else:
            parser.print_help()

def main():
    try:
        parser = Parser().parser
        args = parser.parse_args()
        exec(parser, args)
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nKeyboard Interrupt")
        sys.exit(1)
    except Warning as w:
        print(w)
        sys.exit(1)
    # except Exception as e:
    #     print(e)
    #     sys.exit(1)


if __name__ == '__main__':
    main()