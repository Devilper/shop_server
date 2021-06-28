import logging
import os
import sys
import signal
import argparse
from concurrent import futures

import grpc
from loguru import logger

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)

from user_srv.proto import user_pb2_grpc
from user_srv.handler.user import UserServicer


def on_exit(signo, frame):
    logger.info("Process interrupted")
    sys.exit(0)


def serve():
    # 命令行启动
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        nargs="?",
                        type=str,
                        default="127.0.0.1",
                        help="binding ip"
                        )
    parser.add_argument("--port",
                        nargs="?",
                        type=str,
                        default=50051,
                        help="the listening port"
                        )
    args = parser.parse_args()

    logger.add("logs/user_srv_{time}.log")  # 日志大小
    # 开启线程池
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 添加server服务
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    # 绑定端口
    server.add_insecure_port(f'{args.ip}:{args.port}')
    logger.info(f"server start:{args.ip}:{args.port}")

    # 主进程退出信号监听
    signal.signal(signal.SIGINT, on_exit)  # 中止信号 ctrl+c
    signal.signal(signal.SIGTERM, on_exit)  # 中止信号 kill
    # server 启动
    server.start()
    # 主进程等待
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
