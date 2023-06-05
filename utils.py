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
def check_file(local_path, model_id):
    
    # 파일 인코딩 형식 검사
    try:
        df = pd.read_csv(local_path, encoding="utf-8-sig")
        df_len = len(df)
        df_columns = set(df.columns)
    except UnicodeDecodeError as e:
        return ("0112", "다음의 인코딩 형식을 지원합니다.(utf-8)")
    
    # 데이터 형식 검사
    model_path = os.getenv("model_path")
    sample_path = os.path.join(model_path, model_id, "sample_file.csv")
    try:
        s_df = pd.read_csv(sample_path, encoding="utf-8-sig")
        s_df_columns = set(s_df.columns) 
        s_df_columns.discard("Unnamed: 0")
    except UnicodeDecodeError as e:
        return ("0000", "샘플파일은 다음의 인코딩 형식을 지원합니다.(utf-8) \n 관리자에게 문의바랍니다.")
    
    use_columns = (df_columns & s_df_columns)    
    if use_columns != s_df_columns:
        not_found_column = "/".join(list(s_df_columns - use_columns))
        return ("0113", "%s 컬럼이 없습니다.\n 데이터 내용을 확인하세요.\n (필수컬럼:%s)"%(not_found_column, "/".join(s_df_columns)))

    return ("0110" , "Sucess", df_len)
    