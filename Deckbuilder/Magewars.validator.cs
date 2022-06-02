//Version: 2.2.2.0

namespace Octgn.MageWarsValidator
{
    using Octgn.Core.DataExtensionMethods;
    using Octgn.Core.DataManagers;
    using Octgn.Core.Plugin;
    using Octgn.DataNew.Entities;
    using Octgn.Library;
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;
    using System.Linq;
    using System.Reflection;
    using System.Runtime.InteropServices;
    using System.Text;
    using System.Windows.Forms;



    /*********************************************
     * 
     * 
     *          Main object thing
     *                
     * 
     ********************************************/
    public class MageWarsValidator : IDeckBuilderPlugin
    {
        public IEnumerable<IPluginMenuItem> MenuItems
        {
            get
            {
                // Add your menu items here.
                return new List<IPluginMenuItem> 
                { 
                    new ValidatorMenuItem(), 
                };
            }
        }

        public void OnLoad(GameManager games)
        {
            // I'm showing a message box, but don't do this, unless it's for updates or something...but don't do it every time as it pisses people off.
            //MessageBox.Show("Hello!");
        }

        public Guid Id
        {
            get
            {
                // All plugins are required to have a unique GUID
                // http://www.guidgenerator.com/online-guid-generator.aspx
                return Guid.Parse("a2f6a426-6256-4634-b386-e6267fd23f9e");
            }
        }

        public string Name
        {
            get
            {
                // Display name of the plugin.
                 return "Mage Wars Spellbook Builder Plugin";
            }
        }

        public Version Version
        {
            get
            {
                // Version of the plugin.
                // This code will pull the version from the assembly.
                return Assembly.GetCallingAssembly().GetName().Version;
            }
        }

        public Version RequiredByOctgnVersion
        {
            get
            {
                // Don't allow this plugin to be used in any version less than 3.0.12.58
                return Version.Parse("3.1.0.0");
            }
        }
    }


    /*********************************************
     * 
     * 
     *                Validator
     *                
     * 
     ********************************************/
    public class ValidatorMenuItem : IPluginMenuItem
    {

        public static bool deckValidated = false;
        public static int bookPoints = 0;
        public static int totalCards = 0;
        public static int validatedDeckHash = 0;

        public string Name
        {
            get
            {
                return "Validate Mage Wars Spellbook"; }
        }

