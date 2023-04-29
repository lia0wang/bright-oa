# Bright Class 5 Techical Task Instruction

> Link to **Google App Enginee** instance: [click here](https://bright-tech-task-2.ts.r.appspot.com/)

#### **Example Usage**

Input:

`https://bright-tech-task-2.ts.r.appspot.com/search?latitude=-33.8678447&longitude=151.2077854`

Output:

```json
{
  "venues": [
    {
      "price_type": "$$$",
      "review_highlights": [
        "We absolutely enjoyed our dinner.  Recommended by a friend (a local), beautiful Westin hotel, wonderful location and friendly staff. Ordered olives, chorizo, beef cheeks, potato wedges and pear for appetizer.   Sangria for libation.  For main, the meat paella.  Everything was excellent!  Delicious!  We were so full we just had coffee and tea for dessert. Service was excellent.   Very attentive staff. Great way to end our wonderful trip!",
        "Birthday lunch with a friend and fancy settings for a work lunch. Tried a few dishes/tapas listed below Carrots which was recommended by fellow Yelper. Delicious, I loved the herbs and spices that made up this dish and the sweet tender carrots. Great! Mushrooms. I love mushrooms and the taste of this dish help make the mushroom sing.  Shrimps. Good spice mix, but be warned the temperature of these are hot! Meatballs. These were a little dry so not as good as the others.  Pork belly. Tender, soft and I loved the purée.  Tomato salad. Crisp and fresh.   Overall. Great food and quite filling.",
        "Excellent and caring service. Food was quick and well cooked. It was a last minute decision to go there and it was not regretted.  Wine list was extensive, responsibly priced and the waiter actually cared about our selection. Will be back."
      ],
      "longitude": 151.2077854,
      "url": "/biz/postales-sydney-3?osq=Restaurants",
      "rating": 4.5,
      "address": "1 Martin Pl Lower Ground Flr, Sydney, NSW 2000",
      "latitude": -33.8678447,
      "geohash": "r3gx2fd1sb0s",
      "name": "Postales",
      "distance": 0
    },
    {
	...
    },
    ...
  ]
}
```

#### Steps

##### 1. Install Dependencies

- `pip install -r requirements.txt`

##### 2. Generate Local Json DB

- `python3 -m task1.scraper`

##### 3. Insert  Data to Google Cloud Firestore NoSQL DB

- Configure `Cloud Firestore` and `service_account.json`
- `python3 -m task2.firestore_task`

##### 4. Run the Server & Testing Locally

- `uvicorn main:app --reload`

- Go `localhost:8000/docs#/`

- Test `name, rating, price_type, location` Quries

##### 6. Deployment

- Configure `app.yaml` and `gcloud CLI`
- `gcloud init`
- `gcloud app deploy`
- `gcloud app browse`
