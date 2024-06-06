"""
Controllers for Filter Panel APIs
"""

from apps.core.utils import BaseResponseHandler
from apps.predict_booking.dtos import PredictBookingDto
from flask import request
from flask_restx import Resource

api = PredictBookingDto.api
responseHandler = BaseResponseHandler()


@api.route("/get_first_booking")
class FirstBookingController(Resource):
    """Controller for getting first booking"""

    @api.response(
        PredictBookingDto.service_available_response_code,
        PredictBookingDto.service_available_response_message,
        PredictBookingDto.booking_response_obj,
    )
    @api.response(
        PredictBookingDto.service_unavailable_response_code,
        PredictBookingDto.service_unavailable_response_message,
        PredictBookingDto.booking_response_obj,
    )
    def get(self):
        """Return Info of first booking"""
        try:
            response = {"data": "success"}
            return responseHandler.success_response(200, None, response)
        except Exception as e:
            return responseHandler.error_response(
                "Booking not found", 401, str(e), 401)
