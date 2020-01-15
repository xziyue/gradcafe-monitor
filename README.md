# Gradcafe Monitor

Crawls data from [gradcafe](https://www.thegradcafe.com/) and list them out in a more
compact manner.

## Usage

1. Run `crawler.py` to fetch data from gradcafe. You may want to change `subject` and
`startDate` for your interest.
2. Run `markdown_generator.py` to generate output.

To run scripts in `./alanshawn.com`, make sure to add the current folder to `PYTHONPATH`
environment variable.

## Merging duplicated institutions

If there are duplicated institutions in the result, modify `merge_items.py` accordingly
to group the results.

## Demo

- [Computer Science](https://www.alanshawn.com/pavilion/2020/01/15/gradcafe-cs.html)
- [Statistics](https://www.alanshawn.com/pavilion/2020/01/15/gradcafe-stat.html)