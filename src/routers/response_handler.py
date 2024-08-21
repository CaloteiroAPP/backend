from fastapi.responses import JSONResponse


class ResponseHandler:

    def __init__(self):
        pass

    @staticmethod
    def json_response(data: dict = None, message: str = "", status_code: int = 200):
        return JSONResponse(
            content={
                "status": status_code,
                "message": message,
                "data": data,
            },
            status_code=status_code
        )

    def ok(self, data: dict = None, message: str = "Success"):
        return self.json_response(data, message, 200)

    def created(self, data: dict = None, message: str = "Created"):
        return self.json_response(data, message, 201)

    def bad_request(self, data: dict = None, message: str = "Bad Request"):
        return self.json_response(data, message, 400)

    def unauthorized(self, data: dict = None, message: str = "Unauthorized"):
        return self.json_response(data, message, 401)

    def forbidden(self, data: dict = None, message: str = "Forbidden"):
        return self.json_response(data, message, 403)

    def not_found(self, data: dict = None, message: str = "Not Found"):
        return self.json_response(data, message, 404)
