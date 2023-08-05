from datetime import datetime
import time
import inspect
import re

_CAMEL_CASE_REGEX = re.compile(r"([a-z])([A-Z])")
_UNDERSCORE_REGEX = re.compile(r"([a-z])_([a-z])")

def __getPathInfo():
    for item in inspect.stack():
        if item and __file__ not in item:
            return item[1]

    return __file__

def add_ing(word):
    assert type(word) == str and len(word) > 0

    if len(word) >= 3 and word[-3:] == "ing":
        return word

    if word[-1] == 'e':
        word = word[:-1]

    return word + 'ing'

def decorate_jobname(jobname):
    """
    Decorate job name suitable for humans
    :type jobname: str
    :return: decorated string
    :rtype: str
    """
    assert type(jobname) == str and len(jobname) > 0

    jobname = jobname.strip()
    words = jobname.split()

    assert len(words) > 0

    words[0] = add_ing(words[0])
    words = [word.capitalize() for word in words]

    return " ".join(words)

def log(jobName, func, to_file=False, *args, **kwargs):
    file = __getPathInfo()
    slog = "Task: {}\n      Work started.".format(decorate_jobname(jobName))

    print(slog)
    if (to_file):
        with open("{}.log".format(file), "w+") as f:
            f.write("[{}] In {}: {}\n".format(datetime.now(), file, slog))

    t = datetime.now()
    r = func(*args, **kwargs)

    elog = "      Finished in {} seconds.".format((datetime.now() - t).total_seconds())

    print(elog)

    if (to_file):
        with open("{}.log".format(file), "a") as f:
            f.write("[{}] In {}: {}\n".format(datetime.now(), file, elog))

    return r

def parseFunctionName(name):
    if _UNDERSCORE_REGEX.findall(name):
        regex = _UNDERSCORE_REGEX
    elif _CAMEL_CASE_REGEX.findall(name):
        regex = _CAMEL_CASE_REGEX
    else:
        return None

    return regex.sub("\g<1> \g<2>", name).lower()

def task(name=None, to_file=False, *args, **kwargs):
    """
    This decorator modifies current function such that its start, end, and
    duration is logged in console. If task name is not given, it will attempt to
    infer it from the function name. Optionally, the decorator can log
    information into files.
    """
    if callable(name):
        f = name
        name = parseFunctionName(f.__name__)
        if not name:
            name = f.__name__

        return lambda *args, **kwargs: log(name, f, to_file, *args, **kwargs)

    if name == None:
        def wrapped(f):
            name = parseFunctionName(f.__name__)
            return lambda *args, **kwargs: log(name, f, to_file, *args, **kwargs)

        return wrapped
    else:
        return lambda f: lambda *args, **kwargs: log(name, f, to_file, *args, **kwargs)

@task
def testSomeNumber():
    time.sleep(1)

@task("testing some numbers")
def test():
    time.sleep(1)

def main():
    testSomeNumber()
    test()

if __name__ == "__main__":
    main()