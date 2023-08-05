import botocore.session


session = None


def get_session():
    global session
    if session is None:
        session = botocore.session.get_session()
    return session
