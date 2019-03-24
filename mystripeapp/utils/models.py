def get_model_by_table(table, database):
    """
    Get the model class from the tablename.

    :return {BaseModel|None}:
        Returns the model if one can be found, otherwise None.
    """
    for cls in database.Model._decl_class_registry.values():
        if hasattr(cls, "__tablename__") and cls.__tablename__ == table:
            return cls
    return None
