from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import requests

# توكن بوت Telegram
BOT_TOKEN = '7202775582:AAFK1U0jWK2v_Doj7m3hr1uuPJT0y6iFiTA'

# تحديد حالات المحادثة
PHONE, OTP = range(2)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('مرحبا انا بوت مبرمج من طرف كريمو قناتي https://t.me/Clothona_Algeria ارسل الامر /send ثم ارسل رقمك .')
    return ConversationHandler.END

def send_script(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('ارسل رقمك يوز 05**:')
    return PHONE

def get_number(update: Update, context: CallbackContext) -> int:
    num = update.message.text
    context.user_data['mobile_number'] = num

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    
    # طباعة الاستجابة للتشخيص
    print("Get Number Response Status:", response.status_code)
    print("Get Number Response Text:", response.text)
    
    if 'ROOGY' in response.text:
        update.message.reply_text('لقد تم ارسال الكود ، ارسل الكود الأن:')
        return OTP
    else:
        update.message.reply_text('سمحلي مقدرتش نرسل الكود حاول بعد زوج دقايق.')
        return ConversationHandler.END

def get_otp(update: Update, context: CallbackContext) -> int:
    otp = update.message.text
    num = context.user_data.get('mobile_number')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp',
    }

    data = {
        'client_id': 'ibiza-app',
        'otp': otp,
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    
    # طباعة الاستجابة للتشخيص
    print("Get OTP Response Status:", response.status_code)
    print("Get OTP Response Text:", response.text)
    
    try:
        access_token = response.json()['access_token']
        update.message.reply_text('OTP تم التحقق من الكود ، إنتظر ارسلك الانترنيت...')
        
        url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'language': 'AR',
            'request-id': 'ef69f4c6-2ead-4b93-95df-106ef37feefd',
            'flavour-type': 'gms',
            'Content-Type': 'application/json'
        }

        payload = {"mgmValue": "ABC"}
        
        while True:
            response = requests.post(url, headers=headers, json=payload)
            
            # طباعة الاستجابة للتشخيص
            print("Apply Request Response Status:", response.status_code)
            print("Apply Request Response Text:", response.text)
            
            if 'EU1002' in response.text:
                update.message.reply_text('تم ارسال الإنترنيت يا حلو ، تهلا!')
                break
            else:
                update.message.reply_text('اووف ... الكود صحيح بصح مقدرتش نرسلك الانترنيت سمحلي عاود المحاولة لاحقا.')
                break
                
    except KeyError:
        update.message.reply_text('سمحلي مقدرتش نتحقق من الكود حاول بعد زوج دقايق ')

    return ConversationHandler.END

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('send', send_script)],
        states={
            PHONE: [MessageHandler(Filters.text & ~Filters.command, get_number)],
            OTP: [MessageHandler(Filters.text & ~Filters.command, get_otp)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()