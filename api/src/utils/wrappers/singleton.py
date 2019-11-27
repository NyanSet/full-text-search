def singleton(_class):
    instances = {}

    def get_instance(*args, **kwargs):
        if _class not in instances:
            instances[_class] = _class(*args, **kwargs)
        return instances[_class]

    return get_instance
