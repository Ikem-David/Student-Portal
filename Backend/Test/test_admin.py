from Backend.Test.test_Oauth2 import client
from Backend.index import app

from Backend.Routers.Oauth2 import create_access_token

admin_jwt=create_access_token(data={"sub":"ikemdavid8@gmail.com","role":"admin"})
student_jwt=create_access_token(data={"sub":"kene@example.com","role":"student"})
teacher_jwt=create_access_token(data={"sub":"john@example.com","role":"teacher"})