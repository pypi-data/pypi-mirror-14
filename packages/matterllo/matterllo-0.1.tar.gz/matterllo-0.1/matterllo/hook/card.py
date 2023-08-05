# -*- coding: utf-8 -*-
"""
    matterllo.hook.card
    ~~~~~~~~~~~~~~~~~~~

    The application to parse card action.

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""
from matterllo.hook import BaseHook


class Hook(BaseHook):

    def createCard(self, action):
        data = action['data']
        context = {
            'board_link': data['board']['shortLink'],
            'list_name': data['list']['name'],
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
        }
        payload = u':incoming_envelope: New card "[{card_name}](https://trello.com/c/{card_link})" added to list "[{list_name}](https://trello.com/b/{board_link})"'

        return payload.format(**context)

    def updateCard(self, action):
        data = action['data']
        if data.get('listAfter') and data.get('listBefore'):
            return self.moveCardToList(action=action)

        if data.get('old', False):
            if 'name' in data['old']:
                return self.renameCard(action)
            if 'desc' in data['old']:
                return self.renameCardDesc(action)

        if 'due' in data['card']:
            if data['card']['due']:
                return self.updateCardDueDate(action=action)
            return self.removeCardDueDate(action=action)

        if data['card'].get('closed', False):
            return self.archiveCard(action=action)

        return self.unarchiveCard(action=action)

    def archiveCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Card archived: "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def unarchiveCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Card unarchived: "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def renameCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'card_old_name': data['old']['name'],
        }
        payload = u':incoming_envelope: Card renamed from "{card_old_name}" to "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def renameCardDesc(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'card_desc': data['card']['desc'],
        }
        payload = u''':incoming_envelope: Card updated: "[{card_name}](https://trello.com/c/{card_link})"
**Description**: {card_desc}'''

        return payload.format(**context)

    def commentCard(self, action):
        data = action['data']
        context = {
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
            'member_creator': action['memberCreator']['fullName'],
            'comment': data['text'],
        }
        payload = u''':incoming_envelope: New comment on card "[{card_name}](https://trello.com/c/{card_link})" by `{member_creator}`
> {comment}'''

        return payload.format(**context)

    def moveCardFromBoard(self, action):
        data = action['data']
        context = {
            'board_target_name': data['boardTarget']['name'],
            'board_name': data['board']['name'],
            'board_link': data['board']['shortLink'],
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
        }
        payload = u':incoming_envelope: Card moved: "[{card_name}](https://trello.com/c/{card_link})" moved from "[{board_name}](https://trello.com/b/{board_link}) to board "{board_target_name}"'

        return payload.format(**context)

    def moveCardToBoard(self, action):
        data = action['data']
        context = {
            'board_source_name': data['boardSource']['name'],
            'board_name': data['board']['name'],
            'board_link': data['board']['shortLink'],
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
        }
        payload = u':incoming_envelope: Card moved: "[{card_name}](https://trello.com/c/{card_link})" moved to "[{board_name}](https://trello.com/b/{board_link}) from board "{board_source_name}"'

        return payload.format(**context)

    def updateCardDueDate(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'card_due': data['card']['due'],
        }
        payload = u''':incoming_envelope: Card updated: "[{card_name}](https://trello.com/c/{card_link})"
**Due Date**: Due {card_due}'''

        return payload.format(**context)

    def removeCardDueDate(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u''':incoming_envelope: Card updated: "[{card_name}](https://trello.com/c/{card_link})"
**Due Date**: Removed'''

        return payload.format(**context)

    def addMemberToCard(self, action):
        data = action['data']
        context = {
            'member': action['member']['fullName'],
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: New member `{member}` add to card "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def removeMemberFromCard(self, action):
        data = action['data']
        context = {
            'member': action['member']['fullName'],
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Member `{member}` remove to card "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def addLabelToCard(self, action):
        data = action['data']
        card = self.trello_client.get_card(data['card']['id'])
        labels = {l.name or l.color for l in card.labels}
        label = data['label'].get('name', None) or data['label']['color']
        labels.add(label)
        context = {
            'label_name': label,
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'labels': ', '.join(labels),
        }

        payload = u''':incoming_envelope: Label "{label_name}" added to card "[{card_name}](https://trello.com/c/{card_link})"'
**Labels**: {labels}'''

        return payload.format(**context)

    def removeLabelFromCard(self, action):
        data = action['data']
        card = self.trello_client.get_card(data['card']['id'])
        label = data['label'].get('name', None) or data['label']['color']
        labels = {l.name or l.color for l in card.labels}
        context = {
            'label_name': label,
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'labels': ', '.join(labels),
        }
        payload = u''':incoming_envelope: Label "{label_name}" removed from card "[{card_name}](https://trello.com/c/{card_link})"'
**Labels**: {labels}'''

        return payload.format(**context)

    def addAttachmentToCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'attachment_name': data['attachment']['name'],
            'attachment_url': data['attachment']['url'],
            'attachment_preview_url': data['attachment'].get('previewUrl', ''),
        }
        payload = u''':incoming_envelope: New attachment added to card "[{card_name}](https://trello.com/c/{card_link})"
[**{attachment_name}**]({attachment_url})
{attachment_preview_url}
'''
        return payload.format(**context)
