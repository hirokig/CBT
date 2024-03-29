from datetime import datetime, timedelta
import logging
from common.constant.admin_command import AdminCommand
from common.constant.session_status import SessionStatus
from core.nlp.bot.product.admin_bot import AdminBot
from core.nlp.bot.product.cct_bot import CCTBot
from core.nlp.bot.product.intro_bot import IntroBot
from core.nlp.bot.product.reflection_bot import ReflectionBot
from core.nlp.bot.product.return_visit_bot import ReturnVisitBot


class BotFactory:
    """
    BotFactory create bots that are designed to do specific tasks depending on session status.
    To check what kind of bots there are, see the location ../product/
    """
    __none_error_message = 'None type object passed'

    @classmethod
    def create(cls, user, message, therapy_session):
        """
        Create a bot depending on the session situation.
        :param user:
        :param message:
        :param therapy_session:
        :return:
        """
        args = user, message, therapy_session
        if cls.__should_create_admin_bot(user, message):
            return AdminBot(user, message, therapy_session)

        if not therapy_session.id:
            return IntroBot(user, message)

        if therapy_session.finish_at < datetime.utcnow() - timedelta(hours=8):
            if therapy_session.status == SessionStatus.prepared.value:
                return CCTBot(*args)
            else:
                return ReturnVisitBot(*args)
        else:
            if cls.__should_create_cct_bot(therapy_session):
                return CCTBot(*args)
            elif cls.__should_create_reflection_bot(therapy_session):
                return ReflectionBot(*args)
            elif cls.__should_create_return_visit_bot(therapy_session):
                return ReturnVisitBot(*args)
            else:
                return None

    @classmethod
    def __should_create_admin_bot(cls, user, message):
        try:
            text = [i['text'] for i in message.message_dicts][0]

            if text in AdminCommand.admin_command_list.value:
                if user.first_name in {}:
                    return True
                else:
                    return False
            else:
                return False
        except AttributeError:
            logging.exception(cls.__none_error_message)
            return False

    @classmethod
    def __should_create_cct_bot(cls, therapy_session):
        try:
            if therapy_session.status == SessionStatus.prepared.value:
                return True
            elif therapy_session.status == SessionStatus.active.value:
                if therapy_session.finish_at > datetime.utcnow():
                    return True
                else:
                    return False
            else:
                return False
        except AttributeError:
            logging.exception(cls.__none_error_message)
            return False

    @classmethod
    def __should_create_reflection_bot(cls, therapy_session):
        try:
            if therapy_session.status == SessionStatus.active.value:
                if therapy_session.finish_at < datetime.utcnow():
                    return True
                else:
                    return False
            elif therapy_session.status in {SessionStatus.asking_comment.value, SessionStatus.asking_mood.value}:
                return True
            else:
                return False
        except AttributeError:
            logging.exception(cls.__none_error_message)
            return False

    @classmethod
    def __should_create_return_visit_bot(cls, therapy_session):
        try:
            return therapy_session.status in {SessionStatus.asking_new.value, SessionStatus.ended.value}
        except AttributeError:
            logging.exception(cls.__none_error_message)
            return False
