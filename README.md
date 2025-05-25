Test Case 1: Проверка начального состояния игрока
Метод: test_initial_state()
Цель: Проверить корректность инициализации объекта игрока
Шаги:

Создать объект Player с параметрами (100, 100, 50, 50)

Проверить начальные значения атрибутов

Ожидаемые результаты:

player.rect.x == 100

player.rect.y == 100

player.direction == "right"

player.jump_count == 0

player.y_vel == 0

Test Case 2: Движение влево
Метод: test_movement() (первая часть)
Цель: Проверить корректность движения влево
Шаги:

Вызвать player.move_left(5)

Проверить изменения атрибутов

Ожидаемые результаты:

player.x_vel == -5

player.direction == "left"

Test Case 3: Движение вправо
Метод: test_movement() (вторая часть)
Цель: Проверить корректность движения вправо
Шаги:

Вызвать player.move_right(5)

Проверить изменения атрибутов

Ожидаемые результаты:

player.x_vel == 5

player.direction == "right"

Test Case 4: Одиночный прыжок
Метод: test_jump_mechanics() (первая часть)
Цель: Проверить механику первого прыжка
Шаги:

Вызвать player.jump()

Проверить изменения атрибутов

Ожидаемые результаты:

player.y_vel < 0 (движение вверх)

player.jump_count == 1

Test Case 5: Двойной прыжок
Метод: test_jump_mechanics() (вторая часть)
Цель: Проверить механику второго прыжка
Шаги:

Выполнить первый прыжок

Вызвать player.jump() повторно

Проверить изменения атрибутов

Ожидаемые результаты:

player.jump_count == 2

player.y_vel < -player.GRAVITY*6 (более сильный толчок)

Test Case 6: Приземление
Метод: test_landing()
Цель: Проверить сброс параметров при приземлении
Шаги:

Установить player.y_vel = 10 и player.fall_count = 30

Вызвать player.landed()

Проверить изменения атрибутов

Ожидаемые результаты:

player.y_vel == 0

player.fall_count == 0

player.jump_count == 0
