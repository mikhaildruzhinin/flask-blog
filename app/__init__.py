from .factory import AppFactory


def create_app(test_config=None):
    return AppFactory(
        name=__name__,
        secret_key='dev',
        database='db.sqlite',
    ).create_app(test_config)
