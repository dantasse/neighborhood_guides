# Neighborhood Guides

If you're going to a new city and staying in an AirBnB or similar rental, where are you going to stay? What are the different neighborhoods like? This project aims to help you answer that, using data from social media like Twitter and Flickr.

## Directory structure

These five:

- `aesthetic`
- `convenience`
- `liveliness`
- `localness`
- `safety` 

Are where the scripts for computing the parts of the models are. There's also:

- `data` for "input" data files, like neighborhood boundary GeoJSON files etc. Probably don't check big files into there though still - git doesn't work great with big files.
- `util` for python scripts that are used throughout a bunch of different files.
- `site` for the website
  

## Getting started
To build any of the models, run them from the top level here, like so:

	cd neighborhood_guides
	virtualenv env
	source env/bin/activate
	pip install -r requirements.txt
    python -m aesthetic.foo
    
(if you're running `aesthetic/foo.py`). The first four lines are to install and activate the virtual environment; that makes sure you have all the packages you need and nothing's conflicting with anything you might have installed on your computer already.

The last line is so relative imports work well - since you're running python from the top level, you can do stuff like this:

    import aesthetic.foo
    # or
    from aesthetic import foo
    
If you try to just run python scripts like you're used to, you might find that it's hard to, say, import something from `util` into `aesthetic`.

## Making changes and republishing

Build the app in `site/`. Then copy everything from the `site/dist` directory into `docs`. (This is because github pages [is set up](https://github.com/dantasse/neighborhood_guides/settings/pages) to read from `docs`.) Then, you might have to change index.html to remove some leading slashes in imports, as in [this commit](https://github.com/dantasse/neighborhood_guides/commit/7df250434225ccd9742d736424d157dc661a11be).
