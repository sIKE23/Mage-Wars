//Version: 1.14.0.0

namespace Octgn.MageWarsValidator
{
    using Octgn.Core.DataExtensionMethods;
    using Octgn.Core.DataManagers;
    using Octgn.Core.Plugin;
    using Octgn.DataNew.Entities;
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

        public static bool deckValidated = false;
        public static int bookPoints = 0;
        public static int totalCards = 0;
        public static int validatedDeckHash = 0;

        public IEnumerable<IPluginMenuItem> MenuItems
        {
            get
            {
                // Add your menu items here.
                return new List<IPluginMenuItem> { new ValidatorMenuItem(), new ExportToForumMenuItem(), new ExportToAWSBB() };
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
            var curDeck = con.GetLoadedDeck();
            MageWarsValidator.deckValidated = false;

            if (curDeck.GameId.Equals(Guid.Parse("9acef3d0-efa8-4d3f-a10c-54812baecdda"))) //Is a Mage Wars deck loaded?
            {
                var secArray = curDeck.Sections.ToArray();
                int cardcount = 0;
                int spellbook = 0;
                string magename = "none in deck";
                int spellpoints = 0;
                string reporttxt = "";
                bool Talos = false;
                int hashtotal = 0;

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
                        hashtotal += card.GetHashCode() + card.Quantity;

                        //MessageBox.Show(String.Format("{0}", card.Name));
                        if (Property(card, "Subtype").Contains("Mage"))
                        {
                            var mageschoolcost = Splitme(Property(card, "MageSchoolCost"), ",");
                            var magespellbooklimit = Splitme(Property(card, "Stats"), ",");
                            magename = card.Name;
                            reporttxt += string.Format("{1}\n", card.Quantity.ToString(), card.Name);
                            foreach (var msc in mageschoolcost)
                            {
                                foreach (var t in training.ToList())
                                {
                                    if (msc.Contains(t.Key)) //scan mageschoolcost for training info
                                    {

                                        var tlevel = Splitme(msc, "=");
                                        training[t.Key] = Convert.ToInt32(tlevel[1]);
                                    }
                                }
                            }
                            foreach (var mstat in magespellbooklimit)
                            {
                                if (mstat.Contains("Spellbook"))
                                {
                                    spellpoints = Convert.ToInt32(Splitme(mstat, "=")[1]);
                                }
                            }
                            continue;
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
                                    if (schs[i] != "Water")
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
                                if (school.Contains("+")) //add all spell levels
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

                            //Paladin is trained in level 3 holy, level 2 war, and all holy creatures
                            //If the current card is in the paladin's trainings, it has already been correctly added (assuming paladin's trainings contains Holy=1 and War=1)
                            //so we only need to check for the exceptions
                            if (magename.Contains("Paladin"))
                            {
                                string delim = school.Contains("+") ? "+" : school.Contains("/") ? "/" : "";
                                if (school.Contains("Holy"))
                                {
                                    int holyLevel = Convert.ToInt32(Splitme(level, delim)[Splitme(school, delim).ToList().IndexOf("Holy")]);
                                    if (holyLevel > 3 && Property(card, "Type") != "Creature")
                                    {
                                        spellbook += holyLevel * card.Quantity;
                                        cost += holyLevel;
                                    }
                                }
                                if (school.Contains("War"))
                                {
                                    int warLevel = Convert.ToInt32(Splitme(level, delim)[Splitme(school, delim).ToList().IndexOf("War")]);
                                    if (warLevel > 2 && !school.Contains("+"))
                                    {
                                        spellbook += warLevel * card.Quantity;
                                        cost += warLevel;
                                    }
                                }
                                //{
                                    // Holy Creature rules go here should check of Creatures that are in two schools Holy + Other School 
                                    // (other school should also exclude War)
                                    // we need to reduce the spellbook & cost by the spelllevel as if they were a 1x training.
                                        //spellbook -= spellLevel * card.Quantity;
                                        //cost -= spellLevel
                                //}
                            }

                            //Siren is trained in Water and all spells with Song or Drowned subtype.
                            //By this point, Water has been correctly calculated, but the Song/Drowned spells are overcosted if they are not Water
                            if (magename.Contains("Siren") && !school.Contains("Water") &&
                                (Property(card, "Subtype").Contains("Song") || Property(card, "Subtype").Contains("Drowned")))
                            {
                                //subtract 1 per level per count as this card has been added x2 per non-trained school already
                                spellbook -= totalLevel * card.Quantity;
                                cost -= totalLevel;
                            }

                            //Forcemaster rule: Pay 3x for non-mind creatures
                            if (magename == "Forcemaster" & "Creature" == Property(card, "Type"))
                            {
                                if (!school.Contains("Mind")) //"Mind" not in schools
                                {
                                    if (school.Contains("+"))
                                    {
                                        foreach (var lev in Splitme(level, "+"))
                                        {
                                            spellbook += Convert.ToInt32(lev) * card.Quantity; // we just add 1 point per spell level as 2 points already have been added
                                            cost += Convert.ToInt32(lev);
                                        }

                                    }
                                    else //handle single school or "/" school cards
                                    {
                                        var lev = Splitme(level, "/");
                                        spellbook += Convert.ToInt32(lev[0]) * card.Quantity;
                                        cost += Convert.ToInt32(lev[0]);
                                    }
                                }
                            }

                            //Druid pays double for Water spells 2 and up
                            if (magename == "Druid" && school.Contains("Water")) 
                            {
                                string delimin = school.Contains("+") ? "+" : school.Contains("/") ? "/" : "";
                                var waterLevel = Convert.ToInt32(Splitme(level, delimin)[Splitme(school, delimin).ToList().IndexOf("Water")]);  //whee
                                if (waterLevel > 1)
                                {
                                    spellbook += waterLevel * card.Quantity;
                                    cost += waterLevel;
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
                                    if (onlyPhrase.Contains(mname))
                                        legal = true;

                                    //check class restriction
                                    foreach (string schoolKey in training.Keys)
                                    {
                                        if (training[schoolKey] == 1 && onlyPhrase.Contains(schoolKey + " Mage"))
                                            legal = true;
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

                        }   //card has school and level 
                    }   //foreach card
                }   //foreach section
                foreach (var t in training)
                {
                    spellbook += t.Value * levels[t.Key];
                }
                string reporttmp = "A Mage Wars Spellbook, built using the OCTGN SBB " + DateTime.Now.ToShortDateString() + " " + DateTime.Now.ToShortTimeString() + "\n\n";
                reporttmp += string.Format("Spellbook points: {0} used of {0} allowed\n\n", spellbook, spellpoints);
                reporttmp += "Key: Quantity - Spell Name - Spell Level - Spellbook Cost - Total Spellbook Cost\n\n";
                reporttmp += reporttxt;
                //System.Windows.MessageBox.Show(reporttmp);
                Clipboard.SetText(reporttmp);
                System.Windows.MessageBox.Show(String.Format("Validation result:\n{0} spellpoints in the deck using '{1}' as the mage. {2} spellpoints are allowed.\nDeck has been copied to the clipboard.", spellbook, magename, spellpoints));
                if (spellbook <= spellpoints)
                {
                    MageWarsValidator.deckValidated = true;
                    MageWarsValidator.bookPoints = spellbook;
                    MageWarsValidator.totalCards = cardcount;
                    MageWarsValidator.validatedDeckHash = hashtotal;
                }
            }

        }

        private string[] Splitme(string prop, string delimstr)
        {
            char[] delimiter = delimstr.ToCharArray();
            return prop.Split(delimiter);
        }

        private bool HasProperty(IMultiCard card, string name)
        {
            return card.Properties[card.Alternate].Properties.Any(x => x.Key.Name.Equals(name, StringComparison.InvariantCultureIgnoreCase) && x.Key.IsUndefined == false);
        }

        private string Property(IMultiCard card, string p)
        {
            string ret;
            try
            {
                ret =
                card.PropertySet()
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
    

    /*********************************************
     * 
     * 
     *           Export to Forum Post
     *                
     * 
     ********************************************/
    public class ExportToForumMenuItem : IPluginMenuItem
    {
        public string Name
        {
            get { return "Export to Forum Post"; }
        }

        public void OnClick(IDeckBuilderPluginController controller)
        {
            //did they validate yet?
            var curDeck = controller.GetLoadedDeck();
            int hashtotal = 0;
            foreach (var section in curDeck.Sections)
                foreach (var card in section.Cards)
                    hashtotal += card.GetHashCode() + card.Quantity;
            if (!MageWarsValidator.deckValidated || MageWarsValidator.validatedDeckHash != hashtotal)
            {
                System.Windows.MessageBox.Show("You must successfully validate the current deck before exporting it to a forum post.");
                return;
            }

            if (curDeck.GameId.Equals(Guid.Parse("9acef3d0-efa8-4d3f-a10c-54812baecdda"))) //Is a Mage Wars deck loaded?
            {
                //setup some stuff
                var secArray = curDeck.Sections.ToArray();
                StringBuilder text = new StringBuilder();

                //ask for the deck name
                string deckName = Prompt.ShowDialog("What is the name of this deck?", "Deck Name");
                if (string.IsNullOrEmpty(deckName))
                {
                    deckName = "OCTGN Deck";
                }

                //start the writing
                text.AppendLine("[spellbook]");
                text.AppendLine("[spellbookheader]");
                text.AppendLine("[spellbookname]" + deckName + "[/spellbookname]");
                
                //get and write mage name
                foreach (var section in secArray)
                {
                    foreach (var card in section.Cards)
                    {
                        if (Property(card, "Subtype").Contains("Mage"))
                        {
                            text.AppendLine("[mage]A " + card.Name + " Spellbook[/mage]");

                            //built by me!
                            text.AppendLine("[mage]built by the OCTGN SBB[/mage]");
                        }
                    }
                }
                text.AppendLine("[/spellbookheader]");
                text.AppendLine("[spells]");

                //do all the cards
                bool promoFound = false;
                foreach (var section in secArray)
                {
                    if (section.Name.Contains("Mage")) continue;

                    text.AppendLine("[spellclass]" + section.Name + "[/spellclass]");
                    foreach (var card in section.Cards)
                    {
                        text.AppendLine("[mwcard=" + Property(card, "CardID") + "]" + card.Quantity + " x " + card.Name + "[/mwcard]");
                        if (Property(card, "CardID").Contains("MWPRO"))
                            promoFound = true;
                    }
                }

                //wrap up
                text.AppendLine("[/spells]");
                text.AppendLine("[cost]Total cost: " + MageWarsValidator.bookPoints + " pts[/cost]");
                text.AppendLine("[/spellbook]");

                //copy to clipboard
                Clipboard.SetText(text.ToString());
                if (promoFound)
                    System.Windows.MessageBox.Show("Promos found in deck. Be aware that promos are not supported by the forum preview system.");
                System.Windows.MessageBox.Show("Forum post containing deck has been copied to clipboard.");
            }
        }        

        private string Property(IMultiCard card, string p)
        {
            string ret;
            try
            {
                ret =
                card.PropertySet()
                    .First(x => x.Key.Name.Equals(p, StringComparison.InvariantCultureIgnoreCase))
                    .Value as string;
            }
            catch (Exception)
            {
                ret = "";
            }
            return ret;
        }
    }


    /*********************************************
     * 
     * 
     *           Export to AW SBB
     *                
     * 
     ********************************************/
    public class ExportToAWSBB : IPluginMenuItem
    {
        public string Name
        {
            get { return "Export to Forum Spellbook Builder"; }
        }

        public void OnClick(IDeckBuilderPluginController controller)
        {
            //did they validate yet?
            var curDeck = controller.GetLoadedDeck();
            int hashtotal = 0;
            foreach (var section in curDeck.Sections)
                foreach (var card in section.Cards)
                    hashtotal += card.GetHashCode() + card.Quantity;
            if (!MageWarsValidator.deckValidated || MageWarsValidator.validatedDeckHash != hashtotal)
            {
                System.Windows.MessageBox.Show("You must successfully validate the current deck before exporting it to the AW SBB.");
                return;
            }

            if (curDeck.GameId.Equals(Guid.Parse("9acef3d0-efa8-4d3f-a10c-54812baecdda"))) //Is a Mage Wars deck loaded?
            {
                var secArray = curDeck.Sections.ToArray();
                StringBuilder text = new StringBuilder();

                //ignore spell counts
                text.AppendLine("1");

                //ask for deck name
                string deckName = Prompt.ShowDialog("What is the name of this deck?", "Deck Name");
                if (string.IsNullOrEmpty(deckName))
                {
                    deckName = "OCTGN Deck";
                }
                text.AppendLine(deckName);

                //get mage name
                foreach (var section in secArray)
                {
                    foreach (var card in section.Cards)
                    {
                        if (Property(card, "Subtype").Contains("Mage"))
                        {
                            text.AppendLine(card.Name);
                        }
                    }
                }

                //write spell set counts - one of each should be fine
                text.AppendLine("1,1,1,1,1,1");

                //spellbook cost
                text.AppendLine(MageWarsValidator.bookPoints.ToString());

                //cost per type - does this matter?
                text.AppendLine("120,120,120,120,120,120");

                //cards in deck
                text.AppendLine(MageWarsValidator.totalCards.ToString());

                //card ID and count
                bool promoFound = false;
                foreach (var section in secArray)
                {
                    foreach (var card in section.Cards)
                    {
                        //skip mage cards and promos
                        if (section.Name.Contains("Mage")) continue;
                        if (Property(card, "CardID").Contains("MWPRO"))
                        {
                            promoFound = true;
                            continue;
                        } 

                        text.AppendLine(Property(card, "CardID") + "," + card.Quantity.ToString());

                        //and lower case until AW SBB is fixed
                        text.AppendLine(Property(card, "CardID").ToLower() + "," + card.Quantity.ToString());
                    }
                }

                if (promoFound)
                {
                    System.Windows.MessageBox.Show("There are one or more promos in this spellbook. They have been omitted from the export file because the AW SBB does not currently support them.");
                }

                //all done, ask for file location
                FolderBrowserDialog folderDialog = new FolderBrowserDialog();
                folderDialog.Description = "Choose where to save the spellbook file.";
                if (folderDialog.ShowDialog() != DialogResult.OK) return;
                string writePath = folderDialog.SelectedPath;

                //write file
                StreamWriter writer = new StreamWriter(new FileStream(writePath + "\\" + deckName + ".sbb", FileMode.Create));
                writer.Write(text.ToString());
                writer.Close();
                System.Windows.MessageBox.Show("File has been written to the specified location.");
            }
        }
        
        private string Property(IMultiCard card, string p)
        {
            string ret;
            try
            {
                ret =
                card.PropertySet()
                    .First(x => x.Key.Name.Equals(p, StringComparison.InvariantCultureIgnoreCase))
                    .Value as string;
            }
            catch (Exception)
            {
                ret = "";
            }
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
