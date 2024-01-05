import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import pylab as pl

"""
The outer arm spins around at a speed, precisely π times faster than the inner arm. But because π is this never-ending, irrational number, that outer arm will never, ever stop at its starting point, no matter how long the video goes on. It's like a forever chase scene where the arm always misses the target line by the tiniest bit, and that bit is basically as thin as it gets.

Full explanation: https://www.reddit.com/r/oddlysatisfying/comments/17dif1m/comment/k5y7s8i/?share_id=myKxqqS_5fsqgfMwXrXM7&utm_content=2&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=1

For the two ends of the figure to match up perfectly, x has to be a number such that both parts of the formula are eventually back to a previous value (= both rods are at identical rotation angles).
For example, if x=3, that near miss at 0:12 in the animation would be a hit and the figure would already be complete there.
But x isn't 3, it's pi = 3.1459... - so the inner rod has already turned a tad further than it should have. So they don't match up.
You can see that at that moment, the inner rod has done one full rotation and the other one has done just a tad more than 3 full rotations. It's a near miss because that 3/1 = 3 is close to pi.
[...] The very last close call is at 355/113 (if you're bored, feel free to count the rotations), a famously good approximation for pi - but still just an approximation, not an exact match. If we could ever get to such a fraction for (outer rotation / inner rotations) = pi, the figure would close up perfectly.

Perciò posso calcolare in quale momento andranno a sovrapporsi.
Ad esempio con 3 andranno a sovrapporsi quando il segmento interno avrà ruotato di 360*1 gradi e quello esterno di 360*3.
3 infatti sarebbe 3/1 = rotazioni esterne / rotazioni interne. Perciò basta calcolare theta in 360 gradi * 1 giri

con 1/3 ad esempio ci vorrebbero 1 rotazione esterna e 3 rotazioni interne. Questo pone la necessità di calcolare theta in 360 gradi * 3 giri prima che il punto torni all'inizio.

Con qualsiasi numero intero (>1) quindi basta 1 giro.
Con un numero compreso fra 0 e 1 servono un numero di giri pari al denominatore. Es. 1/3 richiede 3 giri, 1/10 ne richiede 10.
La forma disegnata è la stessa per un intero e il suo reciproco.

Per qualsiasi frazione serve un numero di giri pari al denominatore.

A questo punto è ovvio che un numero irrazionale non incontrerà mai il punto di partenza, perché non si può individuare il denominatore.
In python però ovviamente il numero irrazionale non ha infinite cifre decimali, ma avrà una certa approssimazione, e sarà quindi in realtà razionale. Se allora si riesce a trovare il denominatore di quel numero razionale, sarà possibile capire quanti giri ci vogliono affinché il punto torni alla posizione di partenza.
"""

def set_degrees(from_deg, to_deg, by_step, radians):
    theta_degrees = np.linspace(from_deg,
                                to_deg,
                                by_step)
    
    if radians:
        return np.deg2rad(theta_degrees)
    else:
        return theta_degrees
    
    return theta_degrees

# #Create an array of theta values in degrees (e.g., for T  0 to 113*360 degrees)
# theta_degrees = np.linspace(0, 213*360,10000)

# #Convert degrees to radians
# theta_radians = np.deg2rad(theta_degrees)

# my_coeff = np.pi
# my_coeff=np.e
#my_coeff=np.sqrt(2)
#my_coeff=13
#my_coeff=1/999999

#Calculate z(theta) using the formula, 1j is imaginary number
# z = np.exp(theta_radians * 1j) + np.exp(my_coeff * theta_radians * 1j)

# first_segment = np.exp(theta_radians * 1j)
# second_segment = np.exp(my_coeff * theta_radians * 1j)


def plot_segments(first_segment, second_segment, n_steps=100):
    # create segments lists to plot
    seg_list_1=[]
    seg_list_2=[]
    for i in range(n_steps):
        seg_list_1.append([(0,0),(np.real(first_segment[i]),np.imag(first_segment[i]))])
        seg_list_2.append([seg_list_1[i][1],(np.real(second_segment[i])+np.real(first_segment[i]),np.imag(second_segment[i])+np.imag(first_segment[i]))])

    #plot
    lc = mc.LineCollection(seg_list_1,
                        linewidths=0.5)
    lc2 = mc.LineCollection(seg_list_2)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.add_collection(lc2)
    ax.autoscale()
    ax.margins(0.1)
    
    # plt.show()


