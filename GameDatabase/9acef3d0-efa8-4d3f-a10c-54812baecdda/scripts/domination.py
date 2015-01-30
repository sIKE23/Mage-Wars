############################################################################
##########################				v2.10.0.0				#################################
############################################################################

def createOrbGuardian(group, x=0, y=0):
	orbGuardian = table.create("bf217fd3-18c0-4b61-a33a-117167533f3d", 450, -40 )
	orbGuardian.markers[Guard] = 1

def createGOrbGuardian(group, x=0, y=0):
	orbGuardian = table.create("54e67290-5e6a-4d8a-8bf0-bbb8fddf7ddd", 450, -40 )
	orbGuardian.markers[Guard] = 1

def createPowerOrb(group, x=0, y=0):
	table.create("690a2c72-4801-47b5-84bd-b9e2f5811cb5", -75, -75 )

def setupDom(group, x=0, y=0):
	table.create("690a2c72-4801-47b5-84bd-b9e2f5811cb5", -286, -300 )
	table.create("690a2c72-4801-47b5-84bd-b9e2f5811cb5",  225, -300 )
	table.create("690a2c72-4801-47b5-84bd-b9e2f5811cb5",  -62,  -40 )
	table.create("690a2c72-4801-47b5-84bd-b9e2f5811cb5",    1,  -40 )
	table.create("690a2c72-4801-47b5-84bd-b9e2f5811cb5", -286,  220 )
	table.create("690a2c72-4801-47b5-84bd-b9e2f5811cb5",  225,  220 )

	orbGuardian = table.create("bf217fd3-18c0-4b61-a33a-117167533f3d", -286, -192 )
	orbGuardian.markers[Guard] = 1

	orbGuardian = table.create("bf217fd3-18c0-4b61-a33a-117167533f3d",  225, -192 )
	orbGuardian.markers[Guard] = 1

	orbGuardian = table.create("54e67290-5e6a-4d8a-8bf0-bbb8fddf7ddd", -128,  -40 )
	orbGuardian.markers[Guard] = 1

	orbGuardian = table.create("54e67290-5e6a-4d8a-8bf0-bbb8fddf7ddd",   64,  -40 )
	orbGuardian.markers[Guard] = 1

	orbGuardian = table.create("bf217fd3-18c0-4b61-a33a-117167533f3d", -286,  109 )
	orbGuardian.markers[Guard] = 1

	orbGuardian = table.create("bf217fd3-18c0-4b61-a33a-117167533f3d", 225,  109 )
	orbGuardian.markers[Guard] = 1

	setGameBoard0(group, 0, 0)

