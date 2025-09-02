from flask import request, jsonify
from models import db
from models.task import Task
from models.user import User
from flasgger import Swagger

class TaskController:
    @staticmethod
    def list_tasks():
        """
        Lista todas as tarefas
        ---
        tags:
          - Tasks
        responses:
          200:
            description: Lista de tarefas retornada com sucesso
            schema:
              type: object
              properties:
                tasks:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      title:
                        type: string
                      description:
                        type: string
                      status:
                        type: string
                      user_id:
                        type: integer
          500:
            description: Erro interno no servidor
        """
        try:
            tasks = db.session.query(Task).all()
            tasks_list = [{
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "user_id": task.user_id
            } for task in tasks]
            return jsonify(tasks=tasks_list), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def create_task():
        """
        Cria uma nova tarefa
        ---
        tags:
          - Tasks
        description: Endpoint para criar uma nova tarefa com título, descrição e usuário associado.
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - user_id
              properties:
                title:
                  type: string
                  example: "Comprar leite"
                description:
                  type: string
                  example: "Ir ao supermercado para comprar leite"
                user_id:
                  type: integer
                  example: 1
        responses:
          201:
            description: Tarefa criada com sucesso
            schema:
              type: object
              properties:
                message:
                  type: string
                task_id:
                  type: integer
          400:
            description: Dados inválidos ou campos faltando
          500:
            description: Erro interno no servidor
        """
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            user_id = request.form.get('user_id')

            if not title or not description or not user_id:
                return jsonify(error="Missing required fields"), 400
            
            new_task = Task(title=title, description=description, user_id=user_id, status='Pendente')
            db.session.add(new_task)
            db.session.commit()

            return jsonify(message="Tarefa criada com sucesso!", task_id=new_task.id), 201
        
        except Exception as e:
            return jsonify(error=str(e)), 500

    @staticmethod
    def update_task_status(task_id):
        """
        Atualiza uma tarefa existente
        ---
        tags:
          - Tasks
        description: Atualiza o status de uma tarefa pelo ID informado.
        parameters:
          - in: path
            name: task_id
            required: true
            type: integer
            description: ID da tarefa a ser atualizada
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "Concluído"
        responses:
          200:
            description: Tarefa atualizada com sucesso
            schema:
              type: object
              properties:
                message:
                  type: string
          404:
            description: Tarefa não encontrada
          500:
            description: Erro interno no servidor
        """
        try:
            task = db.session.query(Task).get(task_id)
            if not task:
                return jsonify(error="Tarefa não encontrada"), 404

            # Alternar status
            task.status = 'Concluído' if task.status == 'Pendente' else 'Pendente'
            db.session.commit()

            return jsonify(message="Atualização realizada com sucesso!"), 200
        
        except Exception as e:
            return jsonify(error=str(e)), 500
        
    @staticmethod
    def delete_task(task_id):
        """
        Remove uma tarefa
        ---
        tags:
          - Tasks
        description: Remove uma tarefa pelo ID informado.
        parameters:
          - in: path
            name: task_id
            required: true
            type: integer
            description: ID da tarefa a ser removida
        responses:
          200:
            description: Tarefa removida com sucesso
            schema:
              type: object
              properties:
                message:
                  type: string
          404:
            description: Tarefa não encontrada
          500:
            description: Erro interno no servidor
        """
        try:
            task = db.session.query(Task).get(task_id)
            if not task:
                return jsonify(error="Tarefa não encontrada"), 404

            db.session.delete(task)
            db.session.commit()

            return jsonify(message="Tarefa deletada com sucesso!"), 200
        
        except Exception as e:
            return jsonify(error=str(e)), 500
