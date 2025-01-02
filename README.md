# Фінальне завдання

Вам необхідно реалізувати найпростіший вебдодаток, не використовуючи вебфреймворк.

### Інструкція та вимоги до виконання

За аналогією до розглянутого в конспекті прикладу, створіть вебдодаток з маршрутизацією для двох html-сторінок: `index.html` та `message.html`. За основу візьміть [наступні файли](https://drive.google.com/file/d/19JPeOCRcW8qG90xW4bCl7A2XvqSfmkpG/view?usp=sharing).

Також:
- обробіть під час роботи програми статичні ресурси: `style.css`, `logo.png`;
- організуйте роботу з формою на сторінці `message.html`;
- у разі виникнення помилки `404 Not Found` повертайте сторінку `error.html`.
- ваш HTTP-сервер повинен працювати на порту `3000`.

Для роботи з формою створіть Socket-сервер на порту `5000`. Алгоритм роботи має бути такий:
- вводите дані у форму,
- вони потрапляють у вебдодаток, який пересилає його далі на обробку за допомогою `socket` (протокол `UDP` або `TCP` на ваш вибір) Socket-серверу,
- Socket-сервер переводить отриманий байт-рядок у словник і зберігає його в базу даних MongoDb.

Формат запису документа MongoDB має бути наступного вигляду:
```
{  
	"date": "2022-10-29 20:20:58.020261",    
	"username": "krabaton",    
	"message": "First message"  
},  
{ 
	"date": "2022-10-29 20:21:11.812177",
    "username": "Krabat",    
	"message": "Second message"  
}
```

Ключ `"date"` кожного повідомлення — це час отримання повідомлення: `datetime.now()`. Тобто кожне нове повідомлення від вебпрограми має дописуватися до бази даних з часом отримання.

### Критерії прийняття

1. Використано для створення вебпрограми один файл main.py. Запущено HTTP-сервер і Socket-сервер у різних процесах.
2. Створено Dockerfile та запущено додаток як Docker-контейнер.
3. Написано docker-compose.yaml з конфігурацією для застосунку та MongoDB.
4. Використано Docker Compose для побудови середовища, команду docker-compose up для запуску середовища.
5. За допомогою механізму voluemes збережено дані з бази даних не всередині контейнера.
6. Оброблено статичні ресурси: style.css, logo.png.
7. У разі виникнення помилки 404 Not Found повертається сторінка error.html.
8. Робота з формою організована згідно з наведеними вище вимогами.
9. Формат запису документа MongoDB відповідає вищезазначеним вимогам.