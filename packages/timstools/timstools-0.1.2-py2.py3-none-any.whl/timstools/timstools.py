'''
Short Collection of Classes/Functions used across differnt projects

'''
from collections import OrderedDict
import contextlib
import json 
import os
import urllib.request
import urllib.error
import io
import functools

try:
    import pysftp
except ImportError:
    pass
def universal_setup(): #lost this sigh have to remake
    pass
    
def sftp_upload_window_size_set(srv,file, method_to_call='put'):
    '''
    sets config for uploading files with pysftp
    default method is put, but you can change the
    method_to_call value to do put_d or put_r etc
    '''
    channel = srv.sftp_client.get_channel()
    channel.lock.acquire()
    channel.out_window_size += os.stat(file).st_size *1.1   # bit more bytes incase packet loss
    channel.out_buffer_cv.notifyAll()
    channel.lock.release()
    #~ srv.put(file)
    #~ print('srv.{0}({1})'.format(method_to_call, file))
    #~ exec("srv.{0}('{1}')".format(method_to_call, file))

class InMemoryWriter(list):
    """
    Used to defer saving and opening files to later controllers
    just write data to here
    
    On creation you can read all contents either from:
    an open file,
    a list
    a path/name to a file
    
    by default if the file is not found it will add the str as a row,
    set verbose to True to throw an error instead
    
    While iterating you can set copy=True to edit data
    as you iterate over it
    
    you can accesses the current position using self.i, useful if 
    you are using filter or something like that while iterating
    
    #NOTE NAME VERBOSE IS VERY INAPT I KNOW BUT CBF ATM
    
    """
    def __init__(self, insert_me=None, verbose=False, copy=False):
        list.__init__(self)
        self.copy = copy
        self.data = self            # i was using data variable instead of inheriting from list to lazy to rename
        if type(insert_me) == str:
            try:
                with open(insert_me, 'r') as file: 
                    self.writelines(file)
                    self.original_filename = insert_me
            except FileNotFoundError as err:
                if not verbose:
                    self.append(insert_me)
                raise err
        elif insert_me:
            self.writelines(insert_me)
    def write(self, stuff):
        self.append(stuff)
    def writelines(self, passed_data):
        for item in passed_data:
            self.data.append(item)
    def close(self):
        self.strData = json.dumps(self.data)    #turned into str
    def __call__(self, copy=None):
        if copy:
            self.copy = True
        return self
    def __iter__(self):                 
        self.i=0
        if self.copy:
            self.data_copy = self.data[:]
        return self
    def __next__(self):
        if self.i+1 > len(self.data):
            with ignored(AttributeError):
                del self.data_copy
            raise StopIteration  
        if not self.copy:
            requested = self.data[self.i]
        else:
            requested = self.data_copy[self.i]
        self.i+=1
        return requested

    def readlines(self):
        return self.data

    def save(self, path=False):
        '''If you passed the filename as a str will default to that otherwise pass in a name'''
        if not path:
            path = self.original_filename
        with open(path, 'w') as file: 
            for row in self.data:
                file.write(row)
    #~ def __contains__(self, y):
        
    #~ def __str__(self):
        #~ return self.strData
    #~ def __repr__(self):
        #~ return self.data


class InMemoryReader(): #http://www.diveintopython3.net/iterators.html
    def __init__(self,data): # dont think this has a purpose lol...
        self.data=data
    def __iter__(self):
        self.i=0
        return self
    def __next__(self):
        if self.i+1 > len(self.data):   
             raise StopIteration  
        requested=self.data[self.i]
        self.i+=1
        return requested
            
    def close(self):
        print('in reader close method')
        #~ self.strData=json.dumps(self.data)   #turned into str

@contextlib.contextmanager
def ignored(*exceptions,details=None):
    try:
        yield
    except exceptions as e:
        
        if details and details in str(e):   #skip what was wanting to be skipped
            pass
        elif details:       #if details not in str but details passed in raise
            raise e

