# django_api
이 프로젝트는 Django REST 프레임워크를 사용하여 작성된 API입니다.
<br><br><br>
## 프로젝트 설명
이 API는 적요분류를 위해 데이터(.csv)을 검사하고 서버의 적요분류 스케쥴링 프로세스에 Task를 넘겨줍니다. 
<br><br><br>
## 기술 스택
- python 3.8
- django 4.2
- django rest framework 3.14
<br><br><br>
## 사용 방법

1. 엔드포인트(Endpoints)
	| HTTP 메소드| 엔드포인트|설명|
	|:--------:|:--------:|:--------:|
	| POST     | /api/cf       |- 기업ID, 등록일시를 통해 결과파일을 저장할 경로폴더 생성<br>- 업로드파일명(경로)를 통해 WEB서버에 있는 파일을 sftp로 다운로드<br>- 파일에 인코딩 또는 데이터 갯수 등의 문제가 있는지 검사<br>- TB_TAGG_HIST 테이블 상태코드를 0110(API서버에 파일저장 완료)으로 변경<br>- 위 내용 수행시 에러가 없으면 HTTP: 201 에러가 생기면 HTTP: 500 응답|

2. 요청(Requests)
	| 매개변수| 유형| 필수 여부| 설명|
	|:-------------:|:-------:|:---------:|:-----------:|
	| CORP_ID       | string  |     Y     | 기업ID    	|
	| MODEL_ID      | string  |     N     | 모델ID    	|
	| UPLD_FILE_NM  | string  |     Y     | 업로드파일명 |
	| REG_DT     	| string  |     Y     | 등록일시     |

3. 응답(Responses)
	| HTTP 상태 코드| 응답 본문(JSON)| 비고|
	|:--------------:|:----------:|:---------------:|
	| 200            | {"result": True}||
	| 500            | {"result": False,<br>"error": <파이썬 예외처리 문구>,<br>"code": <에러코드>}|- 파일에 오류가 있을경우 에러목록.txt의 2.0. 참고하여 에러 출력| 											   
	| 400            | 	<에러키>: <에러이유>|- 형식에 맞지않는 key(매개변수)가 들어오면 해당 key를 key로 에러가 발생한 이유를 value로 출력합니다.	|
	
4. 샘플코드

	- 4.0. 엔드포인트 및 data
		- 4.0.1 엔드포인트
			| HTTP 메소드| 엔드포인트       			   |
			|:--------:|:-------------------------:|
			| POST     | http://172.25.3.61/api/cf |
		

		- 4.0.2 data
			| key 	 		| value   			   |
			|:-------------:|:--------------------:|
			| CORP_ID       | blabla2023  		   |
			| MODEL_ID      | BLB_1.0.0  		   |
			| UPLD_FILE_NM  | /path/to/test.csv    |
			| REG_DT     	| 2023-04-13 16:30:43  |

	- 4.1. java-OkHttp
		``` java
		OkHttpClient client = new OkHttpClient().newBuilder()
		  .build();
		MediaType mediaType = MediaType.parse("text/plain");
		RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
		  .addFormDataPart("CORP_ID","blabla2023")
		  .addFormDataPart("MODEL_ID","BLB_1.0.0")
		  .addFormDataPart("UPLD_FILE_NM","/path/to/test.csv")
		  .addFormDataPart("REG_DT","2023-04-13 16:30:43")
		  .build();
		Request request = new Request.Builder()
		  .url("http://172.25.3.61/api/cf")
		  .method("POST", body)
		  .build();
		Response response = client.newCall(request).execute();
		```
		
	- 4.2. java-Unirest
		``` java
		Unirest.setTimeouts(0, 0);
		HttpResponse<String> response = Unirest.post("http://172.25.3.61/api/cf")
		  .multiPartContent()
		  .field("CORP_ID", "blabla2023")
		  .field("MODEL_ID", "BLB_1.0.0")
		  .field("UPLD_FILE_NM", "/path/to/test.csv")
		  .field("REG_DT", "2023-04-13 16:30:43")
		  .asString();
		```
		
	- 4.3. javaScript-Fetch
		``` javaScript
		var formdata = new FormData();
		formdata.append("CORP_ID", "blabla2023");
		formdata.append("MODEL_ID", "BLB_1.0.0");
		formdata.append("UPLD_FILE_NM", "/path/to/test.csv");
		formdata.append("REG_DT", "2023-04-13 16:30:43");

		var requestOptions = {
		  method: 'POST',
		  body: formdata,
		  redirect: 'follow'
		};

		fetch("http://172.25.3.61/api/cf", requestOptions)
		  .then(response => response.text())
		  .then(result => console.log(result))
		  .catch(error => console.log('error', error));
		```
		
	- 4.4. javaScript-jQuery
		``` javaScript
		var form = new FormData();
		form.append("CORP_ID", "blabla2023");
		form.append("MODEL_ID", "BLB_1.0.0");
		form.append("UPLD_FILE_NM", "/path/to/test.csv");
		form.append("REG_DT", "2023-04-13 16:30:43");

		var settings = {
		  "url": "http://172.25.3.61/api/cf",
		  "method": "POST",
		  "timeout": 0,
		  "processData": false,
		  "mimeType": "multipart/form-data",
		  "contentType": false,
		  "data": form
		};

		$.ajax(settings).done(function (response) {
		  console.log(response);
		});
		```

	- 4.5. javaScript-XHR
		``` javaScript
		// WARNING: For POST requests, body is set to null by browsers.
		var data = new FormData();
		data.append("CORP_ID", "blabla2023");
		data.append("MODEL_ID", "BLB_1.0.0");
		data.append("UPLD_FILE_NM", "/path/to/test.csv");
		data.append("REG_DT", "2023-04-13 16:30:43");

		var xhr = new XMLHttpRequest();
		xhr.withCredentials = true;

		xhr.addEventListener("readystatechange", function() {
		  if(this.readyState === 4) {
			console.log(this.responseText);
		  }
		});

		xhr.open("POST", "http://172.25.3.61/api/cf");

		xhr.send(data);
		```

## License
For open source projects, say how it is licensed.


