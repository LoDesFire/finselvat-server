# Примеры запросов API

Примеры curl-запросов для тестирования API межведомственного обмена документами.

## Базовый URL

```bash
BASE_URL=http://localhost:8000
```

---

## 1. Проверка доступности сервиса

### Запрос

```bash
curl -X GET "$BASE_URL/api/health"
```

### Успешный ответ

```
OK
```

---

## 2. Получение входящих сообщений (для Системы А)

Запрос списка транзакций с сообщениями, адресованными Системе А, за указанный период.

### Запрос

```bash
curl -X POST "$BASE_URL/api/messages/outgoing" \
  -H "Content-Type: application/json" \
  -d '{
    "Data": "eyJTdGFydERhdGUiOiIyMDI1LTAxLTAxVDAwOjAwWiIsIkVuZERhdGUiOiIyMDI2LTEyLTAxVDAwOjAwWiIsIkxpbWl0IjoxMCwiT2Zmc2V0IjowfQ==",
    "Sign": "AWXNTWxdabdAoY4G0icEab41CZZKGhbE1WYt5xCLqUk=",
    "SignerCert": "YWFzYXNkYQ=="
}'
```

### Расшифровка Data (SearchRequest)

```json
{
  "StartDate": "2025-01-01T00:00Z",
  "EndDate": "2026-12-01T00:00Z",
  "Limit": 10,
  "Offset": 0
}
```

### Пример ответа

```json
{
  "Data": "<Base64-encoded TransactionsData>",
  "Sign": "<Base64-encoded signature>",
  "SignerCert": "<Base64-encoded certificate>"
}
```

---

## 3. Отправка сообщений в реестр (от Системы А)

Отправка новых сообщений от Системы А в Систему Б.

### Запрос

```bash
curl -X POST "$BASE_URL/api/messages/incoming" \
  -H "Content-Type: application/json" \
  -d '{
    "Data": "eyJUcmFuc2FjdGlvbnMiOlt7IlRyYW5zYWN0aW9uVHlwZSI6OSwiRGF0YSI6ImV5SkVZWFJoSWpvaVpYbEtUMWxYTVd4SmFtOXBXVmhPYTBscGQybFJiVVoxWVRCa01WbFlTbWhpYmxKc1dsVm9hR015WjJsUGFVcG9ZekpSYVV4RFNsUmhWMlIxU1dwdmFWZFdhRTloTVd4WVZWUXdhVXhEU2xSaFYyUjFXbGhLUkZwWVNqQkphbTlwVjFab1QyRjVTamtpTENKVFpXNWtaWEpDWVhSamFDSTZJbE5aVTFSRlRWOUJJaXdpVW1WalpXbDJaWEpDWVhSamFDSTZJbE5aVTFSRlRWOUNJaXdpU1c1bWIwMWxjM05oWjJWVWVYQmxJam95TURJc0lrMWxjM05oWjJWVWFXMWxJam9pTWpBeU5TMHhNaTB4TUZRd01Eb3dNRG93TUZvaUxDSkRhR0ZwYmtkMWFXUWlPaUl4T0RBd1l6RTJaQzB6T0RCa0xUUmhZemt0WWpFMk9TMWhPRFUzWldVeE1EQTRNMk1pTENKUWNtVjJhVzkxYzFSeVlXNXpZV04wYVc5dVNHRnphQ0k2Ym5Wc2JDd2lUV1YwWVdSaGRHRWlPbTUxYkd4OSIsIkhhc2giOiI5OTI2RDcwODYwMDk3QzUxREFFQThFNkVCMDgxMjJGQzU0Nzk4M0MwNzFDRDdBMDcwRkFCNTFBMjJFRjk5M0I3IiwiU2lnbiI6Im1TYlhDR0FKZkZIYTZvNXVzSUVpL0ZSNWc4Qnh6WG9IRDZ0Um9pNzVrN2M9IiwiU2lnbmVyQ2VydCI6IllYTmtZUT09IiwiVHJhbnNhY3Rpb25UaW1lIjoiMjAyNi0wMy0xM1QwMDowMDowMFoiLCJNZXRhZGF0YSI6bnVsbCwiVHJhbnNhY3Rpb25JbiI6bnVsbCwiVHJhbnNhY3Rpb25PdXQiOm51bGx9XSwiQ291bnQiOjF9",
    "Sign": "jmEZm2FAJ3NQ+ishXZXMOpw25qgHvg8dvsFQ5As5GvI=",
    "SignerCert": "YWFzYXNkYQ=="
}'
```

### Расшифровка Data (TransactionsData)

```json
{
  "Transactions": [
    {
      "TransactionType": 9,
      "Data": "<Base64-encoded Message>",
      "Hash": "9926D70860097C51DAEA8E6EB08122FC547983C071CD7A070FAB51A22EF993B7",
      "Sign": "mSbXCGAJfFHa6o5usIEi/FR5g8BxzXoHD6tRoi75k7c=",
      "SignerCert": "YXNkYQ==",
      "TransactionTime": "2026-03-13T00:00:00Z",
      "Metadata": null,
      "TransactionIn": null,
      "TransactionOut": null
    }
  ],
  "Count": 1
}
```

### Ответ

Сервер возвращает конверт `SignedApiData` с массивом транзакций-квитков (тип 215).

---

## Примечания

### Структура конверта SignedApiData

| Поле        | Обязательность | Формат   | Описание                          |
|-------------|----------------|----------|-----------------------------------|
| Data        | обязательно    | byte[]   | JSON запрос/ответ в Base64        |
| Sign        | обязательно    | byte[]   | ЭЦП отправителя (Base64)          |
| SignerCert  | обязательно    | byte[]   | Сертификат ключа отправителя      |

### Кодирование данных

1. Сериализуйте объект в JSON
2. Закодируйте байты JSON в Base64
3. Поместите результат в поле `Data`
