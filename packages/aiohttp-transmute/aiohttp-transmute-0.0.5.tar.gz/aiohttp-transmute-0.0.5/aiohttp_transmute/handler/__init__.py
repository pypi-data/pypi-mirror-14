from functools import wraps
from .parameters import _get_param_extractor
from web_transmute import default_context
from web_transmute.contenttype_serializers import NoSerializerFound
from aiohttp import web


def create_handler(transmute_func, method=None, context=default_context):
    method = method or next(iter(transmute_func.http_methods))

    extract_params = _get_param_extractor(transmute_func, context)

    @wraps(transmute_func.raw_func)
    async def handler(request):
        args = await extract_params(request)
        try:
            output = {
                "result": await transmute_func.raw_func(**args),
                "code": 200,
                "success": True
            }
        except Exception as e:
            output = {
                "result": "as exception occurred: ".format(str(e)),
                "success": False
            }
        if transmute_func.return_type:
            output = context.serializers.dump(
                transmute_func.return_type, output
            )
        try:
            body = context.contenttype_serializers.to_type(
                request.content_type, output
            )
        except NoSerializerFound:
            body = context.contenttype_serializers.to_type("json", output)
        return web.Response(
            body=body
        )

    handler.transmute_func = transmute_func
    return handler
