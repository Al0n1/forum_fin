import pika
from dotenv import dotenv_values
config = dotenv_values(".env")


class MessageSender:
    def __init__(self):
        self.connection_params = pika.ConnectionParameters(
            host=config['RABBITMQ_HOST'],  # Замените на адрес вашего RabbitMQ сервера
            port=config['RABBITMQ_PORT'],          # Порт по умолчанию для RabbitMQ
            virtual_host=config['RABBITMQ_VHOST'],   # Виртуальный хост (обычно '/')
            credentials=pika.PlainCredentials(
                username=config['RABBITMQ_USER'],  # Имя пользователя по умолчанию
                password=config['RABBITMQ_PASSWORD']   # Пароль по умолчанию
            )
        )

    def send_message(self, message) -> dict:
        try:
            # Установка соединения
            connection = pika.BlockingConnection(self.connection_params)

            # Создание канала
            channel = connection.channel()

            # Имя очереди
            queue_name = config['RABBITMQ_QUEUE_NAME']

            # Отправка сообщения
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message
            )

            print(f"Sent: '{message}'")

            # Закрытие соединения
            connection.close()

            return {"status": True}
        except Exception as e:
            return {"status": False, "error_message": str(e)}
