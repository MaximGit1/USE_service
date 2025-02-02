import uvicorn
from dotenv import load_dotenv

from use.main.setup import create_app

if __name__ == "__main__":
    load_dotenv()

    app = create_app()
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        ssl_keyfile="../../certs/key.pem",
        ssl_certfile="../../certs/cert.pem",
    )
