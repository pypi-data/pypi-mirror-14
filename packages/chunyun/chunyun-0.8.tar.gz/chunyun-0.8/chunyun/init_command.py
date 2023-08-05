from configparser import ConfigParser
import os
import shutil

from .command import Command


SQL_TPL = """
-- @up
---------------------------------------------------------------------

{up}

-- @down
---------------------------------------------------------------------

"""
INIT_MIGRATION_TABLE = "'CREATE TABLE IF NOT EXISTS chunyun_migrations(id serial primary key, name varchar not null, created_at TIMESTAMPTZ default CURRENT_TIMESTAMP(0));'"
INIT_RECORD = "'INSERT INTO chunyun_migrations(name) VALUES($$001_init.sql$$)'";


class InitCommand(Command):

    def dump(self, option):
        os.environ['PGPASSWORD'] = option.get(self.args.env, "password")
        handle = os.popen("pg_dump -h {host} -p {port}  -U {user} -x -O -s {name}".format(
                            host=option.get(self.args.env, 'host'),
                            port=option.get(self.args.env, 'port'),
                            user=option.get(self.args.env, 'user'),
                            name=option.get(self.args.env, 'database')))
        output = handle.read()
        handle.close()
        return output

    def create_migration_table(self, option):
        os.environ['PGPASSWORD'] = option.get(self.args.env, "password")
        cmd = "psql -h {host} -p {port}  -U {user} {name} -c {sql}".format(
                            host=option.get(self.args.env, 'host'),
                            port=option.get(self.args.env, 'port'),
                            user=option.get(self.args.env, 'user'),
                            name=option.get(self.args.env, 'database'),
                            sql=INIT_MIGRATION_TABLE)
        handle = os.popen(cmd)
        output = handle.read()
        handle.close()
        print(output)

    def insert_init_record(self, option):
        os.environ['PGPASSWORD'] = option.get(self.args.env, "password")
        cmd = "psql -h {host} -p {port}  -U {user} {name} -c {sql}".format(
                            host=option.get(self.args.env, 'host'),
                            port=option.get(self.args.env, 'port'),
                            user=option.get(self.args.env, 'user'),
                            name=option.get(self.args.env, 'database'),
                            sql=INIT_RECORD)
        handle = os.popen(cmd)
        output = handle.read()
        handle.close()
        print(output)

    def run(self):
        # 同步数据库
        if not os.path.exists("config.ini"):
            raise Exception("你必须先创建项目")

        pg_dump = shutil.which('pg_dump')
        if pg_dump is None:
            raise Exception("确保系统具备pg_dump命令")

        psql = shutil.which('psql')
        if pg_dump is None:
            raise Exception("确保系统具备psql命令")

        parser = ConfigParser()
        parser.read("config.ini")
        dumps = self.dump(parser)
        # 插入migration表
        self.create_migration_table(parser)
        # 导出当前数据库结构
        content = SQL_TPL.format(up=dumps)

        if not os.path.exists("migrations"):
            os.makedirs("migrations")

        with open("migrations/001_init.sql", "w") as handle:
            handle.write(content)

        self.insert_init_record(parser)



