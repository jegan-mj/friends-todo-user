exception_response = {
    "status": {
        "code": 404,
        "message": "Temporarily not available",
        "state": "fasle",
        "type": "error"
    }
}

bad_request_response = {
    "status": {
        "code": 400,
        "state": "false",
        "message": "Please enter all the required details",
        "type": "bad request"
    }
}

failed_session_response = {
    "status": {
        "code": 403,
        "message": "Please login again",
        "state": "fasle",
        "type": "session expired"
    }
}
