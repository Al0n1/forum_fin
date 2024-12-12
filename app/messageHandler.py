import os
import json
import pika
from dotenv import dotenv_values
config = dotenv_values(".env")


# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, properties, body):
    body = json.loads(body)
    print(f"Received: '{body}'")

    with open(os.getcwd() + '/messages.json', 'r') as json_file:
        messages = json.load(json_file)

    messages['messages'].append(body)

    with open(os.getcwd() + '/messages.json', 'w') as json_file:
        json.dump(messages, json_file)


class MessageHandler:
    def __init__(self):
        self.connection_params = pika.ConnectionParameters(
            host=config['RABBITMQ_HOST'],  # Замените на адрес вашего RabbitMQ сервера
            port=config['RABBITMQ_PORT'],  # Порт по умолчанию для RabbitMQ
            virtual_host=config['RABBITMQ_VHOST'],  # Виртуальный хост (обычно '/')
            credentials=pika.PlainCredentials(
                username=config['RABBITMQ_USER'],  # Имя пользователя по умолчанию
                password=config['RABBITMQ_PASSWORD']  # Пароль по умолчанию
            )
        )
        # Установка соединения
        connection = pika.BlockingConnection(self.connection_params)

        # Создание канала
        channel = connection.channel()

        # Имя очереди
        queue_name = config['RABBITMQ_QUEUE_NAME']

        # Создание очереди и настройка его параметров (доступность, привязка к хосту)
        channel.queue_declare(queue=queue_name, durable=True)

        # Подписка на очередь и установка обработчика сообщений
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True  # Автоматическое подтверждение обработки сообщений
        )

        print('Waiting for messages. To exit, press Ctrl+C')
        channel.start_consuming()
