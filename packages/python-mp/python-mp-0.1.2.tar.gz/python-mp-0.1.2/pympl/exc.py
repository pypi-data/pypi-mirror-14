class PymplError(Exception):
    pass


class ServerError(PymplError):
    pass


class ResolverError(ServerError):
    pass


class FunctionError(ServerError):
    pass


class AuthenticateUserError(FunctionError):
    pass


class AddRecordError(FunctionError):
    pass


class UpdateRecordError(FunctionError):
    pass


class UpdateDefaultImageError(FunctionError):
    pass


class UpdateUserAccountError(FunctionError):
    pass


class AttachFileError(FunctionError):
    pass


class ResetPasswordError(FunctionError):
    pass


class EmailError(PymplError):
    pass


class StateError(EmailError):
    pass


class AttachmentError(EmailError):
    pass


class RecipientError(EmailError):
    pass


class EmailRecordCreationError(EmailError):
    pass


class NoRecipientsError(EmailError):
    pass
