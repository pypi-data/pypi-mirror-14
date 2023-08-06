try:
    import cPickle as pickle
except:
    import pickle
import os

def __get_filename(path, name, ext):
    name = name if path == None else os.path.join(path, name)
    ext = "" if ext == None else ".{}".format(ext)
    filename = name + ext

    return filename
 
def dump(obj, name, path=None, ext="dat", overwrite=True, silent=False):
    """
    Dumps the object to disk with given name and extension.
    Optionally the path can be specified as well. (But nothing stops
    you from adding path to the name.
    """
    if path and os.path.isfile(path):
        raise ValueException("Specified path is a file.")

    filename = __get_filename(path, name, ext)
    
    if not overwrite and os.path.exists(filename):
        if not silent:
            raise ValueException("Specified output filename already exists.")
        return
    
    with open(filename, "wb") as f:
        pickle.dump(obj, f)

def load(name, path=None, ext="dat", silent=False):
    """
    Loads an object from file with given name and extension.
    Optionally the path can be specified as well.
    """
    filename = __get_filename(path, name, ext)

    if not os.path.exists(filename):
        if not silent:
            raise ValueException("Specified input filename doesn't exist.")
        return None

    with open(filename, "rb") as f:
        return pickle.load(f)

def main():
    dump({1: "A", 2: "B", 3: "C"}, "test")
    assert load("test")[3] == "C"
    os.remove("test")
