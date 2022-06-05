//Version: 2.2.2.0
//3 June 2022 Completely refactored by Shark Bait, rev 1. Still work to do, but it's significantly easier to read

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

            if (loadedDeck == null)
            {
                MessageBox.Show("You must have a Mage Wars deck loaded to use this feature.");
                return;
            }

            deckValidated = false;
            string reporttxt = "";
            IMultiCard mageStatCard = getMageStatCard(loadedDeck);
            int totalPointsAllowed = Int32.Parse(Property(mageStatCard, "StatSpellBookPoints"));


            if (mageStatCard == null)
            {
                System.Windows.MessageBox.Show("Validation result:\nNo mage stat card is detected in the book");
                return;
            }

            
            int spellPoints = countSpellPointTotal(loadedDeck, mageStatCard);

            reporttxt = generateReportTxt(loadedDeck, spellPoints, totalPointsAllowed);
            Clipboard.SetText(reporttxt);
            bool restrictionViolation = checkRestrictions(loadedDeck, mageStatCard);
            if (restrictionViolation)
            {
                System.Windows.MessageBox.Show("Please fix the restriction violation and validate again");
            }
            else
            {
                System.Windows.MessageBox.Show(String.Format("Validation result:\n{0} spellpoints in the deck. {1} spellpoints are allowed.\nDeck has been copied to the clipboard.", spellPoints, totalPointsAllowed));
            }
            
            
            if (spellPoints <= totalPointsAllowed)
            {
                deckValidated = true;
            }
        
        }

        public string generateReportTxt(IDeck loadedDeck,int spellPoints,int totalPointsAllowed)
        {//Collected all the old report stuff here and haven't messed with it TOO much. To be refactored in rev 2
            string reporttxt = "";
            string reporttmp = "A Mage Wars Spellbook, built using the OCTGN SBB " + DateTime.Now.ToShortDateString() + " " + DateTime.Now.ToShortTimeString() + "\n\n";
            reporttmp += string.Format("Spellbook points: {0} used of {0} allowed\n\n", spellPoints, totalPointsAllowed);
            reporttmp += "Key: Quantity - Spell Name\n\n";
            var secArray = loadedDeck.Sections.ToArray();
            foreach (var section in secArray)
            {
                foreach (var card in section.Cards)
                {
                        
                        var typestr = Property(card, "Type");
                        if (Property(card, "Subtype").Contains("Mage")) typestr = "Mage";
                        if (typestr.Equals("Conjuration-Wall")) typestr = "Conjuration";
                        if (typestr.Equals("Conjuration-Terrain")) typestr = "Conjuration";
                        if (!reporttxt.Contains(typestr)) // has this type been listed before??
                        {
                            reporttxt += string.Format("\n---  {0}  ---\n", typestr);
                        }
                        reporttxt += string.Format("{0} - {1}\n", card.Quantity.ToString(), card.Name);
                }
            }
            reporttmp += reporttxt;
            return reporttmp; 
        }

        public bool checkRestrictions(IDeck loadedDeck, IMultiCard mageStatCard)
        {
            bool restrictionViolation = false;
            var secArray = loadedDeck.Sections.ToArray();
            foreach (var section in secArray)
            {
                foreach (var card in section.Cards)
                {
                    restrictionViolation = ((checkCountRestrictions(card)) || (checkForMageSchoolRestrictionViolation(card, mageStatCard)));
                    if (restrictionViolation)
                    {
                        return restrictionViolation;
                    }
                }
            }
            return restrictionViolation;
        }

        public bool checkCountRestrictions(IMultiCard card)
        {
            int cardLevel = getTotalCardLevel(card);
            if (cardLevel == 1 && card.Quantity > 6)
            {
                string restrictionViolationMessage = "Validation FAILED: Only six copies of " + card.Name + " are allowed.\n" + card.Quantity + " copies found in spellbook.";
                System.Windows.MessageBox.Show(restrictionViolationMessage);
                return true;
            }
            else if(cardLevel > 1 && card.Quantity > 4)
            {
                string restrictionViolationMessage = "Validation FAILED: Only four copies of " + card.Name + " are allowed.\n" + card.Quantity + " copies found in spellbook.";
                System.Windows.MessageBox.Show(restrictionViolationMessage);
                return true;
            }
            else if(Property(card, "Traits").Contains("Epic") && card.Quantity > 1)
            {
                string restrictionViolationMessage = "Validation FAILED: Only one copy of Epic card " + card.Name + " is allowed.\n" + card.Quantity + " copies found in spellbook.";
                System.Windows.MessageBox.Show(restrictionViolationMessage);
                return true;
            }
            return false;
        }

        public bool checkForMageSchoolRestrictionViolation(IMultiCard card, IMultiCard mageStatCard)
        {
            if (Property(card, "Traits").Contains("Only"))
            {
                string onlyPhrase = getOnlyPhrase(card);
                string mageRestrictionName = Property(mageStatCard, "Nickname");
                if ((isCorrectMage(onlyPhrase, mageRestrictionName)) || (isCorrectSchool(card, mageStatCard)))
                {
                    return false;
                }
                else
                {
                    string restrictionMessage = "Validation FAILED: The card " + card.Name + " is " + onlyPhrase + ".\nThus, it cannot be included in this deck.";
                    System.Windows.MessageBox.Show(restrictionMessage);
                    return true;
                }
            }
            return false;
        }

        public bool isCorrectSchool(IMultiCard card,IMultiCard mageStatCard)
        {
            bool legal =  false;
            if (hasPartialTraining(card, mageStatCard))
            {
                legal = true;
            }
            else if (hasSchoolMatch(Property(mageStatCard,"MageSchoolFullTraining"),card))
            {
                legal = true;
            }
            return legal;
        }

        public bool isCorrectMage(string onlyPhrase, string mageRestrictionName)
        {
            bool legal =  false;
            if (onlyPhrase.Contains(mageRestrictionName))
            {
                legal = true;
            }
            return legal;
        }

        public string getOnlyPhrase(IMultiCard card)
        {
            string[] traits = Property(card, "Traits").Split(',');
            List<string> onlyTraits = traits.Where(s => s.Contains("Only")).ToList();
            string onlyPhrase = onlyTraits[0];
            return onlyPhrase; 
        }

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
                        //System.Windows.MessageBox.Show(card.Name);
                        totalSpellPoints += determineCardPointTotal(card, mageStatCard);
                    }
                }
            }

            return totalSpellPoints;
        }


        public int determineCardPointTotal(IMultiCard card, IMultiCard mageStatCard)
        {
            int cardSpellPoints = 0;
            int totalCardLevel = getTotalCardLevel(card);
            if (isNovice(card))
            {
                cardSpellPoints += addPoints("trained", totalCardLevel)*card.Quantity;
            }
            else if (isTalos(card))
            {
                cardSpellPoints = 0;
            }
            else if (isComboTraining(card, mageStatCard))
            {
                cardSpellPoints += addPoints("trained", totalCardLevel)*card.Quantity;
            }
            else if (isSubtypeTraining(card, mageStatCard))
            {
                cardSpellPoints += addPoints("trained", totalCardLevel)*card.Quantity;                
            }
            else if (hasPartialTraining(card, mageStatCard))
            {
                cardSpellPoints = partialTrainingPointsToAdd(card, mageStatCard)*card.Quantity;
            }
            else if (isOpposedCardType(card, mageStatCard))
            {
                cardSpellPoints += addPoints("opposed", totalCardLevel)*card.Quantity;
            }
            else if ((hasSchoolMatch(Property(mageStatCard,"MageSchoolOpposed"),card)) || (hasSchoolMatch(Property(mageStatCard,"MageSchoolFullTraining"),card)))
            {
                cardSpellPoints += addPointsBasedOnFullSchoolTraining(mageStatCard, card)*card.Quantity;
            }
            else
            {
                cardSpellPoints += addPoints("neutral", totalCardLevel)*card.Quantity;
            }
            return cardSpellPoints;
        }

        public bool isOpposedCardType(IMultiCard card, IMultiCard mageStatCard)
        {
            string cardType = Property(card, "Type");
            string mageTypeOpposed = Property(mageStatCard, "MageTypeOpposed").Replace(" ",String.Empty);
            if (cardType.Contains(mageTypeOpposed))
            {
                return true;
            }
            else
            {
                return false;
            }
        }

        public int addPointsBasedOnFullSchoolTraining(IMultiCard mageStatCard, IMultiCard card)
        {//refactor, still a bit nuts
            int cardSpellPoints = 0;
            int cardSchoolLevel = 0;
            string Training = Property(mageStatCard, "MageSchoolFullTraining");
            string Opposed = Property(mageStatCard, "MageSchoolOpposed");
            string[] cardSchoolList = splitCardProperty(card, "School");
            string[] cardLevelList = splitCardProperty(card, "Level");
            if (Property(card, "School").Contains("+"))
            {
                foreach(string schoolBeingChecked in cardSchoolList)
                {
                    if (Training.Contains(schoolBeingChecked))
                    {
                        cardSchoolLevel = findCardSchoolLevel(schoolBeingChecked, cardSchoolList, cardLevelList);
                        cardSpellPoints += addPoints("trained", cardSchoolLevel);
                    }
                    else if (Opposed.Contains(schoolBeingChecked))
                    {
                        cardSchoolLevel = findCardSchoolLevel(schoolBeingChecked, cardSchoolList, cardLevelList);
                        cardSpellPoints += addPoints("opposed", cardSchoolLevel);
                    }
                    else
                    {
                        cardSchoolLevel = findCardSchoolLevel(schoolBeingChecked, cardSchoolList, cardLevelList);
                        cardSpellPoints += addPoints("neutral", cardSchoolLevel);
                    }
                }
                return cardSpellPoints;
            }
            else 
            {
                int cardLevel = getTotalCardLevel(card);
                bool trainingFound = false;
                List<bool> opposedFound = new List<bool>();
                foreach(string schoolBeingChecked in cardSchoolList)
                {
                    if(Training.Contains(schoolBeingChecked))
                    {
                        trainingFound = true;
                        opposedFound.Add(false);
                    }
                    else if (Opposed.Contains(schoolBeingChecked))
                    {
                        opposedFound.Add(true);
                    }
                    else
                    {
                        opposedFound.Add(false);
                    }
                    
                }

                if (trainingFound)
                {
                    cardSpellPoints += addPoints("trained", cardLevel);
                }
                else if (opposedFound.All(o => o == true))
                {
                    cardSpellPoints += addPoints("opposed", cardLevel);
                }
                else
                {
                    cardSpellPoints += addPoints("neutral", cardLevel);
                }
                return cardSpellPoints;
            }      
        }

        public int addPoints(string training, int cardSchoolLevel)
        {
            int cardSpellPoints = 0;
            if(training == "trained")
            {
                int multiplier = 1;
                cardSpellPoints += cardSchoolLevel*multiplier;
            }
            else if (training == "opposed")
            {
                int multiplier = 3;
                cardSpellPoints += cardSchoolLevel*multiplier;
            }
            else
            {
                int multiplier = 2;
                cardSpellPoints += cardSchoolLevel*multiplier;
            }
            return cardSpellPoints;
        }

        public int findCardSchoolLevel(string school, string[] cardSchoolList, string[] cardLevelList)
        {
            int cardIndex = Array.FindIndex(cardSchoolList, m => m == school);
            int cardSchoolLevel = Int32.Parse(cardLevelList[cardIndex]);
            return cardSchoolLevel;
        }

        public int partialTrainingPointsToAdd(IMultiCard card, IMultiCard mageStatCard)
        {//This will need cleaned up and refactored at some point
            int cardSpellPoints = 0;
            int cardSchoolLevel = 0;
            if (Property(card, "School").Contains("+"))
            {
                string[] cardSchoolList = splitCardProperty(card, "School");
                string[] cardLevelList = splitCardProperty(card, "Level");
                string partialTraining = Property(mageStatCard, "MageSchoolPartialTraining");
                string fullTraining = Property(mageStatCard, "MageSchoolFullTraining");
                foreach(string schoolBeingChecked in cardSchoolList)
                {
                    if (partialTraining.Contains(schoolBeingChecked))
                    {
                        string[] magePartialTraining = partialTraining.Replace(" ",String.Empty).Split(',');
                        int mageIndex = Array.FindIndex(magePartialTraining, m => m == schoolBeingChecked) + 1;
                        int mageTrainingLevel = Int32.Parse(magePartialTraining[mageIndex]);
                        cardSchoolLevel = findCardSchoolLevel(schoolBeingChecked, cardSchoolList, cardLevelList);
                        if (cardSchoolLevel<=mageTrainingLevel)
                        {
                            cardSpellPoints += addPoints("trained", cardSchoolLevel);
                        }
                        else
                        {
                            cardSpellPoints += addPoints("neutral", cardSchoolLevel);
                        }
                    }
                    else if(fullTraining.Contains(schoolBeingChecked))
                    {
                        cardSchoolLevel = findCardSchoolLevel(schoolBeingChecked, cardSchoolList, cardLevelList);
                        cardSpellPoints += addPoints("trained", cardSchoolLevel);
                    }
                    else
                    {
                        cardSchoolLevel = findCardSchoolLevel(schoolBeingChecked, cardSchoolList, cardLevelList);
                        cardSpellPoints += addPoints("neutral", cardSchoolLevel);
                    }
                }
                return cardSpellPoints;
            }
            else
            {
                int cardLevel = getTotalCardLevel(card);
                cardSpellPoints += addPoints("trained", cardLevel);
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

        public bool isTalos(IMultiCard card)
        {
            if (Property(card, "Name").Contains("Talos"))
            {
                return true;
            }
            else
            {
                return false;
            }
        }

        public int getTotalCardLevel(IMultiCard card)
        {
            int totalCardLevel = 0;
            if (Property(card, "Level").Contains("+"))
            {
                string[] cardLevel = Property(card, "Level").Split('+');
                foreach (var level in cardLevel)
                {
                    totalCardLevel += Int32.Parse(level);
                }
            }
            else
            {
                string[] cardLevel = Property(card, "Level").Split('/');
                totalCardLevel += Int32.Parse(cardLevel[0]);
            }
            return totalCardLevel;
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