def plot_final(z, title):
    #separate the real and imaginary parts of z
    x = np.real(z)
    y = np.imag(z)

    #Create a plot with specific settings
    plt.figure(figsize=(10, 10)) # Set a square figure 10x10 inches
    plt.plot(x, y, color='white', linewidth=0.5) # Set line color to white and line width to 0.5
    plt.gca().set_facecolor('black') # Set background color to black
    plt.gca().set_aspect('equal') # Equal aspect ratio
    plt.grid(False) # Turn off the grids
    plt.xlim(-2.5, 2.5) # X-axis limit
    plt.ylim(-2.5, 2.5) # Y-axis limit
    plt.title(title)
    
    # plt.show()

def find_min_dist(z, my_coeff, by_step, rounds):

    """
    Ho capito che pi ha il suo minimo a 113 giri, quindi è più importante sapere il giro dove c'è il minimo, non lo step.
    
    Vedi il commento all'inizio del foglio.
    """
    
    diff = z[1:by_step]-z[0]
    
    min_abs_value = np.min(np.abs(diff))
    res_step = np.argmin(np.abs(diff))
    
    print(f"coeff: {my_coeff} -> min dist is {min_abs_value} at step {res_step}")
    
    # Find the indices of all occurrences of the minimum absolute value
    # sta roba è inutile perché i valori corrispondono sempre. Mi sa che ti dà il primo di default
    # min_abs_indices = np.where(np.abs(diff) == min_abs_value)[0]

    # Get the index of the first occurrence
    # first_min_abs_index = min_abs_indices[0]
    
    # print(f"first found at step {first_min_abs_index}")
    
    
    if res_step == 0:
        print(f"No convergence found in {rounds} rounds")
    elif res_step != 0:
        print(f"Convergence found within {rounds} rounds, at step {res_step}")


def mixed_coeff(pezzi_dict, theta_radians):
    """
    è una roba un po' inutile, finisci solo per sovrapporre più grafici uno all'altro
    """
    
    z = []
    start_end_index = 0
    ii = 0
    for i in range(len(pezzi_dict["n_steps"])):
        #Calculate z(theta) using the formula, 1j is imaginary number
        z.append( 
                 np.exp(theta_radians[start_end_index : pezzi_dict['n_steps'][i]] * 1j) + \
            np.exp(pezzi_dict["coeffs"][i] * theta_radians[start_end_index : pezzi_dict['n_steps'][i]] * 1j) 
            )
        
        ii += 1 #serve per contare con quanti step iniziare
        start_end_index = pezzi_dict['n_steps'][i]
        
    return np.concatenate(z).ravel()
    

    

if __name__=='__main__':
    by_step = 10000
    rounds = 32
    
    theta_radians = set_degrees(from_deg = 0, 
                                to_deg = rounds*360,
                                by_step = by_step,
                                radians = True)
    
    # set angle coefficient
    # my_coeff = np.sqrt(2)
    # numbers_sequence = [0, -3, 5, 2.75, -1/3, 1.61803398875, -np.sqrt(2), 10, -0.75, 7/4, np.pi, -np.e]
    # numbers_sequence = [0, 0.1, 0.2, 0.5, 0.55, 0.555, 0.5555, 0.5555]
    # numbers_sequence = [0]
    # numbers_sequence = [10, 0.3, 1/3, np.sqrt(2), np.pi, np.e]
    numbers_sequence = [np.e, np.pi]
    
    for my_coeff in numbers_sequence:
    
        #Calculate z(theta) using the formula, 1j is imaginary number
        z = np.exp(theta_radians * 1j) + np.exp(my_coeff * theta_radians * 1j)
        
        # print(f"with coeff {my_coeff}")
        find_min_dist(z, my_coeff, by_step, rounds)
        print("")

        # first_segment = np.exp(theta_radians * 1j)
        # second_segment = np.exp(my_coeff * theta_radians * 1j)

        
        #plots
        # plot_segments(first_segment, second_segment)
        plot_final(z, title = str(my_coeff))
    plt.show()
    
    """
    pezzi_dict = {
        "n_steps": [3000, 4000],
        "coeffs": [1, 2]
    }
    
    z = mixed_coeff(pezzi_dict, theta_radians)
    plot_final(z, title = str("mixed"))
    plt.show()
    """


"""
Devo calcolare per ogni valore quanto ci mette a tornare al punto iniziale.
In altre parole, dopo quanti giri la linea torna a sovrapporsi a se stessa?

"""