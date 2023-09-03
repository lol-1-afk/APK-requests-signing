# APK-requests-signing

Репозиторий с разбором подписи запросов, с которыми я столкнулся. 

Готово:
- ru.magnit.cosmetic - подпись при отправке SMS кода для авторизации в аккаунте
- ru.oskelly.app - шифрование пароля при авторизации в аккаунте
- su.ias.stolplit - подпись всех запросов
- ru.litres.android - подпись всех запросов
- ru.labirint.android - подпись всех запросов
- ru.briz.rendezvous - подпись при авторизации в аккаунте
- com.platfomni.lot - подпись всех запросов
- com.hushed.release - шифрование пароля в заголовке при авторизации. Интересный случай
- ru.hoff.app - подпись всех запросов
- com.zadarma.sip - Zadarma, подпись всех запросов с sip
- ru.berizaryad - Бери Заряд, подпись при авторизации и подтверждении кода из смс
- ru.tander.magnit - Магнит, подпись при отправке СМС
- ru.rutube.app - RuTUbe, подпись при авторизации, проверке регистрации


# TODO
- com.platfomni.yaapteka - Тоже самое. Ошибка: Неверно указан токен: raw={\"latitude\":11,\"longitude\":11}, platform=2.
- com.platfomni.maxavit - Тоже самое.
- com.chess - подпись всех запросов Ios/Android. ???. Не могу найти место где генерируется заголовок "sig"
- ru.mylavash - подпись при запросе смс. лютое шифрование, хз как переписать на питон. tech.itfood.crypto.Cryptogram, tech.itfood.crypto.CryptogramCipher
