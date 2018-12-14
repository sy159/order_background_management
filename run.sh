python manage.py runserver 192.168.0.60:8001 --insecure   #  启动代码
python manage.py inspectdb > orange_manage/models.py   # 数据库有改变
python manage.py makemigrations
python manage.py migrate
pip freeze > requirements.tx   列出所有依赖包
pip list > requirements.tx   列出所有依赖包
pip install -r requirements.txt 安装所有的依赖包
