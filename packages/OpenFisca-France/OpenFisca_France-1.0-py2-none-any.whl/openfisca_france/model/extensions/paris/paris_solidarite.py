# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where)

from openfisca_france.model.base import *  # noqa analysis:ignore

# Paris solidarité pour les personnes agées et les personnes handicapées

class paris_logement_psol(Variable):
    column = FloatCol
    label = u"Montant de l'aide Paris Solidarité"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month

        parisien = simulation.calculate('parisien', period)
        personnes_agees = simulation.compute('paris_personnes_agees', period)
        personnes_agees_famille = self.any_by_roles(personnes_agees)
        personne_handicap_individu = simulation.compute('paris_personnes_handicap', period)
        personne_handicap = self.sum_by_entity(personne_handicap_individu)
        enfant_handicape = simulation.calculate('paris_enfant_handicape', period)
        nb_enfant = self.sum_by_entity(enfant_handicape)
        montant_aide = simulation.calculate('paris_logement_psol_montant', period)

        adulte_handicape = (personne_handicap - nb_enfant) >= 1

        result = parisien * (personnes_agees_famille + adulte_handicape) * montant_aide

        return period, result

class paris_logement_psol_montant(Variable):
    column = FloatCol
    label = u"Montant de l'aide PSOL"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        last_month = period.last_month

        montant_seul_annuel = simulation.legislation_at(period.start).minim.aspa.montant_seul
        montant_couple_annuel = simulation.legislation_at(period.start).minim.aspa.montant_couple
        plafond_seul_psol = simulation.legislation_at(period.start).paris.paris_solidarite.plafond_seul_psol
        plafond_couple_psol = simulation.legislation_at(period.start).paris.paris_solidarite.plafond_couple_psol

        montant_seul = montant_seul_annuel / 12
        montant_couple = montant_couple_annuel / 12
        personnes_couple = simulation.calculate('concub', period)
        paris_base_ressources_commun = simulation.calculate('paris_base_ressources_commun', last_month)
        aspa = simulation.calculate('aspa', last_month)
        asi = simulation.calculate('asi', last_month)
        aah = simulation.calculate('paris_base_ressources_aah', last_month)

        ressources_mensuelles = paris_base_ressources_commun + asi + aspa + aah

        plafond_psol = select([personnes_couple, (personnes_couple != 1)], [plafond_couple_psol, plafond_seul_psol])

        plancher_ressources = where(personnes_couple, montant_couple, montant_seul)
        ressources_mensuelles_min = where(ressources_mensuelles < plancher_ressources, plancher_ressources,
            ressources_mensuelles)

        result = select([((personnes_couple != 1) * (ressources_mensuelles_min <= plafond_psol)),
            personnes_couple * (ressources_mensuelles_min <= plafond_psol),
            ((personnes_couple != 1) + personnes_couple) * (ressources_mensuelles_min > plafond_psol)],
            [(plafond_seul_psol - ressources_mensuelles_min), (plafond_couple_psol - ressources_mensuelles_min), 0])

        return period, result
