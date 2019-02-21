
# only allow alphanumeric passwords - max length is 18, min is 1
def parseUsername(username):
    clean_un = "".join([ c if c.isalnum() else "" for c in username ])
    return str(clean_un[0:12])


def isValidPw(password):
    if len(password) >= 5 and len(password) <= 12:
        return True
    return False
