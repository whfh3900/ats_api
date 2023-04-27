import os
import pandas as pd

# 원본파일 저장경로 생성
def make_original_folder(corp_id, reg_dt):
    path = "/home/manager/django_api/media/%s/%s"%(corp_id, reg_dt)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

# 파일 검사
def check_file(path):
    
    # 파일 인코딩 형식 검사
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError as e:
        return ("0112", "다음의 인코딩 형식을 지원합니다.(utf-8)")
    
    # 데이터 형식 검사
    use_columns = (set(df.columns) & set(["입출금구분", "적요텍스트"]))    
    if use_columns != {"적요텍스트", "입출금구분"}:
        not_found_column = str(set(["입출금구분", "적요텍스트"]) - use_columns)
        return ("0113", "%s 컬럼이 없습니다.\n 데이터 내용을 확인하세요.\n (필수컬럼:입출금구분/적요텍스트)"%not_found_column)
    
    # 데이터 길이 검사
    #################### 보류

    return ("0110" , "Sucess")
    