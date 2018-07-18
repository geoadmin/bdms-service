# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CheckBorehole(Action):

    async def execute(self, attribute, text):
        sql = None
        if attribute == 'extended.original_name':
            sql = """
                SELECT EXISTS(
                    SELECT 1
                    FROM borehole
                    WHERE original_name_bho = $1
                ) AS exists
            """
        elif attribute == 'custom.public_name':
            sql = """
                SELECT EXISTS(
                    SELECT 1
                    FROM borehole
                    WHERE public_name_bho = $1
                ) AS exists;
            """
        else:
            raise Exception("attribute '%s' unknown" % attribute)

        val = await self.conn.fetchval(sql, text)
        return {
            "check": not val
        }
