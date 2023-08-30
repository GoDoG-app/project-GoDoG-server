class Config():
    # DB 관련 정보
    HOST = 'mydb.cpj8hyqbedp5.ap-northeast-2.rds.amazonaws.com'
    DATABASE = 'walktest_db'
    DB_USER = 'walktest_db_user'
    DB_PASSWORD = '5254'

        # 비번 암호화
    SALT = '0417hello~'

        # JWT 환경 변수 셋팅
    JWT_SECRET_KEY = 'hello~!by@13##hello'
    JWT_ACCESS_TOKEN_EXPIRES = False
    PROPAGATE_EXCEPTIONS = True

    AWS_ACCESS_KEY_ID = 'AKIAQ5336DFWLDN3FM4J'
    AWS_SECRET_ACCESS_KEY = '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'

    S3_BUCKET = 'project4-walking-app'
    S3_BASE_URL = 'https://'+S3_BUCKET+'.s3.amazonaws.com/'