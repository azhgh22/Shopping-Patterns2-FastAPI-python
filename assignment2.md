# Assignment 2

## Intro

Within the scope of this assignment, we are going to design a service with HTTP API for Point of Sales (POS) system.

## User Stories

> As a *cashier*, I would like to open a receipt so that, I can serve a customer.

> As a *cashier*, I would like to add items to an open receipt so that, I can calculate how much the customer needs to pay.

> As a *customer*, I would like to see a receipt with all my items so that, I know how much I have to pay.

> As a *cashier*, I would like to close the paid receipt so that, I can start serving the next customer.

> As a *store manager*, I would like to make sales reports so that, I can see the state of the store.

## Technical Details

- UI is out of scope (we only care for API)
- Concurancy is out of scope (single user, single request at a time).
- Registration/Authorization is out of scope (API is available publically without any restrictions)
- Receipt contains list of items sold with quantity, price at the time of sale and total price, as well as a grand total price of all items.
- Store can have multiple open receipts at the same time.
- Closed receipt cannot be modified.
- Sales reports contain revenue, and number of closed receipts.
- Use [SQLite](https://docs.python.org/3/library/sqlite3.html)) for persistence.
- Use [FastAPI](https://fastapi.tiangolo.com/) as a web framework.
- API reference that you need to implement is given in the last section.

## Linting/formatting

- Format and lint your code using `ruff`
- Check your static types with `mypy`

You can find configuration for these tools in playground project developed during sessions.

## Testing

Provide automated tests that will falsify regressions (change in behaviour) in your software artifacts.

## Grading

We will not grade solutions:
  - without decomposition
  - with needlessly long methods or classes
  - with code duplications

In all these cases you will automatically get 0% so, we sincerely ask you to 
not make a mess of your code and not put us in an awkward position.

Grade breakdown:
  - 20%: It is tested.
  - 20%: It is easy to change.
  - 20%: It demonstrates an understanding of software architecture.
  - 20%: It demonstrates an understanding of S.O.L.I.D principles.
  - 20%: It follows linting/formatting rules.

## Disclaimer

We reserve the right to resolve ambiguous requirements (if any) as we see fit just like a real-life stakeholder would.
So, do not assume anything, ask for clarifications.


## API Reference

### Units

> Create

Request:
`POST /units`

```json
{
  "name": "კგ"
}
```

Response(s):

HTTP 201
```json
{
  "unit": {
    "id": "27b4f218-1cc2-4694-b131-ad481dc08901",
    "name": "კგ"
  }
}
```

HTTP 409
```json
{
  "error": {
    "message": "Unit with name<კგ> already exists."
  }
}
```

> Read one

Request:
`GET /units/27b4f218-1cc2-4694-b131-ad481dc08901`

Response(s):

HTTP 200
```json
{
  "unit": {
    "id": "27b4f218-1cc2-4694-b131-ad481dc08901",
    "name": "კგ"
  }
}  
```

HTTP 404
```json
{
  "error": {
    "message": "Unit with id<27b4f218-1cc2-4694-b131-ad481dc08901> does not exist."
  }
}
```

> List

Request:
`GET /units`

Response(s):

HTTP 200
```json
{
  "units": [
    {
      "id": "27b4f218-1cc2-4694-b131-ad481dc08901",
      "name": "კგ"
    },
    {
      "id": "ddcce001-a295-4d5f-b016-1de552a7f324",
      "name": "ცალი"
    }
  ]
}
```


### Products

> Create

Request:
`POST /products`

```json
{
  "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
  "name": "Apple",
  "barcode": "1234567890",
  "price": 520
}
```

Response(s):

HTTP 201
```json
{
  "product": {
    "id": "7d3184ae-80cd-417f-8b14-e3de42a98031",
    "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
    "name": "Apple",
    "barcode": "1234567890",
    "price": 520
  }
}
```

HTTP 409
```json
{
  "error": {
    "message": "Product with barcode<1234567890> already exists."
  }
}
```

> Read one

Request:
`GET /products/7d3184ae-80cd-417f-8b14-e3de42a98031`

Response(s):

HTTP 200
```json
{
  "product": {
    "id": "7d3184ae-80cd-417f-8b14-e3de42a98031",
    "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
    "name": "Apple",
    "barcode": "1234567890",
    "price": 520
  }
}
```

HTTP 404
```json
{
  "error": {
    "message": "Product with id<7d3184ae-80cd-417f-8b14-e3de42a98031> does not exist."
  }
}
```

> List

Request:
`GET /products`

Response(s):

HTTP 200
```json
{
  "products": [
    {
      "id": "7d3184ae-80cd-417f-8b14-e3de42a98031",
      "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
      "name": "Apple",
      "barcode": "1234567890",
      "price": 520
    }
  ]
}
```

> Update

Request:
`PATCH /products/{product_id}`

```json
{
  "price": 530
}
```

Response(s):

HTTP 200
```json
{

}
```

HTTP 404
```json
{
  "error": {
    "message": "Product with id<7d3184ae-80cd-417f-8b14-e3de42a98031> does not exist."
  }
}
```


### Receipts

> Create

Request:
`POST /receipts`

Response(s):

HTTP 201
```json
{
  "receipt": {
    "id": "25f13441-5fab-4b12-aefe-3fa0089fb63a",
    "status": "open",
    "products": [],
    "total": 0
  }
}
```

> Add a product

Request:
`POST /receipts/25f13441-5fab-4b12-aefe-3fa0089fb63a/products`

```json
{
  "id": "7d3184ae-80cd-417f-8b14-e3de42a98031",
  "quantity": 123
}
```

Response(s):

HTTP 201
```json
{
  "receipt": {
    "id": "25f13441-5fab-4b12-aefe-3fa0089fb63a",
    "status": "open",
    "products": [
      {
        "id": "7d3184ae-80cd-417f-8b14-e3de42a98031",
        "quantity": 123,
        "price": 520,
        "total": 63960
      }
    ],
    "total": 63960
  }
}
```

> Read by id

Request:
`GET /receipts/25f13441-5fab-4b12-aefe-3fa0089fb63a`

Response(s):

HTTP 200
```json
{
  "receipt": {
    "id": "25f13441-5fab-4b12-aefe-3fa0089fb63a",
    "status": "open",
    "products": [
      {
        "id": "7d3184ae-80cd-417f-8b14-e3de42a98031",
        "quantity": 123,
        "price": 520,
        "total": 63960
      }
    ],
    "total": 63960
  }
}
```

HTTP 404
```json
{
  "error": {
    "message": "Receipt with id<25f13441-5fab-4b12-aefe-3fa0089fb63a> does not exist."
  }
}
```

> Close

Request:
`PATCH /receipts/25f13441-5fab-4b12-aefe-3fa0089fb63a`

```json
{
  "status": "closed"
}
```

Response(s):

HTTP 200
```json
{

}
```

HTTP 404
```json
{
  "error": {
    "message": "Receipt with id<25f13441-5fab-4b12-aefe-3fa0089fb63a> does not exist."
  }
}
```

> Delete

Request:
`DELETE /recepts/25f13441-5fab-4b12-aefe-3fa0089fb63a`

Response(s):

HTTP 200
```json
{

}
```

HTTP 403
```json
{
  "error": {
    "message": "Receipt with id<25f13441-5fab-4b12-aefe-3fa0089fb63a> is closed."
  }
}
```

HTTP 404
```json
{
  "error": {
    "message": "Receipt with id<25f13441-5fab-4b12-aefe-3fa0089fb63a> does not exist."
  }
}
```

### Sales

> Report

Request:
`GET /sales`

Response(s):

HTTP 200
```json
{
  "sales": {
    "n_receipts": 23,
    "revenue": 456890
  }
}
```
