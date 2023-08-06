import string
import re

from abc import ABCMeta, abstractmethod, abstractproperty
from math import ceil

# TODO:
# add support for clearing screen

class InvalidMenuException(Exception):
    pass


def get_thing_as_is(st):
    return st


def get_printable(st):
    new_st = re.sub(r'\x1b.*?\[.*?m', '', st)
    return ''.join([x for x in new_st if x in string.printable[:-5]])

def get_num_to_alpha(num):
    st = ''
    n = num
    base = ord('a')-1
    while n > 0:
        st += chr(base + (n%26))
        n /= 26
    return st

def get_set_tuple(li):
    # TODO:Get better name.
    mem = {x:True for x in li}
    set_list = []
    for x in li:
        if mem[x]:
            set_list.append(x)
            mem[x]=False
    return tuple(set_list)

def are_equal(first, other):
    fdict = {x:True for x in first}
    try:
        [fdict.pop(x) for x in other]
    except KeyError:
        return False

    return not bool(fdict)


class Menu(object):
    __metaclass__ = ABCMeta

    allowed_positions = ['top', 'bottom']

    def __init__(self,
                 ambiguous=False,
                 columns=1,
                 func=get_thing_as_is,
                 help_text='',
                 help_pos='bottom',
                 is_main_menu=True,
                 key=None,
                 lazy=False,
                 menu_style='vertical',
                 options=['foo', 'bar'],
                 prompt='>',
                 sort=False,
                 resolve=True,
                 reverse=False,
                 rows=None,
                 *args,
                 **kwargs
                 ):
        '''
        :param ambiguous: Allows selection of multiple items.
        :type ambiguous: bool
        :param columns: Number of columns in printed menu.
        :type columns: int
        :param func: Function to call on options before showing.
        :type func: Function that accepts single arg.
        :param help_text: Text for heading or instructions.
        :type help_text: str
        :help_pos: Help position. Top or bottom of menu.
        :type help_pos: str
        :is_main_menu: Tells if current menu is main menu.
        :type is_main_menu: bool
        :param key: Function to use as key during sorting.
        :type key: Any function that can be used as key.
        :param lazy: Make the picture now or when needed.
        :type lazy: bool
        :param menu_style: Sets the order how options are shown.
        :type menu_tyle: str
        :param options: The things from which the user has to choose from.
        :type options: list, tuple, or set.
        :param prompt: Prompt to show while asking for input.
        :type prompt: str
        :param sort: Tells whether to sort the options or not.
        :type sort: bool
        :param resolve: Keep asking until a single option remains.
        :type resolve: bool
        :param reverse: Sort in reverse order.
        :type reverse: bool
        :param rows: Number of rows to show.
        :param args: Ignore them
        :param kwargs: Ignore them
        '''
        self.ambiguous = ambiguous
        self.help_text = help_text
        pos = help_pos.lower()
        for p in self.allowed_positions:
            if pos in p:
                self.help_pos = pos
                break
        else:
            raise InvalidMenuException(
                    'Invalid value for help text position: '+help_pos)
        self.columns = columns
        self.lazy = lazy
        self.func = func
        self.is_main_menu = is_main_menu
        self.key = key
        if sort:
            self.options = tuple(sorted(set(options), reverse=reverse, key=key))
        else:
            self.options = get_set_tuple(options)
        self.menu_style = menu_style
        self.num_options = len(self.options)
        self.sort = sort
        self.resolve = resolve
        self.reverse = reverse
        self.prompt = prompt
        self.rows = rows
        if not self.lazy:
            self.make_menu()

    def show_menu(self):
        if self.lazy and not self.menu_made:
            self.make_menu()
        print self.picture

    def get_response(self):
        while True:
            # show menu
            self.show_menu()
            # get input
            res = self.get_valid_response()
            # valid response?
            if res is None:
                # no: start over
                continue
            # get matching items
            items = self.get_real_items(self.get_matching_items(res))
            if len(items) > 1:      # items are mutliple?
                # yes: multiple allowed?
                if not self.ambiguous:      # no: start over
                    continue
                if self.resolve:           # yes: resolve?
                    # same options as now?
                    if are_equal(items, self.options):
                        continue
                    # no: make and show new menu
                    new_ops = {x:y for x,y in self.__dict__.items()}
                    new_ops['menu_made'] = False
                    new_ops['lazy'] = False
                    new_ops['options'] = items
                    new_ops['is_main_menu'] = False
                    if self.is_main_menu:
                        new_ops['help_text'] += '''
Enter a wrong option to return to previous menu
'''
                    sub_menu = self.__class__(**new_ops)
                    new_res = sub_menu.get_response()
                    if new_res:
                        return new_res
                    else:
                        continue
                else:
                    # no: return them
                    return items
            elif len(items) == 1:
                # return one item
                return items[0]
            # No items matched.
            if not self.is_main_menu:
                return items

    def get_real_items(self, things):
        '''Process the item(s) before returning.'''
        return things

    def get_valid_response(self):
        '''Returns cleaned response or None if not valid.
        Not really needed but can be useful.'''
        res = raw_input(self.prompt)
        return res

    def make_picture(self):
        self.picture = ''
        l = self.num_options
        max_w = 0
        rows = []
        sep = ' '*4
        if self.rows is not None:
            r = max(1, self.rows)
            c = int(ceil(float(l) / self.rows))
        else:
            c = max(1, self.columns)
            r = int(ceil(float(l) / c))
        for i in range(r):
            if self.menu_style=='horizontal':
                cols_in_row = self.pic_blocks[i*c : min((i+1)*c, l)]
            elif self.menu_style=='vertical':
                cols_in_row = [self.pic_blocks[x] for x in range(i,l,r)]
            else:
                raise Exception('Unknown menu style '+self.menu_style)

            if not cols_in_row:     #TODO: Fix this.
                continue
            rows.append(cols_in_row)
            max_w = max(max_w, max([len(x) for x in cols_in_row]))
        base_str = ':<{}'.format(max_w)
        align_str = '{'+base_str+'}'
        rows = [[align_str.format(col) for col in row] for row in rows]
        self.picture = '\n'.join([sep.join(row) for row in rows])
        if self.help_pos == 'bottom':
            self.picture += '\n' + self.help_text
        else:
            self.picture = self.help_text + self.picture

    @abstractmethod
    def make_menu(self):
        '''Sets variables used in get_matching_items.
        Sets self.picture.
        Sets self.pic_blocks if uses self.make_picture.
        Sets menu_made to true'''
        pass

    @abstractmethod
    def get_matching_items(self, res):
        '''returns set'''
        pass


