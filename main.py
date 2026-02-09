import dotenv

import core

dotenv.load_dotenv(".env")

if __name__ == "__main__":
    core.AimBot().run("AIM_TOKEN")
