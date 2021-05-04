
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from cexprtk import *
import numpy as np
import sympy as sym


class App:

    def __init__(self):
       
        self.root = tk.Tk()
        self.root.title("Function optimalization")
        self.started = True

        self.frame1 = tk.Frame()
        self.frame1.pack(fill=tk.X)
        self.function_label = tk.Label(self.frame1, text="Function:", width=16)
        self.function_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.Function_Text = tk.Entry(self.frame1)
        self.Function_Text.pack(fill=tk.X, padx=5, expand=True)

        self.frame2 = tk.Frame()
        self.frame2.pack(fill=tk.X)
        self.starting_point_label = tk.Label(self.frame2, text="Starting point:", width=16)
        self.starting_point_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.StartingPoint_Text = tk.Entry(self.frame2)
        self.StartingPoint_Text.pack(fill=tk.X, padx=5, expand=True)

        self.frame3 = tk.Frame()
        self.frame3.pack(fill=tk.X)
        self.iterations_label = tk.Label(self.frame3, text="Max iterations:", width=16)
        self.iterations_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.Iterations_Text = tk.Entry(self.frame3)
        self.Iterations_Text.pack(fill=tk.X, padx=5, expand=True)

        self.frame4 = tk.Frame()
        self.frame4.pack(fill=tk.X)
        self.epsilon_label = tk.Label(self.frame4, text="Epsilon:", width=16)
        self.epsilon_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.Epsilon_Text = tk.Entry(self.frame4)
        self.Epsilon_Text.pack(fill=tk.X, padx=5, expand=True)

        self.frame5 = tk.Frame()
        self.frame5.pack(fill=tk.X)
        #       self.area_label = tk.Label(self.frame5, text="Searching Area:", width=16)
        #        self.area_label.pack(side=tk.LEFT, padx=5, pady=5)
        tk.Label(self.frame5, text="Searching Area:", width=16).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Label(self.frame5, text="x0:", width=5).pack(side=tk.LEFT)
        self.Area_Text_X0 = tk.Entry(self.frame5)
        self.Area_Text_X0.pack(side=tk.LEFT)
        tk.Label(self.frame5, text="x1:", width=5).pack(side=tk.LEFT)
        self.Area_Text_X1 = tk.Entry(self.frame5)
        self.Area_Text_X1.pack(side=tk.LEFT)
        tk.Label(self.frame5, text="y0:", width=5).pack(side=tk.LEFT)
        self.Area_Text_Y0 = tk.Entry(self.frame5)
        self.Area_Text_Y0.pack(side=tk.LEFT)
        tk.Label(self.frame5, text="y1:", width=5).pack(side=tk.LEFT)
        self.Area_Text_Y1 = tk.Entry(self.frame5)
        self.Area_Text_Y1.pack(side=tk.LEFT)

        self.frame6 = tk.Frame()
        self.frame6.pack(fill=tk.X)
        self.exit_button = ttk.Button(self.frame6, text="Exit", command=exit)
        self.exit_button.pack(side=tk.RIGHT)
        self.start_button = ttk.Button(self.frame6, text="Start", command=self.start)
        self.start_button.pack(side=tk.RIGHT)

        self.figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.root)
        self.bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        self.figure2 = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax2 = self.figure2.add_subplot(111, projection='3d')
        self.bar2 = FigureCanvasTkAgg(self.figure2, self.root)
        self.bar2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        """df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')"""
       
        self.root.mainloop()

    def start(self):
        self.next_step()
        self.draw_plot()
        return

    def get_function_value(fx, val_x, val_y):
        return evaluate_expression(fx, {"x": val_x, "y": val_y})

    def function_derivative(self,variable):
        fx = self.Function_Text.get()
        x,y = sym.symbols('x y')
        fx.replace("^", "**")
        fx = sym.diff(fx,variable)
        fx = str(fx)
        fx.replace("**", "^")
        return fx

    def next_step(self):
        gradient = ['x','y']
        x0 = 0
        y0 = 0
        x,y = sym.symbols('x y')
        fx = self.Function_Text.get()
        dfx=self.function_derivative(x)
        dfy=self.function_derivative(y)
        gradient[0] =-self.get_function_value(dfx,0,0)
        gradient[1] =-self.get_function_value(dfy,0,0)
        epsilon = 1
        beta =2/5
        Tr = 9
        Tl = 0
        d = [1,0]
        p = np.dot(gradient,d)
        while(e !=0 ):
            T=1/2*(Tl+Tr)
            fxtd = self.get_function_value(fx,x+T*d[0],y+T*d[1])
            if( fxtd < (self.get_function_value(fx,x0,y0)+(1-beta)*p*T)):
                Tl = T
            else: 
                if(fxtd < (self.get_function_value(fx,x0,y0)+beta*p*T)):
                    Tr = T
                else:
                    e = 0
        return T

    def draw_plot(self):
        N = 100
        x0 = evaluate_expression(self.Area_Text_X0.get(), {})
        x1 = evaluate_expression(self.Area_Text_X1.get(), {})
        y0 = evaluate_expression(self.Area_Text_Y0.get(), {})
        y1 = evaluate_expression(self.Area_Text_Y1.get(), {})
        x_axis = np.arange(start=x0, stop=x1, step=abs(x1 - x0) / N)
        y_axis = np.arange(start=y0, stop=y1, step=abs(y1 - y0) / N)
        values = np.empty(int(x_axis.shape[0]*y_axis.shape[0]))
        i = 0
        for x in x_axis:
            for y in y_axis:
                values[i] = self.get_function_value(self.Function_Text.get(),x, y)
                i = i + 1
        values = values.reshape(x_axis.shape[0], y_axis.shape[0])

        self.ax1.clear()
        self.ax1.contour(x_axis, y_axis, values)
        self.bar1.draw_idle()
        x_3d = []
        y_3d=[]
        for i in range(x_axis.shape[0]):
            x_3d.append(x_axis)
            y_3d.append(y_axis)
        x_3d = np.array(x_3d).transpose()
        y_3d = np.array(y_3d)
        self.ax2.clear()
        self.ax2.plot_surface(x_3d, y_3d, values)
        self.bar2.draw_idle()

        return

app = App()
