# -*- coding: utf-8 -*-
"""Unofficial Telegram Bot API

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from requests import Request, Session
from collections import namedtuple
from abc import ABCMeta, abstractmethod
from threading import Thread
from enum import Enum

import json

"""
Telegram Bot API Types as defined at https://core.telegram.org/bots/api#available-types
"""
_UserBase = namedtuple('User', ['id', 'first_name', 'last_name', 'username'])


class User(_UserBase):

    """This object represents a Telegram user or bot.

    Attributes:
        id (int): Unique identifier for this user or bot
        first_name (str): User‘s or bot’s first name
        last_name (Optional[str]): User‘s or bot’s last name
        username (Optional[str]): User‘s or bot’s username

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return User(
            id=result.get('id'),
            first_name=result.get('first_name'),
            last_name=result.get('last_name'),
            username=result.get('username')
            )


_ChatBase = namedtuple('Chat', ['id', 'type', 'title', 'username', 'first_name', 'last_name'])


class Chat(_ChatBase):
    """This object represents a chat.

    Attributes:
        id	        (int)	:Unique identifier for this chat, not exceeding 1e13 by absolute value
        type	    (str)	:Type of chat, can be either “private”, or “group”, or “channel”
        title	    (str)	:*Optional.* Title, for channels and group chats
        username	(str)	:*Optional.* Username, for private chats and channels if available
        first_name	(str)	:*Optional.* First name of the other party in a private chat
        last_name	(str)	:*Optional.* Last name of the other party in a private chat

    """

    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Chat(
            id=result.get('id'),
            type=result.get('type'),
            title=result.get('title'),
            username=result.get('username'),
            first_name=result.get('first_name'),
            last_name=result.get('last_name'),
        )

_MessageBase = namedtuple('Message', [
    'message_id', 'sender', 'date', 'chat', 'forward_from', 'forward_date',
    'reply_to_message', 'text', 'audio', 'document', 'photo', 'sticker',
    'video', 'voice', 'caption', 'contact', 'location', 'new_chat_participant',
    'left_chat_participant', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
    'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
    'migrate_from_chat_id'])


class Message(_MessageBase):

    """This object represents a message.

    Attributes:
        message_id              (int)                 :Unique message identifier
        from                    (User)                :*Optional.* Sender, can be empty for messages sent to channels
        date                    (int)                 :Date the message was sent in Unix time
        chat                    (Chat)                :Conversation the message belongs to
        forward_from            (User)                :*Optional.* For forwarded messages, sender of the original message
        forward_date            (int)                 :*Optional.* For forwarded messages, date the original message was
                                                                  sent in Unix time
        reply_to_message        (Message)             :*Optional.* For replies, the original message. Note that the
                                                                   Message object in this field will not contain further
                                                                   reply_to_message fields even if it itself is a reply.
        text                    (str)                 :*Optional.* For text messages, the actual UTF-8 text of the message
        audio                   (Audio)               :*Optional.* Message is an audio file, information about the file
        document                (Document)            :*Optional.* Message is a general file, information about the file
        photo                   (Sequence[PhotoSize]) :*Optional.* Message is a photo, available sizes of the photo
        sticker                 (Sticker)             :*Optional.* Message is a sticker, information about the sticker
        video                   (Video)               :*Optional.* Message is a video, information about the video
        voice                   (Voice)               :*Optional.* Message is a voice message, information about the file
        caption                 (str)                 :*Optional.* Caption for the photo or video
        contact                 (Contact)             :*Optional.* Message is a shared contact, information about
                                                                   the contact
        location                (Location)            :*Optional.* Message is a shared location, information about the
                                                                   location
        new_chat_participant    (User)                :*Optional.* A new member was added to the group, information about
                                                                   them (this member may be bot itself)
        left_chat_participant   (User)                :*Optional.* A member was removed from the group, information about
                                                                  them (this member may be bot itself)
        new_chat_title          (str)                 :*Optional.* A group title was changed to this value
        new_chat_photo          (Sequence[PhotoSize]) :*Optional.* A group photo was change to this value
        delete_chat_photo       (bool)                :*Optional.* Informs that the group photo was deleted
        group_chat_created      (bool)                :*Optional.* Informs that the group has been created
        supergroup_chat_created (bool)                :*Optional.* Service message: the supergroup has been created
        channel_chat_created    (bool)                :*Optional.* Service message: the channel has been created
        migrate_to_chat_id		(int)                 :*Optional.* The group has been migrated to a supergroup with
                                                       the specified identifier, not exceeding 1e13 by absolute value
        migrate_from_chat_id    (int)                 :*Optional.* The supergroup has been migrated from a group
                                                       with the specified identifier, not exceeding 1e13 by absolute value

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        # photo is a list of PhotoSize
        photo = result.get('photo')
        if photo is not None:
            photo = [PhotoSize.from_result(photo_size) for photo_size in photo]

        return Message(
            message_id=result.get('message_id'),
            sender=User.from_result(result.get('from')),
            date=result.get('date'),
            chat=Chat.from_result(result.get('chat')),
            forward_from=User.from_result(result.get('forward_from')),
            forward_date=result.get('forward_date'),
            reply_to_message=Message.from_result(result.get('reply_to_message')),
            text=result.get('text'),
            audio=Audio.from_result(result.get('audio')),
            document=Document.from_result(result.get('document')),
            photo=photo,
            sticker=Sticker.from_result(result.get('sticker')),
            video=Video.from_result(result.get('video')),
            voice=Voice.from_result(result.get('voice')),
            caption=result.get('caption'),
            contact=Contact.from_result(result.get('contact')),
            location=Location.from_result(result.get('location')),
            new_chat_participant=User.from_result(result.get('new_chat_participant')),
            left_chat_participant=User.from_result(result.get('left_chat_participant')),
            new_chat_title=result.get('new_chat_title'),
            new_chat_photo=result.get('new_chat_photo'),
            delete_chat_photo=result.get('delete_chat_photo'),
            group_chat_created=result.get('group_chat_created'),
            supergroup_chat_created=result.get('supergroup_chat_created'),
            channel_chat_created=result.get('channel_chat_created'),
            migrate_to_chat_id=result.get('migrate_to_chat_id'),
            migrate_from_chat_id=result.get('migrate_from_chat_id'),
            )

_PhotoSizeBase = namedtuple('PhotoSize', ['file_id', 'width', 'height', 'file_size'])


class PhotoSize(_PhotoSizeBase):

    """This object represents one size of a photo or a file / sticker thumbnail.

    Attributes:
        file_id    (str)  :Unique identifier for this file
        width      (int)  :Photo width
        height     (int)  :Photo height
        file_size  (int)  :*Optional.* File size
    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return PhotoSize(
            file_id=result.get('file_id'),
            width=result.get('width'),
            height=result.get('height'),
            file_size=result.get('file_size')
            )


_AudioBase = namedtuple('Audio', ['file_id', 'duration', 'mime_type', 'file_size'])


