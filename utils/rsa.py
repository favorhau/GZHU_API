from des import strenc


def rsa_enc(content):
    result = strenc(content, "1", "2", "3")
    return result
