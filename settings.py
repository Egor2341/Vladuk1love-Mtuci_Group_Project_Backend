class Settings():
    AWS_ACCESS_KEY_ID = 'minio'
    AWS_SECRET_ACCESS_KEY = 'miniopassword'
    AWS_REGION = 'us-east-1'
    AWS_HOST = 'http://localhost:9000'
    AWS_BUCKET = 'photos'

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

settings = Settings()