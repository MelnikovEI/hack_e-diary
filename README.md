# Улучшение результатов в школьном журнале

Набор скриптов для корректировки оценок, удаления замечаний и добавления похвалы в электронном дневнике
https://github.com/devmanorg/e-diary

## Запуск
Для работы необходимо, чтобы сайт электронного дневника https://github.com/devmanorg/e-diary был развёрнут на Вашем
сервере.

- скопируйте файл `scripts.py` в папку электронного дневника рядом с файлом `manage.py`
- запустите в командную строку и перейдите в папку проекта электронного дневника (содержит `manage.py` и `scripts.py`)
- исполните команды:
    - `python manage.py shell`
        - Результат должен выглядеть примерно так:`Python 3.8.10...
          (InteractiveConsole)`
          
          `>>>`
    - `import scripts`

Далее запускайте соответствующий скрипт, например:
- `scripts.fix_marks("Иванов Иван")`
- `scripts.remove_chastisements("Иванов Иван")`
- `scripts.create_commendation("Иванов Иван", "Музыка")`

## Описание скриптов

- `scripts.fix_marks("ФИО ученика")` - исправляет все оценки ниже '4' на '5'. 
- `scripts.remove_chastisements("ФИО ученика")` - удаляет все замечания от учителей.
- `scripts.create_commendation("ФИО ученика", "Предмет")` - добавляет похвалу ученику по заданному предмету в случайную
  дату урока. Если похвала за данный урок уже имеется, то выбирается другая случайная дата. Если похвала проставлена
  за все даты урока, то скрипт сообщит об этом и закончит работу.

ФИО можно указывать не полностью, главное, чтобы по указанная часть ФИО однозначно указывала одного ученика.

## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
## Authors
* **Evgeny Melnikov** - *Initial work* - [Evgeny Melnikov](https://github.com/MelnikovEI)
## Acknowledgments
* Inspired by [Devman](https://dvmn.org/)