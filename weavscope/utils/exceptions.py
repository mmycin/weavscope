"""
WeavScope custom exceptions.

All exceptions inherit from WeavscopeError so callers can catch
them with a single except clause if desired.
"""


class WeavscopeError(Exception):
    """Base exception for all WeavScope errors."""


class WeavscopeConnectionError(WeavscopeError):
    """Raised when the Weaviate client cannot establish a connection."""


class WeavscopeConfigError(WeavscopeError):
    """Raised for invalid or unsupported configuration values."""


class WeavscopeCollectionError(WeavscopeError):
    """Raised on collection create/delete failures."""


class WeavscopeTenantError(WeavscopeError):
    """Raised on tenant create/delete/list failures."""


class WeavscopeBatchError(WeavscopeError):
    """Raised on batch insert/delete failures."""


class WeavscopeQueryError(WeavscopeError):
    """Raised on query execution failures."""