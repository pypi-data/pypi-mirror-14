from marshmallow import ValidationError


class UMongoError(Exception):
    pass


class ValidationError(ValidationError, UMongoError):
    pass


class NoDBDefinedError(UMongoError):
    pass


class NotRegisteredDocumentError(UMongoError):
    pass


class AlreadyRegisteredDocumentError(UMongoError):
    pass


class SchemaFieldNamingClashError(UMongoError):
    pass


class UpdateError(UMongoError):
    pass


class DeleteError(UMongoError):
    pass


class MissingSchemaError(UMongoError):
    pass


class NotCreatedError(UMongoError):
    pass


class NoCollectionDefinedError(UMongoError):
    pass


class FieldNotLoadedError(UMongoError):
    pass


class NoCompatibleDal(UMongoError):
    pass
