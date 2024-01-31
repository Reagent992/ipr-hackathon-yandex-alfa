#!/bin/bash

python ../manage.py loaddata ./fixture/users_position_dump.json --app=users
python ../manage.py loaddata ./fixture/tasks_skill_dump.json --app=tasks
python ../manage.py loaddata ./fixture/users_user_dump.json --app=users
python ../manage.py loaddata ./fixture/ipr_ipr_dump.json --app=ipr
python ../manage.py loaddata ./fixture/tasks_task_dump.json --app=tasks
