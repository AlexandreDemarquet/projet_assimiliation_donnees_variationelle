from plots import plot_outputVDA_bis
from main import run_vda_bis
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# run_vda_bis("/home/n7student/Documents/assimilation_donnees_2/tp2/data/", path_out="./resultats/")

# plt.figure()
# plot_outputVDA_bis("/home/n7student/Documents/assimilation_donnees_2/tp2/data/")
# plot_outputVDA_bis("/home/n7student/Documents/assimilation_donnees_2/tp2/data/","/home/n7student/Documents/assimilation_donnees_2/tp2/resultats/" )
# plt.show()





def plot_test(l_path):
    path_out_ref = "./results/"
    path_data = "./data/"



    # load data
    file_dfr=path_data+'case.csv'
    dfr = pd.read_csv(file_dfr)
    L = dfr["L"][0]; nb_cell = dfr["NP"][0]
    H_up, H_down = dfr["BC"][0], dfr["BC"][1]

    # x array = point locations in km and not in m
    x = np.linspace(0,L/1000,int(nb_cell))

    # vs x (reshape)
    b_t = np.load(path_data+'bathy_t.npy').reshape(np.shape(x))
    b_b = np.load(path_data+'background.npy').reshape(np.shape(x))
    b_1st = np.load(path_out_ref+'bathy_1st.npy').reshape(np.shape(x))
    Href = np.load(path_data+'Href.npy').reshape(np.shape(x))
    H_t = np.load(path_data+'H_t.npy').reshape(np.shape(x))
    b_star = np.load(path_out_ref+'bathy_star.npy').reshape(np.shape(x))
    H_star = np.load(path_out_ref+'H_star.npy').reshape(np.shape(x))
    # obs
    Hobs_full = np.load(path_data+'Hobs.npy').reshape(np.shape(x))
    ind_obs = np.load(path_data+'ind_obs.npy').reshape(np.shape(x))
    Hobs_sparse = Hobs_full * ind_obs
    obs_index = np.nonzero(Hobs_sparse) # non zero values only


    plt.figure()
    #plt.plot(x,Hobs_sparse,'c.',label=r"$H_{obs}$")
    plt.plot(x[obs_index],Hobs_sparse[obs_index],'c.',label=r"$H_{obs}$")
    plt.plot(x,b_b,'g--',label=r"$b_b$")
    plt.plot(x,b_t,'k',label=r"$b_t$")
    
    for path_out in l_path:
        b_1st = np.load(path_out+'bathy_1st.npy').reshape(np.shape(x))
        b_star = np.load(path_out+'bathy_star.npy').reshape(np.shape(x))
        H_star = np.load(path_out+'H_star.npy').reshape(np.shape(x))
        plt.plot(x,H_star,'c',label=r"$H_{*}$")
        plt.plot(x,b_1st,'r--',label=r"$b_{1st}$" + path_out)
        plt.plot(x,b_star,'b--',label=r"$b_{*}$" + path_out)


    plt.fill_between(x, np.min(b_t), b_t, facecolor='k', alpha=0.5)
    plt.xlabel(r"$x$ ($km$)"); plt.xlim(0,L/1000)
    plt.ylabel(r"$z$ ($m$)",rotation="horizontal") #; plt.ylim(np.min(b_t),H_up+1)
    plt.title('1st guess, true & final')
    plt.legend()

    plt.show()

l_path = []
for i in range(5):

    run_vda_bis("/home/n7student/Documents/assimilation_donnees_2/tp2/data/", path_out=f"./resultats{i+1}/", beta=0, paramb_1st=i+1, regul_term="b_b",  monitored=False, alphaset=0.00001)

    l_path.append(f"./resultats{i+1}/")

plot_test(l_path)


"""

si beta != 0 , beta représente le pourcentage d'importance de Jobs par rapport à Jreg
si beta = 0 : alpha reglé avec variable alpha, sinon si b !=0 sert à rien
si monitored = True c'est la dernière question sur la partie monitoré et super résultat pour alpha = 0.01 que j'ai fixé lorsque que monitored = True


Valeurs interessantes:

monitored = True pour partie 2

sinon : beta =0 et alphaset =0. 0001 ou alphaset =0.00001

sinon beta = ....

"""
