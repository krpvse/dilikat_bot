# Telegram-бот магазин для компании Dilikat

Бот для сбора заявок покупателей с каталогом товаров и корзиной

## В приложении реализовано

- Работа с каталогом товаров через csv-файлы, автоматическое обновление данных в СУБД при наличии изменений в csv-файлах;


- Добавление и изменение данных покупателя в БД, валидаторы ввода данных;


- Корзина товаров: пользователь собирает товары в корзину и отправляет заявку менеджеру (заявку невозможно отправить без заполнения данных о покупателе);


- Отправка уведомлений о новых заказах в Telegram и по e-mail


## Запуск приложения / для разработчиков
___________________________________________

### 1. Установить Docker и Docker Compose: 
````
sh scripts/docker.sh
````
### 2. Создать файл "app/.env" с переменными окружения:
````
sh scripts/generate_env.sh
````
### 3. Освободить порты PostgreSQL и Redis (опционально):
Контейнеры PostgeSQL и Redis работают на портах по умолчанию: 5432 - для PostgreSQL, 6379 - для Redis

### 4. Запустить приложение в контейнерах: 
````
sudo docker-compose up
````
![image](https://github.com/karpov-scripts/dilikat_bot/assets/138283843/4bda5dda-ad76-41ed-b0c5-307279cf5df8)
![image](https://github.com/karpov-scripts/dilikat_bot/assets/138283843/ce87d292-ab8e-4cb6-94b3-91a38778b3f0)
![image](https://github.com/karpov-scripts/dilikat_bot/assets/138283843/b143b3f1-7bab-4ea0-be57-39364fb717fb)
![image](https://github.com/karpov-scripts/dilikat_bot/assets/138283843/088e598f-4c95-46f1-9423-4f13d6a01047)
