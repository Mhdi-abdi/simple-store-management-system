class AppError(Exception):
    """Base class for all errors of this application."""


class ValidationError(AppError):
    """Input is invalid (empty, negative, wrong format, .... )."""


class NotFoundError(AppError):
    """The requested record does not exist."""


class DuplicateError(AppError):
    """A unique value (email, product name) already exist."""


class InsufficientStockError(AppError):
    """Not enough stock for the requested quantity."""