class Audio(_AudioBase):

    """This object represents a generic audio file (not voice note).

    Attributes:
        file_id    (str)  :Unique identifier for this file
        duration   (int)  :Duration of the audio in seconds as defined by sender
        performer  (str)  :*Optional.* Performer of the audio as defined by sender or by audio tags
        title      (str)  :*Optional.* Title of the audio as defined by sender or by audio tags
        mime_type  (str)  :*Optional.* MIME type of the file as defined by sender
        file_size  (int)  :*Optional.* File size

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Audio(
            file_id=result.get('file_id'),
            duration=result.get('duration'),
            mime_type=result.get('mime_type'),
            file_size=result.get('file_size')
            )


_DocumentBase = namedtuple('Document', ['file_id', 'thumb', 'file_name', 'mime_type', 'file_size'])


class Document(_DocumentBase):

    """This object represents a general file (as opposed to photos and audio files).

    Attributes:
        file_id    (str)        :Unique file identifier
        thumb      (PhotoSize)  :*Optional.* Document thumbnail as defined by sender
        file_name  (str)        :*Optional.* Original filename as defined by sender
        mime_type  (str)        :*Optional.* MIME type of the file as defined by sender
        file_size  (int)        :*Optional.* File size

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Document(
            file_id=result.get('file_id'),
            thumb=PhotoSize.from_result(result.get('thumb')),
            file_name=result.get('file_name'),
            mime_type=result.get('mime_type'),
            file_size=result.get('file_size')
            )


_StickerBase = namedtuple('Sticker', ['file_id', 'width', 'height', 'thumb', 'file_size'])


class Sticker(_StickerBase):

    """This object represents a sticker.

    Attributes:
        file_id    (str)        :Unique identifier for this file
        width      (int)        :Sticker width
        height     (int)        :Sticker height
        thumb      (PhotoSize)  :*Optional.* Sticker thumbnail in .webp or .jpg format
        file_size  (int)        :*Optional.* File size

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Sticker(
            file_id=result.get('file_id'),
            width=result.get('width'),
            height=result.get('height'),
            thumb=PhotoSize.from_result(result.get('thumb')),
            file_size=result.get('file_size')
            )


_VideoBase = namedtuple('Video', [
    'file_id', 'width', 'height', 'duration', 'thumb', 'mime_type', 'file_size'])


class Video(_VideoBase):

    """This object represents a video file.

    Attributes:
        file_id     (str)       :Unique identifier for this file
        width       (int)       :Video width as defined by sender
        height      (int)       :Video height as defined by sender
        duration    (int)       :Duration of the video in seconds as defined by sender
        thumb       (PhotoSize) :*Optional.* Video thumbnail
        mime_type   (str)       :*Optional.* Mime type of a file as defined by sender
        file_size   (int)       :*Optional.* File size

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Video(
            file_id=result.get('file_id'),
            width=result.get('width'),
            height=result.get('height'),
            duration=result.get('duration'),
            thumb=PhotoSize.from_result(result.get('thumb')),
            mime_type=result.get('mime_type'),
            file_size=result.get('file_size')
            )


_VoiceBase = namedtuple('Audio', ['file_id', 'duration', 'mime_type', 'file_size'])


class Voice(_VoiceBase):

    """This object represents an voice node audio file.

    Attributes:
        file_id    (str)  :Unique identifier for this file
        duration   (int)  :Duration of the audio in seconds as defined by sender
        mime_type  (str)  :*Optional.* MIME type of the file as defined by sender
        file_size  (int)  :*Optional.* File size

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Audio(
            file_id=result.get('file_id'),
            duration=result.get('duration'),
            mime_type=result.get('mime_type'),
            file_size=result.get('file_size')
        )


_ContactBase = namedtuple('Contact', ['phone_number', 'first_name', 'last_name', 'user_id'])


class Contact(_ContactBase):

    """This object represents a phone contact.

    Attributes:
        phone_number    (str)  :Contact's phone number
        first_name      (str)  :Contact's first name
        last_name       (str)  :*Optional.* Contact's last name
        user_id         (int)  :*Optional.* Contact's user identifier in Telegram

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Contact(
            phone_number=result.get('phone_number'),
            first_name=result.get('first_name'),
            last_name=result.get('last_name'),
            user_id=result.get('user_id')
            )


_LocationBase = namedtuple('Location', ['longitude', 'latitude'])


class Location(_LocationBase):

    """This object represents a point on the map.

    Attributes:
        longitude   (float)   :Longitude as defined by sender
        latitude    (float)   :Latitude as defined by sender

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return Location(
            longitude=result.get('longitude'),
            latitude=result.get('latitude')
            )


_UpdateBase = namedtuple('Update', ['update_id', 'message', 'inline_query', 'chosen_inline_result'])


class Update(_UpdateBase):

    """This object represents an incoming update.

    Attributes:
        update_id               (int)                :The update‘s unique identifier. Update identifiers start from a certain
                                                      positive number and increase sequentially. This ID becomes especially handy
                                                      if you’re using Webhooks, since it allows you to ignore repeated updates or to
                                                      restore the correct update sequence, should they get out of order.
        message                 (Message)            :*Optional.* New incoming message of any kind — text, photo, sticker, etc.
        inline_query            (InlineQuery)        :*Optional.* New incoming inline query
        chosen_inline_result	(ChosenInlineResult) :*Optional.* The result of a inline query that was chosen by
                                                      a user and sent to their chat partner

    """
    __slots__ = ()

    @staticmethod
    def from_dict(message_update):
        if message_update is None:
            return None

        return Update(message_update.get('update_id'),
                      Message.from_result(message_update.get('message')),
                      InlineQuery.from_result(message_update.get('inline_query')),
                      ChosenInlineResult.from_result(message_update.get('chosen_inline_result')))

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return [Update.from_dict(message_update) for message_update in result]


_InputFileInfoBase = namedtuple('InputFileInfo', ['file_name', 'fp', 'mime_type'])


class InputFileInfo(_InputFileInfoBase):
    __slots__ = ()


_InputFileBase = namedtuple('InputFile', ['form', 'file_info'])


class InputFile(_InputFileBase):

    """This object represents the contents of a file to be uploaded. Must be posted using multipart/form-data
        in the usual way that files are uploaded via the browser.

        Attributes:
            form        (str)           :the form used to submit (e.g. 'photo')
            file_info   (InputFileInfo) :The file metadata required

        :Example:

            ::

                fp = open('foo.png', 'rb')
                file_info = InputFileInfo('foo.png', fp, 'image/png')

                InputFile('photo', file_info)

                bot.send_photo(chat_id=12345678, photo=InputFile)

            .. note::

                While creating the FileInput currently requires a reasonable amount
                of preparation just to send a file. This class will be extended
                in the future to make the process easier.

    """
    __slots__ = ()


_UserProfilePhotosBase = namedtuple('UserProfilePhotos', ['total_count', 'photos'])


class UserProfilePhotos(_UserProfilePhotosBase):

    """This object represent a user's profile pictures.

    Attributes:
        total_count (int): Total number of profile pictures the target user has
        photos      (list of list of PhotoSize): Requested profile pictures (in up to 4 sizes each)

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        photos = []
        for photo_list in result.get('photos'):
            photos.append([PhotoSize.from_result(photo) for photo in photo_list])

        return UserProfilePhotos(
            total_count=result.get('total_count'),
            photos=photos
            )


_FileBase = namedtuple('File', ['file_id', 'file_size', 'file_path'])


