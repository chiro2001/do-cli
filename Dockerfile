FROM python:3.8
MAINTAINER Chiro <Chiro2001@163.com>
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV host=0.0.0.0
ENV port=5000
EXPOSE ${port}
ENTRYPOINT ["python"]
CMD ["server.py", "-l", "${host}", "-p", "${port}"]
