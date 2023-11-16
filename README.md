# VPN Service
Це простий VPN сервіс, який надає можливість реєстрації клієнтів та використання особистого кабінету для керування особистою інформацією та статистикою. Проект реалізовано з використанням Docker для зручного підняття та розгортання.

# Встановлення та початок роботи

1. Клонуйте проект і створюйте віртуальне середовище.
    ````
    git clone https://github.com/Hant0-0/test_vpn_service
    cd vpn_service
    python -m venv venv
    venv\Scripts\activate

2. Виконайте міграцію
    
    ```
   python manage.py makemigration
   python manage.py migrate
        
# Запустіть з Docker
Docker має бути встановлено та запущено

```
docker-compose up --build

    