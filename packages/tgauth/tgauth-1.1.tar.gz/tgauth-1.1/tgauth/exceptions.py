
class IllegalArgumentError(ValueError):
    pass

# class AuthException(SauthException):
#     """Auth process exception."""
#     def __init__(self, backend, *args, **kwargs):
#         self.backend = backend
#         super(AuthException, self).__init__(*args, **kwargs)

class MissingParameter(IllegalArgumentError):
	""" Auth Parameter is needed for complete the authentication """

	def __init__(self,backend,parameter):
		self.parameter = parameter
	def __str__(self):
		return " missing parameter %s needed " %(self.parameter)