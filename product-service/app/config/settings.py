import os

class Settings:
    APP_NAME = os.getenv("APP_NAME", "ShopEase Product Service")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8003"))

settings = Settings()