class IdentifierMenu(Menu):
    styles = ['number', 'alphabet']

    def __init__(self,
                 join=False,
                 joiner=' ',
                 idfunc=str,
                 style='number',
                 **kwargs
                 ):
        '''
        :param join: Add a joining line.
        :type join: bool
        :param joiner: The joiner to use.
        :type joiner: str
        :param idfunc: Function which is called on identifier index.
        :type idfunc: function returning string
        :param style: Style of identifier.
                     Should be in self.styles.
        :type style: str
        :param width: Width of identifier + joiner
        :type width: int
        '''
        self.join = join
        self.joiner = joiner

        st = style.lower()
        for s in self.styles:
            if st in s:
                self.style = s
                break
        else:
            raise InvalidMenuException(
                    'Invalid value for menu style: '+style)

        if self.style == 'alphabet' and idfunc==str:
            self.idfunc = get_num_to_alpha
        else:
            self.idfunc = idfunc

        super(IdentifierMenu, self).__init__(**kwargs)

    def make_menu(self):
        self.__ids_shown, self.__ops_shown = [], []
        max_width = 0
        pad = int(ceil(6.0/len(self.joiner)))
        self.picture = self.help_text if self.help_pos == 'top' else ''
        # for easier selection
        self.__choice_dict = dict()
        self.__shown_to_real = dict()
        for i, option in enumerate(self.options, start=1):
            # set identifier
            mapped_id = self.idfunc(i)
            self.__ids_shown.append(mapped_id)
            max_width = max(max_width, len(mapped_id))
            # process option
            popt = self.func(option)
            cleaned_popt = get_printable(popt)
            self.__ops_shown.append(popt)
            self.__choice_dict[get_printable(mapped_id)] = cleaned_popt
            self.__shown_to_real[cleaned_popt] = option

        # make the picture
        align = ':{}<{}'.format(self.joiner, max_width+pad)
        ids = [('{'+align+'}').format(x) for x in self.__ids_shown]
        self.pic_blocks = [theid+op for theid,op in zip(ids, self.__ops_shown)]

        self.make_picture()

        # Important to set.
        self.menu_made = True

    def get_matching_items(self, res):
        lres = res.lower()
        possible_options = list()
        cleaned_ids, cleaned_ops = zip(*self.__choice_dict.items())
        possible_ids = [x for x in cleaned_ids if x.lower()==lres]
        possible_options.extend([self.__choice_dict[x] for x in possible_ids])
        if len(possible_options) == 1:
            return possible_options
        possible_options.extend([x for x in cleaned_ops if x.lower().startswith(lres)])
        if len(possible_options) == 1:
            return possible_options
        if self.ambiguous:
            other_possible_ids = [x for x in cleaned_ids if lres in x.lower()]
            possible_options.extend([self.__choice_dict[x] for x in other_possible_ids])
            other_possible_options = [x for x in cleaned_ops if lres in x.lower()]
            possible_options.extend(other_possible_options)
        return get_set_tuple(possible_options)

    def get_real_items(self, things):
        real_things = [self.__shown_to_real[x] for x in things]
        return real_things
