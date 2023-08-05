# -*-coding:Latin-1 -*
from Fkanban.Fkanban import *
from Fkanban.ui_Fkanban import *
from FUTIL.my_logging import *

deville = place("Deville") # not use!!!

montage = workshop("Montage")
peinture = workshop("Peinture")
soudure = workshop("Soudure")
plieuses = workshop("plieuses")
laser = workshop("laser")
presses = workshop("Presses")
ldc = workshop("Ligne de Coupe")
usinage = workshop("Usinage")
expeditions = workshop("Expeditions")


P0020205 = item("P0020205 - CALE DE GACHE", \
	[operation(laser, [], "LASER - P0020205",460,8,), \
        operation(peinture, [], "Peinture - P0020205", 1800, 5)], cost = 0.2)
P0020205_l= fab_kloop( name = "CALE DE GACHE P0020205", item = P0020205, \
                                batch = 256, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 128, red_zone = 1)

P0020086 = item("P0020086 - DESSOUS", \
	[operation(ldc, [], "LDC - P0020086", 316, 8), \
	operation(presses, [], "320t - P0020086", 200, 4)])
P0020086_l= fab_kloop( name = "DESSOUS P0020086", item = P0020086, \
				batch = 192, customer_shop = soudure, kanbans_nb = 6, kanbans_qty = 32, red_zone = 1)

P0020113 = item("P0020113 - PLAQUE ARRIERE", \
	[operation(ldc, [], "LDC - P0020113",250 , 8), \
	operation(presses, [], "320t - P0020113", 310, 4)])
P0020113_l= fab_kloop( name = "PLAQUE ARRIERE P0020113", item = P0020113, \
				batch = 96, customer_shop = montage, kanbans_nb = 3, kanbans_qty = 32, red_zone = 1)

P0020306 = item("P0020306 - CENDRIER", \
	[operation(ldc, [], "LDC - P0020306", 300, 8), \
	operation(presses, [], "320t - P0020306", 210, 4)])
P0020306_l= fab_kloop( name = "CENDRIER P0020306", item = P0020306, \
				batch = 96, customer_shop = montage, kanbans_nb = 3, kanbans_qty = 32, red_zone = 1)

P0029988 = item("P0029988 - RENVOI DE CENDRE", \
	[operation(laser, [], "LASER - P0029988",999,8), \
	operation(plieuses, [], "Pliage - P0029988",100,4)])
P0029988_l= fab_kloop( name = "RENVOI DE CENDRE P0029988", item = P0029988, \
				batch = 64, customer_shop = soudure, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)
				
P0037433 = item("P0037433 - MONTANT AVANT", \
	[operation(presses, [], "200T - P0037433",380,4)])
P0037433_l= fab_kloop( name = "MONTANT AVANT P0037433", item = P0037433, \
				batch = 192, customer_shop = soudure, kanbans_nb = 6, kanbans_qty = 32, red_zone = 1)
				
P0036682 = item("P0036682 - DEVANT DE CHASSIS", \
	[operation(laser, [], "LASER - P0036682",113,8), \
	operation(plieuses, [], "Pliage - P0036682",100,4)])
P0036682_l = fab_kloop( name = "DEVANT DE CHASSIS P0036682", item = P0036682, \
				batch = 64, customer_shop = soudure, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)

P0046093 = item("P0046093 - VOLET", \
	[operation(laser, [], "LASER - P0046093",350,8)])
P0046093_l= fab_kloop( name = "VOLET P0046093", item = P0046093, \
				batch = 96, customer_shop = soudure, kanbans_nb = 3, kanbans_qty = 32, red_zone = 1)

P0046111_P06S = item("P0046111_P06S - CHARNIERE NOIRE", \
        [operation(soudure, [nomenclature_link(P0046093,1)], "Soudure - P0046111_P06S",75,4), \
         operation(peinture, [], "Peinture - P0046111_P06S",800,5)])
P0046111_P06S_l= fab_kloop( name = "CHARNIERE NOIRE P0046111_P06S", item = P0046111_P06S, \
				batch = 96, customer_shop = montage, kanbans_nb = 3, kanbans_qty = 32, red_zone = 1)

