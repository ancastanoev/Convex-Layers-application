import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

import geometry_utils as geometryutils
from algorithm_jarvis import jarvis_layers as jarvislayersfunction
from algorithm_graham import graham_layers as grahamlayersfunction

from algorithm_andrew import andrew_layers as andrewlayersfunction
from algorithm_quickhull import quickhull_layers as quickhulllayersfunction
from algorithm_chan import chan_layers as chanlayersfunction

#this is the main logic class of the project, having all utilities taht appear in the Gui. We hae here teh function for benchamarking all teh algorithm for all point distributions
#we have a function to create widgets, some helpers for the gui and all the methods taht deal with drawing points, animations etc.
#midlfrmonce enetring the main application gui you will see teh options to chosse from one of the 6 point distributions presented in the paper plus an additional one - the heart
#once choosting taht, you can select any nr of points, peel/depeel, genereate report or genearte bechmark
#beacause the algorithm can be viszualised in parallel, we acn see how each of them chooses teh points and differences - both in runtime and in actual visuals-
def benchmark(distributionmodes, sizeslist, repeatcount, mainwindow, textwidget):
    #this is the main function taht deals with benchmarking, for all the 5 algorithms
    algorithmsdict = {
        "jarvis": jarvislayersfunction,
        "graham": grahamlayersfunction,
        "andrew": andrewlayersfunction,
        "quickhull": quickhulllayersfunction,

        "chan": chanlayersfunction
    }

    lineslist = []
    headerline = "DIST, SIZE, ALGO, AVG_TIME_S, LAYERS_COUNT"
    lineslist.append(headerline + "\n" + "=" * 50)

    resultsdata = []
    for distname in distributionmodes:
        for cursize in sizeslist:
            for algoname, algofunc in algorithmsdict.items():
                totaltime = 0.0
                totallayers = 0
                for _ in range(repeatcount):
                    pointslist = geometryutils.generate_points(distname, cursize, 1000, 1000)
                    starttime = time.perf_counter()
                    layerresult = algofunc(pointslist)
                    endtime = time.perf_counter()
                    totaltime += (endtime - starttime)
                    totallayers += len(layerresult)
                avgtime = totaltime / repeatcount
                avglayerscount = totallayers // repeatcount
                lineentry = f"{distname}, {cursize}, {algoname}, {avgtime:.4f}, {avglayerscount}"
                lineslist.append(lineentry)
                resultsdata.append((distname, cursize, algoname, avgtime, avglayerscount))

    from collections import defaultdict
    timesdict = defaultdict(lambda: defaultdict(float))


    countdict = defaultdict(lambda: defaultdict(int))

    for distname, sizeval, algoname, atime, layercount in resultsdata:
        timesdict[distname][algoname] += atime
        countdict[distname][algoname] += 1

    analysislines = []
    analysislines.append("\nExtended Analysis:")
    analysislines.append("-" * 50)

    for distname in timesdict:
        bestalgo = None
        besttime = float("inf")
        for algoname in timesdict[distname]:
            curentavg = timesdict[distname][algoname] / countdict[distname][algoname]
            if curentavg < besttime:
                besttime = curentavg
                bestalgo = algoname
        analysislines.append(
            f"For pointsmode '{distname}', fastest on average: {bestalgo} ({besttime:.4f}s)"
        )





    lineslist.append("\n" + "\n".join(analysislines))
    lineslist.append("\nBenchmark complete.")

    finalresultsstr = "\n".join(lineslist)
    mainwindow.after(0, lambda: widgethelper(textwidget, finalresultsstr))


def widgethelper(textwidget, resultsstring):

    textwidget.configure(state="normal")
    textwidget.delete("1.0", tk.END)
    textwidget.insert("end", "Extended Benchmark Results\n", "heading")
    textwidget.insert("end", "=" * 35 + "\n\n")
    textwidget.insert("end", resultsstring + "\n")
    textwidget.configure(state="disabled")


lavenderbgcolor = "#E6E6FA"
lavenderdarkcolor = "#9370DB"
canvasbgcolor = "#F8F8FF"
framebgcolor = lavenderbgcolor
textbgcolor = "#F8F8FF"

pointsmodes = [
    "Uniform Random",
    "Mostly Collinear",
    "Duplicates",
    "Heart",
    "Fibonacci Spiral",
    "Sierpinski Triangle",
    "Koch Snowflake",
]


