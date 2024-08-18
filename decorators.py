import functools

from utils import check_account_is_new, check_account_exists, check_account_is_IBAN_compliant


def account_is_new(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        check_account_is_new(request.account)
        return await func(*args, **kwargs)

    return wrapper


def account_exists(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")

        account = None
        if (hasattr(request, 'path_params')):
            params = request.path_params

            if 'account' in params:
                account = params.get('account')

        else:
            account = request.account
        check_account_exists(account)
        return await func(*args, **kwargs)

    return wrapper


def transfer_is_IBAN_compliant(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        account = None
        if (hasattr(request, 'path_params')):
            params = request.path_params
            if 'account' in params:
                account = params.get('dest_account')

        else:
            account = request.dest_account

        check_account_is_IBAN_compliant(account)
        return await func(*args, **kwargs)

    return wrapper
