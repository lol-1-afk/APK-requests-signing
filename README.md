# APK-requests-signing

Репозиторий с разбором подписи запросов, с которыми я столкнулся. 

Готово:
- ru.magnit.cosmetic - подпись при отправке SMS кода для авторизации в аккаунте
- ru.oskelly.app - шифрование пароля при авторизации в аккаунте
- su.ias.stolplit - подпись всех запросов
- ru.litres.android - подпись всех запросов
- ru.labirint.android - подпись всех запросов


# TODO
- com.platfomni.lot - подпись всех запросов на Ios/Android. ToUpperCase(SHA256(???)). Не могу найти место где генерируется заголовок "token". Подпись основана на заголовке "platform" и параметрах,контенту запроса
- com.platfomni.yaapteka - Тоже самое. Ошибка: Неверно указан токен: raw={\"latitude\":11,\"longitude\":11}, platform=2.
- com.chess - подпись всех запросов Ios/Android. ???. Не могу найти место где генерируется заголовок "sig"
