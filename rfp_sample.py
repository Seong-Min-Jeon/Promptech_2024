import pandas as pd

print('Made by 전성민')
print('')
print('본 exe 파일과 같은 폴더에 같은 이름의 [RFP txt파일]과 [비어있는 xlsx파일]이 존재해야됩니다!')
print('예) rfp_law.txt, rfp_law.xlsx')
print('자세한 설명은 설명서를 참고해주세요!')
print('')

name = input('파일명을 입력해주세요(English): ')
print('')
print('변환이 끝나면 자동으로 종료됩니다..')
print('')
print('')

try:        
    excel_name = name + '.xlsx'
    f = open(name + '.txt', 'r', encoding='UTF8')

    new_data = {}
    store = ''
    desc = ''
    desc_lines = []

    while True:
        line = f.readline()                

        if not line:
            break

        if line == '' and len(new_data) == 6:
            pass
            
        if line.strip() == '요구사항 고유번호':                    
            store = ''
            
            if(new_data.get('요구사항 고유번호') != None):
                print(new_data.get('요구사항 고유번호'), "------ 작업 완료")

            df = pd.read_excel(excel_name, engine='openpyxl')
            df_new = pd.DataFrame(new_data)
            df_combined = pd.concat([df, df_new], ignore_index=False)  # OLD: df_combined = df.append(df_new, ignore_index=False)
            df_combined.to_excel(excel_name, index=False)     
            new_data = {}                     

            for i in range(len(desc_lines)-1):
                new_data['세부 내용'] = [desc_lines[i+1]]
                df = pd.read_excel(excel_name, engine='openpyxl')
                df_new = pd.DataFrame(new_data)
                df_combined = pd.concat([df, df_new], ignore_index=False)     
                df_combined.to_excel(excel_name, index=False) 
            new_data = {}       
            desc_lines = []

        elif line.strip() == '요구사항 명칭':
            if '\n' in store:
                store = store.split('\n')[1]
            new_data['요구사항 고유번호'] = [store]
            store = ''        
        elif line.strip() == '요구사항 분류':
            new_data['요구사항 명칭'] = [store]
            store = ''
        elif line.strip() == '요구사항':
            new_data['요구사항 분류'] = [store]
            store = ''
        elif line.strip() == '상세설명':
            pass
        elif line.strip() == '정의':
            pass
        elif line.strip() == '세부' or line.strip() == '세부내용':
            new_data['정의'] = [store]
            store = ''
        elif line.strip() == '내용' or line.strip() == '규격':
            pass
        elif line.strip() == '산출정보':
            desc = store
            
            #세부내용 통으로 묶어야될 때 주석처리
            # if(desc[0] == 'ㅇ' or desc[0] == '◦' or desc[0] == 'o'):
            #     desc = '○' + desc[1:]
            # desc = desc.replace('\nㅇ', '\n○').replace('\n◦', '\n○').replace('\no', '\n○').replace('\n○', '\n○') 
            # desc_lines = desc.split('\n○')
            # for i in range(len(desc_lines)-1):
            #     desc_lines[i+1] = '○' + desc_lines[i+1]
            # new_data['세부 내용'] = [desc_lines[0]]    

            #세부내용 나눌 때 주석처리
            new_data['세부 내용'] = [desc]         
            store = ''
        elif line.strip() == '관련 요구사항':
            new_data['산출정보'] = [store]
            store = ''        
        else:
            if store == '':
                store += line.rstrip()               
            else:
                store += '\n' + line.rstrip()    

    print(new_data.get('요구사항 고유번호'), "------ 작업 완료")

    df = pd.read_excel(excel_name, engine='openpyxl')
    df_new = pd.DataFrame(new_data)
    df_combined = pd.concat([df, df_new], ignore_index=False)     
    df_combined.to_excel(excel_name, index=False)       
    new_data = {}                        

    for i in range(len(desc_lines)-1):
        new_data['세부 내용'] = [desc_lines[i+1]]
        df = pd.read_excel(excel_name, engine='openpyxl')
        df_new = pd.DataFrame(new_data)
        df_combined = pd.concat([df, df_new], ignore_index=False)     
        df_combined.to_excel(excel_name, index=False) 
    desc_lines = []

    f.close()
except Exception as e:
    print(e)
    exit(0)