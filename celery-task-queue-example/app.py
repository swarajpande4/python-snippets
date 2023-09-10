from flask import Flask, request, jsonify
from celery import Celery
from dotenv import load_dotenv
import os
import uuid
import time

load_dotenv()

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL')  # Redis broker URL
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_BACKEND_URL')  # Redis backend URL
celery = Celery(
    app.name, 
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)
celery.conf.update(app.config)


@celery.task
def go_to_sleep(sleep_time):
    time.sleep(sleep_time)
    return sleep_time


@app.route("/sleep", methods=["POST"])
def submit_post():
    sleep_times = request.json.get("sleep_times")

    submission_id = str(uuid.uuid4())

    results = [go_to_sleep.apply_async(args=(sleep_time,)) for sleep_time in sleep_times]

    app.results[submission_id] = results

    return jsonify({"submission_id": submission_id, "message": f"Function submitted {len(sleep_times)} times with sleep times: {sleep_times}"}), 202


@app.route("/sleep", methods=["GET"])
def get_completed_jobs():
    submission_id = request.args.get("submission_id")
    results = app.results.get(submission_id)
    if not results:
        return jsonify({"error": "Submission ID not found."}), 404

    completed = []
    all_ready = True
    for result in results:
        if result.ready():
            completed.append(result.get())
        else:
            all_ready = False

    if all_ready:
        del app.results[submission_id]

    return jsonify({"completed": all_ready, "completed_jobs": completed})


if __name__ == "__main__":
    # Initialize results dictionary
    # TODO: Store results in an actual database, and not in memory
    app.results = {}  
    app.run(debug=True, port=5000)