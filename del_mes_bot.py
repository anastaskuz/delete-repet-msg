import telebot
import configure


client = telebot.TeleBot(configure.config['token']) #токен!

users = {}

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


@client.message_handler(content_types=CONTENT_TYPES)
def get_info(message):
#     if (message.forward_sender_name != None) and (user.is_bot == True):
    if message.forward_sender_name != None:
        #работает. шлет имя человека
        user_frwrd_id = message.forward_sender_name
        mes_id = message.message_id
        #client.send_message(message.chat.id, f'{user_frwrd_id} - имя, {mes_id} - номер соо')
        
        if user_frwrd_id not in users.keys():
            users[user_frwrd_id] = [mes_id]
        else:
            users[user_frwrd_id].append(mes_id)
            
        delete_message(message)
        #print(users)
        
    else:
        client.send_message(message.chat.id, 'Пересылай!')


def delete_message(message):
    for k in users.keys():
        if len(users[k]) > 1:
            while len(users[k]) > 1:
                mes_id_del_min = min(users[k])
                mes_id_del_index = users[k].index(mes_id_del_min)
                client.delete_message(message.chat.id, mes_id_del_min)
                users[k].pop(mes_id_del_index)


if __name__ == '__main__':
    client.polling(none_stop=True, interval=0)