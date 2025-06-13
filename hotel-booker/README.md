How to use: 

Run with

```
uvicorn app:app --reload --port 8080
```

Test with
```
curl "http://127.0.0.1:8080/bookings/"
```

```
curl -X POST "http://127.0.0.1:8080/bookings/" \
-H "Content-Type: application/json" \
-d '{
  "hotel_name": "Grand Hyatt",
  "duration": 5,
  "customer_name": "John Doe"
}'
```