import threading
import time
import random
from queue import Queue


# Класс стол, который хранит номер стола и текущего гостя
class Table:
    def __init__(self, number):
        self.number = number  # Номер стола
        self.guest = None  # Гость, сидящий за столом (по умолчанию None)


# Класс гость, который является потоком
class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Имя гостя

    # Метод, запускаемый при начале потока (гость кушает)
    def run(self):
        # Симуляция времени приема пищи от 3 до 10 секунд
        eating_time = random.randint(3, 10)
        print(f"{self.name} начал(а) кушать.")
        time.sleep(eating_time)
        print(f"{self.name} закончил(а) кушать и ушёл(ушла).")


# Класс кафе, который управляет процессом рассадки и обслуживания гостей
class Cafe:
    def __init__(self, *tables):
        self.tables = list(tables)  # Список столов
        self.queue = Queue()  # Очередь гостей

    # Метод для принятия новых гостей
    def guest_arrival(self, *guests):
        for guest in guests:
            seated = False
            # Проходим по столам и ищем свободный
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    guest.start()  # Запускаем поток гостя (он начинает кушать)
                    seated = True
                    break
            # Если нет свободных столов, гость становится в очередь
            if not seated:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    # Метод для обслуживания гостей
    def discuss_guests(self):
        # Процесс идет до тех пор, пока очередь не пуста или за столом есть гости
        while not self.queue.empty() or any(table.guest for table in self.tables):
            for table in self.tables:
                guest = table.guest
                # Если за столом есть гость и он закончил кушать (поток завершился)
                if guest and not guest.is_alive():
                    print(f"{guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

            # Если стол освободился и есть гости в очереди
            for table in self.tables:
                if table.guest is None and not self.queue.empty():
                    next_guest = self.queue.get()
                    table.guest = next_guest
                    print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                    next_guest.start()  # Запускаем поток гостя (он начинает кушать)

            # Короткая пауза между проверками
            time.sleep(1)


if __name__ == "__main__":
    # Создаем столы
    tables = [Table(number) for number in range(1, 6)]

    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    # Создаем гостей
    guests = [Guest(name) for name in guests_names]

    # Инициализируем кафе с созданными столами
    cafe = Cafe(*tables)

    # Приход гостей
    cafe.guest_arrival(*guests)

    # Обслуживание гостей
    cafe.discuss_guests()
