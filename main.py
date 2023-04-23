from dotenv import load_dotenv

from core import AimBot

load_dotenv(".env")

if __name__ == "__main__":
    AimBot().run("TEST_TOKEN")
