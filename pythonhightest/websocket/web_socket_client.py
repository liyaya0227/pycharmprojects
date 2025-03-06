#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: lijiahui
@version: V1.0
@file: web_socket_client.py
@time: 2024/7/4
"""
import asyncio
import json

import websockets

from tools.logger import log


class WebSocketClient:
    def __init__(self, url, initial_message):
        self.url = url
        self.initial_message = initial_message

    async def connect_and_receive(self, max_messages=0):
        async with websockets.connect(self.url) as websocket:
            # 发送初始消息到服务器
            await websocket.send(self.initial_message)

            message_count = 0  # 消息计数器
            message_list = []  # 消息列表

            try:
                async for message in websocket:
                    message_list.append(json.loads(message))
                    message_count += 1
                    if max_messages and message_count >= max_messages:
                        log.info(f"Reached maximum messages ({max_messages}), closing connection.")
                        return message_list
            except websockets.ConnectionClosed:
                log.error("WebSocket connection closed")
                return []
            except Exception as e:
                log.error(f"Error in websocket: {e}")
                return []


def web_socket_run(uri: str, message: str, max_messages: int = 1) -> list:
    """
    :param uri: W3C WebSocket URI
    :param message: 发送的消息
    :param max_messages: 最大接受消息数
    :return:
    """
    client = WebSocketClient(uri, message)
    try:
        return asyncio.run(client.connect_and_receive(max_messages))
    except Exception as e:
        log.error(f"Error in web_socket_run: {e}")
        return []
