import celery.states as states
from flask import Flask,url_for, jsonify,request
from worker import celery

dev_mode = True
app = Flask(__name__)

@app.route('/add', methods=["POST"])
def add():
    data = request.get_json(force=True)
    print(data)
    print(data['nums'])
    data=data['nums']
    task = celery.send_task('tasks.add', args=[data], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response





@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:

    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/health_check')
def health_check() -> str:
        print('asdasdasd')
        return jsonify("OK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
