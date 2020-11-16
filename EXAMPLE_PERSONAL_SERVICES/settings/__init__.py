from .base import *


if os.environ.get("LEVEL") == "PRODUCTION":
    from .production import *
elif os.environ.get("LEVEL") == "TEST":
    from .test import *
else:
    from .local import *