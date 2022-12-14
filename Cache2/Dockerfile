FROM python:3.9
WORKDIR /PAD
COPY ./ /PAD/Cache/
EXPOSE 8078
RUN pip install -r /PAD/Cache/requirements.txt

CMD ["uvicorn", "Cache.cache_main:app", "--host", "0.0.0.0", "--port", "8078"]