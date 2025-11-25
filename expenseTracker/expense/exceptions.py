
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging


logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
  
    response = exception_handler(exc, context)

    if response is not None:
     
        request = context.get("request")
        user = getattr(request, "user", None)
        username = user.username if user and user.is_authenticated else "Anonymous"

        
        logger.error(f"Error {response.status_code} on {request.method} {request.path} by {username}: {exc}")

      
        response.data = {"error": str(exc)}

    return response
