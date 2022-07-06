import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


ONE, TWO = range(2)
VID, VID2, VID3, VID4 = range(4)
keyboard_video = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text="БДСМ порно",
                             url="https://rt.pornhub.com/view_video.php?viewkey=ph5f9e496ecd0d6"),
        InlineKeyboardButton(text="Нежное порно",
                             url="https://rt.pornhub.com/view_video.php?viewkey=ph5d51419307b57"),
    ],
    [InlineKeyboardButton(text="Порно с неграми",
                          url="https://rt.pornhub.com/view_video.php?viewkey=ph616585c05c4ac")],
    [InlineKeyboardButton(text="Другое", callback_data=str(VID2))],
])


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\!',
    )


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(f'"{update.message.text}" from @{update.effective_chat.username}')


def split(update: Update, context: CallbackContext):
    text = update.message.text
    if len(text) < 7:
        update.message.reply_text("Используйте команду правильно")
        return

    splitted_text = text[7:].split()
    for x in splitted_text:
        update.message.reply_text(x)


def video_start(update, context) -> int:
    update.message.reply_text("Выберите пожалуйста", reply_markup=keyboard_video)
    logger.info("В видеос перешли")
    return TWO


def video_main(update: Update, context) -> int:
    query = update.callback_query
    query.answer()
    logger.info("Первое меню")
    query.edit_message_text("Выберите пожалуйста", reply_markup=keyboard_video)

    return TWO


def video_categories(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard2 = [
        [
            InlineKeyboardButton(text="Порноактрисы", callback_data=str(VID3)),
            InlineKeyboardButton(text="Мультики", callback_data=str(VID4)),
        ],
        [InlineKeyboardButton(text="Обратно", callback_data=str(VID))],
    ]

    reply = InlineKeyboardMarkup(keyboard2)
    query.edit_message_text("Выберите пожалуйста", reply_markup=reply)
    logger.info("Второе меню")

    return ONE


def video_actors(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard3 = [
        [
            InlineKeyboardButton(text="Ева Элфи", url="https://rt.pornhub.com/pornstar/eva-elfie"),
            InlineKeyboardButton(text="Саша Грей", url="https://rt.pornhub.com/pornstar/sasha-grey"),
        ],
        [InlineKeyboardButton(text="Миа Халифа", url="https://rt.pornhub.com/pornstar/mia-khalifa")],
        [InlineKeyboardButton(text="Обратно", callback_data=str(VID2))],
    ]

    reply = InlineKeyboardMarkup(keyboard3)
    query.edit_message_text("Выберите пожалуйста", reply_markup=reply)
    logger.info("Третье меню")

    return TWO


def video_cartoons(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard3 = [
        [
            InlineKeyboardButton(text="Гриффины", url="https://rt.pornhub.com/view_video.php?viewkey=1837889960"),
            InlineKeyboardButton(text="Мортал Комбат", url="https://rt.pornhub.com/view_video.php?viewkey=ph61854c322ff77"),
        ],
        [InlineKeyboardButton(text="Геншин", url="https://rt.pornhub.com/view_video.php?viewkey=ph61660bc3ddbda")],
        [InlineKeyboardButton(text="Обратно", callback_data=str(VID2))],
    ]

    reply = InlineKeyboardMarkup(keyboard3)
    query.edit_message_text("Выберите пожалуйста", reply_markup=reply)
    logger.info("Четвертое меню")

    return TWO


def command_quit(update: Update, context: CallbackContext):
    update.message.reply_text("Еще увидимся! :)")

    return ConversationHandler.END


# def button(update: Update, context):
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(text=f"Вы выбрали {query.data}")


def main():
    load_dotenv()
    updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("videos", video_start)],
        states={
            ONE: [CallbackQueryHandler(video_main, pattern='^' + str(VID) + '$'),
                  CallbackQueryHandler(video_actors, pattern='^' + str(VID3) + '$'),
                  CallbackQueryHandler(video_cartoons, pattern='^' + str(VID4) + '$')],
            TWO: [CallbackQueryHandler(video_categories, pattern='^' + str(VID2) + '$')],
        },
        fallbacks=[CommandHandler('quit', command_quit)]


    )

    dispatcher.add_handler(conv_handler)
    # updater.dispatcher.add_handler(CommandHandler('video', video))
    # updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('split', split))
    dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
