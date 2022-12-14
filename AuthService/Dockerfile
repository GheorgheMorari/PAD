FROM python:3.9
WORKDIR /PAD
COPY ./ /PAD/AuthService/
EXPOSE 8081
RUN pip install -r /PAD/AuthService/requirements.txt

CMD ["uvicorn", "AuthService.auth_service_main:app", "--host", "0.0.0.0", "--port", "8081"]