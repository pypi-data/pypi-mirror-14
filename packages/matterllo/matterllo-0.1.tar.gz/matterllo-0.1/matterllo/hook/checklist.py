# -*- coding: utf-8 -*-
"""
    matterllo.hook.checklist
    ~~~~~~~~~~~~~~~~~~~~~~~~

    The application to parse card action.

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""
from matterllo.hook import BaseHook


class Hook(BaseHook):

    def addChecklistToCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'checklist_name': data['checklist']['name'],
        }
        payload = u':incoming_envelope: New checklist "[{checklist_name}](https://trello.com/c/{card_link})" add to card "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def createCheckItem(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'checkitem_name': data['checkItem']['name'],
        }
        payload = u':incoming_envelope: New checklist item "[{checkitem_name}](https://trello.com/c/{card_link})" add to card "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def updateCheckItemStateOnCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'checkitem_name': data['checkItem']['name'],
            'member_fullname': action['memberCreator']['fullName'],
        }
        payload = u':incoming_envelope: Checklist item "{checkitem_name}" on card "[{card_name}](https://trello.com/c/{card_link})" was completed by `{member_fullname}`'
        if data['checkItem']['state'] == 'incomplete':
            payload = u':incoming_envelope: Checklist item "{checkitem_name}" on card "[{card_name}](https://trello.com/c/{card_link})" was marked incomplete by `{member_fullname}`'

        return payload.format(**context)

