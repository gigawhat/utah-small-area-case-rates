# Utah small area case rates

Gather the crude covid case rate per 100,000 people per small area in Utah.

## Why?

Because this is better than clicking on a map and entering the data by hand.

## Running
You can run this as a Docker container.
```bash
docker pull gigawhat/utah-small-area-case-rates:latest
docker run -p 5000:5000 -e PORT=5000 gigawhat/utah-small-area-case-rates:latest
```

## Demo
> https://tranquil-coast-69945.herokuapp.com/
