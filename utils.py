import os
import pandas as pd

# local에 원본파일 저장경로 생성
def make_original_folder(corp_id):
    local_path = os.getenv("local_path")
    local_path = os.path.join(local_path, corp_id)
    if not os.path.isdir(local_path):
        os.makedirs(local_path)
    return local_path

# 파일 검사
def check_file(path):
    
    # 파일 인코딩 형식 검사
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
        df_len = len(df)
    except UnicodeDecodeError as e:
        return ("0112", "다음의 인코딩 형식을 지원합니다.(utf-8)")
    
    # 데이터 형식 검사
    use_columns = (set(df.columns) & set(["거래구분", "적요"]))    
    if use_columns != {"적요", "거래구분"}:
        not_found_column = str(set(["거래구분", "적요"]) - use_columns)
        return ("0113", "%s 컬럼이 없습니다.\n 데이터 내용을 확인하세요.\n (필수컬럼:거래구분/적요)"%not_found_column)
    
    # 데이터 길이 검사
    #################### 보류
    return ("0110" , "Sucess", df_len)
    