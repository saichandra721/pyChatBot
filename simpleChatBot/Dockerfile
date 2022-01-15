FROM python

# Env variables are unused in this project
ENV CHATBOT_USERNAME=admin\
    CHAT_BOTPASSWORD=password

RUN mkdir -p /home/app

COPY . /home/app

RUN pip install -r requirements.txt
RUN python ./home/app/simpleChatBot/init.py

CMD["python","./simpleChatBot/main.py"]