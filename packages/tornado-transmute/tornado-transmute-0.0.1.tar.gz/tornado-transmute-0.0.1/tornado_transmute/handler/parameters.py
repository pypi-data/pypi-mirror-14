from functools import partial


def get_param_extractor(transmute_func, context):
    if "GET" in transmute_func.http_methods:
        return partial(_extract_from_queryparams, transmute_func, context)
    else:
        return partial(_extract_from_body, transmute_func, context)


def _extract_from_queryparams(transmute_func, context, handler, args=None):
    args, kwargs = args or [], {}
    # TODO: there needs to be a good strategy to parse out
    # positional arguments keyward arguments
    # (due to tornado accepting positional arguments matching regex.)
    index = len(args)
    for arg in transmute_func.signature.args[index:]:
        value = handler.get_query_argument(arg.name)
        args.append(context.serializers.load(arg.type, value))

    for name, info in transmute_func.signature.kwargs.items():
        value = handler.get_query_argument(name, default=None)
        if value is not None:
            kwargs[name] = context.serializers.load(info.type, value)

    return args, kwargs


def _extract_from_body(transmute_func, context, handler, args=None):
    kwargs = {}
    # TODO: there needs to be a good strategy to parse out
    # positional arguments keyword arguments
    # (due to tornado accepting positional arguments matching regex.)
    for name, info in transmute_func.arguments.items():
        serializer = context.serializer[info.type]
        value = handler.get_query_argument(name, default=None)
        if value is not None:
            kwargs[name] = serializer.deserialize(value)
    return kwargs
