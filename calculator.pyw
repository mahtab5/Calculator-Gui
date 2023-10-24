from tkinter import *
from PIL import ImageTk, Image
from pyperclip import copy
import tkinter.messagebox as tmsg

todo = None

willclr = True
prevsum = None
prevsym = None


# functions

def opt(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()


def Copy():
    copy(scvalue.get())
    tmsg.showinfo('Copied', 'Copied To Clipboard')


def ilog(n, base):
    """
    Find the integer log of n with respect to the base.

    >>> import math
    >>> for base in range(2, 16 + 1):
    ...     for n in range(1, 1000):
    ...         assert ilog(n, base) == int(math.log(n, base) + 1e-10), '%s %s' % (n, base)
    """
    count = 0
    while n >= base:
        count += 1
        n //= base
    return count

def sci_notation(n, prec=3):
    """
    Represent n in scientific notation, with the specified precision.

    >>> sci_notation(1234 * 10**1000)
    '1.234e+1003'
    >>> sci_notation(10**1000 // 2, prec=1)
    '5.0e+999'
    """
    base = 10
    exponent = ilog(n, base)
    mantissa = n / base**exponent
    return '{0:.{1}f}e{2:+d}'.format(mantissa, prec, exponent)


def button(txt, frame, primary=True):
    button_ixpad = 28
    button_iypad = 10
    font = 'Lexend 15'
    button_pad = 2
    height = 1
    width = 2

    b = Button(frame, text=txt, font=font, bg=bg, relief=FLAT, padx=button_ixpad, fg =fg,
               pady=button_iypad, height=height, width=width, activebackground=bg, activeforeground=fg, bd=0)

    b.pack(pady=button_pad, padx=button_pad, side=LEFT)
    b.bind('<Button-1>', click)
    b.bind("<Enter>", hover)
    b.bind('<Leave>', release)

def release(event):
    event.widget['fg'] = fg


def hover(event):
    event.widget['fg'] = fg


def update(upscrn=True):
    if upscrn:
        up_screen.update()
    screen.update()


def equal():
    global willclr
    global cc

    cc = ccvalue.get()
    sc = scvalue.get()
    if not cc and sc != '0' and len(sc) > 0:
        ccvalue.set(sc + '=')
        willclr = True

    elif cc and cc[-1] != '=':
        ccvalue.set(cc + sc + '=')
        try:
            answer = eval(cc.replace('^', '**').replace('÷', '/').replace('×', '*') + sc)
            if len(str(answer)) <= 13:
                scvalue.set(answer)
            else:
                answer = sci_notation(answer)
                if len(answer) >= 14:
                    scvalue.set('Overflow')
                else:
                    scvalue.set(answer)

        except ZeroDivisionError:
            scvalue.set('Error!')
            willclr = True

        willclr = True


def equation(sym):
    global willclr
    global cc

    cc = ccvalue.get()
    sc = scvalue.get()
    if sym == '+' or sym == '-' or sym == '÷' or sym == '×' or sym == '^':
        if cc == '0' or len(cc) < 1:
            ccvalue.set(sc + sym)
            scvalue.set('0')
            willclr = True

        elif willclr:
            ccvalue.set(cc[:-1] + sym)

        elif cc[-1] != '=':
            ccvalue.set(cc + sc + sym)
            try:
                answer = eval(cc.replace('^', '**').replace('÷', '/').replace('×', '*') + sc)
                if len(str(answer)) <= 13:
                    scvalue.set(answer)
                else:
                    answer = sci_notation(answer)
                    if len(answer) >= 14:
                        scvalue.set('Overflow')
                    else:
                        scvalue.set(answer)

            except ZeroDivisionError:
                scvalue.set('Error!')

            willclr = True

        else:
            ccvalue.set(sc + sym)
            scvalue.set('0')
            willclr = True

    else:
        if not cc and sc and sc != '0':
            scvalue.set('0')
            willclr = True

        elif cc and sc and sc != '0':
            scvalue.set(float(sc) * 0.01)


def click(event):
    global willclr
    text = event.widget.cget('text')

    if text == '=':
        equal()

    elif text == 'C':
        scvalue.set('0')
        ccvalue.set('')
        willclr = True
        update()

    elif text == 'DEL':
        if not willclr:
            scvalue.set(scvalue.get()[0:-1])

            if len(scvalue.get()) == 0:
                scvalue.set('0')
                willclr = True

        update(0)

    elif text == 'CE':
        scvalue.set('0')
        willclr = True
        update()

    elif text == '.' and len(scvalue.get()) <= 12:
        if not willclr or scvalue.get() == '0':
            if '.' not in scvalue.get():
                scvalue.set(scvalue.get() + '.')
                willclr = False
                update(0)


    else:
        chars = ['+', '-', '÷', '×', '^', '%']
        if text in chars:
            equation(text)
        elif text.isdigit() and len(scvalue.get()) <= 13:
            if not willclr and scvalue.get() != '0':
                scvalue.set(scvalue.get() + text)
            else:
                scvalue.set(text)
                willclr = False


def key_pressed(event):
    global willclr
    chars = ['BackSpace', 'Return', 'equal', 'minus', 'slash', 'period', 'plus', 'asterisk', 'percent', 'asciicircum']
    x = scvalue.get()
    if event.char.isdigit() and len(scvalue.get()) <= 13:
        if not willclr and scvalue.get() != '0':
            scvalue.set(scvalue.get() + event.char)
        else:
            scvalue.set(event.char)
            willclr = False

    elif event.char == '.' and len(scvalue.get()) <= 12:
        if not willclr or scvalue.get() == '0':
            if '.' not in scvalue.get():
                scvalue.set(scvalue.get() + '.')
                willclr = False
                update(0)

    else:
        var = event.keysym
        if var in chars:
            if var == 'equal' or var == 'Return':
                equal()
            elif var == 'slash' or var == 'minus' or var == 'plus' or var == 'asterisk' or var == 'percent' or var == 'asciicircum':
                if var == 'slash' or var == 'asterisk':
                    event.char = '×' if event.char == 'asterisk' else '÷'
                equation(event.char)
            else:
                if var == 'BackSpace':
                    scvalue.set(x[:-1:])
                    if len(scvalue.get()) == 0:
                        scvalue.set('0')
                        willclr = True
                    update(0)


# root
height = 400
width = 350

bg = '#000111'
fg = '#FFFFFF'
upclr = dclr = fg


root = Tk()
root.geometry(f'{width}x{height}')
root.resizable(width=False, height=False)
root.title('Calculator')
root.config(bg=bg)
root.overrideredirect(False)
root.attributes('-alpha', 0.995)



root.wm_iconbitmap(default='calculator.ico')


# code
ccvalue = StringVar()
ccvalue.set('')

scvalue = StringVar()
scvalue.set('0')

up_screen = Label(root, textvar=ccvalue, font='lexend 13', fg=upclr, anchor=E, bg=bg, padx=5)
up_screen.pack(fill=X, anchor=NE, side=TOP)

screen = Label(root, textvar=scvalue, font='lexend 30', fg=dclr, anchor=E, bg=bg, padx=15)
screen.pack(fill=X, pady=10, anchor=NE, side=TOP)
screen.bind('<Button-3>', opt)


m = Menu(root, tearoff=0)
m.add_command(label="Copy", command=Copy)



def buttons():
    line1 = Frame(root, bg=bg)
    line1.pack(anchor=W)

    button('^', line1, False)
    button('CE', line1, False)
    button('C', line1, False)
    button('DEL', line1, False)


    line2 = Frame(root, bg=bg)
    line2.pack(anchor=W)

    button('7', line2)
    button('8', line2)
    button('9', line2)
    button('-', line2, False)

    line2 = Frame(root, bg=bg)
    line2.pack(anchor=W)

    button('4', line2)
    button('5', line2)
    button('6', line2)
    button('+', line2, False)

    line2 = Frame(root, bg=bg)
    line2.pack(anchor=W)

    button('1', line2)
    button('2', line2)
    button('3', line2)
    button('×', line2, False)

    line5 = Frame(root, bg=bg)
    line5.pack(anchor=W)

    button('.', line5, False)
    button('0', line5)
    button('=', line5, False)
    button('÷', line5, False)



buttons()

root.bind('<Key>', key_pressed)

root.mainloop()
