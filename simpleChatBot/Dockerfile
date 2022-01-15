FROM python

# Env variables are unused in this project
ENV CHATBOT_USERNAME=admin\
    CHAT_BOTPASSWORD=password

RUN mkdir -p /home/app

COPY ./app /home/app

RUN pip install -r /home/app/requirements.txt
RUN python ./home/app/init.py

CMD ["python","/home/app/main.py"]