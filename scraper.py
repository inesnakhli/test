from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


def scrape_facebook_page(page_id: str):
    # Replace 'your_access_token' with the actual user access token
    access_token = 'EAAKJm3TfNb8BO9XeA94uEp5ihw126RHuQYldlMSA8sS2OEAIu00iSt6A3rZAaeVaaauz2pVZBrmtRMJdBZCB09ZBrc6RCYU2pIWxAB2O7gKehnnR3BZBknyzZCJDOz2a6atGNQW8yEZBvu7DUZBT9aJS7ZAZCreoXyIzGBHcKFi9t0ZCUW4mRrpC97JwIuTlh6cVG6e4ZANv25IzNZBoREZB2WoMZBnJI8UtCUZD'

    # Make a request to the Facebook Graph API to get the page data
    url = f'https://graph.facebook.com/v18.0/{page_id}?access_token={access_token}'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=errh.response.status_code, detail="HTTP Error")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Assume the response is in JSON format
    data = response.json()

    # Extract relevant information from the response
    page_name = data.get('name', 'N/A')
    page_likes = data.get('fan_count', 'N/A')

    # You can customize this part based on the actual structure of the data you want to scrape

    return {"page_name": page_name, "page_likes": page_likes}


@app.get("/scrape/facebook/{page_id}")
def scrape_facebook(page_id: str):
    try:
        scraped_data = scrape_facebook_page(page_id)
        return {"status": "success", "data": scraped_data}
    except HTTPException as e:
        return {"status": "error", "error_message": str(e)}
