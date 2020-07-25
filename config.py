from environs import Env

env = Env()
env.read_env()


class Config:
    DATABASE_URI = env('DATABASE_URL')
    REDIS_URL = env('REDIS_URL')
    JWT_SECRET = env('JWT_SECRET') or 'secret'
    JWT_ALGORITHM = env('JWT_ALGORITHM') or 'HS256'
    JWT_EXP_DELTA_SECONDS = env('JWT_EXP_DELTA_SECONDS') or 3000