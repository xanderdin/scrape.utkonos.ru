Parser of utkonos.ru
====================

A simple Scrapy spider for scraping products data from http://www.utkonos.ru.
This spider saves data to an SQLite database file.

## Spider name

- **collector**


## SQLite settings

Edit utkonos/settings.py file and set the following settings:

- **SQLITE_FILE** -- Database file. Default: output.db.
- **SQLITE_COMMIT_WATERMARK** -- Commit once after so many processed items.
Default: 100.

If you want to save images to a directory enable **FilesPipeline** in
**ITEM_PIPELINES** setting. You can also change the **FILES_STORE** setting
to any directory you want (default: 000).

### Example

> scrapy crawl collector


For available options run:

> scrapy crawl --help


Scrapy docs: http://doc.scrapy.org
