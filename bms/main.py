# -*- coding: utf-8 -*-
"""This is the entry point to run the BDMS as a TornadoWeb service.
"""

__author__ = 'Institute of Earth science - SUPSI'
__version__ = '1.0.0'

from tornado import web
from tornado.options import define, options
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
import asyncpg
from tornado.httpserver import HTTPServer
import sys

sys.path.append('.')

define("port", default=8888, help="Tornado Web port", type=int)
define("pg_user", default="postgres", help="PostgrSQL database user")
define("pg_password", default="postgres", help="PostgrSQL user password")
define("pg_host", default="localhost", help="PostgrSQL database host")
define("pg_port", default="5432", help="PostgrSQL database port")
define("pg_database", default="bms", help="PostgrSQL database name")

async def get_conn():
    return await asyncpg.create_pool(
        user=options.pg_user, password=options.pg_password,
        database=options.pg_database, host=options.pg_host, port=options.pg_port)

async def release_pool(pool):
    await pool.close()

async def system_check(pool):
    async with pool.acquire() as conn:

        # Checking database version
        val = await conn.fetchval("""
            SELECT
                value_cfg
            FROM
                bdms.config
            WHERE
                name_cfg = 'VERSION';
        """)

    if val != __version__:
        from bms import DatabaseVersionMissmatch
        raise DatabaseVersionMissmatch()

if __name__ == "__main__":

    options.parse_command_line()

    from bms import (
        # Exceptions
        DatabaseVersionMissmatch,

        # user handlers
        SettingHandler,
        DownloadHandler,
        UserHandler,
        AdminHandler,
        WorkgroupAdminHandler,

        # Borehole handlers
        BoreholeViewerHandler,
        BoreholeProducerHandler,
        # BoreholeExporterHandler,
        ExportHandler,

        # Stratigraphy handlers
        StratigraphyViewerHandler,
        StratigraphyProducerHandler,

        # Layer handlers
        LayerViewerHandler,
        LayerProducerHandler,

        # Workflow handlers
        WorkflowProducerHandler,

        # Other handlers
        GeoapiHandler,
        ProjectHandler,
        CodeListHandler,
        MunicipalityHandler,
        CantonHandler,
        Wmts,
        Wms,
        # GetFeature
    )

    AsyncIOMainLoop().install()
    ioloop = asyncio.get_event_loop()
    ioloop.set_debug(enabled=True)

    settings = dict(
        debug=True
    )

    application = web.Application([

        # Borehole handlers
        (r'/api/v1/setting', SettingHandler),
        (r'/api/v1/setting/download', DownloadHandler),
        (r'/api/v1/user', UserHandler),
        (r'/api/v1/user/edit', AdminHandler),

        (r'/api/v1/user/workgroup/edit', WorkgroupAdminHandler),

        # Borehole handlers
        (r'/api/v1/borehole', BoreholeViewerHandler),
        (r'/api/v1/borehole/edit', BoreholeProducerHandler),
        (r'/api/v1/borehole/download', ExportHandler),
        (r'/api/v1/borehole/upload', BoreholeProducerHandler),

        # Workflow handlers
        (r'/api/v1/workflow/edit', WorkflowProducerHandler),

        # Stratigraphy handlers
        (r'/api/v1/borehole/stratigraphy', StratigraphyViewerHandler),
        (r'/api/v1/borehole/stratigraphy/edit', StratigraphyProducerHandler),

        # Layer handlers
        (r'/api/v1/borehole/stratigraphy/layer', LayerViewerHandler),
        (r'/api/v1/borehole/stratigraphy/layer/edit', LayerProducerHandler),

        # Other handlers
        # (r'/api/v1/borehole/project', ProjectHandler),
        (r'/api/v1/borehole/codes', CodeListHandler),
        (r'/api/v1/geoapi/municipality', MunicipalityHandler),
        (r'/api/v1/geoapi/canton', CantonHandler),
        (r'/api/v1/geoapi/location', GeoapiHandler),
        (r"/api/v1/geoapi/wmts", Wmts),
        (r"/api/v1/geoapi/wms/swisstopo", Wms),
        # (r"/api/v1/geoapi/getfeature", GetFeature)

    ], **settings)

    application.pool = ioloop.run_until_complete(get_conn())

    try:
        ioloop.run_until_complete(system_check(application.pool))

        http_server = HTTPServer(application)
        http_server.listen(options.port)
        ioloop.run_forever()

    except DatabaseVersionMissmatch as ex:
        print(str(ex))
        print("Please update the database schema.")

    finally:
        print("Releasing connection pool..")
        ioloop.run_until_complete(release_pool(application.pool))
        print(" > done.")