P0050909 = item("P0050909 - EQUERRE", \
	[operation(laser, [], "LASER - P0050909",113,8), \
	operation(plieuses, [], "Pliage - P0050909",400,4)])
P0050909_l = fab_kloop( name = "EQUERRE P0050909", item = P0050909, \
				batch = 64, customer_shop = soudure, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)

P0050915 = item("P0050915 - SUPPORT VOLET", \
	[operation(laser, [], "LASER - P0050915",145,8), \
	operation(plieuses, [], "Pliage - P0050915",99,4), \
        operation(peinture, [], "Peinture - P0050915",500,5)]) 
P0050915_l = fab_kloop( name = "SUPPORT VOLET P0050915", item = P0050915, \
                                batch = 64, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)

P0051718_P06S = item("P0051718_P06S - DECOR", \
	[operation(laser, [], "LASER - P0051718_P06S",41,8), \
         operation(plieuses, [], "Pliage - P0051718_P06S",61,4), \
         operation(plieuses, [], "Pliage - P0051718_P06S",46,4), \
         operation(peinture, [], "Peinture - P0051718_P06S",30,5)]) 
P0051718_P06S_l = fab_kloop( name = "DECOR P0051718_P06S", item = P0051718_P06S, \
                                batch = 64, customer_shop = montage, kanbans_nb = 8, kanbans_qty = 8, red_zone = 4)

P0051434 = item("P0051434 - CHARNIERE", \
	[operation(laser, [], "LASER - P0051434",300,8), \
         operation(plieuses, [], "Pliage - P0051434",415,4)])
P0051434_l = fab_kloop( name = "CHARNIERE P0051434", item = P0051434, \
                                batch = 256, customer_shop = peinture, kanbans_nb = 4, kanbans_qty = 64, red_zone = 1)# erreur soudure => peinture

P0051434_P06S = item("P0051434_P06S - CHARNIERE NOIRE", \
        [operation(peinture, [nomenclature_link(P0051434,1)], "Peinture - P0051434_P06S",2500,4)])
P0051434_P06S_l= fab_kloop( name = "CHARNIERE NOIRE P0051434_P06S", item = P0051434_P06S, \
				batch = 128, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 64, red_zone = 1)

P0052288_P06S = item("P0052288_P06S - CHARNIERE NOIRE", \
        [operation(soudure, [nomenclature_link(P0051434,1)], "Soudure - P0052288_P06S",120,4), \
         operation(peinture, [], "Peinture - P0052288_P06S",2500,5)])
P0052288_P06S_l= fab_kloop( name = "CHARNIERE NOIRE P0052288_P06S", item = P0052288_P06S, \
				batch = 128, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 64, red_zone = 1)

P0052360 = item("P0052360 - SUPPORT CHASSIS", \
	[operation(laser, [], "LASER - P0052360",93,8), \
	operation(plieuses, [], "Pliage - P0052360",60,4), \
        operation(peinture, [], "Peinture - P0052360",37,5)]) 
P0052360_l = fab_kloop( name = "SUPPORT CHASSIS P0052360", item = P0052360, \
                                batch = 64, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)

P0053060 = item("P0053060 - DEFLECTEUR", \
	[operation(laser, [], "LASER - P0053060",165,8)])
P0053060_l = fab_kloop( name = "DEFLECTEUR P0053060", item = P0053060, \
                                batch = 96, customer_shop = presses, kanbans_nb = 3, kanbans_qty = 32, red_zone = 1)

P0053060_A = item("P0053060_A - DEFLECTEUR", \
	[operation(presses, [nomenclature_link(P0053060,1)], "200T - P0053060_A",125,8)])
P0053060_A_l = fab_kloop( name = "DEFLECTEUR P0053060_A", item = P0053060_A, \
                                batch = 96, customer_shop = plieuses, kanbans_nb = 3, kanbans_qty = 32, red_zone = 1)

P0053060_B = item("P0053060_B - DEFLECTEUR", \
	[operation(plieuses, [nomenclature_link(P0053060_A,1)], "pliage - P0053060_B",65,8)])
