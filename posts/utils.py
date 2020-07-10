


def storage_location(instance, filename):
    """Automatically generates storage location name for
    a saved model instance."""
    id = instance.id
    if not id:
        try:
            id = instance.__class__.objects.first().id + 1 
        except:
            id = 1
    return f"img/{id}"

