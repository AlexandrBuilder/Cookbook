def to_dict(schema, model):
    schema = schema()
    return schema.dump(model)


def to_dict_list(schema, models):
    return [to_dict(schema, model) for model in models]

