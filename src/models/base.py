from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    """
    Shared declarative base for all SQLAlchemy models.

    This base class is used as a foundation for all models in the project.
    It provides a common structure and behavior to simplify model definitions
    and ensures consistency across the codebase.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Automatically generate table names based on class names.

        By default, the table name is the lowercase version of the class name.
        This behavior can be overridden in individual models by explicitly
        setting the `__tablename__` attribute.

        Returns:
            str: The table name derived from the class name.
        """
        return cls.__name__.lower()
