import functools
import logging

from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import effective_message_type


def log_formatter(func):
    """
    Every time for bot event print an actor and handler name. Optional print a message id and callback_data
    """

    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        actor_handler = f'[{update.effective_user.id} {update.effective_user.full_name}] [{func.__name__}]'
        if update.callback_query is not None:
            logging.info(f'{actor_handler} [callback {update.callback_query.message.id}]: {update.callback_query.data}')
        elif update.message is not None:
            if update.message.text is not None:
                logging.info(f'{actor_handler} [text]: {repr(update.message.text)}')
            else:
                logging.info(f'{actor_handler} [UNKNOWN MESSAGE TYPE: {effective_message_type(update)}]')
        else:
            logging.info(f'{actor_handler} [UNKNOWN UPDATE TYPE: {effective_message_type(update)}]')

        await func(update, context)

    return wrapper
