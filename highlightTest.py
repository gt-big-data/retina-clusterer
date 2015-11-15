myStr = unicode('Speaking from the Elysee presidential palace the morning after France saw its worst day of violence since World War II, Hollande said the attacks were "an act of war" committed by the Islamic State group\'s "terrorist army". The French president said the atrocities were, "against France, against the values that we defend everywhere in the world, against what we are: A free country that means something to the whole planet." The Islamic State (IS) jihadist group claimed responsibility on Saturday for the series of apparently coordinated attacks in and around Paris. Hollande went on to say that France would "triumph over the barbarism" of the IS militant group and "will act by all means anywhere, inside or outside the country". Hollande declared three days of national mourning in the wake of the attacks. The Socialist president announced a state of emergency on Friday night as France reinstituted border checks.')
# Speaking from the Elysee presidential palace the morning after France saw its worst day of violence since World War II, Hollande said the attacks were "an act of war" committed by the Islamic State group\'s "terrorist army".
# The French president said the atrocities were, "against France, against the values that we defend everywhere in the world, against what we are: A free country that means something to the whole planet." The Islamic State (IS) jihadist group claimed responsibility on Saturday for the series of apparently coordinated attacks in and around Paris.
# Hollande went on to say that France would "triumph over the barbarism" of the IS militant group and "will act by all means anywhere, inside or outside the country".
# Hollande declared three days of national mourning in the wake of the attacks.
# The Socialist president announced a state of emergency on Friday night as France reinstituted border checks.

doc = nlp(myStr)

sentences = doc.sents

for s in sentences:
	verb = s.root
	subj = list(verb.lefts)[-1]
	compl = list(verb.rights)[0]
	print subj, " ", verb, " ", compl
	print "------------"