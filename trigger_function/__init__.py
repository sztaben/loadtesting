import azure.functions as func
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function has been triggered!")

    return func.HttpResponse("Hello from Azure Function!", status_code=200)
