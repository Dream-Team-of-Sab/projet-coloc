#importer les modules correspondant

#importer la base de données à l'aide de la def de classe

#définition de deux variables correspondant au total des factures égalitaires et au total des factures pro-rata

eq_tot = sum (SELECT price FROM facture WHERE type=FALSE)
rata_tot = sum (SELECT price FROM facture WHERE type=TRUE)

#calcul de la variable correspondant au pro-rata de chaque user
rata_user = rata_tot / nombre de repas_user 

#calcul de ce que doit payer chaque user 
# total des factures égalitaires divisé par le nombre de user 
# + total des factures pro-rata fois le pro-rata de l'user, le tout divisé par le nombre de user
# - factures déjà payées par l'user (multipliées ou non par le pro-rata correspondant)
user_payment = ((eq_tot / len TABLE users) + ((rata_tot * rata_user) / len TABLE users)) - (
