import argparse
import asyncio
import aiohttp
from app import create_app

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print('Lib uvloop not exist')

parser = argparse.ArgumentParser('Cookbook service')
parser.add_argument('--host', help='Host to listen', default='0.0.0.0')
parser.add_argument('--port', help='Port to accept connections', default=5000)
parser.add_argument('--dev', action="store_true", help="Dev environment")

args = parser.parse_args()

app = create_app(args.dev)

if args.dev:
    print('Start with code reload')
    import aioreloader
    aioreloader.start()

if __name__ == '__main__':
    aiohttp.web.run_app(app, host=args.host, port=args.port)
