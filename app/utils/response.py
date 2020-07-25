def to_json(schema, model):
    author_schema = schema()
    author_schema.dump(model)
    return author_schema.dump(model)


def to_json_list(schema, models):
    return [to_json(schema, model) for model in models]