class File(_FileBase):

    """This object represents a file ready to be downloaded.

    Attributes:
        file_id (str): Unique identifier for this file
        file_size (int): *Optional.* File size, if known
        file_path (str): *Optional.* File path. Use https://api.telegram.org/file/bot<token>/<file_path>
                         to get the file. It is guaranteed that the link will be valid for at least 1 hour.
    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return File(
            file_id=result.get('file_id'),
            file_size=result.get('file_size'),
            file_path=result.get('file_path')
        )


class File(_FileBase):

    """This object represents a file ready to be downloaded.

    Attributes:
        file_id (str): Unique identifier for this file
        file_size (int): *Optional.* File size, if known
        file_path (str): *Optional.* File path. Use https://api.telegram.org/file/bot<token>/<file_path>
                         to get the file. It is guaranteed that the link will be valid for at least 1 hour.
    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return File(
            file_id=result.get('file_id'),
            file_size=result.get('file_size'),
            file_path=result.get('file_path')
        )


class ReplyMarkup:
    __metaclass__ = ABCMeta
    __slots__ = ()

    @abstractmethod
    def serialize(self):
        raise NotImplementedError("")


_ReplyKeyboardMarkupBase = namedtuple('ReplyKeyboardMarkup', [
    'keyboard', 'resize_keyboard', 'one_time_keyboard', 'selective'])


class ReplyKeyboardMarkup(_ReplyKeyboardMarkupBase, ReplyMarkup):

    """This object represents a custom keyboard with reply options (see Introduction to bots for details and examples).

    Attributes:
        keyboard            (list of list of str)   :Array of button rows, each represented by an Array of Strings
        resize_keyboard     (bool)  :*Optional.* Requests clients to resize the keyboard vertically for optimal
                                        fit (e.g., make the keyboard smaller if there are just two rows of buttons).
                                        Defaults to false, in which case the custom keyboard is always of the
                                        same height as the app's standard keyboard.
        one_time_keyboard   (bool)  :*Optional.* Requests clients to hide the keyboard as soon as it's been
                                        used. Defaults to false.
        selective           (bool)  :*Optional.* Use this parameter if you want to show the keyboard to
                                        specific users only. Targets:

                                            1. users that are @mentioned in the text of the Message object;
                                            2. if the bot's message is a reply (has reply_to_message_id), sender
                                               of the original message.

                                        :example: A user requests to change the bot‘s language, bot replies to the
                                            request with a keyboard to select the new language. Other users in the
                                            group don’t see the keyboard.

    :Example:

        ::

                keyboard = [
                ['7', '8', '9'],
                ['4', '5', '6'],
                ['1', '2', '3'],
                     ['0']
                ]

                reply_markup = ReplyKeyboardMarkup.create(keyboard)
                bot.send_message(12345678, 'testing reply_markup', reply_markup=reply_markup)

    """
    __slots__ = ()

    @staticmethod
    def create(keyboard, resize_keyboard=None, one_time_keyboard=None, selective=None):
        return ReplyKeyboardMarkup(keyboard, resize_keyboard, one_time_keyboard, selective)

    def serialize(self):
        reply_markup = dict(keyboard=self.keyboard)

        if self.resize_keyboard is not None:
            reply_markup['resize_keyboard'] = bool(self.resize_keyboard)

        if self.one_time_keyboard is not None:
            reply_markup['one_time_keyboard'] = bool(self.one_time_keyboard)

        if self.selective is not None:
            reply_markup['selective'] = bool(self.selective)

        return json.dumps(reply_markup)


_ReplyKeyboardHideBase = namedtuple('ReplyKeyboardHide', ['hide_keyboard', 'selective'])


class ReplyKeyboardHide(_ReplyKeyboardHideBase, ReplyMarkup):

    """Upon receiving a message with this object, Telegram clients will hide the current custom keyboard and
        display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard
        is sent by a bot. An exception is made for one-time keyboards that are hidden immediately after the
        user presses a button (see :class:`ReplyKeyboardMarkup`).

    Attributes:
        hide_keyboard   (``True``)  :Requests clients to hide the custom keyboard
        selective       (bool)      :*Optional.* Use this parameter if you want to hide keyboard for specific
                                    users only. Targets:

                                        1. users that are @mentioned in the text of the Message object;
                                        2. if the bot's message is a reply (has reply_to_message_id), sender
                                           of the original message.

                                    :example: A user votes in a poll, bot returns confirmation message in reply
                                        to the vote and hides keyboard for that user, while still showing the
                                        keyboard with poll options to users who haven't voted yet.

    """
    __slots__ = ()

    @staticmethod
    def create(selective=None):
        return ReplyKeyboardHide(True, selective)

    def serialize(self):
        reply_markup = dict(
            hide_keyboard=True
            )

        if self.selective is not None:
            reply_markup['selective'] = bool(self.selective)

        return json.dumps(reply_markup)


_ForceReplyBase = namedtuple('ForceReply', ['force_reply', 'selective'])


class ForceReply(_ForceReplyBase, ReplyMarkup):

    """Upon receiving a message with this object, Telegram clients will display a reply interface to the user
        (act as if the user has selected the bot‘s message and tapped ’Reply'). This can be extremely useful
        if you want to create user-friendly step-by-step interfaces without having to sacrifice privacy mode.

    Attributes:
        force_reply (``True``)  :Shows reply interface to the user, as if they manually selected the bot‘s
                                    message and tapped ’Reply'
        selective   (bool)      :Optional. Use this parameter if you want to force reply from specific users
                                    only. Targets: 1) users that are @mentioned in the text of the Message
                                    object; 2) if the bot's message is a reply (has reply_to_message_id),
                                    sender of the original message.

    :Example: A poll bot for groups runs in privacy mode (only receives commands, replies to its messages and
        mentions). There could be two ways to create a new poll:

            * Explain the user how to send a command with parameters (e.g. /newpoll question answer1 answer2).
              May be appealing for hardcore users but lacks modern day polish.
            * Guide the user through a step-by-step process. ‘Please send me your question’, ‘Cool, now let’s
              add the first answer option‘, ’Great. Keep adding answer options, then send /done when you‘re ready’.

    The last option is definitely more attractive. And if you use ForceReply in your bot‘s questions, it will
    receive the user’s answers even if it only receives replies, commands and mentions — without any extra
    work for the user.

    """
    __slots__ = ()

    @staticmethod
    def create(selective=None):
        return ForceReply(True, selective)

    def serialize(self):
        reply_markup = dict(force_reply=True)
        if self.selective is not None:
            reply_markup['selective'] = bool(self.selective)

        return json.dumps(reply_markup)


_InlineQueryBase = namedtuple('InlineQuery', ['id', 'sender', 'query', 'offset'])
class InlineQuery(_InlineQueryBase):
    """ This object represents an incoming inline query. When the user sends an empty query,
        your bot could return some default or trending results.

    Attributes:
        id     (str)  :Unique identifier for this query
        sender (User) :Sender
        query  (str)  :Text of the query
        offset (str)  :Offset of the results to be returned, can be controlled by the bot

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return InlineQuery(
            id=result.get('id'),
            sender=User.from_result(result.get('from')),
            query=result.get('query'),
            offset=result.get('offset'),
            )


_ChosenInlineResultBase = namedtuple('ChosenInlineResult', ['result_id', 'sender', 'query'])
class ChosenInlineResult(_ChosenInlineResultBase):
    """ This object represents an incoming inline query. When the user sends an empty query,
        your bot could return some default or trending results.

    Attributes:
        result_id     (str)  :The unique identifier for the result that was chosen.
        sender (User) :The user that chose the result.
        query  (str)  :The query that was used to obtain the result.

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        if result is None:
            return None

        return ChosenInlineResult(
            result_id=result.get('result_id'),
            sender=User.from_result(result.get('from')),
            query=result.get('query'),
            )