        /// <summary>
        /// This happens when the menu item is clicked.
        /// </summary>
        /// <param name="con"></param>
        public void OnClick(IDeckBuilderPluginController con)
        {
            if (con.GetLoadedGame() == null || con.GetLoadedGame().Id.ToString() != "9acef3d0-efa8-4d3f-a10c-54812baecdda")
            {
                MessageBox.Show("You must have Mage Wars loaded to use this feature.");
                return;
            }

            var loadedDeck = con.GetLoadedDeck();
            //System.Windows.MessageBox.Show(loadedDeck.GetType().Name);
            if (loadedDeck == null)
            {
                MessageBox.Show("You must have a Mage Wars deck loaded to use this feature.");
                return;
            }

            deckValidated = false;

            var secArray = loadedDeck.Sections.ToArray(); // Is this needed?
            int cardcount = 0;
            int spellbook = 0;
            string magename = "none in deck"; // won't be needed after rework
            int spellpoints = 0;
            string reporttxt = "";
            bool Talos = false;
            int hashtotal = 0;
            
            //won't be needed after rework
            List<string> subtypeTrain = new List<string>();
            List<string> comboTrain = new List<string>();
            List<string> levelXTrain = new List<string>();
            

            Dictionary<string, int> training = new Dictionary<string, int>() // won't be needed after rework
                {
                    {"Dark", 2},{"Holy",2},{"Nature",2},{"Mind",2},{"Arcane",2},{"War",2},{"Earth",2},{"Water",2},{"Air",2},{"Fire",2},{"Creature",0}
                };
            
            Dictionary<string, int> levels = new Dictionary<string, int>() // won't be needed after rework
                {
                    {"Dark", 0},{"Holy",0},{"Nature",0},{"Mind",0},{"Arcane",0},{"War",0},{"Earth",0},{"Water",0},{"Air",0},{"Fire",0},{"Creature",0}
                };

            IMultiCard mageStatCard = getMageStatCard(loadedDeck);  //Will need to handle what to do with Null at some point
                   
            if (mageStatCard == null)
            {
                System.Windows.MessageBox.Show("Validation result:\nNo mage stat card is detected in the book");
            }
            else
            {
                reporttxt += string.Format("{1}\n", mageStatCard.Quantity.ToString(), mageStatCard.Name); 
            }
            
            spellpoints = countSpellPointTotal(loadedDeck, mageStatCard);
            
            
            
            
            
            foreach (var section in secArray)
            {
                foreach (var card in section.Cards)
                {
                    char[] delimSubtypeChars = {',', ' '};
                    char[] delimSchoolChars = {'+', '/'};
                    string[] cardSubtypes = Array.ConvertAll(Property(card, "Subtype").Split(delimSubtypeChars, StringSplitOptions.RemoveEmptyEntries), p => p.Trim());
                    string[] cardSchools = Array.ConvertAll(Property(card, "School").Split(delimSchoolChars, StringSplitOptions.RemoveEmptyEntries), p => p.Trim());
                    string[] cardLevels = Array.ConvertAll(Property(card, "Level").Split(delimSchoolChars, StringSplitOptions.RemoveEmptyEntries), p => p.Trim());
                    bool subtypeFlag = false;
                    bool comboTrainFlag = false;
                    bool levelXFlag = false;
                    hashtotal += card.GetHashCode() + card.Quantity;
                    string Cname = Property(card, "Name");
                    

                    if (Property(card, "Subtype").Contains("Mage") && Property(card, "Type").Contains("Creature") && magename == "none in deck")
                    {
                        magename = Property(card, "Nickname");
                    }

                    if (HasProperty(card, "Traits"))
                    {
                        if (Property(card, "Traits").Contains("Novice")) //Novice spells always cost 1 point
                        {
                            cardcount += card.Quantity;
                            spellbook += card.Quantity;
                            var typestr = Property(card, "Type");
                            if (typestr.Equals("Conjuration-Wall")) typestr = "Conjuration";
                            if (!reporttxt.Contains(typestr)) // has this type been listed before??
                            {
                                reporttxt += string.Format("\n---  {0} ---\n", typestr);
                            }
                            reporttxt += string.Format("{0} - {1} - 1 - 1 - {0}\n", card.Quantity.ToString(), card.Name);
                            continue;
                        }
                    }

                    if (card.Name.Contains("Talos"))
                        Talos = true;
                    else
                        Talos = false;

                    if (HasProperty(card, "School") & HasProperty(card, "Level"))
                    {
                        bool isEmptyLevelX = isEmpty(levelXTrain);
                        var school = Property(card, "School");
                        var level = Property(card, "Level");
                        var typestr = Property(card, "Type");
                        if (typestr.Equals("Conjuration-Wall")) typestr = "Conjuration";
                        if (typestr.Equals("Conjuration-Terrain")) typestr = "Conjuration";
                        if (!reporttxt.Contains(typestr)) // has this type been listed before??
                        {
                            reporttxt += string.Format("\n---  {0}  ---\n", typestr);
                        }
                        reporttxt += string.Format("{0} - {1} - ", card.Quantity.ToString(), card.Name);

                        //Calculate card's spell level
                        int totalLevel = 0;
                        string deli = level.Contains("+") ? "+" : level.Contains("/") ? "/" : "";
                        if (deli == "/")
                        {
                            string lev = level.Substring(0, 1);
                            totalLevel = Convert.ToInt32(lev);
                        }
                        else if (deli == "+")
                        {
                            string[] levs = level.Split('+');
                            string[] schs = school.Split('+');
                            for (int i = 0; i < levs.Length; ++i)
                                totalLevel += Convert.ToInt32(levs[i]);
                        }
                        else
                        {
                            totalLevel = Convert.ToInt32(level);
                        }

                        //calculate spell cost in book
                        int cost = 0;
                        if (!Talos)
                        {
                            bool isEmptySub = isEmpty(subtypeTrain);
                            bool isEmptyCombo = isEmpty(comboTrain);
                            if (!isEmptySub)
                            {
                                foreach(string sType in subtypeTrain)
                                {
                                    foreach(string cSType in cardSubtypes)
                                    {
                                        if (sType == cSType)
                                        {
                                            subtypeFlag = true;
                                        }
                                    }
                                    
                                }
                                
                            }

                            if(!isEmptyCombo)
                            {
                                //I'm cheating on this part since Paladin's the only combo trained mage (Holy + Creature) that will exist in 1.0 as of 7/7/2020
                                //I'm going to just move on to the next edition project. I can fix if ever needed in the future
                                foreach(string cSchool in cardSchools)
                                {
                                    if (cSchool.Contains("Holy") & Property(card, "Type").Contains("Creature"))
                                    {
                                        comboTrainFlag = true;
                                    }
                                }
 
                            }

                            if(!isEmptyLevelX)
                            {
                                foreach(string cSchool in cardSchools)
                                {
                                    if (levelXTrain.Contains(cSchool))
                                    {
                                        int Lx_ind = levelXTrain.IndexOf(cSchool);
                                        int trainLevel = Convert.ToInt32(levelXTrain[Lx_ind-1]);
                                        int c_ind = Array.IndexOf(cardSchools, cSchool);
                                        int cLevel = Convert.ToInt32(cardLevels[c_ind]);
                                        if (cLevel <= trainLevel)
                                        {
                                            levelXFlag = true;
                                        }
                                    }
                                }
                            }

                            if (subtypeFlag)
                            {
                                cost = totalLevel;
                                //This is only built to handle if someone is trained in subtypes (vs Opposed training) since that's all that exists for MW 1. 
                                //It wouldn't be hard to adjust for opposed training, but probably isn't worth the effort at the moment
                            }
                            else if (comboTrainFlag)
                            {
                                cost = totalLevel;
                                //This is only built to handle if someone is combo trained (vs combo Opposed training) since that's all that exists for MW 1. 
                                //It wouldn't be hard to adjust for opposed training, but probably isn't worth the effort at the moment
                            }
                            else if (levelXFlag)
                            {
                                //If the levelxflag is triggered and / in the cost, split the level and schools and just do cost = totalLevel
                                if (school.Contains('/'))
                                {
                                    cost = totalLevel;
                                }
                                else
                                {
                                    foreach(string cSchool in cardSchools)
                                    {
                                        int curInd = Array.IndexOf(cardSchools, cSchool);
                                        int curLevel = Convert.ToInt32(cardLevels[curInd]);
                                        if (levelXTrain.Contains(cSchool))
                                        {
                                            int Lx_ind = levelXTrain.IndexOf(cSchool);
                                            int trainLevel = Convert.ToInt32(levelXTrain[Lx_ind-1]);
                                            if (curLevel<=trainLevel)
                                            {
                                                cost += curLevel;
                                            }
                                            else
                                            {
                                                cost += training[cSchool]*curLevel;
                                            }
                                        }
                                        else
                                        {
                                            cost += training[cSchool]*curLevel;
                                        }
                                    }
                                }
                            }
                            else if ((magename.Contains("Forcemaster") & "Creature" == Property(card, "Type")) | (magename.Contains("Monk") & "Creature" == Property(card, "Type")))
                            {
                                if (!school.Contains("Mind")) //"Mind" not in schools
                                {
                                    if (school.Contains("+"))
                                    {
                                        foreach (var lev in Splitme(level, "+"))
                                        {
                                            cost += Convert.ToInt32(lev)*3;
                                        }

                                    }
                                    else //handle single school or "/" school cards
                                    {
                                        var lev = Splitme(level, "/");
                                        cost += Convert.ToInt32(lev[0])*3;
                                    }
                                }
                                else
                                {
                                    if (school.Contains("+"))
                                    {
                                        foreach (var lev in Splitme(level, "+"))
                                        {
                                            cost += Convert.ToInt32(lev);
                                        }

                                    }
                                    else //handle single school or "/" school cards
                                    {
                                        var lev = Splitme(level, "/");
                                        cost += Convert.ToInt32(lev[0]);
                                    }
                                }
                            }
                            else if (school.Contains("+")) //add all spell levels
                            {
                                var lev = Splitme(level, "+");
                                int x = 0;
                                foreach (var s in Splitme(school, "+"))
                                {
                                    cost += Convert.ToInt32(lev[x]) * training[s];
                                    levels[s] += Convert.ToInt32(lev[x]) * card.Quantity;
                                    x++;
                                }
                            }
                            else if (school.Contains("/")) //add just the cheapest of these
                            {
                                if (magename == "none in deck") //no mage found yet
                                {
                                    System.Windows.MessageBox.Show("Warning - No mage card has been found yet. This may lead to inaccurate calculations. Ensure that the first card in the deck is a mage");
                                }
                                var lev = Splitme(level, "/")[0]; //just take the first value as each is the same
                                var mincost = 3;
                                string minschool = "";
                                foreach (var s in Splitme(school, "/"))
                                {
                                    if (training[s] < mincost)
                                    {
                                        minschool = s;
                                        mincost = training[s];
                                    }
                                }
                                cost += Convert.ToInt32(lev) * training[minschool];
                                levels[minschool] += Convert.ToInt32(lev) * card.Quantity;
                            }
                            else //Only one school in spell
                            {
                                if (training.ContainsKey(school))
                                {
                                    cost += Convert.ToInt32(level) * training[school];
                                    levels[school] += Convert.ToInt32(level) * card.Quantity;
                                }
                            }
                        }
                        //check for multiples of Epic spells
                        if (Property(card, "Traits").Contains("Epic") && card.Quantity > 1)
                        {
                            System.Windows.MessageBox.Show("Validation FAILED: Only one copy of Epic card " + card.Name + " is allowed.\n" +
                                card.Quantity + " copies found in spellbook.");
                            return;
                        }
                        //check for illegal school- or mage-specific spells
                        if (Property(card, "Traits").Contains("Only"))
                        {
                            string[] traits = Property(card, "Traits").Split(',');
                            List<string> onlyTraits = traits.Where(s => s.Contains("Only")).ToList();
                            if (onlyTraits.Count == 1)
                            {
                                string onlyPhrase = onlyTraits[0];
                                bool legal = false;

                                //check mage restriction
                                if (onlyPhrase.Contains(magename))
                                    legal = true;

                                //check class restriction
                                foreach (string schoolKey in training.Keys)
                                {
                                    if (training[schoolKey] == 1 && onlyPhrase.Contains(schoolKey + " Mage"))
                                        {
                                            legal = true;
                                        }
                                    else if(!isEmptyLevelX)
                                    {
                                        foreach(string cSchool in cardSchools)
                                        {
                                            if (levelXTrain.Contains(cSchool))
                                            {
                                                int Lx_ind = levelXTrain.IndexOf(cSchool);
                                                int trainLevel = Convert.ToInt32(levelXTrain[Lx_ind-1]);
                                                int c_ind = Array.IndexOf(cardSchools, cSchool);
                                                int cLevel = Convert.ToInt32(cardLevels[c_ind]);
                                                if (cLevel <= trainLevel)
                                                {
                                                    legal = true;
                                                }
                                            }

                                        }
                                    }
                                }


                                if (!legal)
                                {
                                    System.Windows.MessageBox.Show("Validation FAILED: The card " + card.Name + " is not legal in a " + magename + " deck.");
                                    return;
                                }
                            }
                        }

                        // Check for correct number of cards
                        int l = 0;
                        if (level.Contains("+"))
                        {
                            var levArr = Splitme(level, "+");
                            foreach (string s in levArr)
                                l += Convert.ToInt32(s);
                        }
                        else if (level.Contains("/"))
                        {
                            var levArr = Splitme(level, "/");
                            l = Convert.ToInt32(levArr[0]);
                        }
                        else
                        {
                            l = Convert.ToInt32(level);
                        }
                        if ((l == 1 && card.Quantity > 6 && (!card.Name.Contains("Shallow Sea") && magename.Contains("Siren")) ||
                        (l >= 2 && card.Quantity > 4)))
                        {
                            // too many
                            System.Windows.MessageBox.Show("Validation FAILED: There are too many copies of " + card.Name + " in the deck.");
                            return;
                        }

                        cardcount += card.Quantity;
                        reporttxt += string.Format("{0} - {1} - {2}\n", totalLevel.ToString(), cost.ToString(), (cost * card.Quantity).ToString());
                        spellbook += cost*card.Quantity;
                        //System.Windows.MessageBox.Show(card.Name + "\nPoints:"+cost);
                    }   //card has school and level 
                }   //foreach card
            }   //foreach section

            string reporttmp = "A Mage Wars Spellbook, built using the OCTGN SBB " + DateTime.Now.ToShortDateString() + " " + DateTime.Now.ToShortTimeString() + "\n\n";
            reporttmp += string.Format("Spellbook points: {0} used of {0} allowed\n\n", spellbook, spellpoints);
            reporttmp += "Key: Quantity - Spell Name - Spell Level - Spellbook Cost - Total Spellbook Cost\n\n";
            reporttmp += reporttxt;
            Clipboard.SetText(reporttmp);
            if (mageStatCard == null)
            {
                System.Windows.MessageBox.Show("Validation result:\nNo mage stat card is detected in the book");
            }
            else
            {
                System.Windows.MessageBox.Show(String.Format("Validation result:\n{0} spellpoints in the deck using '{1}' as the mage. {2} spellpoints are allowed.\nDeck has been copied to the clipboard.", spellbook, magename, spellpoints));
            }
            
            if (spellbook <= spellpoints)
            {
                deckValidated = true;
                bookPoints = spellbook;
                totalCards = cardcount;
                validatedDeckHash = hashtotal;
            }
        
        }// OnClick

