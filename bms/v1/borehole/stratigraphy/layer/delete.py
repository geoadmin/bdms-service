# -*- coding: utf-8 -*-
from bms.v1.action import Action
from .list import ListLayers
from .patch import PatchLayer
from bms.v1.exceptions import (
    ActionWrong
)


class DeleteLayer(Action):

    async def execute(self, id, user_id, then = 0, value = None):
        if then == 0:
            # Just delete the layer
            await self.delete(id)

        else:

            # Get borehole id
            id_sty = await self.conn.fetchval("""
                SELECT
                    id_sty_fk
                FROM
                    layer
                WHERE
                    id_lay = $1
            """, id)

            print(f'id_sty_fk: {id_sty}')

            # Get all layers
            layers = await (
                ListLayers(self.conn)
            ).execute(id_sty)

            patch = PatchLayer(self.conn)

            cnt = len(layers['data'])

            print(layers)
            print(f"layers: {cnt}")

            for index in range(0, cnt):

                layer = layers['data'][index]

                if layer['id'] == id:

                    upper = None
                    lower = None

                    if index > 0:
                        upper = layers['data'][(index-1)]

                    if (index+1) < cnt:
                        lower = layers['data'][(index+1)]

                    if then == 1:  # Extend upper layer to bottom

                        if upper == None:
                            raise ActionWrong()

                        depth = None

                        if (
                            lower == None or
                            lower['depth_from'] is None
                        ):
                            depth = layer['depth_to']
                        else:
                            depth = lower['depth_from']

                        await patch.execute(
                            upper['id'],
                            'depth_to',
                            depth,
                            user_id
                        )

                    elif then == 2:  # Extend lower layer to top

                        if lower == None:
                            raise ActionWrong()

                        depth = None

                        if (
                            upper == None or
                            upper['depth_to'] is None
                        ):
                            depth = layer['depth_from']
                        else:
                            depth = upper['depth_to']

                        await patch.execute(
                            lower['id'],
                            'depth_from',
                            depth,
                            user_id
                        )

                    elif then == 3:

                        if upper == None and lower == None:
                            raise ActionWrong()

                        # Set top depth of lower level to given value
                        if lower is not None:
                            await patch.execute(
                                lower['id'],
                                'depth_from',
                                value,
                                user_id
                            )

                        # Set base depth of upper level to given value
                        if upper is not None:
                            await patch.execute(
                                upper['id'],
                                'depth_to',
                                value,
                                user_id
                            )

                    # Finally delete the layer
                    await self.delete(id)
                    break

    async def delete(self, id):
        await self.conn.fetchval("""
            DELETE FROM public.layer
            WHERE id_lay = $1
        """, id)
