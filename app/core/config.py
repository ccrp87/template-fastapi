import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")  
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))  