        // DOWN HERE
        public int countSpellPointTotal(IDeck loadedDeck, IMultiCard mageStatCard)
        {
            int totalSpellPoints = 0;
            var secArray = loadedDeck.Sections.ToArray();
            foreach (var section in secArray)
            {
                foreach (var card in section.Cards)
                {
                    if (!(Property(card, "Subtype").Contains("Mage") || Property(card, "Type").Contains("Magestats") || Property(card, "Subtype").Contains("Aura")))
                    {
                        System.Windows.MessageBox.Show(card.Name);
                        totalSpellPoints += determineCardPointTotal(card, mageStatCard);
                    }
                    //Check mage/school only cards
                }
            }

            return totalSpellPoints;
        }


        public int determineCardPointTotal(IMultiCard card, IMultiCard mageStatCard)
        {
            /*remaining functions to make
            Full School Training
            Type Opposed (FM, creatures)
            School Opposed
            All others
            */
            int cardSpellPoints = 0;
            int rawCardLevel = getRawCardlevel(card);
            System.Windows.MessageBox.Show("rawCardLevel: "+rawCardLevel.ToString());


            if (isNovice(card))
            {
                System.Windows.MessageBox.Show("Is Novice");
                int multiplier = 1;
                cardSpellPoints = multiplier*rawCardLevel;
            }
            else if (isComboTraining(card, mageStatCard))
            {
                System.Windows.MessageBox.Show("Is Combo");
                int multiplier = 1;
                cardSpellPoints = multiplier*rawCardLevel;
            }
            else if (isSubtypeTraining(card, mageStatCard))
            {
                System.Windows.MessageBox.Show("Is Subtype");
                int multiplier = 1;
                cardSpellPoints = multiplier*rawCardLevel;                
            }
            else if (hasPartialTraining(card, mageStatCard))
            {
                System.Windows.MessageBox.Show("Partial Training");
                cardSpellPoints = partialTrainingPointsToAdd(card, mageStatCard);
            }
            return cardSpellPoints;
        }


