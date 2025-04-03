# -*- coding: UTF-8 -*-
"""
程序启动入口

Author: worship-dog
Email: worship76@foxmail.com>
"""

import uvicorn

from app.main import app


uvicorn.run(app, host="0.0.0.0", port=8001)
