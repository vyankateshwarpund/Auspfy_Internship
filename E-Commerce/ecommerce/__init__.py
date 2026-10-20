"""
ecommerce package initialization.
Ensures MySQL database connectivity using mysqlclient or PyMySQL fallback.
"""
try:
    import MySQLdb  # type: ignore # noqa: F401
except ImportError:
    try:
        import pymysql  # type: ignore
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