        public int partialTrainingPointsToAdd(IMultiCard card, IMultiCard mageStatCard)
        {
            int cardSpellPoints = 0;
            if (Property(card, "School").Contains("+"))
            {
                string[] cardSchoolList = splitCardProperty(card, "School");
                string[] cardLevelList = splitCardProperty(card, "Level");
                string Training = Property(mageStatCard, "MageSchoolPartialTraining");
                foreach(string school in cardSchoolList)
                {
                    if (Training.Contains(school))
                    {
                        string[] magePartialTraining = Training.Replace(" ",String.Empty).Split(',');
                        int mageIndex = Array.FindIndex(magePartialTraining, m => m == school) + 1;
                        int cardIndex = Array.FindIndex(cardSchoolList, m => m == school);
                        int cardSchoolLevel = Int32.Parse(cardLevelList[cardIndex]);
                        int mageTrainingLevel = Int32.Parse(magePartialTraining[mageIndex]);
                            if (cardSchoolLevel<=mageTrainingLevel)
                            {
                                int multiplier = 1;
                                cardSpellPoints += cardSchoolLevel*multiplier;
                            }
                            else
                            {
                                int multiplier = 2;
                                cardSpellPoints += cardSchoolLevel*multiplier;
                            }
                    }
                    else
                    {
                        int cardIndex = Array.FindIndex(cardSchoolList, m => m == school);
                        int cardSchoolLevel = Int32.Parse(cardLevelList[cardIndex]);
                        int multiplier = 2;
                        cardSpellPoints += cardSchoolLevel*multiplier;
                    }
                }
                return cardSpellPoints;
            }
            else
            {
                int cardLevel = getRawCardlevel(card);
                int multiplier = 1;
                cardSpellPoints += cardLevel*multiplier;
                return cardSpellPoints;
            }
        }

