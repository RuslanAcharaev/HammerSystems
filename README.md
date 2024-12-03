# Referral App

Простейшая реферальная система.

Необходимые зависимости можно установить при помощи `pip install -r requirements.txt`.

Приложение создано с использованием фреймворка Django. 

В приложении доступны следующие эндпоинты:
- `api/auth/` принимает POST запрос с номером телефона.
    Пример запроса:
```json
{
    "phone_number": "89263698810"
}
```
Пример ответа (код в скобках указан для удобства тестирования):
```json
{
    "message": "Код (8473) отправлен на указанный номер телефона"
}
```  
- `api/verify/` принимает POST запрос с номером телефона и кодом подтверждения. В случае ввода правильного кода подтверждения отображает аутентификационный токен и профиль пользователя.
    Пример запроса:
```json
{
    "phone_number": "89263008010",
    "auth_code": "5879"
}
```
Пример ответа:
```json
{
    "message": "Код подтвержден",
    "token": "e23e4a75d503803ab13e3c51c62e0a3a52fc333d",
    "profile": {
        "phone_number": "89263008010",
        "referral_code": "RbcjOE",
        "other_code": null,
        "entered_my_referral": [
            {
                "phone_number": "89263008020"
            },
            {
                "phone_number": "89263008030"
            }
        ]
    }
}
```  
- `api/profile/` принимает GET запрос. При передаче корректного токена аутентификации в заголовке Authorization, отображает профиль пользователя.
    
Пример ответа:
```json
{
    "phone_number": "89263008020",
    "referral_code": "q7VKhZ",
    "other_code": "RbcjOE",
    "entered_my_referral": []
}
```  

- `api/profile/referral/` принимает POST запрос с реферальным кодом.
    Пример запроса:
```json
{
    "other_code": "RbcjOE"
}
```
Пример ответа:
```json
{
    "message": "Код успешно введен.",
    "profile": {
        "phone_number": "89263008040",
        "referral_code": "rItyD2",
        "other_code": "RbcjOE",
        "entered_my_referral": []
    }
}
```  
