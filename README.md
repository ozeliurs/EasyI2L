# EasyI2L - Easy IP2Location Wrapper

`easyi2l` is a Python wrapper around the [IP2LOCATION](https://www.ip2location.com/) library. It allows you to automatically download and load the IP2LOCATION database, simplifying the process of working with IP geolocation data.

## Features

- **Automatic Download**: Fetches the IP2LOCATION database directly using your IP2LOCATION token.
- **Database Loading**: Automatically loads the downloaded database for immediate use.
- **Simple API**: Retrieve IP geolocation data with minimal setup.

## Installation

Install the package via pip:

```bash
pip install easyi2l
```

## Usage

Before using the package, ensure you have the `IP2LOCATION_TOKEN` environment variable set. You can obtain a token from [IP2Location LITE](https://lite.ip2location.com/).

### Example

Here's a simple example of how to use `easyi2l`:

```python
from easyi2l import EasyI2L, DBType


db = EasyI2L.download(DBType.DB11LITEBIN).load()

# Retrieve all data for an IP address
print(db.get_all("1.1.1.1"))
```

### Environment Setup

You need to set the `IP2LOCATION_TOKEN` environment variable for the package to function correctly. The package uses `load_dotenv` from the `dotenv` module to load this variable from a `.env` file in your working directory.

Create a `.env` file with the following content:

```plaintext
IP2LOCATION_TOKEN=your_token_here
```

## Contributing

Feel free to open issues or submit pull requests to improve the library.

## License

This project is licensed under the MIT License.