## Celery task queue example

## Command to start Celery
```
celery -A app.celery worker --loglevel=info
```


## API Reference

1. **Submit sleep times**
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"sleep_times": [2, 3, 4, 10, 20, 30, 40, 60]}' \ 
    http://localhost:5000/sleep
    ```

2. **Get results**
    ```bash
    curl http://localhost:5000/sleep? submission_id=<SUBMISSION ID>
    ```