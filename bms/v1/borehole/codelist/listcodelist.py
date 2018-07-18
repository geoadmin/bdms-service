# -*- coding: utf-8 -*-
from bms.v1.action import Action


class ListCodeList(Action):

    async def execute(self, schema=None):
        recs = await self.conn.fetch("""
            SELECT
                DISTINCT schema_cli
            FROM
                public.codelist
        """)
        data = {}
        for rec in recs:
            val = await self.conn.fetchval("""
                SELECT
                    array_to_json(
                        array_agg(
                            row_to_json(t)
                        )
                    )
                FROM (
                    SELECT
                        id_cli as id,
                        code_cli as code,
                        (
                            select row_to_json(t)
                            FROM (
                                SELECT
                                    text_cli_en as text,
                                    description_cli_en as descr
                            ) t
                        ) as en,
                        (
                            select row_to_json(t)
                            FROM (
                                SELECT
                                    COALESCE(
                                        text_cli_de,
                                        text_cli_en
                                    ) as text,
                                    COALESCE(
                                        description_cli_de,
                                        description_cli_en
                                    ) as descr
                            ) t
                        ) as de,
                        (
                            select row_to_json(t)
                            FROM (
                                SELECT
                                    COALESCE(
                                        text_cli_fr,
                                        text_cli_en
                                    ) as text,
                                    COALESCE(
                                        description_cli_fr,
                                        description_cli_en
                                    ) as descr
                            ) t
                        ) as fr,
                        (
                            select row_to_json(t)
                            FROM (
                                SELECT
                                    COALESCE(
                                        text_cli_it,
                                        text_cli_en
                                    ) as text,
                                    COALESCE(
                                        description_cli_it,
                                        description_cli_en
                                    ) as descr
                            ) t
                        ) as it
                    FROM
                        public.codelist
                    WHERE
                        schema_cli = $1
                    ORDER BY
                        order_cli
                ) AS t
            """, rec[0])
            data[rec[0]] = self.decode(val)

        return {
            "data": data
        }
