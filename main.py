# PROJECT -CRUD operation-> CRUD refers to create read update delete 

import os
from pathlib import Path
def readfileandfolder():
  try:
    p=Path('')
    items=list(p.rglob('*'))
    for index , file in enumerate(items):
        print(f'{index+1 } - { file}')
  except Exception as e:
      print(e)
def create_file():
  try :
    readfileandfolder()
    file_name=input("enter name of your file : ")
    p=Path(file_name)
    if p.exists():
        print('file already exists')
    else:
        with open(file_name,'w') as file:
           content= input("batao jo jo likhna hai : ")
           file.write(content)
           print("file added")
  except Exception as e:
      print(e)

def read_file():
   try:
     readfileandfolder()
     file_name=input("enter name of your file :")
     p=Path(file_name)
     if p.exists():
         with open(file_name,'r') as file:
             print(file.read())
     else:
         print('file not found')
   except Exception as e: 
      print(e)
def update_file():
    try :
        readfileandfolder()
        file_name=input("enter your file name :" )
        p=Path(file_name)
        if p.exists():
          print("Press 1 to overwrite the content ")
          print("Press 2 to append new content ")
          option = int(input("enter your option : "))
          if option==1:
            with open(file_name,'w') as file:
              content =input("enter your content:")
              file.write(content)
              print('content chnged .... ')
          elif option ==2:
            with open(file_name,'a') as file:
               content =input("enter your content:")
               file.write(content)
               print('content updated.... ')
          else:
              print("invalid input")
        else:
          print("file doesnt exist")
    except Exception as e :
       print(e)

def delete_file():
    try:
        readfileandfolder()
        file_name=input("enter your file name :" )
        p=Path(file_name)
        if p.exists():
            os.remove(p)
            print("file deleted")
        else:
            print("file doesnt exist")
    except Exception as e:
       print(e)

def rename_file():
    readfileandfolder()
    file_name=input("enter your file name : ")
    p = Path(file_name)
    if p.exists():
      new_file=input("enter your new name : ")
      p.rename(new_file)
      print("File renamed ")
    else:
       print("file not exist")

def create_folder():
    readfileandfolder()
    folder_name=input("Enter your folder name : ")
    p=Path(folder_name)
    if p.exists():
       print("already exists !!!!!!!")
    else:
       p.mkdir()
       print("FOLDER CREATED !!")

def remove_folder():
    readfileandfolder()
    folder_name=input("enter your folder name : ")
    p =Path(folder_name)
    if p.exists():
       p.rmdir()
       print("hata diya folder !!!!!!!")
    else:
       print("folder banana pdega bhai aapko...")

# def create_file_in_folder():
#    folder_name=input("enter your folder name :")
#    file_name = input("enter your file name")
#    p=Path(folder_name)/(file_name)
#    if p.exists():
#       print("file hai already")
#    else:
#       with open(p,'w') as file:
#         content= input("batao jo jo likhna hai : ")
#         file.write(content)
#         print("file added")
         
while True:
    print("Press 1 for creating a file")
    print("Press 2 for reading a file")
    print("Press 3 for updating a file")
    print("Press 4 for deleting a file")
    print("Press 5 for renaming a file")
    print("Press 6 for creating a folder")
    print("Press 7 for removing a folder ")
   #  print("Press 8 for creting file in folder")
    print("press 0 for exit ")

    option = int(input("enter your option : "))
    if option ==1:
       create_file()
    if option==2:
       read_file()
    if option ==3 :
       update_file()
    if option==4:
       delete_file()
    if option == 5:
       rename_file()
    if option == 6:
       create_folder()
    if option == 7 :
       remove_folder()
   #  if option == 8:
   #     create_file_in_folder()
    if option==0:
       break 

