FROM python:3
WORKDIR /
RUN mkdir -p /upload_folder
RUN apt-get -y update
ADD requirements.txt /
ADD app.py /
ADD database.db /
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python3", "./app.py"]
