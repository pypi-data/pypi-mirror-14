# Bibblio API Python
Python wrapper of Bibblio API

Register in [Bibblio](bibblio.org) and get your CLIENT_ID and CLIENT_SECRET

## Install
```pip install bibblio```

## Configuration
```python
import bibblio
```

set client_id and client_secret

```python
bibblio.client_id = 'YOUR_CLIENT_ID'
```

```python
bibblio.client_secret = 'YOUR_CLIENT_SECRET'
```

get access_token

```python
bibblio.access_token = bibblio.Token.get_access_token()
```

* the access token has a duration of 5 minutes, remember to update it.

## Usage

For more information use [Bibblio API Documentation](http://docs.bibblio.apiary.io/)
* payload is always a dict
* limit and page are optional and integers
* text is a string
* content_item_id is a string

### Enrichment

```python
response = bibblio.Enrichment.create_content_item(payload)
```

```python
response = bibblio.Enrichment.get_content_items(limit=10, page=1)
```

```python
response = bibblio.Enrichment.get_content_item(content_item_id)
```

```python
response = bibblio.Enrichment.update_content_item(content_item_id, payload)
```

```python
response = bibblio.Enrichment.delete_content_item(content_item_id)
```

```python
response = bibblio.Enrichment.metadata(text)
```

### Discovery

```python
response = bibblio.Discovery.recommendations(content_item_id)
```
