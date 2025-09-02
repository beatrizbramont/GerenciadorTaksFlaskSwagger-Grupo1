import os
from flask import Flask
from config import Config 
from models import db
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from flasgger import Swagger


app = Flask(__name__)
app.config.from_object(Config)

swagger = Swagger(app)
# inicializa o banco de dados
db.init_app(app)

# cria tabelas
with app.app_context():
    db.create_all()

# Rotas de tarefas
app.add_url_rule('/tasks', view_func=TaskController.list_tasks, methods=['GET'], endpoint='get_tasks')
app.add_url_rule('/tasks', view_func=TaskController.create_task, methods=['POST'], endpoint='post_tasks')
app.add_url_rule('/tasks/<int:task_id>', view_func=TaskController.update_task_status, methods=['PUT'], endpoint='put_task')
app.add_url_rule('/tasks/<int:task_id>', view_func=TaskController.delete_task, methods=['DELETE'], endpoint='delete_task')

# forma alternativa de criar rotas, parâmetros: rota em si, endpoint interno do flask e função a ser executada quando a URL for acessada
app.add_url_rule('/contact', 'contact', UserController.contact, methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(debug=True, port=5002)