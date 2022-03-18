def returnMarkers(card, cardTraitsDict):
	reusableAbilityTokens = [BloodReaper,
							 EternalServant,
							 HolyAvenger,
							 Pet]
				#reusableGeneralTokens = [Light]
	mage = Card(cardTraitsDict.get('MageID'))
	for t in reusableAbilityTokens:
			if card.markers[t]: mage.markers[t] = 1 #Return mage ability markers to their owner.
	
	if card.markers[WoundedPrey]:
			mages = [m for m in table if m.Name == "Johktari Beastmaster" and not m.markers[WoundedPrey]] #WARNING: This may identify the wrong JBM if there are more than 1 in the match. Unfortunately, markers cannot be associated with players, so it is difficult to correctly reassign the marker (not impossible, just not worth the effort)
			if mages:
					mage = mages[0]
					mage.markers[WoundedPrey] = 1
	if card.markers[DivineChallenge]:
			mages = [m for m in table if m.Name == "Paladin" and not m.markers[DivineChallenge]] #
			if mages:
					mage = mages[0]
					mage.markers[DivineChallenge] = 1
	if card.markers[SirensCall]:
			mages = [m for m in table if m.Name == "Siren" and not m.markers[SirensCall]] #
			if mages:
					mage = mages[0]
					mage.markers[SirensCall] = 1
	if card.markers[Light]:
			for card in table:
				if card.Name == "Malakai\'s Basilica" and not card.markers[Light]:
					card.markers[Light] = 1
	if card.markers[scoutToken]:
			for card in table:
				if card.Name == "Straywood Scout" and not card.markers[scoutToken]:
					card.markers[scoutToken] = 1
	return