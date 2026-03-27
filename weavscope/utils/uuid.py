"""
WeavScope UUID utilities.

Weaviate requires UUIDs (v4 or v5) as object identifiers. Using
deterministic v5 UUIDs from (object_id, tenant_id) pairs gives
idempotent inserts — inserting the same logical object twice updates
rather than duplicates it.
"""

import uuid as _uuid
from typing import Optional


# Shared namespace for all WeavScope-generated UUIDs.
# Using uuid5.NAMESPACE_OID so the UUID space is clearly owned by this package.
_NAMESPACE = _uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # uuid.NAMESPACE_OID


def generate_uuid(object_id: str, tenant_id: str) -> str:
    """
    Generates a deterministic UUID v5 from an (object_id, tenant_id) pair.

    The same inputs always produce the same UUID, so re-inserting an
    object into the same tenant is an upsert rather than a duplicate.

    Args:
        object_id:  Application-level identifier for the object
                    (e.g. a user ID, document ID, record PK).
        tenant_id:  The Weaviate tenant the object belongs to.

    Returns:
        A UUID v5 string (e.g. "550e8400-e29b-41d4-a716-446655440000").
    """
    seed = f"{tenant_id}:{object_id}"
    return str(_uuid.uuid5(_NAMESPACE, seed))


def random_uuid() -> str:
    """
    Generates a random UUID v4.

    Use this when no stable identifier is available and idempotency is
    not required.

    Returns:
        A UUID v4 string.
    """
    return str(_uuid.uuid4())