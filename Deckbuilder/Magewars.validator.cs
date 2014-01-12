namespace Octgn.MageWarsValidator
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Reflection;
    using System.Windows;
    using System.Windows.Forms;

    using Octgn.Core.DataExtensionMethods;
    using Octgn.Core.DataManagers;
    using Octgn.Core.Plugin;
    using Octgn.DataNew.Entities;
    using Octgn.Library.Plugin;

    public class MageWarsValidator : IDeckBuilderPlugin
    {

        public IEnumerable<IPluginMenuItem> MenuItems
        {
            get
            {
                // Add your menu items here.
                return new List<IPluginMenuItem> { new PluginMenuItem() };
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
                return "Mage Wars deck validator plugin";
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

    public class PluginMenuItem : IPluginMenuItem
    {
        public string Name
        {
            get
            {
                return "Mage Wars validator";
            }
        }

        /// <summary>
        /// This happens when the menu item is clicked.
        /// </summary>
        /// <param name="con"></param>
        public void OnClick(IDeckBuilderPluginController con)
        {
            var curDeck = con.GetLoadedDeck();

            if (curDeck.GameId.Equals(Guid.Parse("9acef3d0-efa8-4d3f-a10c-54812baecdda"))) //Is a Mage Wars deck loaded?
            {
                var secArray = curDeck.Sections.ToArray();
                int cardcount = 0;
                int spellbook = 0;
                string magename = "none in deck";
                int spellpoints = 0;
                string reporttxt = "";

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
                        //MessageBox.Show(String.Format("{0}", card.Name));
                        if ("Mage" == Property(card, "Type")) 
                        {
                            var magestats = Splitme(Property(card, "Stats"),",");
                            magename = card.Name;
                            reporttxt += string.Format("{0} {1}\n", card.Quantity.ToString(), card.Name);
                            foreach (var ms in magestats)
                            {
                                if (ms.Contains("Spellbook"))
                                {
                                    spellpoints = Convert.ToInt32(Splitme(ms, "=")[1]);
                                }
                                foreach (var t in training.ToList())
                                {
                                    if (ms.Contains(t.Key)) //scan magestats for training info
                                    {
                                        
                                        var tlevel = Splitme(ms, "=");
                                        training[t.Key] = Convert.ToInt32(tlevel[1]);
                                    }
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
                                    reporttxt += string.Format("\n---  {0}  ---\n", typestr);
                                }
                                reporttxt += string.Format("{0} {1}\n", card.Quantity.ToString(), card.Name);
                                continue;
                            }
                        }

                        if (HasProperty(card, "School") & HasProperty(card, "Level"))
                        {
                            var school = Property(card, "School");
                            var level = Property(card, "Level");
                            var typestr = Property(card, "Type");
                            if (typestr.Equals("Conjuration-Wall")) typestr = "Conjuration";
                            if (!reporttxt.Contains(typestr)) // has this type been listed before??
                            {                                
                                reporttxt += string.Format("\n---  {0}  ---\n", typestr);
                            }
                            reporttxt += string.Format("{0} {1}\n", card.Quantity.ToString(), card.Name);

                            if (school.Contains("+")) //add all spell levels
                            {
                                var lev = Splitme(level, "+");
                                int x = 0;
                                foreach (var s in Splitme(school, "+"))
                                {
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
                                levels[minschool] += Convert.ToInt32(lev) * card.Quantity;
                            }
                            else //Only one school in spell
                            {
                                if (training.ContainsKey(school))
                                {
                                    levels[school] += Convert.ToInt32(level) * card.Quantity;
                                }
                            }
                            if (magename == "Forcemaster" & "Creature" == Property(card, "Type")) //Forcemaster rule: Pay 3x for non-mind creatures
                            {
                                if (!school.Contains("Mind")) //"Mind" not in schools
                                {
                                    if (school.Contains("+"))
                                    {
                                        foreach (var lev in Splitme(level, "+"))
                                        {
                                            spellbook += Convert.ToInt32(lev) * card.Quantity; // we just add 1 point per spell level as 2 points already have been added
                                        }

                                    }
                                    else //handle single school or "/" school cards
                                    {
                                        var lev = Splitme(level, "/"); 
                                        spellbook += Convert.ToInt32(lev[0]) * card.Quantity;
                                    }
                                }
                            }
                            if (magename == "Druid" && school.Contains("Water"))  //Druid pays double for Water spells 2 and up
                            {
                                string delim = school.Contains("+") ? "+" : school.Contains("/") ? "/" : "";
                                var waterLevel = Convert.ToInt32(Splitme(level, delim)[Splitme(school, delim).ToList().IndexOf("Water")]);  //whee
                                if (waterLevel > 1) spellbook += waterLevel * card.Quantity;
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
                                            legal = true;
                                    }

                                    if (!legal)
                                    {
                                        System.Windows.MessageBox.Show("Validation FAILED: The card " + card.Name + " is not legal in a " + magename + " deck.");
                                        return;
                                    }
                                }
                            }

                            cardcount += card.Quantity;

                        }   //card has school and level 
                    }   //foreach card
                }   //foreach section
                foreach (var t in training)
                {
                    spellbook += t.Value * levels[t.Key];
                }
                string reporttmp = "Mage Wars deck (built using OCTGN deckbuilder) " + DateTime.Today.Date.ToString() + "\n\n";
                reporttmp += string.Format("Spellbook points: {0} used of {0} allowed\n\n",spellbook, spellpoints);
                reporttmp += reporttxt;
                //System.Windows.MessageBox.Show(reporttmp);
                Clipboard.SetText(reporttmp);
                System.Windows.MessageBox.Show(String.Format("Validation result:\n{0} spellpoints in the deck using '{1}' as the mage. {2} spellpoints are allowed.\nDeck has been copied to the clipboard.",spellbook,magename,spellpoints));
            }   

        }

        private string [] Splitme(string prop, string delimstr)
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
            catch (Exception e)
            {
                ret = "";
            }
            return ret;
        }

    }
}
