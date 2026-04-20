class OpenRouterError(Exception):
    pass


class OpenRouterTimeoutError(OpenRouterError):
    pass


class OpenRouterAuthenticationError(OpenRouterError):
    pass


class OpenRouterRateLimitError(OpenRouterError):
    pass


class OpenRouterInvalidRequestError(OpenRouterError):
    pass
