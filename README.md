# Discogs Scraper

Discogs Scraper is a web scraper built using Python and Scrapy to scrape release data from Discogs.com. It allows you to specify sorting, release format, genre, and style, and it outputs the data in CSV or JSON format.

## Features

- Scrape Discogs release data based on user-defined criteria
- Choose from different sorting methods, release formats, genres, and styles
- Limit the number of pages to scrape
- Export data to CSV or JSON format
- Output includes:

  - Artist
  - Title
  - Label
  - Format
  - Release year
  - Genre
  - Styles
  - Have (number of users who have this release)
  - Want (number of users who want this release)
  - Ratings (number of ratings)
  - Average rating (out of 5)
  - Last sold date
  - Lowest sold price
  - Medium sold price
  - Highest sold price

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/discogs-scraper.git
```
2. Install required dependencies:
```cd discogs-scraper
pip install -r requirements.txt
```
## Usage
Run the scraper with the following command:
```
python discogs_scraper.py [OPTIONS]
```

## Command Line Options
| --- | --- |
| -so, --sort | Sort format (choices: hot, most wanted, most collected; default: most wanted) |
| -f, --format | Release format (default: Vinyl) |
| -g, --genre | Release genre (default: Electronic) |
| -s, --style | Release style (default: Electro) |
| -l, --limit | Limit the number of pages to scrape (default: 100) |
| -o, --output | Output format (choices: csv, json; default: csv) |


## Example usage:
```
python discogs_scraper.py --sort=want --format=CD --genre=Electronic --style=Ambient --limit=50 --output=json
```
