import argparse


def main():
    """
    命令工具户主入口
    :return: None
    """
    parser = argparse.ArgumentParser(description="A simple database migration tool")

    parser.add_argument("-e", dest="engine", default="postgres", choices=("postgres", "mysql", "sqlite3"),
                        help="database engine (default: %(default)s")
