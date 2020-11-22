# about_doc

__Скрипт проверяет api и генерирует отчеты в текстовых файлах__

# conf.yaml
- query_interval - задает интервал опроса api

- users_url - путь до данных users

- todos_url - путь до данных todos

- title_max_len - задает макимальную длину названия таска

- file_dir - задает папку для сохранения отчетов(при ииспользовании docker-compose изменить и в путь для volume)

- logger:
  -  log_level - задает уровень логирования, допустимые значения: debug, info, warning, error
  -  log_file - задает название файла с логами
  -  log_dir - задает папку для сохранения логов(при ииспользовании docker-compose изменить и в путь для volume)

** При перемещении конфига внесите изменения в __watcher.py__>__get_conf(conf_path='conf/conf.yaml')__  и __test_conf.py__>__ConfTest__>__SetUp__

# Запуск
Перед запуском проверьте корректонось заполнения watcher/conf/conf.yaml

__cli__

```bash
apt install virtualenv
cd watcher/
venv -p /usr/bin/python3 venv
source venv/bin/activate
pip install requirements.txt
python watcher.py
```


__docker-compose__

```bash
#up
docker-compose up -d --build
#down and remove
docker-compose down -v --rmi all
```
 

# ToDo:
 
- [x] API для получения списка задач и api для получения списка юзеров __get_data__
- [x] После запуска скрипта, рядом должна появиться директория "tasks" с текстовыми файлами __save_report__
- [x] Файл называть по username пользователя в формате "Antonette.txt" __save_report__
- [x] Внутри файла на первой строке писать полное имя, и рядом в < > записывать email. Через пробел от email записывать время составления отчёта в формате 23.09.2020 15:25 __gen_report__
- [x] На второй строке записывать название компании, в которой работает юзер. __gen_report__
- [x] Третья строка должна быть пустой. __gen_report__
- [x] На четвёртой строке "Завершённые задачи:" и далее список названий завершённых задач. __gen_report__
- [x] После завершённых задач через пустую строку записать "Оставшиеся задачи:" и вывести остальные задачи. __gen_report__
- [x] Если название задачи больше 50 символов, то обрезать до 50 символов и добавить троеточие. __create_df__, __cut_50__
- [x] Старые отчёты не удаляются, а переименовываются. __save_report__
 