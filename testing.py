import logging
import os
import requests
import azure.functions as func

# Load environment variables (set these in Azure Function App settings)
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP")
LOAD_TEST_RESOURCE = os.getenv("AZURE_LOAD_TEST_RESOURCE")
TEST_ID = os.getenv("AZURE_TEST_ID")
TOKEN = os.getenv("AZURE_BEARER_TOKEN")  # Ideally, use a Managed Identity instead

# Azure Load Testing API endpoint
LOAD_TEST_API_URL = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.LoadTestService/loadTests/{LOAD_TEST_RESOURCE}/testRuns/{TEST_ID}?api-version=2023-04-01"

def start_load_test():
    """Triggers a new Azure Load Test Run"""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "testRunId": f"{TEST_ID}-run",
        "testId": TEST_ID,
        "displayName": "Automated Load Test Run"
    }

    response = requests.put(LOAD_TEST_API_URL, json=payload, headers=headers)

    if response.status_code in [200, 201, 202]:
        return f"Load test {TEST_ID} started successfully!"
    else:
        return f"Error starting test: {response.text}"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Received request to trigger Load Test")
    
    result = start_load_test()

    return func.HttpResponse(result, status_code=200)
