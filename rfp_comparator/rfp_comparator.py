import os
import time
from difflib import context_diff

def find_files(file_name1, file_name2):
    # 이름으로 파일을 찾고 경로를 반환
    file_path1 = file_name1 + '.txt'
    file_path2 = file_name2 + '.txt'
    files_found = True
    
    if not os.path.exists(file_path1):
        print(f"'{file_path1}'을 찾을 수 없습니다.")
        files_found = False
    
    if not os.path.exists(file_path2):
        print(f"'{file_path2}'을 찾을 수 없습니다.")
        files_found = False
        
    if not files_found:
        time.sleep(3)
        exit(1)
    
    return file_path1, file_path2

def compare_files(file_path1, file_path2):
    # 두 파일의 내용을 비교하고 다른 점을 result.txt에 기록
    with open(file_path1, 'r', encoding='utf-8') as file1, \
         open(file_path2, 'r', encoding='utf-8') as file2, \
         open('result.txt', 'w', encoding='utf-8') as result:
        diff = context_diff(file1.readlines(), file2.readlines(), n=3, fromfile='file1', tofile='file2')
        prior_line = ""
        for line in diff:
            if(line.startswith('!') or line.startswith('+')):
                if(prior_line==""):
                    prior_line = line
                    continue
                if(prior_line.rstrip() != line.rstrip()):
                    print("사전공고: " + prior_line[1:])
                    print("본공고: " + line[1:])
                    print("")
                prior_line=""                

name1 = input("사전공고 RFP txt파일명: ")
name2 = input("본공고 RFP txt파일명: ")

file_path1, file_path2 = find_files(name1, name2)

compare_files(file_path1, file_path2)