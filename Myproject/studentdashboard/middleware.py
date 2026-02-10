import time
import logging
import traceback
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class StudentSystemMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. START TIMER & GET INITIAL DATA
        start_time = time.time()
        user = request.user if request.user.is_authenticated else "Anonymous"

        # 2. PHASE 1: LOGGING (Before View)
        # We use logger instead of print
        logger.info(f"REQUEST | User: {user} | Method: {request.method} | Path: {request.path}")

        # 3. PROCEED TO VIEW
        response = self.get_response(request)

        # 4. PHASE 2: CALCULATE DURATION (After View)
        duration = time.time() - start_time
        response['X-Process-Time'] = f"{duration:.3f}s"
        response['X-Student-System-Active'] = 'True'

        # Log the success and the time it took
        logger.info(f"RESPONSE | Status: {response.status_code} | Time: {duration:.3f}s")
        
        return response

    def process_exception(self, request, exception):
        # 5. PHASE 3: DETAILED ERROR LOGGING
        # This captures the EXACT line where the code broke
        error_details = traceback.format_exc()
        logger.error(f"CRASH | Path: {request.path} | Error: {error_details}")

        return JsonResponse({
            "error": "Internal Server Error",
            "message": str(exception),
            "dev_hint": "Check system logs for full traceback"
        }, status=500)