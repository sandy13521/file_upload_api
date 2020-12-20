# file_upload_api

Steps to Build -
- docker build -t sandy13521/file_upload_api:latest 

How to Run - 
- docker run -d sandy13521/file_upload_api:latest

ScreenShots - 
1. Starting Page -

![Alt text](images/start.png?raw=true "Start")

2. After clicking the Upload button - Uploading starts and after the file is uploaded. Processing of the uploaded file starts using a thread in the background. The processing of the file can be paused or cancelled by the user. Once Paused user can resume the process from the point it was paused.

![Alt text](images/upload_processing_started.png?raw=true "Processing in the background.")