        public bool hasPartialTraining(IMultiCard card,IMultiCard mageStatCard)
        {
            string Training = Property(mageStatCard, "MageSchoolPartialTraining");
            if (!(Training.Contains('0')))
            {
                if (hasSchoolMatch(Training, card))
                {
                    return hasLevelMatch(Training, card);
                }
                else
                {
                    return false;
                }
            }
            else
            {
                return false;
            }
        }

        public bool hasLevelMatch(string Training, IMultiCard card)
        {
            string[] cardSchoolList = splitCardProperty(card, "School");
            string[] cardLevelList = splitCardProperty(card, "Level");
            foreach(string school in cardSchoolList)
            {
                if (Training.Contains(school))
                {
                    string[] magePartialTraining = Training.Replace(" ",String.Empty).Split(',');
                    int mageIndex = Array.FindIndex(magePartialTraining, m => m == school) + 1;
                    int cardIndex = Array.FindIndex(cardSchoolList, m => m == school);
                    if (Int32.Parse(cardLevelList[cardIndex])<=Int32.Parse(magePartialTraining[mageIndex]))
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        public bool hasSchoolMatch(string Training,IMultiCard card)
        {
            string[] cardSchoolList = splitCardProperty(card, "School");
            foreach (var school in cardSchoolList)
            {
                if (Training.Contains(school))
                {
                    return true;
                }
            }
            return false;
        }

        public string[] splitCardProperty(IMultiCard card, string property)
        {
            if (Property(card, property).Contains('+'))
            {
                string[] cardPropertyList = Property(card, property).Replace(" ",String.Empty).Split('+');
                return cardPropertyList;
            }
            else
            {
                string[] cardPropertyList = Property(card, property).Replace(" ",String.Empty).Split('/');
                return cardPropertyList;
            }
        }

        public bool isSubtypeTraining(IMultiCard card,IMultiCard mageStatCard)
        {
            bool subtypeFlag = false;
            if (!(Property(mageStatCard, "MageSubtypeTraining").Contains('0')))
            {   
                string[] mageSubtypeTraining = Property(mageStatCard, "MageSubtypeTraining").Replace(" ",String.Empty).Split(',');
                foreach (var element in mageSubtypeTraining)
                {
                    if(Property(card, "Subtype").Contains(element))
                    {
                        subtypeFlag = true;
                    }
                }
            }
            return subtypeFlag;
        }


        public bool isComboTraining(IMultiCard card, IMultiCard mageStatCard)
        {
            bool comboFlag = false;
            if (!(Property(mageStatCard, "MageComboTraining").Contains('0')))
            {   
                comboFlag = true;
                string[] comboTraining = Property(mageStatCard, "MageComboTraining").Replace(" ",String.Empty).Split(';');
                foreach(var element in comboTraining)
                {
                    string[] testableAttributes = element.Replace(" ",String.Empty).Split(',');
                    if (!(Property(card, testableAttributes[1]).Contains(testableAttributes[0])))
                    {
                        comboFlag = false;
                        return comboFlag;
                    }
                }
            }
            return comboFlag;
        }

        public bool isNovice(IMultiCard card)
        {
            if (Property(card, "Traits").Contains("Novice"))
            {
                return true;
            }
            else
            {
                return false;
            }
        }

        public int getRawCardlevel(IMultiCard card)
        {
            int rawCardLevel = 0;
            if (Property(card, "Level").Contains("+"))
            {
                string[] cardLevel = Property(card, "Level").Split('+');
                foreach (var level in cardLevel)
                {
                    rawCardLevel += Int32.Parse(level);
                }
            }
            else
            {
                string[] cardLevel = Property(card, "Level").Split('/');
                rawCardLevel += Int32.Parse(cardLevel[0]);
            }
            return rawCardLevel;
        }
        

        private IMultiCard getMageStatCard(IDeck loadedDeck)
        {
            var secArray = loadedDeck.Sections.ToArray();
            foreach (var section in secArray)
            {
                foreach (var card in section.Cards)
                {
                    if (Property(card, "Subtype").Contains("Mage") && Property(card, "Type").Contains("Magestats"))
                    {
                        return card;
                    }
                    
                }
            }
            return null;
        }

        private string[] Splitme(string prop, string delimstr)
        {
            char[] delimiter = delimstr.ToCharArray();
            return prop.Split(delimiter);
        }

        private bool HasProperty(IMultiCard card, string name)
        {
            return card.GetFullCardProperties().Any(x => x.Key.Name.Equals(name, StringComparison.InvariantCultureIgnoreCase));
        }

        public string DictionaryToString(Dictionary < string, int > dictionary)
        {
            string dictionaryString = "{";  
            foreach(KeyValuePair < string, int > keyValues in dictionary) 
            {
                dictionaryString += keyValues.Key + " : " + keyValues.Value + ", ";  
            }
            return dictionaryString.TrimEnd(',', ' ') + "}";  
        } 

        public static bool isEmpty<T>(List<T> list)
        {
            if (list == null)
            {
                return true;
            }
            return !list.Any();
        }

        private string messageBoxTest(string message)
        {
            string str = message;
            return str;
        }

        private string Property(IMultiCard card, string p)
        {
            string ret;
            try
            {
                ret =
                card.GetFullCardProperties()
                    .First(x => x.Key.Name.Equals(p, StringComparison.InvariantCultureIgnoreCase))
                    .Value as string;
            }
            catch (Exception)
            {
                ret = "";
            }
            if (ret == String.Empty)
            	ret = "0";
            return ret;
        }

    }
    
    public static class Prompt
    {
        public static string ShowDialog(string text, string caption)
        {
            Form prompt = new Form();
            prompt.StartPosition = FormStartPosition.CenterScreen;
            prompt.Width = 500;
            prompt.Height = 120;
            prompt.Text = caption;
            Label textLabel = new Label() { Left = 50, Top = 20, Text = text, Height = 30, Width = 400 };
            TextBox inputField = new TextBox() { Left = 50, Top = 50, Width = 400 };
            Button confirmation = new Button() { Text = "Ok", Left = 350, Width = 100, Top = 50 };
            confirmation.Click += (sender, e) => { prompt.Close(); };
            prompt.Controls.Add(confirmation);
            prompt.Controls.Add(textLabel);
            prompt.Controls.Add(inputField);
            prompt.ShowDialog();
            return inputField.Text;
        }
    }

}
