import telegram
import logging
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,BaseFilter

#cache functions
from mwt import MWT

@MWT(timeout=60*30)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

#defines the banned packs list globally
banned_list = []

class BannedStickersFilter(BaseFilter):
    def filter(self,message):
        global banned_list
        return message.sticker.set_name in banned_list


#Defining the commands

# /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='StickerFilterBot started.')

# /documentation
def documentation(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Documentation and the source code is at https://github.com/Caiofcas/StickerFilterBot ')

# deletes the stickers in the banned list
def del_message(bot, update):
    bot.delete_message(chat_id = update.message.chat_id,
                       message_id = update.message.id)

# /addPack
def addPack(bot,update,args):
    global banned_list
    if update.message.from_user.id in get_admin_ids(bot, update.message.chat_id):
        banned_list.append(args[0])
        bot.send_message(chat_id=update.message.chat_id,
                         text="The \"%s\" pack was added to the banned list" %(args[0]))


# /rmvPack
def rmvPack(bot,update,args):
    global banned_list
    if update.message.from_user.id in get_admin_ids(bot, update.message.chat_id):
        if args[0] in banned_list:
            banned_list.remove(args[0])
            bot.send_message(chat_id=update.message.chat_id,
                             text="Sticker Pack \"%s\" was removed" %(args[0]))
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="The pack \"%s\" is not banned" %(args[0]))

#/showBanList
def showBanList(bot,update):
    global banned_list
    msgText = 'The sticker packs banned in this group are:\n'
    for name in banned_list:
        msgText = msgText + "- " + name + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=msgText)


def main():

    #initializing the banned stickers filter
    banned_filter = BannedStickersFilter()
    
    #initializing the bot
    bot = telegram.Bot(token='658579017:AAEAsI7YzILDJdMmU6c7uicoHs2CA0KGTHg')
    updater = Updater(token = '658579017:AAEAsI7YzILDJdMmU6c7uicoHs2CA0KGTHg')
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    documentation_handler = CommandHandler('documentation',documentation)
    dispatcher.add_handler(documentation_handler)

    addPack_handler = CommandHandler('addPack',addPack,pass_args = True)
    dispatcher.add_handler(addPack_handler)

    rmvPack_handler = CommandHandler('rmvPack',rmvPack,pass_args = True)
    dispatcher.add_handler(rmvPack_handler)        

    showBanList_handler = CommandHandler('showBanList',showBanList)
    dispatcher.add_handler(showBanList_handler)

    delete_handler = MessageHandler(banned_filter,del_message)
    dispatcher.add_handler(delete_handler)

    updater.start_polling()
    updater.idle()



if __name__ =='__main__':
    main()
