from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TagghistSerializer

import sys
sys.path.append('/home/manager/django_api') # 상위 디렉토리 추가
from connect_server import connect_mysql_change_cd, connect_ssh
from utils import make_original_folder, check_file

# Create your views here.

class AddSchedule(APIView):
    def post(self, request):
        
        # request 데이터 형식 확인
        serializer = TagghistSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            # 폴더 생성
            local_path = make_original_folder(data['CORP_ID'], data['REG_DT'])
            
            # 파일 다운로드
            try:
                local_file_path = connect_ssh(local_path, data['UPLD_FILE_NM'], work='download')
            except Exception as e:
                return Response({"result": False,
                                 "error": str(e),
                                 "code": "0111"}, 
                                 status = status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 파일 검사
            result = check_file(local_file_path)
            if result[0] != "0110":
                # 파일 검사 결과 데이터에 오류가 있으면 해당 에러코드 반환
                return Response({"result": False,
                                 "error": result[1],
                                 "code": result[0]}, 
                                 status = status.HTTP_500_INTERNAL_SERVER_ERROR)

            # mysql 접속 및 상태코드 변경
            connect_mysql_change_cd(data['CORP_ID'], data['UPLD_FILE_NM'], data['REG_DT'], data['MODEL_ID'], "0110")

            return Response({"result":True}, status = status.HTTP_200_OK)
        else:
            # request 데이터 형식이 맞지 않을 경우
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

