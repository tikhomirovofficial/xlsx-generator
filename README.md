
# xlsx-generator

Эта программа поможет вам сгенерировать файл типа excel, на основе JSON.\
Также вы можете указать название получаемого файла и список кастомных заголовков




## API Reference

#### Пример запроса для получения файла

```http
  GET /?data=[{"name": "Artem", "age": 18, "birthday": "16-08-2004"}]&filename="My_sheet"&keys=["Имя", "Возраст", "День рождения"]
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `filename` | `string` | **Required**. Желаемое название файла |
| `keys` | `JSON` | **Required**. Массив кастомных заголовков |
| `data` | `JSON` | **Required**. Основные данные|

## Возможные ошибки в ответе




#### Если в поле data положены данные примитивного типа 
```javascript
{
    "err": "data is incorrect"
}
```
#### Если отправлен невалидный запрос (с ошибками в URL)
```javascript
{
    "err": "request is incorrect"
}
```
#### Если пропущено какое-либо требуемое поле в запросе
```javascript
{
    "detail": [
        {
            "loc": [
                "query",
                "<field>"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },

    ]
}

```

