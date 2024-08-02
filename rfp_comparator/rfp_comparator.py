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
        time.sleep(2)
        exit(1)
    
    return file_path1, file_path2

def compare_files(file_path1, file_path2, prior_rfp, new_rfp, add_sentence, drop_sentence):
    # 사전공고와 비교했을 때 본공고에서 추가됐거나, 워딩이 다른 것 추출
    with open(file_path1, 'r', encoding='utf-8') as file1, \
         open(file_path2, 'r', encoding='utf-8') as file2: 
        temp = 0
        diff = context_diff(file1.readlines(), file2.readlines(), n=3, fromfile='file1', tofile='file2')        
        for line in diff:            
            new_line = line[1:].strip()
            if(new_line == ''): continue
            if(line.startswith('!')):                
                if(temp == 0):                    
                    prior_rfp.append(new_line)
                    temp = 1
                    continue
                if(temp == 1):
                    new_rfp.append(new_line)
                    temp = 0
                    continue        
            if(line.startswith('+')):
                add_sentence.append(new_line)                   
    # 사전공고와 비교했을 때 본공고에서 삭제된 것 추출
    with open(file_path1, 'r', encoding='utf-8') as file1, \
         open(file_path2, 'r', encoding='utf-8') as file2:      
        temp = 0
        diff = context_diff(file2.readlines(), file1.readlines(), n=3, fromfile='file2', tofile='file1')        
        for line in diff:            
            new_line = line[1:].strip()
            if(new_line == ''): continue
            if(line.startswith('+')):
                drop_sentence.append(new_line)        

def write_file(prior_rfp, new_rfp, add_sentence, drop_sentence):
    # result.txt에 작성
    with open('result.txt', 'w', encoding='utf-8') as result:
        result.write('1. 사전공고와 본공고에서 차이가 있는 부분')
        result.write('\n')
        intersection = set(prior_rfp) & set(new_rfp)
        prior_rfp = list(set(prior_rfp) - intersection)
        new_rfp = list(set(new_rfp) - intersection)

        result.write('===사전공고 RFP===')
        result.write('\n')
        for line in prior_rfp:
            result.write(line)
            result.write('\n')
            result.write('\n')
        result.write('\n')
        result.write('\n')
        result.write('===본공고 RFP===')
        result.write('\n')
        for line in new_rfp:
            result.write(line)    
            result.write('\n')
            result.write('\n')
        result.write('\n')
        result.write('\n')
        result.write('\n')
        result.write('2. 사전공고에만 있는 부분')
        result.write('\n')
        for line in drop_sentence:
            result.write(line)    
            result.write('\n')
            result.write('\n')
        result.write('\n')
        result.write('\n')
        result.write('\n')
        result.write('3. 본공고에만 있는 부분')
        result.write('\n')
        for line in add_sentence:
            result.write(line)    
            result.write('\n')
            result.write('\n')

name1 = input("사전공고 RFP txt파일명: ")
name2 = input("본공고 RFP txt파일명: ")

prior_rfp = []
new_rfp = []
add_sentence = []
drop_sentence = []

file_path1, file_path2 = find_files(name1, name2)

compare_files(file_path1, file_path2, prior_rfp, new_rfp, add_sentence, drop_sentence)
write_file(prior_rfp, new_rfp, add_sentence, drop_sentence)