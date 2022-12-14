FROM python:3.9
WORKDIR /PAD
COPY ./ /PAD/MessagingService/
EXPOSE 8069
RUN pip install -r /PAD/MessagingService/requirements.txt

CMD ["uvicorn", "MessagingService.messaging_service_main:app", "--host", "0.0.0.0", "--port", "8069"]