"""
DTO for Predict Booking
"""

from flask_restx import Namespace, fields


class PredictBookingDto:
    """
    Predict Booking DTO definition
    """

    api = Namespace("PredictBooking", description="Predict Booking operations")
    service_available_response_code = 200
    service_available_response_message = "Predict Booking Service available"

    service_unavailable_response_code = 503
    service_unavailable_response_message = "Predict Booking service unavailable"

    booking_obj = api.model(
        "booking",
        {
            "user": fields.String,
            "pred_destination": fields.String,
        },
    )

    booking_response_obj = api.model(
        "Bookings",
        {
            "status": fields.Integer,
            "message": fields.String,
            "data": fields.List(fields.Nested(booking_obj)),
        },
    )
