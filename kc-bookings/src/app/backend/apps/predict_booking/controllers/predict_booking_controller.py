"""
Controllers for Filter Panel APIs
"""

from apps.core.utils import BaseResponseHandler
from apps.predict_booking.dtos import PredictBookingDto
from apps.predict_booking.services import BookingPredictions
from flask import request,jsonify 
from flask_restx import Resource
import pandas as pd
import io

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


@api.route("/upload")
class UploadTestController(Resource):
    """Controller for getting uploaded csv"""

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
    def post(self):
        """Returns the data uploaded"""
        if 'file' not in request.files:
            return responseHandler.error_response(
                "File not found", 401,
                'No file part in the request', 401)
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            try:
                # Read the file into a pandas DataFrame
                df = pd.read_csv(io.StringIO(file.stream.read().decode('UTF-8')))
                # get the predictions
                obj_pred_bookings = BookingPredictions()
                df = obj_pred_bookings.main(df)
                # Convert DataFrame to JSON for demonstration purposes
                df = df.head(100)
                data = df.to_dict(orient='records')
                # print(data)
                # return jsonify({'data': data}), 200
                return responseHandler.success_response(200, None, data)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
