
class UserResponse():
    @staticmethod
    def parsedUser(raw):
        if raw is not None:
            data = {
                "token": raw['token'],
                "depot": raw['depot'],
                "ruc": raw["ruc"],
                "name": "No hay ninguna tabla que registe este campo",
                "empresa": raw['empresa']
            }
            return data
        else:
            raise Exception("Usuario no válido")