# -*- coding: utf-8 -*-
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

if __name__ == "__main__":

    options.parse_command_line()

    from bms import (
        # user handlers
        SettingHandler,
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
        Wms
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
        (r'/api/v1/user', UserHandler),
        (r'/api/v1/user/edit', AdminHandler),

        (r'/api/v1/user/workgroup/edit', WorkgroupAdminHandler),

        # Borehole handlers
        (r'/api/v1/borehole', BoreholeViewerHandler),
        (r'/api/v1/borehole/edit', BoreholeProducerHandler),
        (r'/api/v1/borehole/download', ExportHandler),

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
        (r"/api/v1/geoapi/wms/swisstopo", Wms)

    ], **settings)

    application.pool = ioloop.run_until_complete(get_conn())

    http_server = HTTPServer(application)
    http_server.listen(options.port)
    ioloop.run_forever()
