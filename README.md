# APK-requests-signing

Репозиторий с разбором подписи запросов, с которыми я столкнулся. 

Готово:
- ru.magnit.cosmetic - подпись при отправке SMS кода для авторизации в аккаунте
- ru.oskelly.app - шифрование пароля при авторизации в аккаунте
- su.ias.stolplit - подпись всех запросов
- ru.litres.android - подпись всех запросов
- ru.labirint.android - подпись всех запросов


# TODO
- com.platfomni.lot - подпись всех запросов на Ios/Android. ToUpperCase(SHA256(???)). Не могу найти место где генерируется заголовок "token"
- com.chess - подпись всех запросов Ios/Android. ???. Не могу найти место где генерируется заголовок "sig"
