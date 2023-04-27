import pymysql
import yaml
import paramiko
import os

# 변수들어있는 파일 불러오기
with open('./config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# mysql 접속 및 상태처리코드 수정하기
def connect_mysql_change_cd(corp_id, updl_file_nm, reg_dt, model_id, prcs_cd):
    
    # mysql 접속
    connection = pymysql.connect(host=config['mysql_host'], 
                                user=config['mysql_user'], 
                                password=config['mysql_password'], 
                                db=config['mysql_db'], 
                                charset='utf8')
    cursor = connection.cursor()
    
    # select 조건문으로 pk 찾기
    query = "select SEQ_NO from TB_TAGG_HIST_copy where CORP_ID=%s and \
                                                        UPLD_FILE_NM=%s and \
                                                        REG_DT=%s and \
                                                        MODEL_ID=%s;"
    cursor.execute(query, (corp_id, updl_file_nm, reg_dt, model_id))
    seq_no = [int(row[0]) for row in cursor.fetchall()]

    # select 조건문으로 찾은 pk가 1개일 경우 상태코드 수정
    if len(seq_no) == 1:
        query = "update TB_TAGG_HIST_copy set PRCS_CD=%s where SEQ_NO=%s;"
        cursor.execute(query, (prcs_cd, seq_no[0]))
    
    # 연결종료
    connection.commit()
    connection.close()


# ssh 접속 및 sftp 열고 업무수행하기
def connect_ssh(local_path, remote_file_path, work='download'):
    
    # ssh 접속 및 sftp 열기
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(config['ssh_host'], 
                       config['ssh_port'], 
                       config['ssh_username'], 
                       config['ssh_password'])
    sftp_client = ssh_client.open_sftp()

    if work == 'download':
        # 파일명 추출
        remote_file = os.path.basename(remote_file_path)
        local_file_path = os.path.join(local_path, remote_file)
        
        # 다운로드
        sftp_client.get(remote_file_path, local_file_path) 
        
        # sftp 및 ssh 닫기
        sftp_client.close()
        ssh_client.close()
        
        return local_file_path
    
    elif work == 'remove':
        # 삭제
        sftp_client.remove(remote_file_path)
    elif work == 'send':
        # 전송
        sftp_client.put(local_file_path, remote_file_path)



if __name__ == '__main__':
    
    ## test
    corp_id = 'blabla2023'
    updl_file_nm = "upload1.csv"
    reg_dt = "2023-04-13 16:30:47"
    model_id = 'BLB_RealAts_v1.00001'
    prcs_cd = "0110"
    connect_mysql_change_cd(corp_id, updl_file_nm, reg_dt, model_id, prcs_cd)
        
    remote_file_path = "/home/manager/work/file/test.csv"
    work='download'
    connect_ssh(corp_id, reg_dt, remote_file_path, work)
    
    
    
    
    