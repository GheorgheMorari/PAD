FROM python:3.9
WORKDIR /PAD
COPY ./ /PAD/SpellcheckerService/
EXPOSE 8082
RUN pip install -r /PAD/SpellcheckerService/requirements.txt

CMD ["uvicorn", "SpellcheckerService.spellchecker_main:app", "--host", "0.0.0.0", "--port", "8082"]