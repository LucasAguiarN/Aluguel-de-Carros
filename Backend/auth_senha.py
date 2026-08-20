import bcrypt


def hash_senha(senha):
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha, hash_salvo):
    if not senha or hash_salvo is None:
        return False
    hash_bytes = hash_salvo.encode("utf-8") if isinstance(hash_salvo, str) else hash_salvo
    return bcrypt.checkpw(senha.encode("utf-8"), hash_bytes)
