FROM python:3.8
ENV FLASK_APP=main
COPY . /usr/src/main/
WORKDIR /usr/src/main
RUN /usr/local/bin/python -m pip install --upgrade pip --root-user-action=ignore requests
RUN pip3 install --no-cache -r requirements.txt --root-user-action=ignore requests

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
EXPOSE 5000/tcp