P0053060_B_l = fab_kloop( name = "DEFLECTEUR P0053060_B", item = P0053060_B, \
                                batch = 96, customer_shop = montage, kanbans_nb = 3, kanbans_qty = 32, red_zone = 1)

P0A53548 = item("P0A53548 - VIROLE A PLAT", \
	[operation(ldc, [], "LDC - P0A53548",260,8), \
	operation(presses, [], "320T - P0A53548",160,4), \
	operation(presses, [], "320T - P0A53548",160,4)])
P0A53548_l = fab_kloop( name = "VIROLE A PLAT P0A53548", item = P0A53548, \
				batch = 192, customer_shop = plieuses, kanbans_nb = 6, kanbans_qty = 32, red_zone = 2)
		
P0053548 = item("P0053548 - VIROLE", \
	[operation(plieuses, [nomenclature_link(P0A53548, 1)], "Pliage - P0053548", 30, 4)])
P0053548_l= fab_kloop( name = "VIROLE P0053548", item = P0053548, \
				batch = 64, customer_shop = soudure, kanbans_nb = 4, kanbans_qty = 16, red_zone = 1)
				
P0T53071_P06S = item("P0T53071 - BUSE", \
		[operation(usinage, [], "USINAGE - P0T53071",160,4), \
		operation(peinture, [], "Peinture - P0T53071",220,5)])
P0T53071_P06S_l = fab_kloop( name = "BUSE P0T53071", item = P0T53071_P06S, \
				batch = 64, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)

P0T16569 = item("P0T16569 - VERROU", \
		[operation(usinage, [], "USINAGE - P0T16569",125,4), \
		operation(peinture, [], "Peinture - P0T16569",1450,5)])
P0T16569_l = fab_kloop( name = "VERROU P0T16569", item = P0T16569, \
				batch = 64, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)

P0U50878 = item("P0U50878 - PLAQUE ARRIERE", \
		[operation(usinage, [], "USINAGE - P0U50878",23,4)])
P0U50878_l = fab_kloop( name = "PLAQUE ARRIERE P0U50878", item = P0U50878, \
				batch = 32, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 32, red_zone = 1)

P0T52232_P06S = item("P0T52232_P06S - DESSUS NOIR", \
		[operation(usinage, [], "USINAGE - P0T52232_P06S",34,4), \
                 operation(peinture, [], "Peinture - P0T52232_P06S",60,5)])
P0T52232_P06S_l = fab_kloop( name = "DESSUS NOIR P0T52232_P06S", item = P0T52232_P06S, \
				batch = 32, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 32, red_zone = 2)

P0T51457_P06S = item("P0T51457_P06S - PORTE NOIR", \
		[operation(usinage, [], "USINAGE - P0T51457_P06S",24,4), \
                 operation(usinage, [], "USINAGE - P0T51457_P06S",71,4), \
                 operation(peinture, [], "Peinture - P0T51457_P06S",63,5)])
P0T51457_P06S_l = fab_kloop( name = "PORTE NOIRE P0T51457_P06S", item = P0T51457_P06S, \
				batch = 32, customer_shop = montage, kanbans_nb = 2, kanbans_qty = 32, red_zone = 2)
				
P0731109 = item("P0731109 - VIS")

P0T11271_P06S = item("P0T11271_P06S - TAMPON NOIR", \
		[operation(peinture, [], "Peinture P0T11271_P06S",250,5)])
P0T11271_P06S_l= fab_kloop( name = "TAMPON NOIR P0T11271_P06S", item = P0T11271_P06S, \
				batch = 32, customer_shop = montage, kanbans_nb = 1, kanbans_qty = 32, red_zone = 1)

P0T20048 = item("P0T20048 - GACHE", \
		[operation(peinture, [], "Peinture P0T20048",1800,5)])
P0T20048_l= fab_kloop( name = "GACHE P0T20048", item = P0T20048, \
				batch = 32, customer_shop = montage, kanbans_nb = 1, kanbans_qty = 32, red_zone = 1)

P0T50897 = item("P0T50897 - FACADE", \
		[operation(peinture, [], "Peinture P0T50897",74,5)])
P0T50897_l= fab_kloop( name = "FACADE P0T50897", item = P0T50897, \
				batch = 32, customer_shop = montage, kanbans_nb = 1, kanbans_qty = 32, red_zone = 1)