class Convexlayersapp(tk.Frame):
    def __init__(self, mainwindow=None):
        super().__init__(mainwindow)
        self.mainwindow = mainwindow
        self.pack(fill="both", expand=True)

        self.aftercallbacks = {}
        self.canvaswidth = 400
        self.canvasheight = 300



        self.numpoints = 50
        self.stopanimation = True

        self.refreshinprogress = False

        self.pointslist = []
        self.jarvislayerslist = []
        self.grahamlayerslist = []


        self.andrewlayerslist = []
        self.quickhulllayerslist = []
        self.listchan = []

        self.algorithmstarttimes = {}


        self.animationtimes = {}
        self.animationinprogress = False

        self.mainwindow.configure(bg=lavenderbgcolor)
        self.configure(bg=lavenderbgcolor)
        self.createwidgets()

    def ongeneratepoints(self):
        if self.animationinprogress:
            messagebox.showinfo("Animation in proress",
                                "Stopping curent animation before generating new points.")
            self.stopanimation = True

        self.numpoints = int(self.nrpoints.get()) if self.nrpoints.get().isdigit() else 50

        disttype = self.pointmod.get()
        self.pointslist = geometryutils.generate_points(disttype, self.numpoints,
                                                        self.canvaswidth, self.canvasheight)

        self.jarvislayerslist.clear()
        self.grahamlayerslist.clear()
        self.andrewlayerslist.clear()
        self.quickhulllayerslist.clear()
        self.listchan.clear()

        self.algorithmstarttimes.clear()


        self.animationtimes.clear()

        for cvs in [self.canvasjarvis, self.canvasgraham, self.canvasandrew,
                    self.canvasquickhull, self.canvaschan]:
            self.drawpoints(cvs, self.pointslist)

    def computeonionlayersn2(self, pts):

        tmp = pts[:]
        layersres = []
        while len(tmp) >= 3:
            hullfound = self.jarvishull(tmp)
            layersres.append(hullfound)
            for p in hullfound:
                tmp.remove(p)
        return layersres


    def distancesq(self, a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def createwidgets(self):
        #this function deals with the creation of widgets. we use separate threads to simulate widget paralelism
        frametop = tk.Frame(self, bg=framebgcolor)
        frametop.pack(side="top", fill="x", padx=5, pady=5)


        self.pointmod = tk.StringVar(value=pointsmodes[0])
        tk.Label(frametop, text="pointsmode:", font=("Helvetica", 11, "bold"), bg=framebgcolor
                 ).pack(side="left", padx=2)
        distmeniu = ttk.OptionMenu(frametop, self.pointmod, pointsmodes[0], *pointsmodes)
        distmeniu.pack(side="left", padx=2)

        self.nrpoints = tk.StringVar(value=str(self.numpoints))
        tk.Label(frametop, text="Num Points:", font=("Helvetica", 11, "bold"), bg=framebgcolor
                 ).pack(side="left", padx=2)
        anca_widget_pints = tk.Entry(frametop, textvariable=self.nrpoints, width=5, font=("Helvetica", 10))
        anca_widget_pints.pack(side="left", padx=2)




        stylebuton = {"font": ("Helvetica", 10, "bold"), "bg": lavenderdarkcolor, "fg": "white", "relief": "raised"}

        tk.Button(frametop, text="Generate Points", command=self.ongeneratepoints, **stylebuton
                  ).pack(side="left", padx=5)

        tk.Button(frametop, text="Compute Layers", command=self.computealllayers, **stylebuton
                  ).pack(side="left", padx=5)

        tk.Button(frametop, text="Start Animation", command=self.animstart, **stylebuton
                  ).pack(side="left", padx=5)





        tk.Button(frametop, text="Generate Report", command=self.displayreport, **stylebuton
                  ).pack(side="left", padx=5)

        tk.Button(frametop, text="Extended Benchmark", command=self.extbeanchmark, **stylebuton
                  ).pack(side="left", padx=5)

        tk.Button(frametop, text="Refresh", command=self.refresh, **stylebuton
                  ).pack(side="left", padx=5)

        tk.Button(frametop, text="Dynamic Peel", command=self.dynwidget, **stylebuton
                  ).pack(side="left", padx=5)


        #de terminat rendering
        midlfrm = tk.Frame(self, bg=framebgcolor)
        midlfrm.pack(side="top", fill="both", expand=True)

        canvasfrm = tk.Frame(midlfrm, bg=framebgcolor)
        canvasfrm.pack(side="left", fill="both", expand=True)

        self.canvasjarvis = self.makecanvas(canvasfrm, "Jarvis", 0, 0)



        self.canvasgraham = self.makecanvas(canvasfrm, "Graham", 0, 1)
        self.canvasandrew = self.makecanvas(canvasfrm, "Andrew", 1, 0)
        self.canvasquickhull = self.makecanvas(canvasfrm, "Quickhull", 1, 1)
        self.canvaschan = self.makecanvas(canvasfrm, "Chan", 2, 0)

        reportframe = tk.Frame(midlfrm, bd=2, relief="groove", bg=framebgcolor)
        reportframe.pack(side="right", fill="y", padx=5, pady=5)

        tk.Label(reportframe, text="Algorithm Report", font=("Helvetica", 12, "bold"), bg=framebgcolor
                 ).pack(side="top", padx=5, pady=5)

        self.reptx = tk.Text(reportframe, wrap="word", font=("Helvetica", 10, "italic"),
                                  height=15, width=30, bg=textbgcolor, fg="#333333")
        self.reptx.pack(fill="both", expand=True, padx=5, pady=5)
        scrl = ttk.Scrollbar(reportframe, command=self.reptx.yview)
        self.reptx.configure(yscrollcommand=scrl.set)
        scrl.pack(side="right", fill="y")
        self.reptx.configure(state="disabled")
        self.reptx.tag_configure("heading", font=("Helvetica", 12, "bold"))

        canvasfrm.grid_rowconfigure(0, weight=1)
        canvasfrm.grid_rowconfigure(1, weight=1)





        canvasfrm.grid_rowconfigure(2, weight=1)
        canvasfrm.grid_columnconfigure(0, weight=1)
        canvasfrm.grid_columnconfigure(1, weight=1)

    def dynwidget(self):
        # with this func we open a small window nmaed 'dynamic Peel' to add remove points
        peel_win = tk.Toplevel(self.mainwindow)
        peel_win.title("Dynamic Peel")
        peel_win.configure(bg=framebgcolor)
        peel_win.resizable(False, False)


        # the intial guid was not rendered for some widges like teh report generator taht we  use. now we render it
        tk.Label(peel_win, text="X:", bg=framebgcolor).grid(row=0, column=0, padx=4, pady=4, sticky="e")
        x_entry = tk.Entry(peel_win, width=8)
        x_entry.grid(row=0, column=1, padx=4, pady=4)



        tk.Label(peel_win, text="Y:", bg=framebgcolor).grid(row=1, column=0, padx=4, pady=4, sticky="e")
        yent = tk.Entry(peel_win, width=8)
        yent.grid(row=1, column=1, padx=4, pady=4)

        action_var = tk.StringVar(value="insert")



        radio_frm = tk.Frame(peel_win, bg=framebgcolor)
        radio_frm.grid(row=0, column=2, rowspan=2, padx=10, sticky="n")

        tk.Radiobutton(radio_frm, text="Insert", variable=action_var, value="insert",
                       bg=framebgcolor).pack(anchor="w", pady=2)
        tk.Radiobutton(radio_frm, text="Delete", variable=action_var, value="delete",
                       bg=framebgcolor).pack(anchor="w", pady=2)

        submtbutton = tk.Button(peel_win, text="Submit",
                               command=lambda: self.dynamiconionupdaten2(x_entry.get(), yent.get(), action_var.get()))
        submtbutton.grid(row=2, column=0, columnspan=3, pady=10)

    def makecanvas(self, parentframe, algoname, rowval, colval):
        newframe = tk.Frame(parentframe, bd=2, relief="groove", bg=lavenderbgcolor)
        newframe.grid(row=rowval, column=colval, padx=5, pady=5, sticky="nsew")
        tk.Label(newframe, text=algoname, font=("Helvetica", 12, "bold"), bg=lavenderbgcolor
                 ).pack(side="top")
        newcanvas = tk.Canvas(newframe, width=self.canvaswidth, height=self.canvasheight, bg=canvasbgcolor)
        newcanvas.pack(side="top", fill="both", expand=True)
        return newcanvas


    def computealllayers(self):

        if self.animationinprogress:
            messagebox.showinfo("Animtion in progress",
                                "Stopping curent animation before recomputing layers.")
            self.stopanimation = True



        if not self.pointslist:
            messagebox.showwarning("No Points", "Generate points before computing layers.")
            return

        self.jarvislayerslist = jarvislayersfunction(self.pointslist)
        self.grahamlayerslist = grahamlayersfunction(self.pointslist)
        self.andrewlayerslist = andrewlayersfunction(self.pointslist)


        self.quickhulllayerslist = quickhulllayersfunction(self.pointslist)
        self.chanlayerslchanist = chanlayersfunction(self.pointslist)



        self.listchan = chanlayersfunction(self.pointslist)

        self.algorithmstarttimes.clear()
        self.animationtimes.clear()

        for cvs in [self.canvasjarvis, self.canvasgraham, self.canvasandrew,
                    self.canvasquickhull, self.canvaschan]:


            self.drawpoints(cvs, self.pointslist)


    def extbeanchmark(self):
        listadistribut = [
            "Uniform Random",
            "Mostly Collinear",
            "Circular",
            "Duplicates",
            "Fibonacci Spiral",
            "Sierpinski Triangle",
            "Koch Snowflake"
        ]
        sizeslist = [1000]
        repeatcount = 1

        def backgroundtask():
            benchmark(listadistribut, sizeslist, repeatcount, self.mainwindow, self.reptx)





        threading.Thread(target=backgroundtask).start()


    def animstart(self, algoname=None, canvasobj=None, layerslist=None, colorval=None,
                  layeridx=0, lineidx=0):

        if algoname is None:
            if self.refreshinprogress or self.animationinprogress:
                print("animation is already running or in refresh, Ignoring start.")
                return

            if not self.pointslist or not self.jarvislayerslist:
                messagebox.showwarning("No Points", "generate and compute layers frist.")
                return

            self.stopanimation = False
            self.animationinprogress = True

            self.animstart("jarvis", self.canvasjarvis, self.jarvislayerslist, "red", 0, 0)



            self.animstart("graham", self.canvasgraham, self.grahamlayerslist, "blue", 0, 0)
            self.animstart("andrew", self.canvasandrew, self.andrewlayerslist, "green", 0, 0)
            self.animstart("quickhull", self.canvasquickhull, self.quickhulllayerslist, "purple", 0, 0)
            self.animstart("chan", self.canvaschan, self.listchan, "orange", 0, 0)
            return

        if self.stopanimation or self.refreshinprogress:
            return

        if layeridx >= len(layerslist):
            if algoname in self.algorithmstarttimes and algoname not in self.animationtimes:
                self.animationtimes[algoname] = time.perf_counter() - self.algorithmstarttimes[algoname]
            return

        currlayer = layerslist[layeridx]

        n = len(currlayer)

        if layeridx == 0 and lineidx == 0 and algoname not in self.algorithmstarttimes:
            self.algorithmstarttimes[algoname] = time.perf_counter()

        if lineidx == 0:
            canvasobj.delete("all")
            self.drawpoints(canvasobj, self.pointslist)

            for previndex in range(layeridx):
                prevlayer = layerslist[previndex]
                stepval = max(1, len(prevlayer) // 10)
                i = 0
                while i < len(prevlayer):
                    endindex = min(i + stepval, len(prevlayer))
                    for j in range(i, endindex):
                        x1, y1 = prevlayer[j]
                        x2, y2 = prevlayer[(j + 1) % len(prevlayer)]
                        x1 = x1 * self.scale + self.xoffset
                        y1 = y1 * self.scale + self.offsety



                        
                        x2 = x2 * self.scale + self.xoffset




                        y2 = y2 * self.scale + self.offsety
                        canvasobj.create_line(x1, y1, x2, y2, fill=colorval, width=2)
                    i += stepval

        if lineidx < n:
            x1, y1 = currlayer[lineidx]
            x2, y2 = currlayer[(lineidx + 1) % n]
            x1 = x1 * self.scale + self.xoffset
            y1 = y1 * self.scale + self.offsety

            y2 = y2 * self.scale + self.offsety
            x2 = x2 * self.scale + self.xoffset
            canvasobj.create_line(x1, y1, x2, y2, fill=colorval, width=2)

            idforanim = canvasobj.after(
                20,
                lambda: self.animstart(algoname, canvasobj, layerslist, colorval,
                                       layeridx, lineidx + 1)
            )
            self.aftercallbacks[f"{algoname}_{layeridx}_{lineidx}"] = idforanim
        else:
            idforanim = canvasobj.after(
                200,
                lambda: self.animstart(algoname, canvasobj, layerslist, colorval,
                                       layeridx + 1, 0)
            )
            self.aftercallbacks[f"{algoname}_layer_{layeridx}"] = idforanim

    
    def onclose(self):

        self.stopanimation = True

        for idforanim in self.aftercallbacks.values():
            self.mainwindow.after_cancel(idforanim)

        self.aftercallbacks.clear()




        self.mainwindow.destroy()

    def displayreport(self):
        complexitiesdict = {
            "jarvis": "O(n^2)",
            "graham": "O(n log n)",
            "andrew": "O(n log n)",
            "quickhull": "O(n log n) (avg)",
            "chan": "O(n log h)"
        }

        for algo in complexitiesdict.keys():
            self.animationtimes.setdefault(algo, 0.0)

        fastestalgo = min(self.animationtimes, key=self.animationtimes.get, default="N/A")
        fastesttime = self.animationtimes.get(fastestalgo, 0.0)
        bestmemoryalgo = "chan"
        bestmemcomplexity = "O(n log h)"

        curentpointmode = self.pointmod.get()
        if curentpointmode == "Mostly Collinear":
            bestmemoryalgo = "graham"
            bestmemcomplexity = "O(n log n)"
        elif curentpointmode in ["Duplicates", "Uniform Random"]:
            bestmemoryalgo = "quickhull"
            bestmemcomplexity = "O(n log n) (avg)"

        self.reptx.configure(state="normal")
        self.reptx.delete("1.0", tk.END)

        self.reptx.tag_configure("heading", font=("Helvetica", 14, "bold"), foreground="#4B0082")






        self.reptx.tag_configure("subheading", font=("Helvetica", 12, "bold"), foreground="#2E8B57")
        #we do a report foe each alg
        self.reptx.tag_configure("highlight", font=("Helvetica", 11, "bold"), foreground="#8B0000")
        self.reptx.tag_configure("fastest", font=("Helvetica", 11, "bold"), foreground="#008000")
        self.reptx.tag_configure("normal", font=("Helvetica", 10))

        self.reptx.insert("end", "Algorithm Performance Report\n", "heading")
        self.reptx.insert("end", "=" * 40 + "\n\n", "heading")

        self.reptx.insert("end", "Algorithm Details:\n", "subheading")
        self.reptx.insert("end", "-" * 25 + "\n", "subheading")

        for algo, comp in complexitiesdict.items():
            tval = self.animationtimes.get(algo, 0.0)
            self.reptx.insert("end", f"\u2022 {algo.capitalize()} Algorithm:\n", "highlight")
            self.reptx.insert(
                "end",
                f"   Complexity: {comp}\n"
                f"   Execution Time: {tval:.6f} seconds\n\n",
                "normal"
            )

        self.reptx.insert("end", "Conclusions:\n", "subheading")
        self.reptx.insert("end", "-" * 25 + "\n", "subheading")

        if fastestalgo != "N/A":
            self.reptx.insert(
                "end",
                f"\u2714 Fastest Algorithm: {fastestalgo.capitalize()} ({fastesttime:.6f} seconds)\n",
                "fatsest"
            )
        else:
            self.reptx.insert("end", "Fastest Algorithm: N/A\n", "highlight")

        self.reptx.insert("end", "\nMemory Usage:\n", "subheading")
        self.reptx.insert("end", "-" * 25 + "\n", "subheading")
        self.reptx.insert(
            "end",
            f"Best fr Memory: {bestmemoryalgo.capitalize()} ({bestmemcomplexity})\n",
            "normal"
        )

        self.reptx.configure(state="disabled")




        #de adaugat restul de functii helper

    def refresh(self):
        self.refreshinprogress = True
        self.stopanimation = True

        for idforanim in self.aftercallbacks.values():




            self.mainwindow.after_cancel(idforanim)

        self.aftercallbacks.clear()
        self.pointslist.clear()
        self.jarvislayerslist.clear()
        self.grahamlayerslist.clear()




        self.andrewlayerslist.clear()
        self.quickhulllayerslist.clear()
        self.listchan.clear()
        self.algorithmstarttimes.clear()



        self.animationtimes.clear()
        self.canvasjarvis.delete("all")
        self.canvasgraham.delete("all")




        self.canvasandrew.delete("all")
        self.canvasquickhull.delete("all")
        self.canvaschan.delete("all")

        self.reptx.configure(state="normal")
        self.reptx.delete("1.0", tk.END)


        self.reptx.configure(state="disabled")

        self.pointmod.set(pointsmodes[0])

        self.nrpoints.set("50")

        self.animationinprogress = False
        self.refreshinprogress = False
        print("aplication state has been RESET,")


    def jarvishull(self, pts):

        if len(pts) < 3:
            return pts[:]
        startpt = min(pts, key=lambda p: (p[0], p[1]))
        hullres = [startpt]
        curent = startpt
        while True:
            candidate = None
            for p in pts:
                if p != curent:
                    candidate = p
                    break
            for p in pts:
                if p == curent:
                    continue
                direction = self.crossproduct(curent, candidate, p)
                if direction > 0 or (direction == 0 and self.distancesq(curent, p) > self.distancesq(curent, candidate)):
                    candidate = p
            curent = candidate




            if curent == startpt:
                break
            hullres.append(curent)
        return hullres

    def crossproduct(self, origin, a, b):
        return (a[0] - origin[0]) * (b[1] - origin[1]) - (a[1] - origin[1]) * (b[0] - origin[0])




    def dynamiconionupdaten2(self, pxval, pYval, action="insert"):




        if action == "insert":

            newpt = (float(pxval), float(pYval))
            self.pointslist.append(newpt)
        elif action == "delete":
            target_point = (float(pxval), float(pYval))
            if target_point in self.pointslist:

                self.pointslist.remove(target_point)

            else:
                messagebox.showwarning("Deletion Errr",
                                       f"Point ({pxval}, {pYval}) not found; canot delete")
                return
        else:
            messagebox.showwarning("invalid Action", "Use 'insert' or 'delete'.")
            return








        affected_layer_idx = 0

        if action == "insert":
            for idx, layer in enumerate(self.jarvislayerslist):
                excluded_points = set()
                for prev_layer in self.jarvislayerslist[:idx]:
                    excluded_points.update(prev_layer)
                points_excluding_prev = [p for p in self.pointslist if p not in excluded_points]

                hull = self.jarvishull(points_excluding_prev)

                if newpt in hull:
                    affected_layer_idx = idx
                    break
                affected_layer_idx = idx + 1
        elif action == "delete":
            for idx, layer in enumerate(self.jarvislayerslist):



                if (pxval, pYval) in layer:
                    affected_layer_idx = idx
                    break
            else:
                messagebox.showwarning("Deletion Notice..",
                                       f"Point ({pxval}, {pYval}) not found in any layer.")
                return

        newlyrs = self.jarvislayerslist[:affected_layer_idx]
        pointsremain = [p for p in self.pointslist if p not in set().union(*newlyrs)]

        while len(pointsremain) >= 3:

            hull = self.jarvishull(pointsremain)
            newlyrs.append(hull)
            pointsremain = [p for p in pointsremain if p not in hull]

        if pointsremain:
            newlyrs.append(pointsremain.copy())

        self.jarvislayerslist = newlyrs

        self.algorithmstarttimes.clear()
        self.animationtimes.clear()

        self.drawpoints(self.canvasjarvis, self.pointslist)

        self.animstart("jarvis", self.canvasjarvis, self.jarvislayerslist, "red", 0, 0)

    def drawpoints(self, canvasobj, points):
        canvasobj.delete("all")
        if not points:
            return

        cw = canvasobj.winfo_width()




        ch = canvasobj.winfo_height()
        margin = 20

        minx = min(x for x, _ in points)
        maxy = max(y for _, y in points)
        miny = min(y for _, y in points)




        maxX = max(x for x, _ in points)

        scalex = (cw - 2 * margin) / (maxX - minx) if (maxX != minx) else 1
        scaley = (ch - 2 * margin) / (maxy - miny) if (maxy != miny) else 1
        self.scale = min(scalex, scaley)

        self.xoffset = (cw - (maxX - minx) * self.scale) / 2 - minx * self.scale
        self.offsety = (ch - (maxy - miny) * self.scale) / 2 - miny * self.scale

        radius = 2
        for px, py in points:
            xval = px * self.scale + self.xoffset
            
            
            
            yval = py * self.scale + self.offsety
            canvasobj.create_oval(xval - radius, yval - radius, xval + radius, yval + radius,
                                  fill="black", outline="")

if __name__ == "__main__":
    root = tk.Tk()
    
    
    
    root.title("Convex Layers Visualization")
    app = Convexlayersapp(mainwindow=root)
    root.protocol("WM_DELETE_WINDOW", app.onclose)
    app.mainloop()
