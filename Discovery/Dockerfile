FROM python:3.9
WORKDIR /PAD
COPY ./ /PAD/Discovery/
EXPOSE 6969
RUN pip install -r /PAD/Discovery/requirements.txt

CMD ["uvicorn", "Discovery.discovery_main:app", "--host", "0.0.0.0", "--port", "6969"]