def SCREAM(message,note=None,header='$(#)@$() ---SCREAMMM ----!!!!!'):
    """
    NICE VISABLE MESSAGE FOR DEBUGGING SCREAMMM RAWR
    DO YOU SEE ME KNOW!!!
    """
    print()
    print('!@#$%^&*()!@#$%^&*(!@#$%^&*-----')
    print()
    if note != None:
        #~ message =[message,'---->',note]
        header =[header,'-->  ', note]
    print(header)
    print(message)
    print()
    print('!@#$%^&*()!@#$%^&*(!@#$%^&*-----')
    print('ENDING THE SCREAM-- IT ALL goes silent now..')
    print()

def DPRINT(message,note=None,header='--------- Debug Below----------'):
    #~ return                   # USED FOR NOT PRINTING XD
    """
    Debug Print, easier to see XD
    """
    #~ for i in flattenUntil(message,list):
        #~ print('LIST')
        #~ print(i)
    print()
    if note != None:
        #~ message =[message,'---->',note]
        header =[header,'-->  ', note]
    print(header)
    print(message)
    print()

@staticmethod
def PDICT(objD,comparison=None):    #object Dictionary, Prints each key value on a line
    print('----------Start of Dict-----------')
    if type(objD)!=dict:objD=objD.__dict__
    if comparison==None:
        if type(objD)==dict:    
            sortedObj = OrderedDict(sorted(objD.items()))
            for key, value in sortedObj.items():
                print([key,'  --->  ',value])
    elif type(objD)==dict:  #comparison dict method     ### TBD
        sortedObj = OrderedDict(sorted(objD.items()))
        sortedObj2 = OrderedDict(sorted(comparison.items()))
        
        for key,key2 in zip(sortedObj.keys(),sortedObj2.keys()):
            #~ print(key,key2)
            if not sortedObj.get(key2):
                print('First Object: Doesnt contain key :  '+key2+'        from Second Object')
            #~ if not sortedObj2.get(key):
                #~ print(str(comparison)+': Doesnt contain key:'+key+'from :'+str(objD))
    print('----------end of dict----------')

def PTYPE(obj): #TBD
    print('----------- Printing Types---------')
    for i in obj:
        print(type(obj))
        try:
            print(obj.__name__)#FAILS..
        except:
            pass
    print('-----------Fin Print Types -----------')

def PMETHODS(obj): #prints all methods
    print('-------Printing Methods---------------')
    a=[method for method in dir(obj) if callable(getattr(obj, method))]
    #~ print(a)
    for i in a:
        print(i)
    print('-------------methods fin--------------')
    
def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))
        
def error_to_bool(func,*args):
    try:
        func(*args)
        return True
    except:
        return False

basestring = (str,bytes)
#~ typestruct = (type(list),type(dict),type(tuple))
import sys
from functools import wraps
class TraceCalls(object):
    """ Use as a decorator on functions that should be traced. Several
        functions can be decorated - they will all be indented according
        to their call depth.
    """
    def __init__(self, stream=sys.stdout, indent_step=2, show_ret=False):
        self.stream = stream
        self.indent_step = indent_step
        self.show_ret = show_ret

        # This is a class attribute since we want to share the indentation
        # level between different traced functions, in case they call
        # each other.
        TraceCalls.cur_indent = 0

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            indent = ' ' * TraceCalls.cur_indent
            argstr = ', '.join(
                [repr(a) for a in args] +
                ["%s=%s" % (a, repr(b)) for a, b in kwargs.items()])
            self.stream.write('%s%s(%s)\n' % (indent, fn.__name__, argstr))

            TraceCalls.cur_indent += self.indent_step
            ret = fn(*args, **kwargs)
            TraceCalls.cur_indent -= self.indent_step

            if self.show_ret:
                self.stream.write('%s--> %s\n' % (indent, ret))
            return ret
        return wrapper