P0050910_P06S = item("P0050910_P06S - GUIDE D'AIR NOIR", \
		[operation(peinture, [], "Peinture P0050910_P06S",300,5)])
P0050910_P06S_l= fab_kloop( name = "GUIDE D'AIR NOIR P0050910_P06S", item = P0050910_P06S, \
				batch = 32, customer_shop = montage, kanbans_nb = 1, kanbans_qty = 32, red_zone = 1)
		
P0053547 = item("P0053547 - ENS. CHASSIS", \
	[operation(soudure, \
                        [nomenclature_link(P0020086,1), \
                         nomenclature_link(P0029988,1), \
                         nomenclature_link(P0037433,1), \
                         nomenclature_link(P0036682,1), \
                         nomenclature_link(P0053548,1), \
                         nomenclature_link(P0050909,1), \
                         nomenclature_link(P0731109,1,False)], \
			"Soudure P0053547",7,4), \
	operation(peinture, \
			[], "Peinture P0053547",37,5)])
P0053547_l = fab_kloop( name = "ENS. CHASSIS P0053547", item = P0053547, \
				batch = 32, customer_shop = montage, kanbans_nb = 4, kanbans_qty = 8, red_zone = 1)

c077aa = item("C077AA - POELE A BOIS Saphir", \
	[operation(montage, \
			[nomenclature_link(P0053547,1), \
                         nomenclature_link(P0T53071_P06S,1), \
                         nomenclature_link(P0T52232_P06S,1), \
                         nomenclature_link(P0T11271_P06S,1), \
                         nomenclature_link(P0052360,1), \
                         nomenclature_link(P0020205,4), \
                         nomenclature_link(P0051718_P06S,1), \
                         nomenclature_link(P0T51457_P06S,1), \
                         nomenclature_link(P0050910_P06S,1), \
                         nomenclature_link(P0051434_P06S,1), \
                         nomenclature_link(P0052288_P06S,1), \
                         nomenclature_link(P0T20048,1), \
                         nomenclature_link(P0T50897,1), \
                         nomenclature_link(P0T16569,1), \
                         nomenclature_link(P0U50878,1), \
                         nomenclature_link(P0020113,1), \
                         nomenclature_link(P0053060_B,1), \
                         nomenclature_link(P0020306,1), \
                         nomenclature_link(P0046111_P06S,1), \
                         nomenclature_link(P0050915,1)], \
                   "Montage C077AA",4,0)])
	
c077aa_l = fab_kloop(name = "POELE A BOIS Saphir C077AA", item = c077aa, \
			batch = 32, customer_shop = expeditions, kanbans_nb = 5, kanbans_qty = 32, red_zone = 1)

sortie = item("Expeditions", [operation(expeditions, [nomenclature_link(c077aa,1)],"Consos:")])
sortie_l = customer_kloop(name = "Conso Client", item = sortie, workshop = expeditions, period = 8, qty = 9, qty_alea_range = 1, period_alea_rate = 1)
		

mes_ateliers = [montage, peinture, soudure, plieuses, laser, presses, ldc, usinage] #inutil!!!

logging.debug("Creation of loops ...")

mes_boucles = [sortie_l, \
				c077aa_l, \
				P0053547_l, P0053548_l, P0A53548_l, P0029988_l, P0050909_l, P0036682_l, P0037433_l, P0020086_l, \
                                P0052360_l, P0050915_l, P0020205_l, \
                                P0051718_P06S_l, \
                                P0046093_l, P0046111_P06S_l, \
                                P0051434_l, P0051434_P06S_l, \
				P0052288_P06S_l, \
				P0T11271_P06S_l, P0050910_P06S_l, P0T20048_l, P0T50897_l, \
                                P0T51457_P06S_l, P0T52232_P06S_l, P0T53071_P06S_l, P0T16569_l, \
                                P0020113_l, P0020306_l, \
                                P0U50878_l, \
				P0053060_l, P0053060_A_l, P0053060_B_l]


app = ui_Fkanban(mes_ateliers, mes_boucles, speed = 5)
				
