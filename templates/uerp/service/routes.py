# -*- coding: utf-8 -*-
'''
Equal Plus
@author: Hye-Churn Jang
'''

#===============================================================================
# Import
#===============================================================================
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from common import getConfig, Logger, MultiTask, AsyncRest
from .controls import Control

#===============================================================================
# SingleTone
#===============================================================================
config = getConfig('../module.conf')
Logger.register(config)
api = FastAPI(title=config['default']['title'])
ctrl = Control(api, config)

#===============================================================================
# API Interfaces
#===============================================================================