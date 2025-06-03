Установка Python и Pygame.
1. Нужно скачать и установить Python (по ссылке https://www.python.org/downloads/ ). При установке отметьте галочку Add Python to PATH. 
Далее стоит проверить установку:
1.	Откройте командную строку (Win + R -> cmd)
2.	Введите:
python --version
Должна появится версия Python.
2. Также следует установить библиотеку Pygame.
В командной строке введите pip install pygame. (Если команда не работает, попробуйте 
python -m pip install pygame или pip3 install pygame)
Проверьте установку:
python -c "import pygame; print(pygame.version.ver)"
3.	Нужно установить IDE 
Рaсмотрим на примере Visual Studio Code
Скачать Visual Studio Code (по ссылке https://code.visualstudio.com/download)
И следует его настроить.
4.	В Visual Studio Code создаём пустую папку
Далее в терминале прописывается:
git init
git remote add main https://github.com/alinyason/TeamGirls
git pull main main 
