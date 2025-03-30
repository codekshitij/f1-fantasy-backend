import firebase_admin
from firebase_admin import credentials
import os
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent

# Initialize Firebase Admin with service account
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "f1-fantasy-league-dee25",
    "private_key_id": "6c8434eb0f3fce63b48c615fa23ac5ca2dec7c69",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCheCYUBtBFjIZg\nyXyx+2Uhx/Kp5to3gsf0fGKmMJCb8XzNwJAqbST76R6FJRLTLObiMlvtN/ZnBObo\nxNj2AwnLiuqewAFp5V7MtgVDbETGhcy0G3P4Xd+zpFQaTO6coYHITtgc5QT63mg1\nTntLgKuuPDvYYP5x9WNHvpOt8A/GJM+ZYr3Mjz10v5o1Qv/ruP25bZw1tIKBCy6h\nzYOaAJr6cgkkJu/dIfiUc7A0SstkdShc/33RgF7rc91IV0F4wDE9bzWZsyVPCo+b\nb7/abJT1MflXmonDwl1TL0BgrZuTiDpeJyVfOfF1HtytXOzlNYZ7waznueoZUO+S\n4MvfJK5zAgMBAAECggEATaOP66E7E7X2ByPaqVnPzuZtb/RoiLiBnLUSWgaQAeuj\nrusgZsYEOnxlCHBDFPdKLQk52l5GRFK/FL1R9TiQxSYOmjaId3qqkpQTA9BTYYGE\nZDWvFYVNwvsI1XyYXwfpd38xuvMD6fx27urFrhA4fJbJz8kTj4gGLMEeEUyUyRi2\njH+PgBhhN4LgKg/gV77s7r8aaUX8+h3PfGP5ll9YMDu2NY6FnkzuwUyCefJRxrFm\nv0f7Q58Nq5m054X3QsZ7If0/MRLQOe18PjlHd5LVI2yTMFGh9cAk+jNE6z5o+p/r\nAC6FtaaqeAi9U7r+mvXW2B/ES+hXhXWrzSVNBKBlQQKBgQDO8dcKuDxTYI5XFoH7\niHJlwcQqeevTFNqT5dN26mWRl/nJYWB/8tFi6cKlr/ejDek+YFTNEckQWunDfzBU\nFXj10YziAnQR9hvQyCWH5NGO+D5c8RTaxZgibj/+X/MR3L9hvNNP09Q0GapBGc4H\nA/5QFCWKywdVhC4ynNTpFRgoNQKBgQDHvrKpZgTIzedes4Svk9R/B53ucsuwZYnC\nXGllUJS+hLA4FOKuuPc+6wGZceS1GcEIVRCkC93mr+9q8xzttOzpVXWFlSZ/lYXd\nV06XfUnPq3BXFId8HBvYSKEEA25mJ8v8LfS0TNcl8EJTdwZEhf89kf7Rn41QCOhd\nqUhwpjHhBwKBgEoA2bGPqKL4SG6EMf9ND/uriwbViqt1LaTt7uz7bU7fVgfZtrSK\nlK4WgfDWOGwqsVoJAMpEre4XVLkAZrvq4dKmGQdJcVBq/g9vQ1yRSw8hXsvFuntx\nZbIKUwAYN8gPdLDy4W4OhjgLZYLaQ37mwq7IRZSYfgrqtcqLouenD3hxAoGAUh+c\nkztHokvN4cjLN+j+yA+Ypk36YxcMMaYPC0G7Ni2VyikEHjQcK3kx2iXSk4b4L3XR\n9rCOVmdld0JnVXA6q6CgRgDRqEkQlbVssaooa8Kf2J2vKp7f7+fEk8LZZBTesFsw\nreSd3JJQosJgCFJTY7wf2Y3Q6uQOrVuJVg9umIcCgYEAn3hb9K/XHWG8zPbQyWPF\ntUn6MjmxjozhDChIHnAqzm2ICv0fNmfNr8pAZONRh+HnrpqdeVQMmMeu9QJffIxv\npMjvdea/HhNTfbf2hvxo7OcSc6xEfHax7OryXdUf9ZW6NkgKOPz2LQYB4tBpz3lg\n5vgAyLOJpU07QIxH+0ofNUU=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@f1-fantasy-league-dee25.iam.gserviceaccount.com",
    "client_id": "104754858609166102853",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40f1-fantasy-league-dee25.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
})

default_app = firebase_admin.initialize_app(cred) 