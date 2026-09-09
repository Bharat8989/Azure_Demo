import os


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"
    )

    # MySQL Database Connection
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:Bharat%401297@localhost:3306/js"
    )

    JWT_EXPIRATION_SECONDS = int(
        os.getenv(
            "JWT_EXPIRATION_SECONDS",
            "3600"
        )
    )

    FRONTEND_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS",
            "http://127.0.0.1:5500,http://127.0.0.1:5500/"
        ).split(",")
        if origin.strip()
    ]

    MAX_CONTENT_LENGTH = 16 * 1024  # 16 KB