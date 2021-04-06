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

            var curDeck = con.GetLoadedDeck();

            if (curDeck == null)
            {

                MessageBox.Show("You must have a Mage Wars deck loaded to use this feature.");
                return;
            }

            deckValidated = false;

            var secArray = curDeck.Sections.ToArray();
            int cardcount = 0;
            int spellbook = 0;
            string magename = "none in deck";
            int spellpoints = 0;
            string reporttxt = "";
            bool Talos = false;
            int hashtotal = 0;
            
            //THIS COVERS THE UNIQUE TRAINING OF EXISTING MAGES. NOT FUTURE PROOFING SINCE FINAL SET BEING RELEASED, WILL MAKE 2.0 BETTER FUNCTIONALITY
            List<string> subtypeTrain = new List<string>();
            List<string> comboTrain = new List<string>();
            List<string> levelXTrain = new List<string>();
            

            Dictionary<string, int> training = new Dictionary<string, int>()
                {
                    {"Dark", 2},{"Holy",2},{"Nature",2},{"Mind",2},{"Arcane",2},{"War",2},{"Earth",2},{"Water",2},{"Air",2},{"Fire",2},{"Creature",0}
                };
            
            Dictionary<string, int> levels = new Dictionary<string, int>()
                {
                    {"Dark", 0},{"Holy",0},{"Nature",0},{"Mind",0},{"Arcane",0},{"War",0},{"Earth",0},{"Water",0},{"Air",0},{"Fire",0},{"Creature",0}
                };



            

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
                    
                    //THIS PART IS THE EQUIVALENT OF statCardParse(deck) IN THE SBV
                    //Get things like the Mage Name, Training, and Spellbook Limit
                    if (Property(card, "Subtype").Contains("Mage") && Property(card, "Type").Contains("Creature"))
                    {
                        magename = card.Name;
                    }
                    if (Property(card, "Subtype").Contains("Mage") && Property(card, "Type").Contains("Magestats"))
                    {
                        // magename = card.Name.Split(' ')[0];
                        // mageName
                        var mageschoolcost = Splitme(Property(card, "MageSchoolCost"), ",");
                        
                        // mageschoolcost IS THE EQUIVALENT OF 'spellbook' IN THE SpellbookValidator.py

                        var magespellbooklimit = Splitme(Property(card, "Stats"), ",");
                        // mageStats
                        reporttxt += string.Format("{1}\n", card.Quantity.ToString(), card.Name);
                        
                        
                        
                        
                        
                        foreach (var msc in mageschoolcost)
                        {
                            foreach (var t in training.ToList())
                            {
                                if (msc.Contains(t.Key)) //scan mageschoolcost for training info
                                {
                                    var tlevel = Splitme(msc, "=");
                                    training[t.Key] = Convert.ToInt32(tlevel[1]);
                                    string messageStr = DictionaryToString(training);
                                }
                            }
                        }

                        //Figure out how many spellbook points are allowed by the mage from the "Stats" property
                        foreach (var mstat in magespellbooklimit)
                        {
                            if (mstat.Contains("Spellbook"))
                            {
                                spellpoints = Convert.ToInt32(Splitme(mstat, "=")[1]);
                                //spellPointsTotal
                            }
                        }

                        char[] delimiterChars = {'-', '=', ' '};
                        foreach (string msc in mageschoolcost)
                        // for key in spellbook:
                        {
                            if (msc.StartsWith("S-") | (msc.StartsWith(" S-")))
                            // if key.startswith ('S-'):
                            {
                                string[] addStr = msc.Split(delimiterChars, StringSplitOptions.RemoveEmptyEntries);
                                foreach (string tempStr in addStr)
                                {
                                    int len = tempStr.Length;
                                    if (len > 1)
                                    {
                                        subtypeTrain.Add(tempStr);
                                    }
                                }
                                 
                            }
                            else if (msc.StartsWith("C-") | (msc.StartsWith(" C-")))
                            // elif key.startswith ('C-'):
                            {
                                string[] addStr = msc.Split(delimiterChars, StringSplitOptions.RemoveEmptyEntries);
                                foreach (string tempStr in addStr)
                                {
                                    comboTrain.Add(tempStr);
                                }
                            }
                            else if (msc.StartsWith("L-") | (msc.StartsWith(" L-")))
                            // elif key.startswith ('L-'):
                            {
                                
                                string[] addStr = msc.Split(delimiterChars, StringSplitOptions.RemoveEmptyEntries);
                                foreach (string tempStr in addStr)
                                {
                                    if (tempStr.Length > 1)
                                    {
                                        training[tempStr] = 2;
                                    }
                                    levelXTrain.Add(tempStr);
                                }
                            }
                        }
                        continue;
                    }
                    
                    
                    




                    // FROM HERE BELOW ARE THINGS WRAPPED UP IN cardPointCount FROM THE SBV. WILL NEED TO REWRITE WITH THE NEW METHODOLOGY
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
                                string mname = magename;
                                if (mname.Contains("Beastmaster")) mname = "Beastmaster";
                                if (mname.Contains("Wizard")) mname = "Wizard";
                                if (mname.Contains("Warlock")) mname = "Warlock";
                                if (mname.Contains("Warlord")) mname = "Warlord";
                                if (mname.Contains("Priestess")) mname = "Priestess";
                                if (mname.Contains("Paladin")) mname = "Paladin";
                                if (mname.Contains("Siren")) mname = "Siren";
                                if (mname.Contains("Forcemaster")) mname = "Forcemaster";
                                if (mname.Contains("Monk")) mname = "Monk";
                                if (onlyPhrase.Contains(mname))
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
                        spellbook+=cost*card.Quantity;
                        //System.Windows.MessageBox.Show(card.Name + "\nPoints:"+cost);
                    }   //card has school and level 
                }   //foreach card
            }   //foreach section

            string reporttmp = "A Mage Wars Spellbook, built using the OCTGN SBB " + DateTime.Now.ToShortDateString() + " " + DateTime.Now.ToShortTimeString() + "\n\n";
            reporttmp += string.Format("Spellbook points: {0} used of {0} allowed\n\n", spellbook, spellpoints);
            reporttmp += "Key: Quantity - Spell Name - Spell Level - Spellbook Cost - Total Spellbook Cost\n\n";
            reporttmp += reporttxt;
            Clipboard.SetText(reporttmp);
            if (magename == "none in deck")
            {
                System.Windows.MessageBox.Show("Validation result:\nNo mage is detected in the book");
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
