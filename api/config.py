import os


def get_database_url() -> str:
    return os.getenv("DATABASE_URL")


def get_test_database_url() -> str:
    return os.getenv("TEST_DATABASE_URL")
