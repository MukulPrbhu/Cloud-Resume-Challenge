import azure.functions as func
import logging
import json  # Import JSON module to ensure proper JSON formatting

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="HttpExample")  # Define the HTTP trigger route
@app.cosmos_db_input(
    arg_name="inputDocument",
    database_name="my-database",
    container_name="my-container",
    connection="CosmosDbConnectionSetting",
    sql_query="SELECT * FROM c"  # Query to fetch all documents
)
@app.cosmos_db_output(arg_name="outputDocument", database_name="my-database", container_name="my-container", connection="CosmosDbConnectionSetting")
def HttpExample(req: func.HttpRequest, inputDocument: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info("Fetching data from Cosmos DB.")

    # Check if any documents are retrieved
    if not inputDocument:
        return func.HttpResponse(
            "No data found in the database.",
            status_code=404
        )

    # Convert the DocumentList to a JSON-compatible structure
    # data = [doc.to_dict().get("count") for doc in inputDocument]
    # data = int(data[0]) + 1
    # updated_value = inputDocument.to_dict()
    # updated_value["id"] = "1"  # Ensure the same ID is maintained
    # updated_value["count"] = data
    # outputDocument.set(func.Document.from_dict(updated_value))
    # Serialize to JSON and return the response

    data = inputDocument[0].to_dict()  # Assuming there's at least one document
    current_count = int(data.get("count", 0))  # Get the current count, default to 0 if not found
    new_count = current_count + 1

    # Update the "count" field in the document
    data["count"] = new_count

    # Write the updated document back to the database
    outputDocument.set(func.Document.from_dict(data))

    return func.HttpResponse(
        body=json.dumps({"count": new_count}),  # Properly serialize to JSON
        mimetype="application/json",  # Set the correct content type
        status_code=200
    )