@TraceCalls()
def flatten(l, typestruct=(list,tuple),global_count=''):
    def track(global_count,count):
        return
        global_count = global_count.split(',')
        try:
            current = int(global_count[-1])
        except ValueError:  #errors out on first level
            current = int(global_count[0])
        new = current + count
        global_count.append(str(new))
        global_count = ','.join(global_count)
        string = 'Global: '+global_count+' current: '+str(current)+' new: '+str(new)
        return string
        print(string)
    if global_count:
        #each level is seperated by a comma with deeper levels being on the right
        global_count = global_count + '.0'
        current = 0
    else:
        global_count = '0,'
    
    for i, el in enumerate(l):
        if isinstance(el, typestruct) and not isinstance(el, basestring):
            for j, sub in enumerate(flatten(el)):
                #~ print('USING RECURSION ELEMENT')
                print('Element:',sub,'  :',track(global_count,j))
                return sub
        
        elif isinstance(el,dict) and not isinstance(el, basestring):
            for j, (key, value) in enumerate(el.items()):
                print('dict key:',key,' :',track(global_count,j))
                return key
                if isinstance(value, typestruct) and not isinstance(value, basestring):
                    for k, sub in enumerate(flatten(value)):
                        #~ print('USING RECURSION ELEMENT')
                        print('dict value:',sub,'   :',track(global_count,k))
                        return sub
                else:
                    print('dict value:',value,' :',track(global_count,j))
                    return value
            
        else:
            print('top level el I:',el,'    :',track(global_count,i))
            return el

            
def flattenUntil(l,typestruct=(list,dict,tuple)):
    if isinstance(l, typestruct): #only return elements of typestruct dont go deepeter
        for el in l:
            if isinstance(el, typestruct):  #if the next element is a typestruct
                for subel in flattenUntil(el):
                    if isinstance(subel,typestruct):
                        yield subel
                yield el    
                    
def traverse(item):
    try:
        for i in iter(item):
            for j in traverse(i):
                yield j
    except TypeError:
        yield item
        #~ 
def sysArgsDict(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
            argv = argv[2:]
        else:
            opts[argv[0]] = argv[0]
            argv = argv[1:]
    return opts

def inIf(items,Check):
    for i in items:
        if i in check:
            yield i
        else:
            yield False


def unique_int(values):
    '''
    if a list looks like 3,6
    if repeatedly called will return 1,2,4,5,7,8
    '''
    last = 0
    for num in values:  #generate a unique number
        if last not in values:  #num is  uniquie (will return numbers if the list has skips so p1 p2 p5,
            #~ print('checking if last not in
            break
        else:               #number already exists
            last += 1
    return last             #looped till end, then it was plussed so just return new value

def next_highest_num(values):
    '''
    The next highest number will be returned
    if a list looks like 2,3,19
    will return 20,21,22 on succesive calls
    '''
    if not values:
        return 0
    for last_num in reversed(sorted(values)):
        return last_num + 1

def internet_on():
    try:
        urllib.request.urlopen('http://74.125.228.100',timeout=1)
        return True
    except urllib.error.URLError: pass
    return False                

def parent_path(path, level=1):
    '''Returnts a parent of a path, or parent parent etc depending on level specifed'''
    splitup = path.split(os.sep)
    return splitup[:-level]
    
def python_bit_version():
    if sys.maxsize > 2**32:
        return 64
    else:
        return 32

@contextlib.contextmanager
def silence():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

def get_drf(__file__, file):
    '''returns the directory relative to the current file'''
    return os.path.join(os.path.dirname(__file__), file)


def preserve_cwd(function):
    '''Decorator used for keeping the original cwd after function call'''

    @functools.wraps(function)
    def decorator(*args, **kwargs):
        cwd = os.getcwd()
        try:
            return function(*args, **kwargs)
        finally:
            os.chdir(cwd)

    return decorator
