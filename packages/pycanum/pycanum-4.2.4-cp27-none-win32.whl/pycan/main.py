#coding = utf-8
# -*- coding: utf-8 -*-
import pycan.pysysam as sysam
import numpy
import math


SYSAM_SP5 = 1
SYSAM_PCI = 2
ENTREE_CHRONO = 16

class Sysam:
    def __init__(self,nom):
        self.ouvert = False
        self.sysamid = 0
        if (nom=="SP5"):
            self.sysamid = SYSAM_SP5;
        if (nom=="PCI"):
            self.sysamid = SYSAM_PCI;
        self.ouvrir()
    def ouvrir(self):
        if self.ouvert:
            print("CAN Sysam ouvert")
            return
        if (self.sysamid==0):
            print("CAN Sysam non connu")
            return
        sysam.can_ouvrir(self.sysamid)
        self.ouvert = True
    def fermer(self):
        sysam.can_fermer()
        self.ouvert = False
    def reset(self):
        sysam.can_reset()
    def config_entrees(self,voies,calibres,diff=[]):
       sysam.can_config_entrees(voies,calibres,diff)
    def config_echantillon(self,techant,nbpoints):
        sysam.can_config_echantillon(techant,nbpoints)
    def config_echantillon_permanent(self,techant,nbpoints):
        sysam.can_config_echantillon_permanent(techant,nbpoints)
    def config_trigger(self,voie,seuil,montant=1,pretrigger=1,pretriggerSouple=0,hysteresis=0):
        sysam.can_config_trigger(0,voie,seuil,montant,pretrigger,pretriggerSouple,hysteresis)
    def config_trigger_externe(self,pretrigger=1,pretriggerSouple=0):
        sysam.can_config_trigger(1,0,0,1,pretrigger,pretriggerSouple,0)
    def acquerir(self):
        sysam.can_acquerir()
    def acquerir_permanent(self):
        sysam.can_acquerir_permanent()
    def lancer(self):
        sysam.can_lancer()  
    def lancer_permanent(self,repetition=0):
        sysam.can_lancer_permanent(repetition)
    def stopper_acquisition(self):
        sysam.can_stopper_acquisition()
    def temps(self,reduction=1):
        return sysam.can_temps(reduction)
    def entrees(self,reduction=1):
        return sysam.can_entrees(reduction)
    def entrees_filtrees(self,reduction=1):
        return sysam.can_entrees_filtrees(reduction)
    def nombre_echant(self):
        return sysam.can_nombre_echant()
    def paquet(self,premier,reduction=1):
        if premier >=0:
            return sysam.can_paquet(premier,reduction)
        else:
            return sysam.can_paquet_circulaire(reduction)
    def paquet_filtrees(self,premier,reduction=1):
        if premier >= 0:
            return sysam.can_paquet_filtrees(premier,reduction)
        else:
            return sysam.can_paquet_circulaire_filtrees(reduction)
    def config_sortie(self,nsortie,techant,valeurs,repetition=0):
        sysam.can_config_sortie(nsortie,techant,valeurs,repetition)
    def declencher_sorties(self,ns1,ns2):
        sysam.can_declencher_sorties(ns1,ns2)
    def stopper_sorties(self,ns1,ns2):
        sysam.can_stopper_sorties(ns1,ns2)
    def acquerir_avec_sorties(self,valeurs1,valeurs2):
        if type(valeurs1)!=numpy.ndarray:
            valeurs1 = numpy.zeros(0)
        if type(valeurs2)!=numpy.ndarray:
            valeurs2 = numpy.zeros(0)
        sysam.can_acquerir_avec_sorties(valeurs1,valeurs2)
    def lancer_avec_sorties(self,valeurs1,valeurs2):
        if type(valeurs1)!=numpy.ndarray:
            valeurs1 = numpy.zeros(0)
        if type(valeurs2)!=numpy.ndarray:
            valeurs2 = numpy.zeros(0)
        sysam.can_lancer_avec_sorties(valeurs1,valeurs2)
    def ecrire(self,ns1,valeur1,ns2,valeur2):
        sysam.can_ecrire(ns1,valeur1,ns2,valeur2)
    def activer_lecture(self,voies):
        sysam.can_activer_lecture(voies,0)
    def desactiver_lecture(self):
        sysam.can_desactiver_lecture()
    def lire(self):
        return sysam.can_lire()
    def portC_config(self,bit,etat):
        sysam.can_portC_config(bit,etat)
    def portC_ecrire(self,bit,etat):
        sysam.can_portC_ecrire(bit,etat)
    def portC_lire(self,bit):
        return sysam.can_portC_lire(bit)
    def portB_config(self,bit,etat):
        sysam.can_portB_config(bit,etat)
    def portB_ecrire(self,bit,etat):
        sysam.can_portB_ecrire(bit,etat)
    def portB_lire(self,bit):
        return sysam.can_portB_lire(bit)        
    def config_filtre(self,listeA,listeB):
        sysam.can_config_filtre(numpy.array(listeA,dtype=numpy.double),numpy.array(listeB,dtype=numpy.double))
    def config_compteur(self,entree,front_montant,front_descend,hysteresis,duree):
        sysam.can_config_compteur(entree,front_montant,front_descend,hysteresis,duree)
    def compteur(self):
        sysam.can_compteur()
    def lire_compteur(self):
        n = sysam.can_lire_compteur()
        return numpy.uint64(numpy.left_shift(n[0],32)+n[1])
    def config_chrono(self,entree,front_debut,front_fin,hysteresis):
        sysam.can_config_chrono(entree,front_debut,front_fin,hysteresis)
    def chrono(self):
        sysam.can_chrono()
    def lire_chrono(self):
        n = sysam.can_lire_chrono()
        return numpy.uint64(2**32)*numpy.uint64(n[0])+numpy.uint64(n[1])
    def afficher_calibrage(self):
        sysam.can_afficher_calibrage()
        
def audio_table_start(ch1,ch2,f1,f2,fs=44000,fpb=256):
    ch1 = numpy.array(ch1,dtype=numpy.float32)
    ch2 = numpy.array(ch2,dtype=numpy.float32)
    sysam.table_dds_start(fs,fpb,ch1,ch2,f1,f2)
    
def audio_table_stop(seconds):
    sysam.table_dds_stop(seconds)

def harmonics_table(amp_list,phase_list,normalize,gain):
    TABLE_SIZE = 256
    amp = numpy.array(amp_list,dtype=numpy.float32)
    phase = numpy.array(phase_list,dtype=numpy.float32)
    if amp.size != phase.size:
        raise SystemExit("amplitude et phase : tailles incompatibles")
    t = numpy.arange(TABLE_SIZE)*1.0/TABLE_SIZE
    table = numpy.zeros(TABLE_SIZE,dtype=numpy.float32)
    for n in range(amp.size):
        table = table+amp[n]*numpy.sin(2*numpy.pi*(n+1)*t+phase[n])
    table = numpy.array(table,dtype=numpy.float32)
    m = abs(table.min())
    M = abs(table.max())
    if normalize:
        table = table/max(m,M)
    return table*gain
    

def audio_harmonics_start(a1,p1,a2,p2,f1,f2,norm=True,gain=1.0,fs=44000,fpb=256):
    table_1 = harmonics_table(a1,p1,norm,gain)
    table_2 = harmonics_table(a2,p2,norm,gain)
    sysam.table_dds_start(fs,fpb,table_1,table_2,f1,f2)
    return(table_1,table_2)
       
def audio_harmonics_stop(seconds):
    sysam.table_dds_stop(seconds)

        