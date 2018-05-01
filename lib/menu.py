
import curses


def home_screen(win):

    win.addstr(0, 25, "############################################################")
    win.addstr(1, 25, "#            Welcome to the PDI scientific Suite           #")
    win.addstr(2, 25, "#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  #")
    win.addstr(2, 25, "#            Written and maintained by Jimmy Layne         #")
    win.addstr(3, 25, "#            with the help of Patrick Chuang               #")
    win.addstr(4, 25, "############################################################")
    win.addstr(10, 15, "    Please select an option:                                ")
    win.addstr(11, 15, "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                       ")
    win.addstr(12, 15, "    A) Visualizations                                       ")
    win.addstr(13, 15, "    B) View metrics                                         ")
    win.addstr(14, 15, "    C) Output data to CSV                                   ")
    win.addstr(15, 15, "    Q) Quit                                                 ")
    win.refresh()

    x_home=15
    y_home=18

    return (x_home,y_home)


def vis_screen(win):
    win.addstr(0, 50, "############################################################")
    win.addstr(1, 50, "    Please select from the available visualizations:        ")
    win.addstr(2, 50, "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       ")
    win.addstr(3, 50, "    A) Event Time Series                                    ")
    win.addstr(4, 50, "    B) DSD Percentiles                                      ")
    win.addstr(5, 50, "    C) View Volume                                          ")
    win.addstr(6, 50, "    D) Concentration                                        ")
    win.addstr(7, 50, "    E) Liquid Water Content                                 ")
    win.addstr(8, 50, "    F) Probe Volume Diameter                                ")
    win.addstr(9, 50, "    Q) Go Back                                              ")
    win.refresh()

    x_home=50
    y_home=12

    return((x_home,y_home))


def save_screen():
    print("######################################")
    print("Please enter each item you would like to save, separated by comma then press enter")
    print("1) Full events file (csv)")
    print("2) Visualisations")
