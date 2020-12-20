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


API ENDPINTS - 
- /upload  -  Uploads the file to server and starts a background thread to process.
- /upload/pause - Pauses the background task.
- /upload/cancel - Cancels/Terminates the background task.
- /upload/resume - Resumses the background task from where it was stop/pause.

Method - 
- start_processing_the_uploaded_file(file_name,start=0)  - takes two arguments file name and the starting point in the file to be processed.