"""
InlineQuery Types
"""


class InlineQueryResult:
    pass


class InlineQueryResultArticle(InlineQueryResult):
    """ Represents a link to an article or web page.

    Attributes:
        id                       (str)  :Unique identifier of this result
        title                    (str)  :Title of the result
        message_text             (str)  :Text of the query
        parse_mode               (str)  :*Optional.* Send “Markdown”, if you want Telegram apps to show bold, italic and
                                         inline URLs in your bot's message.
        disable_web_page_preview (bool) :*Optional.* Disables link previews for links in the sent message
        url	                     (str)  :*Optional.* URL of the result
        hide_url	             (bool) :*Optional.* Pass True, if you don't want the URL to be shown in the message
        description              (str)  :*Optional.* Short description of the result
        thumb_url                (str)  :*Optional.* Url of the thumbnail for the result
        thumb_width              (int)  :*Optional.* Thumbnail width
        thumb_height             (int)  :*Optional.* Thumbnail height

    """

    def __init__(self, id, title, message_text,
                 parse_mode=None, disable_web_page_preview=None, url=None, hide_url=None, description=None,
                 thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = "article"
        self.id = id
        self.title = title
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.url = url
        self.hide_url = hide_url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height


class InlineQueryResultPhoto(InlineQueryResult):
    """ Represents a link to a photo. By default, this photo will be sent by the user with optional caption.
    Alternatively, you can provide message_text to send it instead of photo.

    Attributes:
        id                          (str)    :Unique identifier of this result
        photo_url                   (str)    :A valid URL of the photo. Photo size must not exceed 5MB
        mime_type                   (str)    :*Optional.* MIME type of the photo, defaults to image/jpeg
        photo_width                 (int)    :*Optional.* Width of the photo
        photo_height                (int)    :*Optional.* Height of the photo
        thumb_url                   (str)    :*Optional.* URL of the thumbnail for the photo
        title                       (str)    :*Optional.* Title for the result
        description                 (str)    :*Optional.* Short description of the result
        caption                     (str)    :*Optional.* Caption of the photo to be sent
        message_text                (str)    :*Optional.* Text of a message to be sent instead of the photo
        parse_mode                  (str)    :*Optional.* Send “Markdown”, if you want Telegram apps to show bold,
                                                          italic and inline URLs in your bot's message.
        disable_web_page_preview    (bool)   :*Optional.* Disables link previews for links in the sent message

    """

    def __init__(self, id, photo_url,
                 mime_type=None, photo_width=None, photo_height=None, thumb_url=None, title=None,
                 description=None, caption=None, message_text=None, parse_mode=None, disable_web_page_preview=None):
        self.type = "photo"
        self.id = id
        self.photo_url = photo_url
        self.mime_type = mime_type
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.thumb_url = thumb_url
        self.title = title
        self.description = description
        self.caption = caption
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview


class InlineQueryResultGif(InlineQueryResult):
    """ Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with
    optional caption. Alternatively, you can provide message_text to send it instead of the animation.

    Attributes:
        id                          (str)    :Unique identifier of this result
        gif_url                     (str)    :A valid URL for the GIF file. File size must not exceed 1MB
        gif_width                   (int)    :*Optional.* Width of the GIF
        gif_height                  (int)    :*Optional.* Height of the GIF
        thumb_url                   (str)    :*Optional.* URL of a static thumbnail for the result (jpeg or gif)
        title                       (str)    :*Optional.* Title for the result
        caption                     (str)    :*Optional.* Caption of the GIF file to be sent
        message_text                (str)    :*Optional.* Text of a message to be sent instead of the animation
        parse_mode                  (str)    :*Optional.* Send “Markdown”, if you want Telegram apps to show bold,
                                                          italic and inline URLs in your bot's message.
        disable_web_page_preview    (bool)   :*Optional.* Disables link previews for links in the sent message

    """

    def __init__(self, id, gif_url,
                 gif_width=None, gif_height=None, thumb_url=None, title=None,
                 caption=None, message_text=None, parse_mode=None, disable_web_page_preview=None):
        self.type = "gif"
        self.id = id
        self.gif_url = gif_url
        self.gif_width = gif_width
        self.gif_height = gif_height
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    """ Represents a link to a video animation (H.264/MPEG-4 AVC video without sound).
    By default, this animated MPEG-4 file will be sent by the user with optional caption. Alternatively,
    you can provide message_text to send it instead of the animation.

    Attributes:
        id                        (str)    :Unique identifier of this result
        mpeg4_url                 (str)    :A valid URL for the mp4 file. File size must not exceed 1MB
        mpeg4_width               (int)    :*Optional.* Width of the mp4
        mpeg4_height              (int)    :*Optional.* Height of the mp4
        thumb_url                 (str)    :*Optional.* URL of a static thumbnail for the result (jpeg or mpeg4)
        title                     (str)    :*Optional.* Title for the result
        caption                   (str)    :*Optional.* Caption of the mp4 file to be sent
        message_text              (str)    :*Optional.* Text of a message to be sent instead of the animation
        parse_mode                (str)    :*Optional.* Send “Markdown”, if you want Telegram apps to show bold,
                                                        italic and inline URLs in your bot's message.
        disable_web_page_preview  (bool)   :*Optional.* Disables link previews for links in the sent message

    """

    def __init__(self, id, mpeg4_url,
                 mpeg4_width=None, mpeg4_height=None, thumb_url=None, title=None,
                 caption=None, message_text=None, parse_mode=None, disable_web_page_preview=None):
        self.type = "mpeg4_gif"
        self.id = id
        self.mpeg4_url = mpeg4_url
        self.mpeg4_width = mpeg4_width
        self.mpeg4_height = mpeg4_height
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview


class InlineQueryResultVideo(InlineQueryResult):
    """ Represents link to a page containing an embedded video player or a video file.

    Attributes:
        type                     (str)     :Type of the result, must be video
        id                       (str)     :Unique identifier of this result
        video_url                (str)     :A valid URL for the embedded video player or video file
        mime_type                (str)     :Mime type of the content of video url, i.e. “text/html” or “video/mp4”
        message_text             (str)     :Text of a message to be sent instead of the video
        parse_mode               (str)     :*Optional.* Send “Markdown”, if you want Telegram apps to show bold, italic and inline URLs in your bot's message.
        disable_web_page_preview (bool)    :*Optional.* Disables link previews for links in the sent message
        video_width              (int)     :*Optional.* Video width
        video_height             (int)     :*Optional.* Video height
        video_duration           (int)     :*Optional.* Video duration in seconds
        thumb_url                (str)     :*Optional.* URL of the thumbnail (jpeg only) for the video
        title                    (str)     :*Optional.* Title for the result
        description              (str)     :*Optional.* Short description of the result

    """

    def __init__(self, id, video_url, mime_type,
                 message_text=None, parse_mode=None, disable_web_page_preview=None, video_width=None, video_height=None,
                 video_duration=None, thumb_url=None, title=None, description=None):
        self.type = "video"
        self.id = id
        self.video_url = video_url
        self.mime_type = mime_type
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.video_width = video_width
        self.video_height = video_height
        self.video_duration = video_duration
        self.thumb_url = thumb_url
        self.title = title
        self.description = description



"""
Types added for utility purposes
"""


_ErrorBase = namedtuple('Error', ['error_code', 'description'])


class Error(_ErrorBase):

    """The error code and message returned when a request was successfuly but the method call was invalid

    Attributes:
        error_code  (int)   :An Integer ‘error_code’ field is also returned, but its
                            contents are subject to change in the future.
        description (str)   :The description of the error as reported by Telegram

    """
    __slots__ = ()

    @staticmethod
    def from_result(result):
        return Error(error_code=result.get('error_code'), description=result.get('description'))

"""
RPC Objects
"""


class RequestMethod(str, Enum):

    """Used to specify the HTTP request method.

    Attributes:
        GET : 'GET'
        POST: 'POST'

    :example:

    ::

        bot.get_me(request_method=RequestMethod.GET)

    """
    GET = 'GET'
    POST = 'POST'


class TelegramBotRPCRequest:

    """Class that handles creating the actual RPC request, and sending callbacks based on response

    :param api_method: The API method to call. See https://core.telegram.org/bots/api#available-methods
    :param token: The API token generated following the instructions at https://core.telegram.org/bots#botfather
    :param params: A dictionary mapping the api method parameters to their arguments
    :param on_result: a callback function that gets called before when te request finishes. The return value
                      of this function gets passed to on_success. Useful if you wish to override the generated
                      result type
    :param on_success: a callback function that gets called when the api call was successful, gets passed
                       the return value from on_result
    :param on_error: called when an error occurs
    :param files: a list of :class:`InputFile`s to be sent to the server`
    :param request_method: ``RequestMethod.POST`` or ``RequestMethod.GET``

    :type api_method: str
    :type token: str
    :type params: dict
    :type on_result: callable
    :type on_success: callable
    :type on_error: callable
    :type files: `list` of :class:`InputFile`
    :type request_method: RequestMethod

    .. note::

        Typically you do not have to interact with this class directly. However, you may override any of these
        arguments by specifiying it in the the `\*\*kwargs` of any api method.
    """

    api_url_base = 'https://api.telegram.org/bot'

    def __init__(self, api_method, token, params=None, on_result=None, on_success=None, callback=None,
                 on_error=None, files=None, request_method=RequestMethod.POST):
        reply_markup = params.get('reply_markup') if params else None
        if reply_markup is not None:
            params['reply_markup'] = reply_markup.serialize()

        if callback is not None:
            print('WARNING: callback is deprecated in favor of on_success')
            if on_success:
                print('WARNING: callback parameter will be ignored, on_success will be used instead')
            else:
                on_success = callback

        self.api_method = api_method
        self.token = token
        self.params = params
        self.on_result = on_result
        self.on_success = on_success
        self.on_error = on_error
        self.files = files
        self.request_method = RequestMethod(request_method)

        self.result = None
        self.error = None

        self.thread = Thread(target=self._async_call)

    def _get_url(self):
        return '{base_url}{token}/{method}'.format(base_url=TelegramBotRPCRequest.api_url_base,
                                                   token=self.token,
                                                   method=self.api_method)

    def _get_request(self):
        data, files = None, None
        if self.params is not None:
            data = self.params
        if self.files is not None:
            files = self.files

        return Request(self.request_method, self._get_url(), data=data, files=files).prepare()

    def _async_call(self):
        self.error = None
        self.response = None

        s = Session()
        request = self._get_request()
        resp = s.send(request)

        if resp.status_code == 200:
            try:
                api_response = resp.json()
            except ValueError:
                api_response = {'ok': False, 'description': 'Invalid Value in JSON response', 'error_code': None}
        else:
            api_response = {'ok': False, 'description': 'API doesn\'t answer', 'error_code': resp.status_code}

        if api_response.get('ok'):
            result = api_response['result']
            if self.on_result is None:
                self.result = result
            else:
                self.result = self.on_result(result)

            if self.on_success is not None:
                self.on_success(self.result)
        else:
            self.error = Error.from_result(api_response)
            if self.on_error:
                self.on_error(self.error)

        return None

    def run(self):
        self.thread.start()

        return self

    def join(self, timeout=None):
        self.thread.join(timeout)
        return self

    def wait(self):
        """
        Wait for the request to finish and return the result or error when finished

        :returns: result or error
        :type: result tyoe or Error
        """
        self.thread.join()
        if self.error is not None:
            return self.error
        return self.result


class TelegramDownloadRequest(TelegramBotRPCRequest):

    """Class that handles downloading files from telegram.

    :param file_path: The remote file path received via :func:`get_file`
    :param out_file: File to save to. Can be a file path (str) or a file-like object
    :param token: The API token generated following the instructions at https://core.telegram.org/bots#botfather
    :param on_success: a callback function that gets called when the api call was successful, gets passed
                       the return value from on_result
    :param on_error: called when an error occurs

    :type file_path: str
    :type out_file: str
    :type token: str
    :type on_success: callable
    :type on_error: callable

    .. note::

        Typically you do not have to interact with this class directly.
    """
    download_url_base = 'https://api.telegram.org/file/bot'

    def __init__(self, file_path, out_file, token, on_success=None,
                 on_error=None, request_method=None):  # request_method eats the kwarg from TelegramBot.request_args
        self.file_path = file_path
        self.out_file = out_file
        self.token = token
        self.on_success = on_success
        self.on_error = on_error
        self.request_method = RequestMethod.GET  # Others are not allowed

        self.params = None
        self.files = None

        self.result = None
        self.error = None

        self.thread = Thread(target=self._async_call)

    def _get_url(self):
        return '{base_url}{token}/{path}'.format(base_url=self.download_url_base,
                                                 token=self.token,
                                                 path=self.file_path)

    def _do_download(self, resp, f):
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive chunks
                f.write(chunk)

    def _async_call(self):
        s = Session()
        request = self._get_request()
        resp = s.send(request)

        if not resp.status_code == 200:
            self.error = RuntimeError("Bad HTTP Status Code", resp, resp.status_code)
        else:
            try:
                if isinstance(self.out_file, str):
                    with open(self.out_file, 'w+b') as f:
                        self._do_download(resp, f)

                elif hasattr(self.out_file, 'write'):
                    self._do_download(resp, self.out_file)
            except OSError as e:
                self.error = e

        if self.error:
            if self.on_error:
                self.on_error(self.error)
        else:
            self.result = self.out_file
            if self.on_success:
                self.on_success(self.out_file)


def _clean_params(**params):
    return {name: val for name, val in params.items() if val is not None}


"""
Telegram Bot API Methods as defined at https://core.telegram.org/bots/api#available-methods
"""


def get_me(**kwargs):
    """
    A simple method for testing your bot's auth token. Requires no parameters.
    Returns basic information about the bot in form of a User object.

    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :returns: Returns basic information about the bot in form of a User object.
    :rtype: User
    """
    return TelegramBotRPCRequest('getMe', on_result=User.from_result, **kwargs)


def send_message(chat_id, text,
                 parse_mode=None, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 disable_notification=False, **kwargs):
    """
    Use this method to send text messages.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param text: Text of the message to be sent
    :param parse_mode: Send ``"Markdown"``, if you want Telegram apps to show bold,
                       italic and inline URLs in your bot's message.
    :param disable_web_page_preview: Disables link previews for links in this message
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a
                         custom reply keyboard, instructions to hide keyboard or to
                         force a reply from the user.
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type text: str
    :type disable_web_page_preview: bool
    :type reply_to_message_id: int
    :type reply_markup: :class:`ReplyKeyboardMarkup` or :class:`ReplyKeyboardHide` or :class:`ForceReply`

    :returns: On success, the sent Message is returned.
    :rtype: Message

    """
    # required args
    params = dict(chat_id=chat_id, text=text)

    # optional args
    params.update(
        _clean_params(
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendMessage', params=params, on_result=Message.from_result, **kwargs)


def forward_message(chat_id, from_chat_id, message_id, disable_notification=False,
                    **kwargs):
    """
    Use this method to forward messages of any kind.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param from_chat_id: Unique identifier for the chat where the original message was sent — User or
                         GroupChat id
    :param message_id: Unique message identifier
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type from_chat_id: int
    :type message_id: int

    :returns: On success, the sent Message is returned.
    :rtype: Message
    """

    # required args
    params = dict(
        chat_id=chat_id,
        from_chat_id=from_chat_id,
        message_id=message_id,
        disable_notification=disable_notification,
    )

    return TelegramBotRPCRequest('forwardMessage', params=params, on_result=Message.from_result, **kwargs)


def send_photo(chat_id,  photo,
               caption=None, reply_to_message_id=None, reply_markup=None, disable_notification=False,
               **kwargs):
    """
    Use this method to send photos.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param photo: Photo to send. You can either pass a file_id as String to resend a
                  photo that is already on the Telegram servers, or upload a new photo
                  using multipart/form-data.
    :param caption: Photo caption (may also be used when resending photos by file_id).
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a
                         custom reply keyboard, instructions to hide keyboard or to
                         force a reply from the user.
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type photo: InputFile or str
    :type caption: str
    :type reply_to_message_id: int
    :type reply_markup: :class:`ReplyKeyboardMarkup` or :class:`ReplyKeyboardHide` or :class:`ForceReply`

    :returns: On success, the sent Message is returned.
    :rtype: TelegramBotRPCRequest
    """

    files = None
    if isinstance(photo, InputFile):
        files = [photo]
        photo = None
    elif not isinstance(photo, str):
        raise Exception('photo must be instance of InputFile or str')

    # required args
    params = dict(
        chat_id=chat_id,
        photo=photo
    )

    # optional args
    params.update(
        _clean_params(
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendPhoto', params=params, files=files, on_result=Message.from_result, **kwargs)


def send_audio(chat_id, audio,
               duration=None, performer=None, title=None, reply_to_message_id=None, reply_markup=None,
               disable_notification=False, **kwargs):
    """
    Use this method to send audio files, if you want Telegram clients to display them in the music player.

    Your audio must be in the .mp3 format. On success, the sent Message is returned. Bots can currently send audio
    files of up to 50 MB in size, this limit may be changed in the future.

    For backward compatibility, when the fields title and performer are both empty and the mime-type of the file to
    be sent is not audio/mpeg, the file will be sent as a playable voice message. For this to work, the audio must
    be in an .ogg file encoded with OPUS. This behavior will be phased out in the future. For sending voice
    messages, use the sendVoice method instead.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param audio: Audio file to send. You can either pass a file_id as String to resend an audio that is already on
                  the Telegram servers, or upload a new audio file using multipart/form-data.
    :param duration: Duration of the audio in seconds
    :param performer: Performer
    :param title: Track name
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a custom reply keyboard,
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type audio: InputFile or str
    :param duration: int
    :param performer: str
    :param title: str
    :type reply_to_message_id: int
    :type reply_markup: ReplyKeyboardMarkup or ReplyKeyboardHide or ForceReply

    :returns: On success, the sent Message is returned.
    :rtype: TelegramBotRPCRequest
    """
    files = None
    if isinstance(audio, InputFile):
        files = [audio]
        audio = None
    elif not isinstance(audio, str):
        raise Exception('audio must be instance of InputFile or str')

    # required args
    params = dict(
        chat_id=chat_id,
        audio=audio
    )

    # optional args
    params.update(
        _clean_params(
            duration=duration,
            performer=performer,
            title=title,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendAudio', params=params, files=files, on_result=Message.from_result, **kwargs)


def send_document(chat_id, document,
                  reply_to_message_id=None, reply_markup=None, disable_notification=False,
                  **kwargs):
    """
    Use this method to send general files.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param document: File to send. You can either pass a file_id as String to resend a file that is already on
                     the Telegram servers, or upload a new file using multipart/form-data.
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a custom reply keyboard,
                         instructions to hide keyboard or to force a reply from the user.
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type document: InputFile or str
    :type reply_to_message_id: int
    :type reply_markup: ReplyKeyboardMarkup or ReplyKeyboardHide or ForceReply

    :returns: On success, the sent Message is returned.
    :rtype: TelegramBotRPCRequest
    """
    files = None
    if isinstance(document, InputFile):
        files = [document]
        document = None
    elif not isinstance(document, str):
        raise Exception('document must be instance of InputFile or str')

    # required args
    params = dict(
        chat_id=chat_id,
        document=document
    )

    # optional args
    params.update(
        _clean_params(
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendDocument', params=params, files=files, on_result=Message.from_result, **kwargs)


def send_sticker(chat_id, sticker,
                 reply_to_message_id=None, reply_markup=None, disable_notification=False,
                 **kwargs):
    """
    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param sticker: Sticker to send. You can either pass a file_id as String to resend a sticker
                    that is already on the Telegram servers, or upload a new sticker using multipart/form-data.
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a custom reply keyboard,
                         instructions to hide keyboard or to force a reply from the user.
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type sticker: InputFile or str
    :type reply_to_message_id: int
    :type reply_markup: ReplyKeyboardMarkup or ReplyKeyboardHide or ForceReply

    :returns: On success, the sent Message is returned.
    :rtype: TelegramBotRPCRequest
    """
    files = None
    if isinstance(sticker, InputFile):
        files = [sticker]
        sticker = None
    elif not isinstance(sticker, str):
        raise Exception('sticker must be instance of InputFile or str')

    # required args
    params = dict(
        chat_id=chat_id,
        sticker=sticker
    )

    # optional args
    params.update(
        _clean_params(
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendSticker', params=params, files=files, on_result=Message.from_result, **kwargs)


def send_video(chat_id, video,
               duration=None, caption=None, reply_to_message_id=None, reply_markup=None, disable_notification=False,
               **kwargs):
    """
    Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as Document).

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param video: Video to send. You can either pass a file_id as String to resend a
                  video that is already on the Telegram servers, or upload a new video
                  using multipart/form-data.
    :param duration: Duration of sent video in seconds
    :param caption: Video caption (may also be used when resending videos by file_id)
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a
                         custom reply keyboard, instructions to hide keyboard or to
                         force a reply from the user.
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type video: InputFile or str
    :type duration: int
    :type caption: str
    :type reply_to_message_id: int
    :type reply_markup: ReplyKeyboardMarkup or ReplyKeyboardHide or ForceReply

    :returns: On success, the sent Message is returned.
    :rtype:  TelegramBotRPCRequest
    """
    files = None
    if isinstance(video, InputFile):
        files = [video]
        video = None
    elif not isinstance(video, str):
        raise Exception('video must be instance of InputFile or str')

    # required args
    params = dict(
        chat_id=chat_id,
        video=video
    )

    # optional args
    params.update(
        _clean_params(
            duration=duration,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendVideo', params=params, files=files, on_result=Message.from_result, **kwargs)


def send_voice(chat_id, voice,
               duration=None, reply_to_message_id=None, reply_markup=None, disable_notification=False,
               **kwargs):
    """
    Use this method to send audio files, if you want Telegram clients to display the file as a playable voice
    message.

    For this to work, your audio must be in an .ogg file encoded with OPUS (other formats may be sent as Audio or
    Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in
    size, this limit may be changed in the future.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param voice: Audio file to send. You can either pass a file_id as String to resend an audio that is already on
                  the Telegram servers, or upload a new audio file using multipart/form-data.
    :param duration: Duration of sent audio in seconds
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a custom reply keyboard,
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type voice: InputFile or str
    :type duration: int
    :type reply_to_message_id: int
    :type reply_markup: ReplyKeyboardMarkup or ReplyKeyboardHide or ForceReply

    :returns: On success, the sent Message is returned.
    :rtype: TelegramBotRPCRequest
    """
    files = None
    if isinstance(voice, InputFile):
        files = [voice]
        voice = None
    elif not isinstance(voice, str):
        raise Exception('voice must be instance of InputFile or str')

    # required args
    params = dict(
        chat_id=chat_id,
        voice=voice
    )

    # optional args
    params.update(
        _clean_params(
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendVoice', params=params, files=files, on_result=Message.from_result, **kwargs)


def send_location(chat_id, latitude, longitude,
                  reply_to_message_id=None, reply_markup=None, disable_notification=False,
                  **kwargs):
    """
    Use this method to send point on the map.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param latitude: Latitude of location.
    :param longitude: Longitude of location.
    :param reply_to_message_id: If the message is a reply, ID of the original message
    :param reply_markup: Additional interface options. A JSON-serialized object for a
                         custom reply keyboard, instructions to hide keyboard or to
                         force a reply from the user.
    :param disable_notification: Sends the message silently. iOS users will not receive a notification, Android users
                                 will receive a notification with no sound. Other apps coming soon.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type latitude: float
    :type longitude: float
    :type reply_to_message_id: int
    :type reply_markup: ReplyKeyboardMarkup or ReplyKeyboardHide or ForceReply

    :returns: On success, the sent Message is returned.
    :rtype:  TelegramBotRPCRequest
    """

    # required args
    params = dict(
        chat_id=chat_id,
        latitude=latitude,
        longitude=longitude
    )

    # optional args
    params.update(
        _clean_params(
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
    )

    return TelegramBotRPCRequest('sendLocation', params=params, on_result=Message.from_result, **kwargs)


class ChatAction(str, Enum):
    TEXT = 'typing'
    PHOTO = 'upload_photo'
    RECORD_VIDEO = 'record_video'
    VIDEO = 'upload_video'
    RECORD_AUDIO = 'record_audio'
    AUDIO = 'upload_audio'
    DOCUMENT = 'upload_document'
    LOCATION = 'find_location'


def send_chat_action(chat_id, action,
                     **kwargs):
    """
    Use this method when you need to tell the user that something is happening on the bot's side. The status is set
     for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status).

    Example: The ImageBot needs some time to process a request and upload the image. Instead of sending a text message
    along the lines of “Retrieving image, please wait…”, the bot may use sendChatAction with action = upload_photo.
    The user will see a “sending photo” status for the bot.

    We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param action: Type of action to broadcast.  Choose one, depending on what the user is about to receive:
                   typing for text messages, upload_photo for photos, record_video or upload_video for videos,
                   record_audio or upload_audio for audio files, upload_document for general files,
                   find_location for location data.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type chat_id: int
    :type action: ChatAction

    :returns: Returns True on success.
    :rtype:  bool
    """
    # required args
    params = dict(
        chat_id=chat_id,
        action=action
    )

    return TelegramBotRPCRequest('sendChatAction', params=params, on_result=lambda result: result, **kwargs)


def answer_inline_query(inline_query_id, results, cache_time=None, is_personal=None, next_offset=None, **kwargs):
    """ Use this method to send answers to an inline query. On success, True is returned.

    :param inline_query_id: Unique identifier for the message recipient — String
    :param results: An array of results for the inline query — Array of InlineQueryResult
    :param cache_time: The maximum amount of time the result of the inline query may be cached on the server
    :param is_personal: Pass True, if results may be cached on the server side only for the user that sent the query.
                        By default, results may be returned to any user who sends the same query
    :param next_offset: Pass the offset that a client should send in the next query with the same text to receive more
                        results. Pass an empty string if there are no more results or if you don‘t support pagination.
                        Offset length can’t exceed 64 bytes.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type inline_query_id: str
    :type results: InlineQueryResult[]
    :type cache_time: int
    :type is_personal: bool
    :type next_offset: stri


    :returns: On success, the sent True is returned.
    :rtype: bool
    """

    json_results = []
    for result in results:
        json_results.append(dict((k, v) for k, v in result.__dict__.items() if v))  # Don't serialize None keys.

    # required args
    params = dict(
        inline_query_id=inline_query_id,
        results=json.dumps(json_results)
    )

    # optional args
    params.update(
        _clean_params(
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset
        )
    )

    return TelegramBotRPCRequest('answerInlineQuery', params=params, on_result=Message.from_result, **kwargs)


def get_user_profile_photos(user_id,
                            offset=None, limit=None,
                            **kwargs):
    """
    Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object.

    :param user_id: Unique identifier of the target user
    :param offset: Sequential number of the first photo to be returned. By default, all photos are returned.
    :param limit: Limits the number of photos to be retrieved. Values between 1—100 are accepted. Defaults to 100.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type user_id: int
    :type offset: int
    :type limit: int

    :returns: Returns a UserProfilePhotos object.
    :rtype: TelegramBotRPCRequest
    """
    # required args
    params = dict(user_id=user_id)

    # optional args
    params.update(
        _clean_params(
            offset=offset,
            limit=limit
        )
    )

    return TelegramBotRPCRequest('getUserProfilePhotos', params=params,
                                 on_result=UserProfilePhotos.from_result, **kwargs)


def get_file(file_id,
             **kwargs):
    """
    Use this method to get basic info about a file and prepare it for downloading.

    For the moment, bots can download files of up to 20MB in size. On success, a File object is returned. The file can
    then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>, where <file_path> is taken
    from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new
    one can be requested by calling getFile again.

    :param file_id: File identifier to get info about

    :type file_id: str

    :returns: Returns a File object.
    :rtype: TelegramBotRPCRequest
    """
    # required args
    params = dict(file_id=file_id)

    return TelegramBotRPCRequest('getFile', params=params,
                                 on_result=File.from_result, **kwargs)


def get_updates(offset=None, limit=None, timeout=None,
                **kwargs):
    """
    Use this method to receive incoming updates using long polling.

    .. note::

        1. This method will not work if an outgoing webhook is set up.
        2. In order to avoid getting duplicate updates, recalculate offset after each server response.

    :param offset: Identifier of the first update to be returned. Must be
                   greater by one than the highest among the identifiers of
                   previously received updates. By default, updates starting
                   with the earliest unconfirmed update are returned. An update
                   is considered confirmed as soon as getUpdates is called with
                   an offset higher than its update_id.
    :param limit: Limits the number of updates to be retrieved. Values between
                  1—100 are accepted. Defaults to 100
    :param timeout: Timeout in seconds for long polling. Defaults to 0, i.e.
                    usual short polling
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type offset: int
    :type limit: int
    :type timeout: int

    :returns: An Array of Update objects is returned.
    :rtype: TelegramBotRPCRequest
    """
    # optional parameters
    params = _clean_params(
            offset=offset,
            limit=limit,
            timeout=timeout
        )

    return TelegramBotRPCRequest('getUpdates', params=params, on_result=Update.from_result, **kwargs)


def set_webhook(url=None, certificate=None, **kwargs):
    """
    Use this method to specify a url and receive incoming updates via an outgoing webhook.
    Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url, containing a
    JSON-serialized Update. In case of an unsuccessful request, we will give up after a reasonable amount of attempts.

    Please note that you will not be able to receive updates using getUpdates for as long as an outgoing
    webhook is set up.

    To use a self-signed certificate, you need to upload your public key certificate using certificate parameter.
    Please upload as InputFile, sending a String will not work.

    Ports currently supported for Webhooks: 443, 80, 88, 8443.

    :param url: HTTPS url to send updates to. Use an empty string to remove webhook integration
    :param certificate: Upload your public key certificate so that the root certificate in use can be checked.
                        See telegram's self-signed guide for details (https://core.telegram.org/bots/self-signed).
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`

    :type url: str
    :type certificate: InputFile

    :returns: Returns True on success.
    :rtype:  TelegramBotRPCRequest
    """
    # optional args
    params = _clean_params(url=url, certificate=certificate)

    return TelegramBotRPCRequest('setWebhook', params=params, on_result=lambda result: result, **kwargs)


def download_file(file_path, out_file, **kwargs):
    """
    Use this method to download a file from the telegram servers.

    It is guaranteed that the link will be valid for at least 1 hour.

    :param file_path: The remote file path received via :func:`get_file`
    :param out_file: File to save to. Can be a file path (str) or a file-like object
    :param \*\*kwargs: Args that get passed down to :class:`TelegramDownloadRequest`

    :type file_path: str
    :type out_file: str or file-like object

    :returns: Returns out_file on success or an Exception on error.
    :rtype: TelegramDownloadRequest
    """
    return TelegramDownloadRequest(file_path, out_file, **kwargs)


class TelegramBot:

    """A `TelegramBot` object represents a specific regisitered bot user as identified by its token. The bot
    object also helps try to maintain state and simplify interaction for library users.

    Attributes:
        token (str) :The api token generated by BotFather
        request_method (`RequestMethod` or `str`) :*Optional.* The http method to use
                                                    (e.g. 'POST' or RequestMethod.POST')

    .. note::

        Unlike the unbound API methods, when the bot executes an API call, ``run()`` is immediately called
        on the request object.

    """

    def __init__(self, token, request_method=RequestMethod.POST):
        self._bot_user = None

        self.request_args = dict(
            token=token,
            request_method=request_method
        )

    def __str__(self):
        return self.token

    def _merge_overrides(self, **kwargs):
        ra = self.request_args.copy()
        ra.update(kwargs)
        return ra

    def get_me(self, *args, **kwargs):
        """See :func:`get_me`"""
        return get_me(*args, **self._merge_overrides(**kwargs)).run()

    def answer_inline_query(self, *args, **kwargs):
        return answer_inline_query(*args, **self._merge_overrides(**kwargs)).run()

    def send_message(self, *args, **kwargs):
        """See :func:`send_message`"""
        return send_message(*args, **self._merge_overrides(**kwargs)).run()

    def forward_message(self, *args, **kwargs):
        """See :func:`forward_message`"""
        return forward_message(*args, **self._merge_overrides(**kwargs)).run()

    def send_photo(self, *args, **kwargs):
        """See :func:`send_photo`"""
        return send_photo(*args, **self._merge_overrides(**kwargs)).run()

    def send_audio(self, *args, **kwargs):
        """See :func:`send_audio`"""
        return send_audio(*args, **self._merge_overrides(**kwargs)).run()

    def send_document(self, *args, **kwargs):
        """See :func:`send_document`"""
        return send_document(*args, **self._merge_overrides(**kwargs)).run()

    def send_sticker(self, *args, **kwargs):
        """See :func:`send_sticker`"""
        return send_sticker(*args, **self._merge_overrides(**kwargs)).run()

    def send_video(self, *args, **kwargs):
        """See :func:`send_video`"""
        return send_video(*args, **self._merge_overrides(**kwargs)).run()

    def send_voice(self, *args, **kwargs):
        """See :func:`send_voice`"""
        return send_voice(*args, **self._merge_overrides(**kwargs)).run()

    def send_location(self, *args, **kwargs):
        """See :func:`send_location`"""
        return send_location(*args, **self._merge_overrides(**kwargs)).run()

    def send_chat_action(self, *args, **kwargs):
        """See :func:`send_chat_action`"""
        return send_chat_action(*args, **self._merge_overrides(**kwargs)).run()

    def get_user_profile_photos(self, *args, **kwargs):
        """See :func:`get_user_profile_photos`"""
        return get_user_profile_photos(*args, **self._merge_overrides(**kwargs)).run()

    def get_file(self, *args, **kwargs):
        """See :func:`get_file`"""
        return get_file(*args, **self._merge_overrides(**kwargs)).run()

    def get_updates(self, *args, **kwargs):
        """See :func:`get_updates`"""
        return get_updates(*args, **self._merge_overrides(**kwargs)).run()

    def set_webhook(self, *args, **kwargs):
        """See :func:`set_webhook`"""
        return set_webhook(*args, **self._merge_overrides(**kwargs)).run()

    def _update_bot_info(self, response):
        self._bot_user = response

    def update_bot_info(self):
        """See :func:`get_me`.

        After calling this, you may access
        :attr:`id`, :attr:`first_name`, :attr:`last_name` and :attr:`username`.
        """
        return self.get_me(on_success=self._update_bot_info)

    def download_file(self, *args, **kwargs):
        """See :func:`download_file`"""
        return download_file(*args, **self._merge_overrides(**kwargs)).run()

    @property
    def token(self):
        return self.request_args['token']

    @token.setter
    def token(self, val):
        self.request_args['token'] = val

    @property
    def request_method(self):
        return self.request_args['request_method']

    @request_method.setter
    def request_method(self, val):
        self.request_args['request_method'] = val

    @property
    def id(self):
        if self._bot_user is not None:
            return self._bot_user.id

    @property
    def first_name(self):
        if self._bot_user is not None:
            return self._bot_user.first_name

    @property
    def last_name(self):
        if self._bot_user is not None:
            return self._bot_user.last_name

    @property
    def username(self):
        if self._bot_user is not None:
            return self._bot_user.username
