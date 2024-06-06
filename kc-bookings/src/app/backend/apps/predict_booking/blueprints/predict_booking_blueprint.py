from apps.predict_booking.controllers import predict_booking_ns
from flask import Blueprint
from flask_restx import Api

predictbooking_bp = Blueprint("predictbooking", __name__)

predictbooking_api = Api(
    predictbooking_bp,
    title="Predict Booking",
    description="predictbooking services",
    doc="/swagger/",
    authorizations=None,
    security=[],
)

# API namespaces
predictbooking_api.add_namespace(predict_booking_ns)
