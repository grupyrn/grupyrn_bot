from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, CallbackQueryHandler)
import logging
import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text(
        "Seja bem vind@ ao bot do Grupy-RN"
    )


def help(bot, update):
    update.message.reply_text(
        "Está com duvidas? Fale com nossos membros!\n"
        "Em caso de duvidas mais especificas procure nossos Administradores."
    )


def welcome(bot, update):
    full_name = update.message.new_chat_members[0].full_name
    welcome = (
        f"Olá {full_name}, seja bem-vindo ao Grupy-RN\n\n"
        "Somos um grupo de pessoas interessadas em usar, remixar e compartilhar "
        "tecnologia, aprendizado, diversão e cultura de forma colaborativa e indiscriminada.\n\n"
        "Leia nossas /regras e agora porque você não fala um pouco sobre você?"
    )
    
    keyboard = [
        [
            InlineKeyboardButton(
                "Resumo das regras!", 
                callback_data='rules')
        ],
        
        [ 
            InlineKeyboardButton(
                "Nosso site!", 
                callback_data='site', 
                url="https://meetup.grupyrn.org/"), 
        
            InlineKeyboardButton(
                "Nosso Facebook!",
                callback_data='site',
                url="https://www.facebook.com/grupyrn/")
        ],

        [
            InlineKeyboardButton(
                "Nosso GitHub!",
                callback_data='site',
                url="https://github.com/grupy-rn/")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome, reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    
    if query.data == "rules":
        bot.answer_callback_query(
            callback_query_id=query.id,
            text=(
                "REGRAS:\n\n"
                "1.Respeitar todos os membros do grupo\n"
                "2.Não compartilhar conteúdo pirata\n"
                "3.Divirta-se aprendendo/ensinando!"
            ),
            show_alert=True
        )
    elif query.data == "site":
       bot.answer_callback_query(
           callback_query_id=query.id
       )

def bye(bot, update):
    full_name = update.message.left_chat_member.full_name
    bye = (
        "Um membro acabou de sair.\n"
        f"O que aconteceu com {full_name}?\n"
        "Espero que volte logo!"
    )
    update.message.reply_text(bye)

def rules(bot, update):
    rules = (
        "1. Não haver discriminação em nenhum sentido, raça, religião, "
        "sexo ou linguagem de programação.\n"
        "2. Esse não é um grupo para discussões de política ou religião, "
        "existe lugares para isso, mas não é aqui.\n"
        "3. Evite postagens de cunho comercial, venda de produtos e "
        "serviços, e outros tipos de ações correlacionadas. Não é "
        "proibido, mas peça permissão aos administradores antes.\n"
        "4. Não compartilhar conteúdo sem autorização ou que a licença"
        " permita. \n"
        "5. Proibido envio de vídeos ou imagens pornográficas, acidentes, "
        "informações que não sejam de carácter tecnológico. \n"
        "6. Encontrou alguma mensagens em desacordo com nossas regras, "
        "por favor avise nossos administradores.\n"
        "Att. Coordenação do Grupy-RN"
    )
    update.message.reply_text(rules)


def error(bot, update, error):
    if error.message == "Forbidden: bot can't initiate conversation with a user":
        update.message.reply_text(
            "Por favor, inicie uma conversa comigo para que eu possa te enviar uma mensagem!"
        )
    elif error.message == "Forbidden: bot was blocked by the user":
        update.message.reply_text(
            "Você me bloqueou?! Tsc tsc. Que feio!!!🙄"
        )
    else:
        logger.warning(f'Update {update} caused error {error}')



if __name__ == '__main__':
    updater = Updater(os.getenv("BOT_TOKEN"))

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ajuda", help))
    dp.add_handler(CommandHandler("regras", rules))

    dp.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome))

    dp.add_handler(MessageHandler(
        Filters.status_update.left_chat_member, bye))

    dp.add_handler(CallbackQueryHandler(button))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()