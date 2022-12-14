FROM python:3.9
WORKDIR /PAD
COPY ./ /PAD/ToxicityDetectionService/
EXPOSE 8085
RUN pip install -r /PAD/ToxicityDetectionService/requirements.txt

CMD ["uvicorn", "ToxicityDetectionService.toxicity_detection_main:app", "--host", "0.0.0.0", "--port", "8085"]