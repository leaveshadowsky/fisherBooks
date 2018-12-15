# 机密信息放在这个配置文件中，如app key，数据库配置参数等
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:971224@localhost:3306/fisher'
SECRET_KEY = "mysql+cymysql://root:971224@localhost:3306/fisherBook"

# Email配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'leaveyinhao@qq.com'
MAIL_PASSWORD = 'mygxxaidzlurbdei'
