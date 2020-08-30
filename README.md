# Photosorter
*Sort photos by their capture time.*  

**Photosorter** will try to find the `capture time` of all the photos placed inside `PHOTOS_DIR_PATH`
and place it in the specified folder `SORTED_DIR_PATH` by `year` and `month`. If the `capture time` is
not accessible, it will be placed inside `UNKNOWN_STUFF_DIR_PATH`.

### Installation and usage
1. Make sure you are in `virtualenv` using `Python 3+` and then and install dependencies:
    
        pip install -r requirements.txt
    
2. Define all variables in `.env` file:

        PHOTOS_DIR_PATH=""
        SORTED_DIR_PATH=""
        UNKNOWN_STUFF_DIR_PATH=""
        DUPLICATES_DIR_PATH=""
    
3. Run `sorter.py` script