from PIL import ImageTk
import numpy as np
import Tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import scipy as sp
from scipy import special
from scipy import integrate
import matplotlib.pyplot as plt



l = 1
alpha = sp.pi * 10 / 180 * 13.5
m = 2


k = sp.sin(alpha/2)
lmb = 2*m*special.ellipk(k)

###  Spaces
s = np.arange(0,l,0.001)
x1s = []
x2s = []


E = 1
I = 1
B = E*I
force = (B*m*m) / (l^2) * (2*k*sp.sin(alpha/2))*(2*k*sp.sin(alpha/2))


##  Functions
def JacobiAmplitude(u_, m_):	
	return special.ellipj(u_,m_)[3]

def EllipticK(k_):
	return special.ellipk(k_)


def EllipticE(phi_, m_):
	return special.ellipeinc(phi_, m_)

def JacobiCN(u_, m_):
	return special.ellipj(u_,m_)[1]


def x1(s_,k,lmb):
	return -s_ + ((2/lmb) * EllipticE(JacobiAmplitude((s_*lmb) + EllipticK(k), k),k) )- (2/lmb)*EllipticE(JacobiAmplitude(EllipticK(k), k), k)
def x2(s_,k,lmb):
	return -2*k/lmb * JacobiCN(EllipticK(k) + s_*lmb, k)


def arc_length(x, y):
    npts = len(x)
    arc = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    for k in range(1, npts):
        arc = arc + np.sqrt((x[k] - x[k-1])**2 + (y[k] - y[k-1])**2)

    return arc




###		GUI

root = Tk.Tk()
root.resizable(True, False);
root.title("Elastica plotter")
rootframe = Tk.Frame(root)
rootframe.pack(fill=Tk.BOTH, expand=True)

f = plt.figure()
a = f.add_subplot(111)
a.plot(x1(s,k,lmb), x2(s,k,lmb))

f2 = plt.figure()
a2 = f2.add_subplot(111)
def x1derr(s,k,lmb):
	return (x1(s+0.001,k,lmb) - x1(s,k,lmb) ) / 0.001

def x2derr(s,k,lmb):
	return (x2(s+0.001,k,lmb) - x2(s,k,lmb) ) / 0.001

a2.plot(s, x2derr(s,k,lmb))


canvas = FigureCanvasTkAgg(f, master=rootframe)
canvas.show()
canvas.get_tk_widget().grid(row=1,column=0, columnspan=5,sticky='W')

framen = Tk.Frame(rootframe)
framen.grid(row=0,column=0, columnspan=5, sticky=Tk.W)
toolbar = NavigationToolbar2TkAgg(canvas, framen)
toolbar.update()





def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=rootframe, text='Quit', command=_quit)
button.grid(row=0,column=4)

### 	GUI for paramteres


l_var = Tk.DoubleVar()
alpha_var = Tk.DoubleVar()
m_var = Tk.IntVar()
I_var = Tk.DoubleVar()

force_text_var = Tk.StringVar()

def redraw_plot(canvas):
	global a
	global s
	global m_var
	global alpha_var
	global l_var
	k = sp.sin(alpha_var.get()*sp.pi/360)
	lmb = 2*m_var.get()*special.ellipk(k)
	s = np.arange(0,l_var.get(),1e-4)

	x1s = x1(s, k, lmb)
	x2s =x2(s, k, lmb)
	bmax = 0
	bavg = 0
	x1derrs = x1derr(s, k, lmb)
	x2derrs = x2derr(s, k, lmb)

	for n in range(1, len(x1s)-2):
		if np.absolute(x1s[n+1]-x1s[n]) > np.absolute(x1s[n+2]-x1s[n])*2 :
			print 'ERROR ' + str(np.absolute(x1s[n+1]-x1s[n]))+ ' ' + str(np.absolute(x1s[n+2]-x1s[n])) + ' ' + str(x1derrs[n-1])
			x1s[n+1] = x1s[n]
			print str(x1s[n]) + ' ' + str(x1s[n+1])

	#x2derrs = m_var.get() ** 2 / l_var.get() ** 2 (2* EllipticK(sp.sin(alpha_var.get()/2*sp.pi/360))) 

	#force = (E_var.get()*I_var.get()*m_var.get()*m_var.get()) / (l_var.get()*l_var.get()) * (2*k*sp.sin(alpha_var.get()/2))*(2*k*sp.sin(alpha_var.get()/2))
	#force_text_var.set(force)		



	a.clear()

	#a.quiver(x1s[0], x2s[0],  np.cos(alpha_var.get()/360*6.28),  np.sin(alpha_var.get()/360*6.28), color='r')
	#a.quiver(x1s[len(x1s)-1], x2s[len(x2s)-1],  np.cos(alpha_var.get()/360*6.28+3.14),  np.sin(alpha_var.get()/360*6.28+3.14), color='b')

	a.plot(x1s, x2s)


	canvas.draw()

	print(k)
	print(lmb)
	print(s)
	print([x1s, x2s])
	print('redraw_plot')




l_frame = Tk.Frame(master=rootframe)
l_frame.grid(row=2,column=0)
label_l = Tk.Label(master=l_frame, text='l [0:1] ')        
label_l.pack()
inp_l = Tk.Scale(master=l_frame, from_=0, to=1, orient=Tk.HORIZONTAL, showvalue=0, resolution=0.1, variable=l_var)
inp_l.pack()
inp_l.set(l)
label_lv = Tk.Label(master=l_frame, textvariable=l_var)
label_lv.pack()


alpha_frame = Tk.Frame(master=rootframe)
alpha_frame.grid(row=2,column=1)
label_alpha = Tk.Label(master=alpha_frame, text='alpha [0:180] ')        
label_alpha.pack()
inp_alpha = Tk.Scale(master=alpha_frame, from_=0, to=180, orient=Tk.HORIZONTAL, showvalue=0, resolution=1, variable=alpha_var)
inp_alpha.pack()
inp_alpha.set(alpha /sp.pi * 180)
label_alphav = Tk.Label(master=alpha_frame, textvariable=alpha_var)
label_alphav.pack()



m_frame = Tk.Frame(master=rootframe)
m_frame.grid(row=2,column=2)
label_m = Tk.Label(master=m_frame, text='m [0:4]')        
label_m.pack()
inp_m = Tk.Scale(master=m_frame, from_=1, to=4, orient=Tk.HORIZONTAL,showvalue=0, resolution=1, variable=m_var)
inp_m.pack()
inp_m.set(m)
label_mv = Tk.Label(master=m_frame, textvariable=m_var)
label_mv.pack()








btn_redraw = Tk.Button(master=rootframe, text='Redraw', command= lambda: redraw_plot(canvas))
btn_redraw.grid(row=2,column=3)


rootframe.grid_columnconfigure(0, weight=1)
rootframe.grid_columnconfigure(1, weight=1)

rootframe.grid_columnconfigure(2, weight=1)
rootframe.grid_columnconfigure(3, weight=1)

rootframe.grid_rowconfigure(0, weight=1)
rootframe.grid_rowconfigure(1, weight=1)
rootframe.grid_rowconfigure(2, weight=1)


root.mainloop()









