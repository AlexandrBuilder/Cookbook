def to_json(schema, model):
    schema = schema()
    return schema.dump(model)


def to_json_list(schema, models):
    return [to_json(schema, model) for model in models]

