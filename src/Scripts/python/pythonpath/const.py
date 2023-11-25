from uno import getCurrentContext, getComponentContext

from format import ExtendedFormatter


FORMATTER = ExtendedFormatter()

XSC = getCurrentContext()
CTX = getComponentContext()
SM = CTX.getServiceManager()