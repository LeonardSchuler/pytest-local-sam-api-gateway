from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.event_handler.api_gateway import APIGatewayHttpResolver
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
metrics = Metrics()
app = APIGatewayHttpResolver()


@app.get("/")
def info():
    # logger.info(f"Request from {name} received")
    # metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    return {"message": "hello world!"}


@app.post("/")
def echo():
    logger.info("Request received")
    data = app.current_event.json_body
    metrics.add_metric(name="NumberOfInvocations", unit=MetricUnit.Count, value=1)
    return {"message": data}


@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
