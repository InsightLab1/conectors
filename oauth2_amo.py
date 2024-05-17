import dotenv
from dotenv import load_dotenv
import requests
import os

# Подгружаем env где хранятся данные. Переписать, когда будет кнопка
dotenv_path = os.path.join('./', ".env")
load_dotenv(dotenv_path=dotenv_path)
load_dotenv()

# Некие данные пользователя
subdomain = os.getenv("AMOCRM_SUBDOMAIN")
client_id = os.getenv("AMOCRM_CLIENT_ID")
client_secret = os.getenv("AMOCRM_CLIENT_SECRET")
redirect_uri = os.getenv("AMOCRM_REDIRECT_URL")
secret_code = "def502005b5924c1291baadcbd1704742dcd20fdd790076d19afe0f5975f1c28b1643819dd576a028caf764a94775934dfba1ed3a9ee0241700ec99c1eb33a3c0f3531eb059dfad46b9e27a25e7c675c3f471f47c9c80b74c7ab33af6a39f31ab88967c6dec4386bfb8632a726cbabb56563351d45d24458939dc1958baf198d60a22e8d9b5b793b250baadeae436ad90e315492acb926907e15a2000c1103106d00ce2442b4cb6f80b54924324911c31d0d642bd03da5f9d2166e39f1bc02c32d1f29fd8f9666ec0c38f74d2ef1bfebaefbe021ac13f8642e09f5d39f691aece5a5f391f35db73c202470b5fcfee0bcc6f440384e44631d3f5c16a4f5ad3dd8096f0f8c2cc3fd665b1ec85424d32cca7a8b9e27758214ddfeb52f93425f8e105d0ff5640e9645413ce8ac4f7ec7281dab4f0bf23747befa98a18dc822bb700445603f5f731ccbf0030a3c37d73e67e3497485a97160b304618d2895ae002ab65afae7150bb9b4acd5584dc443bcaebe2619663ecd6e49bd25da61f4167caa5455da0b6dbcc773d0008d43ea037ecc0d6ad43a055a75aae36b040f43b168449d8a04f3e23796c0c8d2bb5a7a613de49b4dfbda015abfba0f6e67ff5f35695c5c3e3b764123f429383a80faa54510b9b7bcdf98f4fdc2583f7f86a00ce01554e99a19dc7b03f7b9e22f0cb946cb"

# Записываем в ключи .env
def _save_tokens(access_token: str, refresh_token: str):
    os.environ["AMOCRM_ACCESS_TOKEN"] = access_token
    os.environ["AMOCRM_REFRESH_TOKEN"] = refresh_token
    dotenv.set_key(dotenv_path, "AMOCRM_ACCESS_TOKEN", os.environ["AMOCRM_ACCESS_TOKEN"])
    dotenv.set_key(dotenv_path, "AMOCRM_REFRESH_TOKEN", os.environ["AMOCRM_REFRESH_TOKEN"])

# Обновляем токен доступа
def _get_refresh_token():
    return os.getenv("AMOCRM_REFRESH_TOKEN")

class AmoCRMWrapper:
    # первичное получение пары ключей
    def init_oauth2(self):
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": secret_code,
            "redirect_uri": redirect_uri
        }
        response = requests.post("https://{}.amocrm.ru/oauth2/access_token".format(subdomain), json=data).json()
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]

        _save_tokens(access_token, refresh_token)

    # Обновление ключа авторизации
    def _get_new_tokens(self):
        data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": _get_refresh_token(),
                "redirect_uri": redirect_uri
        }
        response = requests.post("https://{}.amocrm.ru/oauth2/access_token".format(subdomain), json=data).json()
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        print(access_token)
        _save_tokens(access_token, refresh_token)

amocrm_wrapper_1 = AmoCRMWrapper() 
amocrm_wrapper_1._get_new_tokens()
